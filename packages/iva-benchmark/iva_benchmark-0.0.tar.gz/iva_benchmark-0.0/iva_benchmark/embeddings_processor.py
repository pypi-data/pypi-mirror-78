import os

import cv2
import numpy as np
from tqdm import tqdm

from .utils import DataLoader


def load_dataset(input_directory, dataset_name):
    dataloader = DataLoader(dataset_name, input_directory)
    files = dataloader.load_dataset()
    return files


def read_embeddings(filename):
    data = np.load(filename)
    embeddings = data['embeddings']
    labels = data['labels']
    filepaths = data['filepaths']
    return embeddings, labels, filepaths


class EmbeddingLoader:
    def __init__(self, filename, batch_size):
        self.emb_filename = filename
        self.batch_size = batch_size
        self.embeddings, self.labels, self.filepaths = read_embeddings(self.emb_filename)

    def get(self, i=-1):
        if i != -1:
            embeddings_part = self.embeddings[i * self.batch_size: (i + 1) * self.batch_size, :]
            labels_part = self.labels[i * self.batch_size: (i + 1) * self.batch_size]
            filepath_part = self.filepaths[i * self.batch_size: (i + 1) * self.batch_size]
            return embeddings_part, labels_part, filepath_part
        else:
            return self.embeddings, self.labels, self.filepaths


class EmbeddingWriter(object):
    def __init__(self, output_directory, output_prefix, num_labels_per_file):
        self.output_directory = output_directory
        self.output_prefix = output_prefix
        self.num_labels_per_file = num_labels_per_file
        self.labels_per_file = set()
        self.embeddings = []
        self.labels = []
        self.filepaths = []
        self.written_files_counter = 0

    def flush(self):
        output_filename = os.path.join(self.output_directory,
                                       self.output_prefix + '_%05d.npz' % self.written_files_counter)
        # print('Write embeddings to {output_filename}')
        np.savez(output_filename,
                 embeddings=self.embeddings,
                 labels=self.labels,
                 filepaths=self.filepaths)
        self.written_files_counter += 1
        self.embeddings = []
        self.labels = []
        self.filepaths = []
        self.labels_per_file = set()

    def write(self, embedding, label, filepath):
        if len(self.labels_per_file) > self.num_labels_per_file:
            self.flush()

        self.labels_per_file.add(label)
        self.embeddings.append(embedding)
        self.labels.append(label)
        self.filepaths.append(filepath)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()


class EmbeddingBuilder:
    def __init__(self, detector, embedder):  # metrics will be an array
        self.detector = detector
        self.embedder = embedder

    def _get_image(self, path):
        image_bgr = cv2.imread(path, 1)
        if self.detector is not None:
            raise NotImplementedError()
        else:
            return image_bgr

    def _get_embedding(self, image):
        embedding = self.embedder.get_embedding(image)
        return embedding

    def save_embeddings(self, input_directory, dataset_name, output_directory, output_prefix, n_labels_per_file):
        with EmbeddingWriter(output_directory, output_prefix, n_labels_per_file) as writer:
            files = load_dataset(input_directory, dataset_name)
            for path in tqdm(files):
                label = files[path]
                image = self._get_image(path)
                embedding = self._get_embedding(image)
                writer.write(embedding, label, path)
