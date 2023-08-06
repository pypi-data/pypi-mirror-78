from .embedders import create_mxnet_embedder


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_object(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)

class EmbedderFactory(ObjectFactory):
    pass


embedder_factory = EmbedderFactory()
embedder_factory.register_object('MXNET', create_mxnet_embedder)
