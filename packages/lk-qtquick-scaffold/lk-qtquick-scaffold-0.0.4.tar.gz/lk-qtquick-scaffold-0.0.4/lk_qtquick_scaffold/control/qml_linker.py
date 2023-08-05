from PySide2.QtCore import QObject
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQuick import QQuickItem


# noinspection PyTypeChecker
class QmlLinker:
    """
    当 qml engine 加载布局完成后, 使用本类连接 qml 核心对象, 以便于其他 python
    对象通过本类接触到 qml object.
    """
    
    def __init__(self, engine: QQmlApplicationEngine):
        self.root = engine.rootObjects()[0]
        self.context = engine.rootContext()
    
    def find_obj(self, obj_name: str) -> QObject:
        return self.root.findChild(QObject, obj_name)

    # noinspection PyUnusedLocal
    def connect(self, qml_target, signal, py_method):
        view = self.find_obj(qml_target)
        eval(f'view.{signal}.connect(py_method)')
    
    @staticmethod
    def get_children(view: QObject) -> list:
        if view.property('model'):
            # https://blog.csdn.net/Likianta/article/details/105863572
            children = []
            for i in range(view.property('count')):
                view.setProperty('currentIndex', i)  # 强制切换 index.
                item = view.property('currentItem')  # type: QQuickItem
                children.append(item)
            return children
        else:
            return view.children()
