import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

import kanjiease
import listings2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        print 'fuccck'
        return s


class ExampleApp(QtGui.QMainWindow, kanjiease.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        self.charline.returnPressed.connect(self.UpdateKanjiBox)

    def kanjiDef(self, text):
            entries = listings2.trydef(text)
            entries = listings2.parsedef(entries)
            self.KanjiList.setRowCount(len(entries))
            self.KanjiList.setColumnCount(3)
            header = self.KanjiList.horizontalHeader()
            header.setStretchLastSection(True)

            print entries
            trans = []
            # todo: add sublists so that it splits items by 3 and wraps them.
            for i, entry in enumerate(entries):
                head, read = entry[0:2]
                self.KanjiList.setItem(i, 0, QtGui.QTableWidgetItem(head))
                self.KanjiList.setItem(i, 1, QtGui.QTableWidgetItem(read))
                trans = [x for x in entry[2:]]
                trans = '|'.join(trans)
                self.KanjiList.setItem(i, 2, QtGui.QTableWidgetItem(trans))
            # self.KanjiList.setColumnCount(len(entries[0]))
            #for i, row in enumerate(entries):
            #        print row
            #        item = QtGui.QTableWidgetItem(row)
            #        self.KanjiList.setItem(i, 0, head)
            #        self.KanjiList.setItem(i, 1, read)
            #        self.KanjiList.setItem(i, 1, trans)



    def UpdateKanjiBox(self):
        message = unicode(self.charline.text())
        kanjitext = message
        layout = kanjiease._translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">" + kanjitext + "</span></p></body></html>", None)
        self.KanjiBox.setHtml(layout)
        self.kanjiDef(message)
        self.KanjiBox.show()


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
