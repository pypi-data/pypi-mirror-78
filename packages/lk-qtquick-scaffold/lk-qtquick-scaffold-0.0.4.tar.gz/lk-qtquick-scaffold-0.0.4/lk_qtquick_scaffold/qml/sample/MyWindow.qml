import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    color: "black"  // 注意: 必须 `import QtQuick 2.15`, color 属性才可以定义.
    //  否则会报 "Invalid property assignment: color expected" 错误.
    visible: true
    width: 800; height: 600

    MyEditbar {
        width: 200; height: 40
    }
}
