from Serializers.Factory import factory


# final serializer
class Serializer:

    def __init__(self, path="", name='json'):
        self._path = path
        self._name = name
        self.factory = factory.Factory(self._path)
        self.serializer = self.factory.create_serializer(self._name)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path
        self.factory = factory.Factory(self._path)
        self.serializer = self.factory.create_serializer(self._path)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.serializer = self.factory.create_serializer(self._name)

    def dump(self, obj):
        self.serializer.dump(obj)

    def dumps(self, obj):
        return self.serializer.dumps(obj)

    def load(self):
        return self.serializer.load()

    def loads(self, obj_str):
        return self.serializer.loads(obj_str)
