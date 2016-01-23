# -*- coding: utf-8 -*-

#from PyQt4 import QtCore, QtGui
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
import jdict



class Dialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.resize(600,200)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.KanjiBox = QtWidgets.QTextBrowser(parent=self)
        self.readList = QtWidgets.QTextBrowser(self)
        self.deflist = QtWidgets.QTableWidget(self)
        self.deflist.setStyleSheet('background-color:#d6d6d6')
        print self.deflist.horizontalHeader().setVisible(False)
        self.deflist.setColumnCount(1)
        self.deflist.setRowCount(1)
        self.deflist.setItem(0, 0, QtWidgets.QTableWidgetItem('test'))
        self.deflist.setGeometry(QtCore.QRect(0, 100, 400, 100))
        self.deflist.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.setStyleSheet("background-color:#3d3d3d;")
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(1)
        grid.addWidget(self.KanjiBox, 1, 0)
        grid.addWidget(self.readList, 1, 1)
        grid.addWidget(self.deflist, 2, 0, QtCore.Qt.AlignLeft, 2)
        self.deflist.setMinimumSize(QtCore.QSize(10, 10))
        self.deflist.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        grid.setRowStretch(2, 0)
        self.setLayout(grid)

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(qp.Antialiasing, on=True)
        font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        qp.setFont(font)
        qp.end()

    def setDefList(self, text):
        entries = jdict.trydef(text)
        print text
        entries = jdict.parsedef(entries)
        print entries
        self.deflist.setRowCount(len(entries))
        self.deflist.setColumnCount(3)
        header = self.deflist.horizontalHeader()
        header.setStretchLastSection(False)

        #print entries
        trans = []
        #todo: add sublists so that it splits items by 3 and wraps them.
        for i, entry in enumerate(entries):
            head, read = entry[0:2]
            try:
                self.deflist.setItem(i, 0, QtWidgets.QTableWidgetItem(head))
                self.deflist.setItem(i, 1, QtWidgets.QTableWidgetItem(read))
                trans = [x for x in entry[2:]]
                trans = '|'.join(trans)
                self.deflist.setItem(i, 2, QtWidgets.QTableWidgetItem(trans))
            except TypeError:
                print 'error'
        self.deflist.setWordWrap(True)
        self.deflist.horizontalHeader().setStretchLastSection(True)


    def setkanjiBox(self, text):
        self.KanjiBox.setStyleSheet("background-color:#d6d6d6")
        self.KanjiBox.setText(u'<center style="color:black; font-size:30pt;">{t}</center>'.format(t=text))
        #boxsize = QtCore.QSize(90, 90)
        self.KanjiBox.setMaximumSize(QtCore.QSize(100, 150))
        self.KanjiBox.show()

    def setreadList(self, text):
        self.readList.setStyleSheet('background-color:#d6d6d6')
        self.readList.setGeometry(QtCore.QRect(90, 0, 310, 100))
        self.readList.setText(u'<strong>Kun: </strong><br><br><strong>On: </strong>')
        self.readList.show()

    def showEvent(self, event):
        geom = self.frameGeometry()
        cursor = QtGui.QCursor.pos()
        corner = (cursor.x() + (geom.width() / 2), cursor.y() + (geom.height() / 2))
        corner = (corner[0] + 30, corner[1] + 30)
        newpos = QtCore.QPoint(*corner)
        geom.moveCenter(newpos)
        self.setGeometry(geom)
        super(Dialog, self).showEvent(event)


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            event.accept()
        else:
            super(Dialog, self).keyPressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    d = Dialog()
    d.show()
    d.raise_()

    app.exec_()
