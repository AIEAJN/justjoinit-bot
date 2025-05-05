import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "Setup The bot"

    property bool isLoading: false
    property bool hasJobs: false

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
                enabled: !isLoading
            }

            TextField {
                id: positionField
                placeholderText: "Enter Position"
                font.pixelSize: 16
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                Material.accent: "#007bff"
                enabled: !isLoading
            }

            Button {
                id: validateButton
                text: "Valider"
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 150
                Layout.preferredHeight: 40
                Material.background: "#007bff"
                Material.foreground: "white"
                enabled: !isLoading
                visible: !isLoading
                onClicked: {
                    isLoading = true
                    backend.set_config(locationField.text, positionField.text)
                }
            }

            ColumnLayout {
                visible: isLoading
                Layout.fillWidth: true
                spacing: 10

                ProgressBar {
                    Layout.fillWidth: true
                    indeterminate: true
                    Material.accent: "#007bff"
                }

                Text {
                    text: backend.loadingMessage
                    Layout.alignment: Qt.AlignHCenter
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    Layout.maximumWidth: parent.width
                }
            }
        }
    }

    Dialog {
        id: completionDialog
        title: "Process completed"
        modal: true
        standardButtons: Dialog.Ok
        anchors.centerIn: parent
        width: 300

        ColumnLayout {
            anchors.fill: parent
            spacing: 10

            Text {
                text: "The process is completed.\nThe file 'applied_jobs.csv' has been generated."
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
            }
        }

        onAccepted: {
            close()
        }
    }

    Dialog {
        id: noJobsDialog
        title: "No jobs found"
        modal: true
        standardButtons: Dialog.Ok
        anchors.centerIn: parent
        width: 300

        ColumnLayout {
            anchors.fill: parent
            spacing: 10

            Text {
                text: "No jobs found.\nPlease try again with different parameters."
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
            }
        }

        onAccepted: {
            close()
        }
    }

    Connections {
        target: backend
        function onLoadedChanged(loaded) {
            isLoading = !loaded
            if (loaded && hasJobs) {
                completionDialog.open()
            }
            else {
                noJobsDialog.open()
            }
        }
    }
}
