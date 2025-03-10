# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KeyLocker(object):
    def setupUi(self, KeyLocker):
        KeyLocker.setObjectName("KeyLocker")
        KeyLocker.setWindowModality(QtCore.Qt.WindowModal)
        KeyLocker.resize(852, 473)
        KeyLocker.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        KeyLocker.setFocusPolicy(QtCore.Qt.ClickFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\../assets/icons/icon_by_icons8.com.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        KeyLocker.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(KeyLocker)
        self.centralwidget.setObjectName("centralwidget")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 50, 401, 381))
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.setObjectName("listView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 120, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btnCopyU = QtWidgets.QPushButton(self.centralwidget)
        self.btnCopyU.setGeometry(QtCore.QRect(750, 150, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnCopyU.setFont(font)
        self.btnCopyU.setObjectName("btnCopyU")
        self.btnCopyP = QtWidgets.QPushButton(self.centralwidget)
        self.btnCopyP.setGeometry(QtCore.QRect(750, 240, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnCopyP.setFont(font)
        self.btnCopyP.setObjectName("btnCopyP")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(450, 210, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.btnAdd = QtWidgets.QPushButton(self.centralwidget)
        self.btnAdd.setGeometry(QtCore.QRect(440, 400, 91, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnAdd.setFont(font)
        self.btnAdd.setObjectName("btnAdd")
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setGeometry(QtCore.QRect(540, 400, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnDelete.setFont(font)
        self.btnDelete.setObjectName("btnDelete")
        self.btnEdit = QtWidgets.QPushButton(self.centralwidget)
        self.btnEdit.setGeometry(QtCore.QRect(640, 400, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnEdit.setFont(font)
        self.btnEdit.setObjectName("btnEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(450, 30, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setGeometry(QtCore.QRect(340, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnSearch.setFont(font)
        self.btnSearch.setObjectName("btnSearch")
        self.tbP = QtWidgets.QLineEdit(self.centralwidget)
        self.tbP.setGeometry(QtCore.QRect(440, 240, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tbP.setFont(font)
        self.tbP.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tbP.setObjectName("tbP")
        self.tbU = QtWidgets.QLineEdit(self.centralwidget)
        self.tbU.setGeometry(QtCore.QRect(440, 150, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tbU.setFont(font)
        self.tbU.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tbU.setObjectName("tbU")
        self.tbKey = QtWidgets.QLineEdit(self.centralwidget)
        self.tbKey.setGeometry(QtCore.QRect(440, 70, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tbKey.setFont(font)
        self.tbKey.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tbKey.setObjectName("tbKey")
        self.tbSearch = QtWidgets.QLineEdit(self.centralwidget)
        self.tbSearch.setGeometry(QtCore.QRect(70, 10, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tbSearch.setFont(font)
        self.tbSearch.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tbSearch.setObjectName("tbSearch")
        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setGeometry(QtCore.QRect(740, 400, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnClear.setFont(font)
        self.btnClear.setObjectName("btnClear")
        self.cbSPass = QtWidgets.QCheckBox(self.centralwidget)
        self.cbSPass.setGeometry(QtCore.QRect(440, 290, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cbSPass.setFont(font)
        self.cbSPass.setObjectName("cbSPass")
        KeyLocker.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(KeyLocker)
        self.statusbar.setObjectName("statusbar")
        KeyLocker.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(KeyLocker)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 852, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu_Help = QtWidgets.QMenu(self.menuBar)
        self.menu_Help.setObjectName("menu_Help")
        KeyLocker.setMenuBar(self.menuBar)
        self.actionAbout = QtWidgets.QAction(KeyLocker)
        self.actionAbout.setObjectName("actionAbout")
        self.menu_Help.addAction(self.actionAbout)
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(KeyLocker)
        QtCore.QMetaObject.connectSlotsByName(KeyLocker)

    def retranslateUi(self, KeyLocker):
        _translate = QtCore.QCoreApplication.translate
        KeyLocker.setWindowTitle(_translate("KeyLocker", "KeyLocker"))
        self.label.setText(_translate("KeyLocker", "Username or Email or Phone"))
        self.btnCopyU.setText(_translate("KeyLocker", "Copy"))
        self.btnCopyP.setText(_translate("KeyLocker", "Copy"))
        self.label_2.setText(_translate("KeyLocker", "Password"))
        self.btnAdd.setText(_translate("KeyLocker", "Add"))
        self.btnDelete.setText(_translate("KeyLocker", "Delete"))
        self.btnEdit.setText(_translate("KeyLocker", "Edit"))
        self.label_3.setText(_translate("KeyLocker", "Name Key"))
        self.label_4.setText(_translate("KeyLocker", "Search"))
        self.btnSearch.setText(_translate("KeyLocker", "Search"))
        self.btnClear.setText(_translate("KeyLocker", "Clear"))
        self.cbSPass.setText(_translate("KeyLocker", "Show Password"))
        self.menu_Help.setTitle(_translate("KeyLocker", "&Help"))
        self.actionAbout.setText(_translate("KeyLocker", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    KeyLocker = QtWidgets.QMainWindow()
    ui = Ui_KeyLocker()
    ui.setupUi(KeyLocker)
    KeyLocker.show()
    sys.exit(app.exec_())
