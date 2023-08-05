import QtQuick 2.15
import "../Specifications/palette.js" as Palette

BasicRect {
    id: root
    border.color: Palette.BORDER_NORMAL
    border.width: p_enableBorder && _area.pressed ? 0 : 1
    color: Palette.BG_GRAY

    property bool p_enableBorder: true
    property alias p_defaultColor: root.color
    property alias p_duration: _transition.duration
    property alias p_radius: root.radius
    signal clicked

    MouseArea {
        id: _area
        anchors.fill: parent
        onClicked: parent.clicked()
    }

    states State {
        when: _area.pressed
        PropertyChanges {
            target: root
            color: Palette.BG_WHITE
        }
    }

    transitions Transition {
        id: _transition
        duration: 200
    }
}
