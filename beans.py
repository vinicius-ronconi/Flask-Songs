from collections import namedtuple


class RequestParameterValidator(namedtuple('RequestParameterValidator', [
    'cast_func',  # collections.Callable
    'required',  # bool
    'min_value',  # obj
    'max_value',  # obj
    'default',  #obj
])):
    pass
