import QtQuick 2.15
import "../Specifications/geometry.js" as Geometry

Rectangle {
    id: root
    implicitWidth: Geometry.BAR_WIDTH; implicitHeight: Geometry.BAR_HEIGHT
    radius: Geometry.RADIUS1
    property alias p_radius: root.radius
}
