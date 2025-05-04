import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "Setup The bot"

    Rectangle {
        anchors.centerIn: parent
        width: 400
        height: 300
        color: "#f0f0f0"
        radius: 10
        border.color: "#cccccc"
        border.width: 1

        ColumnLayout {
            anchors.centerIn: parent
            spacing: 20
            width: parent.width - 40

            Text {
                text: "Bot Configuration"
                font.pixelSize: 24
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            TextField {
                id: locationField
                placeholderText: "Enter Location"
                font.pixelSize: 16
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                Material.accent: "#007bff"
            }

            TextField {
                id: positionField
                placeholderText: "Enter Position"
                font.pixelSize: 16
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                Material.accent: "#007bff"
            }

            Button {
                text: "Valider"
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 150
                Layout.preferredHeight: 40
                Material.background: "#007bff"
                Material.foreground: "white"
                onClicked: {
                    backend.set_config(locationField.text, positionField.text)
                }
            }
        }
    }
}