from abc import ABC, abstractmethod

import cv2
import mxnet as mx
import numpy as np


class Embedder(ABC):
    @abstractmethod
    def preprocess_input(self, image):
        pass

    @abstractmethod
    def get_embedding(self, image):
        pass


class MXNET_Embedder(Embedder):
    def __init__(self, device, prefix, epoch, flip):
        self.ctx = mx.cpu() if device == 'cpu' else mx.gpu()
        sym, self.arg_params, self.aux_params = mx.model.load_checkpoint(prefix, epoch)
        all_layers = sym.get_internals()
        self.sym = all_layers['fc1_output']
        self.flip = flip

    def preprocess_input(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 1, 2)
        img = img[np.newaxis, :]
        return img

    def get_net_out(self, image):
        self.arg_params["data"] = mx.nd.array(image, self.ctx)
        self.data_shape = self.arg_params["data"].shape
        model = self.sym.bind(self.ctx, self.arg_params, args_grad=None, grad_req="null", aux_states=self.aux_params)
        model.forward(is_train=False)
        net_out = np.squeeze(model.outputs[0].asnumpy())
        return net_out

    def get_embedding(self, image):
        image_ppsd = self.preprocess_input(image)
        embedding = self.get_net_out(image_ppsd)
        if self.flip:
            image_flipped = cv2.flip(image, 1)
            image_flipped_ppsd = self.preprocess_input(image_flipped)
            embedding_flipped = self.get_net_out(image_flipped_ppsd)
            embedding += embedding_flipped
        embedding_norm = embedding/np.linalg.norm(embedding)
        return embedding_norm


def create_mxnet_embedder(device, prefix, epoch, flip, **_ignored):
    return MXNET_Embedder(device, prefix, epoch, flip)
