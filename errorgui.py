# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'errordialog.ui'
#
# Created: Thu Apr 24 17:42:04 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(411, 142)
        self.okbutton = QtGui.QDialogButtonBox(Dialog)
        self.okbutton.setGeometry(QtCore.QRect(40, 100, 341, 32))
        self.okbutton.setOrientation(QtCore.Qt.Horizontal)
        self.okbutton.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.okbutton.setObjectName("okbutton")
        self.error = QtGui.QLabel(Dialog)
        self.error.setGeometry(QtCore.QRect(40, 30, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.error.setFont(font)
        self.error.setText("")
        self.error.setObjectName("error")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.okbutton, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QObject.connect(self.okbutton, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

"""
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

"""
