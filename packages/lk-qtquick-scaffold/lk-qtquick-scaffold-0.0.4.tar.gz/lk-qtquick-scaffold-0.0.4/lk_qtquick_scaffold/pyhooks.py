"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : pyhooks.py
@Created : 2020-08-31
@Updated : 2020-09-01
@Version : 0.1.0
@Desc    : 
"""
from typing import *

from PySide2.QtCore import QObject, Slot
from PySide2.QtQml import QJSValue, QQmlContext


# noinspection PyTypeChecker
class PyHooks(QObject):
    """
    Usecase:
        // === ./qml/SomeFolder/SomeComp.qml ===
        import QtQuick 2.15
        Rectangle {
            Text { id: _txt }
            Component.onCompleted: {
                PyHooks.set
            }
        }
    """
    
    def __init__(self, engine: QQmlContext):
        super().__init__()
        self.hooks = {}  # {url: QObject}
        engine.setContextProperty('PyHooks', self)
    
    @Slot()
    def debug(self):
        from lk_utils.lk_logger import lk
        lk.loga(self.hooks)
    
    @staticmethod
    def _qjsval_2_pylist(data: QJSValue) -> list:
        """
        
        :param data: Maybe string or list.
        :return:
        """
        data = data.toVariant()  # type: Union[str, list]
        if isinstance(data, str):
            return [data]
        else:
            return data
    
    @Slot(str, QObject)
    def bind_hook(self, url: str, obj: QObject):
        self.hooks[url] = obj
    
    @Slot(str, QJSValue)
    def bind_hooks(self, url: str, qid_2_obj: QJSValue):
        qid_2_obj = qid_2_obj.toVariant()  # type: dict
        for qid, obj in qid_2_obj.items():
            self.bind_hook(f'{url}#{qid}', obj)
    
    @Slot(str, result=QObject)
    def get_hook(self, url):
        return self.hooks[url]
    
    @Slot(QJSValue, result="QVariant")
    def get_hooks(self, urls):
        return self.get_hooks_of_list(urls)
    
    @Slot(QJSValue, result="QVariant")
    def get_hooks_of_list(self, urls):
        urls = self._qjsval_2_pylist(urls)
        return list(map(self.get_hook, urls))
    
    @Slot(QJSValue, result="QVariant")
    def get_hooks_of_dict(self, urls):
        urls = self._qjsval_2_pylist(urls)
        return dict(zip(urls, map(self.get_hook, urls)))
    
    @Slot(QJSValue, result="QVariant")
    def get_hooks_of_short_dict(self, urls):
        urls = self._qjsval_2_pylist(urls)
        keys = []
        for url in keys:
            qid = url.rsplit('#', 1)[1]
            if qid in keys:
                keys.append(f'{qid}{keys.count(qid)}')
            else:
                keys.append(qid)
        return dict(zip(keys, map(self.get_hook, urls)))
