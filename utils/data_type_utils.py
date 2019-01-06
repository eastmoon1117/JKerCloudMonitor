# -*- coding: utf-8 -*-
import types


class DataTypeUtils:
    @staticmethod
    def is_Int(data):
        return type(data) == type(1)

    @staticmethod
    def is_String(data):
        return type(data) == type('a') or type(data) == type(u'a')

    @staticmethod
    def is_Boolean(data):
        # return type(data) == types.BoolType
        return isinstance(data, (bool))
