import os

PREFIX = 'SOURCE'


class Source:
    @staticmethod
    def loadFromEnv():
        name = os.environ[f'{PREFIX}_NAME']
        identifier = os.environ[f'{PREFIX}_IDENTIFIER']

        return Source({
            'name': name,
            'identifier': identifier
        })

    def __init__(self, config):
        self._name = config['name']
        self._identifier = config['identifier']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    def serialize(self):
        return {
            'name': self._name,
            'identifier': self._identifier
        }
