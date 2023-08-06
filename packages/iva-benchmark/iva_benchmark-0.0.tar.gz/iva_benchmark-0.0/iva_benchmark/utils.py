import os
import base64
import numpy as np

def base64_to_numpy(string, dtype):
    decoded = base64.b64decode(string)
    array = np.frombuffer(decoded, dtype=dtype)
    return array

def file_to_base64(filepath):
    with open(filepath, 'rb') as input_stream:
        return base64.b64encode(input_stream.read())

def get_full_paths(input_directory):
    for root, directories, filenames in os.walk(input_directory):
        for filename in filenames:
            yield os.path.join(root, filename)


def get_pairs_for_comparison(filenames):
    pairs = []
    for i in range(len(filenames)):
        for j in range(len(filenames)):
            pairs.append((filenames[i], filenames[j]))
    return pairs


class DataLoader:
    def __init__(self, dataset_name, dataset_path):
        self.dataset_name = dataset_name
        self.dataset_path = dataset_path

    def load_dataset(self):
        loader = self._get_dataset_loader()
        return loader()

    def _get_dataset_loader(self):
        if self.dataset_name == 'LFW':
            return self._load_lfw
        elif self.dataset_name == 'EBS':
            raise NotImplementedError()
        else:
            raise ValueError(self.dataset_name)

    def _load_lfw(self):
        files = {}
        filepaths = get_full_paths(self.dataset_path)
        for path in filepaths:
            directory_path = os.path.split(path)[0]
            label = os.path.split(directory_path)[1]
            files[path] = label
        return files



