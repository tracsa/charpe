class Handler:

    def __init__(self, config):
        self.config = config

    def publish(self, message):
        raise NotImplementedError('Overwrite in subclass')
