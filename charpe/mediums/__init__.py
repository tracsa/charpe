class BaseMedium:

    def __init__(self, config):
        self.config = config
        self.initialize()

    def initialize(self):
        pass

    def publish(self, message):
        raise NotImplementedError('Overwrite in subclass')
