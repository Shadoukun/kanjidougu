import sip
sip.setapi('QVariant', 2)
import win32api
import functions, jdict, nhocr, popup, rectangle
import settings
from functions import imageOCR
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
from ctypes import wintypes
import ctypes
import pyHook
import os


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
myappid = u'Kanjidougu.v.0.2'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class KanjiDougu(QtWidgets.QMainWindow):

    closep = QtCore.pyqtSignal()

    def __init__(self):
        super(KanjiDougu, self).__init__()
        self.settings = QSettings("__settings.ini", QSettings.IniFormat)
        self.setWindowTitle("KanjiDougu")
        self.resize(900, 500)
        self.initUI()
        self.createActions()
        self.createTrayIcon()
        self.setIcon()
        self.dialog = popup.Dialog()
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = self.hotkeyPressEvent
        self.hm.HookKeyboard()


    def initUI(self):

        # setting menu selector
        self.settingwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.settingwidget)
        self.createSettingList()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.settinglist, 0, 0, 5, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.currentmenu, 0, 1, 0, 3, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.settingwidget.setLayout(grid)

    def createSettingList(self):
        self.SettingIndex = QtCore.pyqtSignal
        self.settinglist = QtWidgets.QListView()
        self.menus = ["General"]
        model = QtGui.QStandardItemModel(self.settinglist)
        for menu in self.menus:
            menuitem = QtGui.QStandardItem(menu)
            model.appendRow(menuitem)
        self.settinglist.setModel(model)
        self.settinglist.clicked.connect(self.on_setting_changed)
        self.settinglist.setCurrentIndex(model.index(0, 0))
        self.currentmenu = settings.GeneralSettings()

    def createActions(self):

        self.restoreAction = QtWidgets.QAction("&Settings", self, triggered=self.showNormal)
        self.quitAction = QtWidgets.QAction("&Quit", self, triggered=QtWidgets.qApp.quit)


    def on_setting_changed(self):

        if self.settinglist.currentIndex() is 0:
            self.currentmenu = settings.GeneralSettings()
    def createTrayIcon(self):
        self.trayIconMenu = QtWidgets.QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def setIcon(self):
        icon = QtGui.QIcon('./images/ji.svg')
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.trayIcon.show()

    def hotkeyPressEvent(self, event):
        if event.KeyID is 163:
            self.ocrEvent()
        if event.KeyID is 27:
            QtWidgets.qApp.quit()

    def ocrEvent(self):
        cx, cy = win32api.GetCursorPos()
        # height and width of screengrab
        h = self.settings.value('height', type=int)
        w = self.settings.value('width', type=int)
        text, img, preview = imageOCR(h, w)
        self.makeBox(h, w, cx, cy)
        self.makePopup(text)

    def makeBox(self, h, w, cx, cy):
        self.box = rectangle.Box()
        self.box.height = h
        self.box.width = w
        self.box.cx = cx - (h / 2)
        self.box.cy = cy - (w / 2)
        self.box.setVisible(True)
        self.box.closep.connect(self.closepopups)
        self.box.show()

    def makePopup(self, text):
        self.dialog.setkanjiBox(text)
        self.dialog.setDefList(text)
        self.dialog.show()

    def closepopups(self):
        self.dialog.setHidden(True)
        self.box.setHidden(True)

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)

    if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
        QtWidgets.QMessageBox.critical(None, "KanjiDougu", "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)

    window = KanjiDougu()
    window.show()
    sys.exit(app.exec_())
