本目录文件说明:

**qtquick.qch**

该文件是 QML Types 手册, 可通过 Qt 助手加载.

如需获取完整的手册, 请这样做:

1. 从 PyPI 下载 PyQtdoc 的 whl 文件 (国内可使用镜像源链接: https://pypi.tuna.tsinghua.edu.cn/simple/pyqtdoc/).
2. 将 .whl 后缀名 改为 .zip, 并解压缩.
3. 在解压后的文件夹中, 向下找到 'data' 文件夹, 内含 .qch 文件.
4. 将这些 .qch 文件加载到 Qt 助手即可.

由于 PyQtdoc 提供的 .qch 文件似乎不是完整的, 尤其是缺少 'qtquick\*.qch', 所以本项目提供了这些文件资源.
