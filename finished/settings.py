from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings


class GeneralSettings(QtWidgets.QWidget):

    def __init__(self):
        super(GeneralSettings, self).__init__()
        self.settings = QSettings("__settings.ini", QSettings.IniFormat)
        self.general = QtWidgets.QWidget()
        self.general.setObjectName("OCRSize")
        self.general.setMaximumHeight(200)
        self.general.setMinimumWidth(300)

        boxsizegroup = QtWidgets.QGroupBox("OCR Box Size", self.general)
        boxsizegroup.setMinimumWidth(200)
        boxsizegroup.setMinimumHeight(200)
        # OCR bbox height box
        label = QtWidgets.QLabel(boxsizegroup)
        label.setText("OCR Height:")
        self.heightbox = QtWidgets.QSpinBox(boxsizegroup)
        self.heightbox.setObjectName("OCRHeightBox")
        heightvalue = self.settings.value('height', type=int)
        self.heightbox.setValue(heightvalue)
        self.heightbox.valueChanged.connect(self.on_heightbox_valueChanged)
        # Seperator
        line = QtWidgets.QFrame(boxsizegroup)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        # OCR bbox width box
        label_2 = QtWidgets.QLabel(boxsizegroup)
        label_2.setText("OCR Width:")
        self.widthbox = QtWidgets.QSpinBox(boxsizegroup)
        self.widthbox.setObjectName("OCRWidthBox")
        widthvalue = self.settings.value('width', type=int)
        self.widthbox.setValue(widthvalue)
        self.widthbox.valueChanged.connect(self.on_widthbox_changed)

        rectanglecheck = QtWidgets.QCheckBox(boxsizegroup)
        #Layout
        verticalLayout = QtWidgets.QVBoxLayout(boxsizegroup)
        verticalLayout.addWidget(label)
        verticalLayout.addWidget(self.heightbox)
        verticalLayout.addWidget(line)
        verticalLayout.addWidget(label_2)
        verticalLayout.addWidget(self.widthbox)
        self.general.setLayout(verticalLayout)

    def on_heightbox_valueChanged(self):
        value = self.heightbox.value()
        self.settings.setValue('height', value)

    def on_widthbox_changed(self):
        value = self.widthbox.value()
        self.settings.setValue('width', value)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = GeneralSettings()
    window.show()
    sys.exit(app.exec_())
