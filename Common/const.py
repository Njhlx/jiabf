# -*- coding: utf-8 -*-
import sys


class _Const:
    class ConsError(TypeError):pass

    def __setattr__(self, name, value):
        for key in self.__dict__:
            if key == name:
                raise self.ConsError("Can't rebind const " + name)
        self.__dict__[name] = value


sys.modules[__name__] = _Const()


# import sys
#
# sys.modules[__name__] = _const()
#
# class _const:
#     class ConstError(TypeError) : pass
#
#
# def __setattr__(self, key, value):
#         # self.__dict__
#         if self.__dict__.has_key(key):
#             raise self.ConstError("constant reassignment error!")
#         self.__dict__[key] = value

