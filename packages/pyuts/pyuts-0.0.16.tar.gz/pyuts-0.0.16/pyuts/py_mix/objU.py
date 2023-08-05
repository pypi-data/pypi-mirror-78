# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class ObjU(PyApiB):
    """
    obj相关操作工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def find(self, item, filed):
        """ 查找数据项 """
        if item == None:
            return None
        if '.' in filed:
            fs = filed.split('.')
            newItem = self.find(item, fs[0])
            return self.find(newItem, filed[len(fs[0]) + 1:])
        else:
            if filed.isdigit() or (filed[:1] == '-' and filed[1:].isdigit()):
                try:
                    return item[int(filed)]
                except BaseException as e:
                    return None
            else:
                return item.get(filed)

    def update(self, item, filed, value):
        """ 更新数据项 """
        if item == None:
            return
        if '.' in filed:
            fs = filed.split('.')
            newItem = self.find(item, fs[0])
            if newItem == None:
                newV = {}
                if fs[1].isdigit():
                    newV = [None] * (int(fs[1])+1)
                if fs[1][:1] == '-' and fs[1][1:].isdigit():
                    newV = [None] * (int(fs[1][1:]))
                self.update(item, fs[0], newV)
                newItem = newV
            self.update(newItem, filed[len(fs[0]) + 1:], value)
        else:
            if filed.isdigit() or (filed[:1] == '-' and filed[1:].isdigit()):
                ss = int(filed)
                if ss < 0:
                    ss = -ss - 1
                if len(item) <= ss:
                    apNum = ss - len(item) + 1
                    for ii in range(0, apNum):
                        item.append(None)
                item[int(filed)] = value
            else:
                item[filed] = value

    def merge(self, fromItem, toItem, fromFiled, toFiled, formatFun=None):
        """ 复制数据项 """
        value = self.find(fromItem, fromFiled)
        if value == None:
            return
        if formatFun:
            value = formatFun(value)
        self.update(toItem, toFiled, value)

    def merge2(self, canCopy, fromItem, toItem, fromFiled, toFiled, formatFun=None):
        """ 复制数据项，与copy方法功能一样，唯一区别第一位加入开关参数 """
        if not canCopy:
            return
        self.merge(fromItem, toItem, fromFiled, toFiled, formatFun)

    def copy(self, data):
        import copy
        return copy.copy(data)
    
    def deepcopy(self, data):
        import copy
        return copy.deepcopy(data)
