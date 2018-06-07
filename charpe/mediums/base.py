class BaseMedium:

    def __init__(self, config):
        self.config = config
        self.initialize()

    def initialize(self):
        pass

    def render_template(self, name, **kwargs):
        template = self.jinja.get_template(name, globals={
            'config': self.config,
        })

        return template.render(**kwargs)

    def publish(self, message):
        raise NotImplementedError('Overwrite in subclass')
