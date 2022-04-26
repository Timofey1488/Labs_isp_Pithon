from Serializers.picker import picker, unpicker
from Serializers.json_serializer import parser


class JsonSerializer:
    def __init__(self, path: str):
        self.path = path
        self.picker = picker.Picker()
        self.unpicker = unpicker.Unpicker()

    def dump(self, obj: object):
        obj_dict = self.picker.pack(obj)
        with open(self.path, "w") as f:
            parser.dump_parser(obj_dict, fp=f)

    def dumps(self, obj: object):
        obj_dict = self.packer.pack(obj)
        result_string = parser.dumps_parser(obj_dict)
        return result_string

    def load(self):
        obj_dict = {}
        with open(self.path, "r") as f:
            obj_dict = parser.load_parser(f)
        obj = self.unpicker.unpack(obj_dict)
        return obj

    def loads(self, obj_str: str):
        obj_dict = parser.loads_parser(obj_str)
        obj = self.unpicker.unpack(obj_dict)
        return obj