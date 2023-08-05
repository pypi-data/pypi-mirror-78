import QtQuick 2.15
import "../Specifications/palette.js" as Palette

Text {
    id: root
    color: Palette.TEXT_NORMAL
    font.family: "Microsoft YaHei UI"
    font.pixelSize: 13
    horizontalCenter: Text.AlignHCenter; verticalCenter: Text.AlignVCenter

    property alias p_text: root.text
    property alias p_size: root.font.pixelSize
}
