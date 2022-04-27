from collections import namedtuple

# all primitives
num_temp = 7
float_temp = 6.23
str_temp = "microwave"
bool_temp = True
bytes_temp = bytes(b'\xd0\x91\xd0\xb0\xd0\xb9\xd1\x82\xd1\x8b')
bytes_arr_temp = bytearray(bytes_temp)
buitin_func_temp = dir


class TempClass:
    def __init__(self):
        self.el1 = 't'
        self.el2 = 2


class ClassB:
    pass


class ClassA(TempClass, ClassB):
    pass


# temp object
obj1 = TempClass()


# global variable
age = 'eighteen'


# function with globals variable
def my_age_question():
    global age
    return 'How old are you? I am ' + age


test_age_answer = 'How old are you? I am eighteen'


# temp function
def question():
    return 'How old are you?'


test_question = 'How old are you?'


# lambda function
multiple = lambda x, y: x * y
test_multiple = 10  # x = 2, y = 5

# lists(set, tuple, frozenset)
list_temp = ['one', 2, 'three']
set_temp = set(list_temp)
frozenset_temp = frozenset(list_temp)
tuple_temp = tuple(list_temp)

# dict
dict_temp = {'first': 1, 'second': 2}
test_dict = namedtuple('object', ['first', 'second'])(*[1, 2])


# function with parameters
def mul_params(first, second):
    return first * second



