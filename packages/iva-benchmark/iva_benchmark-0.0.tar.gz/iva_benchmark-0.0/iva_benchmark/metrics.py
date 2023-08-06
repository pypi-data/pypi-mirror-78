import glob
import itertools
import os
from functools import partial
from multiprocessing import Pool

import numpy as np
from sklearn.metrics import auc
from scipy.sparse import csr_matrix

from .embeddings_processor import EmbeddingLoader
from .utils import get_pairs_for_comparison

from tqdm import tqdm


def parse_vals(vals):
    len_tr = len(vals[0][4])
    fp, tp, fn, tn = np.zeros(len_tr), np.zeros(len_tr), np.zeros(len_tr), np.zeros(len_tr)
    for k in range(len(vals)):
        fp += vals[k][4]
        tp += vals[k][5]
        fn += vals[k][6]
        tn += vals[k][7]
    return fp, tp, fn, tn


class ConfusionMatrix(object):
    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.tp = np.zeros(len(thresholds))
        self.fp = np.zeros(len(thresholds))
        self.tn = np.zeros(len(thresholds))
        self.fn = np.zeros(len(thresholds))

    def update(self, scores, is_same):
        is_not_same = np.logical_not(is_same)
        for i, threshold in enumerate(self.thresholds):
            scores_greater_thresh = scores >= threshold
            scores_less_thresh = np.logical_not(scores_greater_thresh)
            self.fp[i] += np.sum(np.logical_and(scores_greater_thresh, is_not_same))
            self.tp[i] += np.sum(np.logical_and(scores_greater_thresh, is_same))
            self.fn[i] += np.sum(np.logical_and(scores_less_thresh, is_same))
            self.tn[i] += np.sum(np.logical_and(scores_less_thresh, is_not_same))

    def fix_tp_fn(self, n):
        """Fix tp for the case when scores contains cosine distances between the same pictures. In this case
        scores has 0 (set manually) on the main diagonal, and we don't want to count them. Because we set 0 score
        for such pairs, they will be counted as tp for 0 threshold, and they will be counted as fn for all thresholds
        except 0.

        :param n: number of embeddings to eliminate
        :type n: int
        """
        self.tp[0] = self.tp[0] - n
        self.fn[1:] = self.fn[1:] - n


class BasicMetricsEvaluator(object):
    def __init__(self, filenames_pair, batch_size, top, th_step):
        self.filenames_pair = filenames_pair
        self.batch_size = batch_size
        self.top = top
        self.th_step = th_step

        self.emb_loader1 = EmbeddingLoader(filenames_pair[0], batch_size)
        self.emb_loader2 = EmbeddingLoader(filenames_pair[1], batch_size)
        thresholds = np.arange(0.0, 1 + th_step, th_step)
        # in order to take into account that cos similarity could be greater than one
        thresholds[-1] += 0.1
        self.confusion_matrix = ConfusionMatrix(thresholds)
        self.local_top_scores = []
        self.local_top_labels = []
        self.n_batches = int(np.ceil(len(self.emb_loader1.labels) / batch_size))

    def eval(self):
        for i in range(self.n_batches):
            self.update_on_batch(i)

        self.local_top_scores = np.concatenate(self.local_top_scores, axis=0)
        self.local_top_labels = np.concatenate(self.local_top_labels, axis=0)
        if self.is_the_same_embeddings():
            self.confusion_matrix.fix_tp_fn(self.local_top_labels.shape[0])
        return self.confusion_matrix, self.local_top_scores, self.local_top_labels

    def update_on_batch(self, i):
        embeddings_1_part, labels_1_part, filepaths_1_part = self.emb_loader1.get(i)
        embeddings_2, labels_2, filepaths_2 = self.emb_loader2.get()

        embeddings_1_part = csr_matrix(embeddings_1_part)
        scores = embeddings_1_part.dot(embeddings_2.T)
        # Set cos similarity to 0 between embeddings to themselves in order to not consider an embedding
        # as the closest one to itself.
        # This cause the situation that tp[0] and fn[1:] will count all such pairs, and we will fix it later
        if self.is_the_same_embeddings():
            scores[filepaths_1_part[:, np.newaxis] == filepaths_2[np.newaxis, :]] = 0
        scores = np.maximum(0, scores)
        self.update_tops(scores, labels_2)

        is_same = labels_1_part[:, np.newaxis] == labels_2[np.newaxis, :]
        self.confusion_matrix.update(scores, is_same)

    def update_tops(self, scores, labels):
        batch_top_scores, batch_top_labels = get_tops(scores, labels, self.top)
        self.local_top_scores.append(batch_top_scores)
        self.local_top_labels.append(batch_top_labels)

    def is_the_same_embeddings(self):
        return self.filenames_pair[0] == self.filenames_pair[1]


def get_tops(scores, labels, top):
    if len(labels.shape) == 1:
        labels = labels[np.newaxis, :]
    ind_top = np.argsort(scores, 1)[:, -top:]
    top_scores = np.take_along_axis(scores, ind_top, axis=1)
    top_labels = np.take_along_axis(labels, ind_top, axis=1)
    return top_scores, top_labels


def get_scores(filenames_pair, batch_size, top, th_step):
    metrics_evaluator = BasicMetricsEvaluator(filenames_pair, batch_size, top, th_step)
    confusion_matrix, local_top_scores, local_top_labels = metrics_evaluator.eval()
    labels_1 = metrics_evaluator.emb_loader1.labels
    fp = confusion_matrix.fp
    tp = confusion_matrix.tp
    tn = confusion_matrix.tn
    fn = confusion_matrix.fn
    return local_top_scores, local_top_labels, labels_1, fp, tp, fn, tn


def write_far_frr(output, far, frr):
    file = open(output, "w")
    for i in range(len(far)):
        file.write(str(far[i]) + ' ' + str(frr[i]) + '\n')


def approximate(val, far, frr):
    far_approx = val
    frr_approx = None
    for i in range(1, len(far)):
        if far[i] < far_approx < far[i - 1]:
            frr_approx = frr[i] + (frr[i - 1] - frr[i]) * (far[i] - far_approx) / (far[i] - far[i - 1])
    return frr_approx


class Metrics:
    def __init__(self, input, batch_size, n_workers, th_step, top):
        self.input = input
        self.batch_size = batch_size
        self.n_workers = n_workers
        self.th_step = th_step
        self.top = top
        self.fp = None
        self.tp = None
        self.fn = None
        self.tn = None
        self.far = None
        self.frr = None
        self.frr_approx = None
        self.err = None
        self.recall = None
        self.precision = None
        self.f1_score = None
        self.top1_acc = None
        self.area = None
        self.top_acc = 0

    def eval_base_metrics(self):
        if self.fp is None or self.tp is None or self.fn is None or self.tn is None or self.top1_acc is None:
            print('Evaluating False Positives, True Positives, True Negatives, False Negatives, Top 1 Accuracy')
            embeddings_filenames = list(glob.glob(os.path.join(self.input, '*.npz')))
            print(embeddings_filenames)
            self.fp, self.tp, self.fn, self.tn = 0, 0, 0, 0
            n_correct_matches = 0
            n_labels = 0
            for filename_1 in (embeddings_filenames):
                compare_pairs = list(itertools.product([filename_1], embeddings_filenames))
                work = partial(get_scores, batch_size=self.batch_size, top=self.top, th_step=self.th_step)
                with Pool(self.n_workers, maxtasksperchild=1) as pool:
                    # with Pool(1, maxtasksperchild=1) as pool:
                    vals = list((pool.imap(work, compare_pairs)))
                    pool.close()
                    pool.join()
                # на выходе получили значения для всей строки блочной матрицы.
                # распаковываем результат. в batches_top_scores будут batches_top_scores вычисленные на всех блоках
                # текущей строки блоков, аналогично с другими массивами.
                batches_top_scores, batches_top_labels, gt_labels, fp, tp, fn, tn = list(zip(*vals))
                # c ft, tp, tn, fn все просто - их просто суммируем
                self.fp += np.sum(fp, axis=0)
                self.tp += np.sum(tp, axis=0)
                self.tn += np.sum(tn, axis=0)
                self.fn += np.sum(fn, axis=0)
                # нам нужно сконкатенировать локальные топы по горизонтали
                # в итоге batches_top_scores содержит топ скоры со всей строки блоков, то есть будет размера
                # (число эмбеддингов в файле filename_1) x (top * число файлов с эмбеддингами)
                batches_top_scores = np.concatenate(batches_top_scores, axis=1)
                batches_top_labels = np.concatenate(batches_top_labels, axis=1)
                gt_labels = gt_labels[0]
                _, top_labels = get_tops(batches_top_scores, batches_top_labels, self.top)
                # проверяем есть ли среди top_labels правильные. для этого вычитаем из top_labels
                # истинные метки gt_labels и проверяем есть ли там нули. если есть 0, то значит
                # сматченная метки совпала с настоящей
                matches = top_labels == gt_labels[:, np.newaxis]
                # считаем сколько в каждой строке правильных совпадений
                n_matches = np.sum(matches, axis=1)
                n_correct_matches += np.sum(n_matches > 0)
                n_labels += len(gt_labels)

            # fix everything because of cosine similarity symmetry
            #assert np.allclose(np.remainder(self.tp, 2), 0)
            #assert np.allclose(np.remainder(self.fp, 2), 0)
            #assert np.allclose(np.remainder(self.tn, 2), 0)
            #assert np.allclose(np.remainder(self.fn, 2), 0)
            self.tp /= 2
            self.fp /= 2
            self.tn /= 2
            self.fn /= 2
            #assert np.allclose(self.tp + self.fp + self.tn + self.fn, n_labels * (n_labels - 1) / 2)
            self.top_acc = n_correct_matches / n_labels

    def eval_far_frr(self):
        print('Evaluating FAR and FRR')
        if self.fp is None or self.tp is None or self.fn is None or self.tn is None:
            self.eval_base_metrics()
        self.far = self.fp / (self.fp + self.tn)
        self.frr = self.fn / (self.fn + self.tp)

    def eval_frr(self, val):
        if self.far is None or self.frr is None:
            self.eval_far_frr()
        self.frr_approx = approximate(val, self.far, self.frr)

    def eval_det_curve_area(self):
        print('Evaluating Area under DET Curve')
        self.area = auc(self.far, self.frr)

    def eval_err(self):
        print('Evaluating Error')
        if self.far is None or self.frr is None:
            self.eval_far_frr()
        far = np.array(self.far)
        frr = np.array(self.frr)
        diff = abs(far - frr)
        err_id = np.argmin(diff)
        far_err = far[err_id]
        frr_err = frr[err_id]
        self.err = (far_err + frr_err) / 2

    def eval_recall_precision(self):
        print('Evaluating Recall and Precision')
        if self.fp is None or self.tp is None or self.fn is None:
            self.eval_base_metrics()
        self.recall = self.tp / (self.tp + self.fn)
        self.precision = self.tp / (self.tp + self.fp)

    def eval_f1_score(self):
        print('Evaluating F1 Score')
        if self.recall is None and self.precision is None:
            self.eval_recall_precision()
        self.f1_score = 2 * (self.recall * self.precision) / (self.recall + self.precision)


    def generate_result(self):
        self.eval_far_frr()
        self.eval_frr(10 ** (-4))
        self.eval_det_curve_area()
        self.eval_err()
        self.eval_recall_precision()
        self.eval_f1_score()

        metric = {'threshold_step': self.th_step,
                  'FP': list(self.fp),
                  'TP': list(self.tp),
                  'FN': list(self.fn),
                  'TN': list(self.tn),
                  'FAR': list(self.far),
                  'FRR': list(self.frr),
                  'FRR@FAR = 10^-4': self.frr_approx,
                  'Area under DET curve': self.area,
                  'ERR': self.err,
                  'Recall': list(self.recall),
                  'Precision': list(self.precision),
                  'F1_Score': list(self.f1_score),
                  'Top_1': self.top_acc}
        return metric
