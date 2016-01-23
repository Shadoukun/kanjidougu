from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt

class GeneralSettings(QtWidgets.QWidget):

    def __init__(self):
        super(GeneralSettings, self).__init__()
        self.settings = QSettings("__settings.ini", QSettings.IniFormat)
        checkbox = QtWidgets.QCheckBox('Hide Border')
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.bbox_options(), 0, 0, Qt.AlignTop)
        grid.addWidget(checkbox, 0, 1, Qt.AlignLeft)
        self.setLayout(grid)
    def bbox_options(self):
        groupBox = QtWidgets.QGroupBox("OCR Box")
        label = QtWidgets.QLabel("Height:")
        heightbox = QtWidgets.QSpinBox()
        heightvalue = self.settings.value('height', type=int)
        heightbox.setValue(heightvalue)
        heightbox.valueChanged.connect(self.on_heightbox_valueChanged)
        # OCR bbox width box
        label_2 = QtWidgets.QLabel("Width:")
        widthbox = QtWidgets.QSpinBox()
        widthvalue = self.settings.value('width', type=int)
        widthbox.setValue(widthvalue)


        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.addWidget(label)
        verticalLayout.addWidget(heightbox)
        verticalLayout.addWidget(label_2)
        verticalLayout.addWidget(widthbox)
        groupBox.setLayout(verticalLayout)
        groupBox.setMinimumWidth(150)
        return groupBox



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
