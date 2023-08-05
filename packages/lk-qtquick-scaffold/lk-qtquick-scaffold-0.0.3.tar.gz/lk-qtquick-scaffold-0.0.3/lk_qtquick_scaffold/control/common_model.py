from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt


class CommonModel(QAbstractListModel):
    """
    NOTE:
        1. to subclass CommonModel, you only need to do is defining roles_meta
        and add_item().
        2. make sure the qml use the same key name.
    
    https://blog.csdn.net/Likianta/article/details/105820227
    http://cn.voidcc.com/question/p-zilozvfe-ug.html
    https://www.xdbcb8.com/archives/701.html
    
    why subclassing QAbstractListModel?
        according to QML.ListView.model property description:
            The model provides the set of data that is used to create the items
            in the view. Models can be created directly in QML using ListModel,
            XmlListModel or ObjectModel, or provided by C++ model classes. If a
            C++ model class is used, it must be a subclass of QAbstractItemModel
            or a simple list.
        well actually we can use QAbstractListModel instead of
        QAbstractItemModel, that's what the later one suggested us in its
        detailed description:
            If you need a model to use with an item view such as QML's List View
            element or the C++ widgets QListView or QTableView, you should
            consider subclassing QAbstractListModel or QAbstractTableModel
            instead of this class.
    """
    roles_meta: tuple  # (<str key>, ), user defined
    _roles_dct_4_data: dict  # auto gen
    _roles_dct_4_qml: dict  # auto gen
    
    def __init__(self, model: list = None):
        super().__init__()
        self.model = model or []
        self._adapt_roles()
    
    def _adapt_roles(self):
        """
        roles_meta = {'name': 'abc', 'age': 20}
        -> _roles_dct_4_data = {1: 'name', 2: 'age'}
        -> _roles_dct_4_qml = {1: b'name', 2: b'age'}
        """
        self._roles_dct_4_data = {}
        self._roles_dct_4_qml = {}
        for num, key in enumerate(self.roles_meta, 1):
            # role_no 是随便定义的值, 只要保证不重复且为整数就行了. 这里我没有用
            # 1, 2, 3, ... 而是用了 Qt.UserRole + 1, 2, 3, ... 就是为了保证与其
            # 他 flag "不重复".
            role_no = Qt.UserRole + num
            self._roles_dct_4_qml[role_no] = bytes(key, encoding='utf-8')
            self._roles_dct_4_data[role_no] = key
            # use bytes(key), also to make sure the qml use the same key name.
    
    # noinspection PyUnusedLocal
    def row_count(self, parent=None) -> int:
        return len(self.model)
    
    rowCount = row_count
    
    def role_names(self):
        return self._roles_dct_4_qml
    
    roleNames = role_names
    
    def data(self, index: QModelIndex, role_no: int = None):
        """
        :param index: 注意这个是 QModelIndex 类型. 我们需要通过
            QModelIndex.row() 方法取得它的真正的 (int 类型的) index.
        :param role_no:
        :return:
        """
        # noinspection PyUnusedLocal
        row = self.model[index.row()]  # type: dict
        # e.g. row = {'index': 4, 'duration': 120, 'clock': '02:00:00'}
        key = self._roles_dct_4_data[role_no]  # type: str
        # e.g. role_no = 258 -> key = 'duration'
        return row.get(key)
    
    def add_item(self, item):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.model.append(item)
        self.endInsertRows()
    
    def delete_item(self, index):
        self.beginRemoveRows(QModelIndex(), index, index)
        self.model.pop(index)
        self.endRemoveRows()

    def updated_item(self, index, item):
        self.beginResetModel()
        self.model[index] = item
        self.endResetModel()
