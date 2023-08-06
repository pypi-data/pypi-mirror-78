ATTRIBUTES = [
    'title', 'publisher',
    'description', 'specURL', 'visibility'
]

class API:
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        self._publisher = publisher

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def specURL(self):
        return self._specURL

    @specURL.setter
    def specURL(self, specURL):
        self._specURL = specURL

    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        self._visibility = visibility

    def __init__(self, title, publisher, **args):
        self._title = title
        self._publisher = publisher
        self._description = args.get('description', None)
        self._specURL = args.get('specURL', None)
        self._visibility = args.get('visibility', None)

    def serialize(self):
        result = dict()

        for item in ATTRIBUTES:
            attr = getattr(self, item)

            if attr and attr != '':
                result[item] = attr

        return result
