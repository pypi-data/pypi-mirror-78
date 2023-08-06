ATTRIBUTES = [
    'identifier', 'title', 'publisher', 'description', 'visibility'
]

class Dataset:
    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def publisher(self):
        return self.publisher

    @publisher.setter
    def publisher(self, publisher):
        self._publisher = publisher

    @property
    def visibility(self):
        return self.visibility

    @visibility.setter
    def visibility(self, visibility):
        self._visibility = visibility

    def serialize(self):
        result = dict()

        for item in ATTRIBUTES:
            attr = getattr(self, item)

            if attr and attr != '':
                result[item] = attr

        return result
