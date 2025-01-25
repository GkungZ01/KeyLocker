from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *
from tkinter.messagebox import *
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from PyQt5 import QtCore, QtGui, QtWidgets

import components.tkinterMore as tkM
import base64
import secrets
import os
import json
import hashlib
import random
import sys
import ui.main as UiMain
import pyperclip


FPassLock: Fernet = ""
MainPass = {}
data = {}

random.seed(random.random())

def askPassword():
    top = Tk()  # use Toplevel() instead of Tk()
    tkM.SetGeometry(top,"450x80", True)
    tkM.NotReSize(top)
    if "salt" in MainPass:
        top.title("KeyLocker | Login")
    else :
        top.title("KeyLocker | New Password")
    value = StringVar()
    FI = Frame(top)
    FI.pack()
    Label(FI, text='Enter Password:').pack(side='left')
    tbPass = Entry(FI, width=40, show="*", textvariable=value)
    tbPass.pack(side='left')
    FD = Frame(top, pady=10)
    FD.pack()
    btnS = Button(FD,text="Submit")
    btnS.pack(side='left')
    btnS.bind('<Button-1>', lambda _: top.destroy())
    btnC = Button(FD,text="Cancel")
    btnC.pack(side='right')
    btnC.bind('<Button-1>', lambda _: top.destroy())
    top.grab_set()
    top.wait_window(top)  # wait for itself destroyed, so like a modal dialog
    return value.get()

def getMainPass():
    global MainPass
    if os.path.exists("mainpass.passlock"):
        mpf = open("mainpass.passlock", "r+").read()
        if mpf:
            try:
                MainPass = json.loads(mpf)
            except json.decoder.JSONDecodeError:
                showerror("PassLock", "File is not json")
                exit(1)
    else :
        open("mainpass.passlock", "x")


def generate_salt(size=16):
    return secrets.token_bytes(size)


def get_salt(password: str):
    return generate_salt(random.randint(1, 16))


def derive_key(password, salt):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def get_key(password):
    global MainPass
    # get salt
    salt: bytes

    if "salt" in MainPass:
        salt = base64.b64decode(MainPass["salt"].encode())
    else:
        salt = get_salt(password)
        MainPass["salt"] = base64.b64encode(salt).decode()
        saveMainPass()

    # generate the key from the salt and the password
    derived_key = derive_key(password, salt)
    # encode it using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)


def saveMainPass():
    global data, MainPass

    if FPassLock:
        MainPass['data'] = base64.b64encode(
            FPassLock.encrypt(json.dumps(data).encode())).decode()
    with open("mainpass.passlock", "w") as file_data:
        file_data.write(json.dumps(MainPass))
    print("SAVE")


def login():
    global data, FPassLock
    password = askPassword()

    if not password:
        exit(1)

    fernet = Fernet(get_key(
        hashlib.sha256(password.encode()).hexdigest()))

    try:
        data = {} if "data" not in MainPass else json.loads(
            fernet.decrypt(base64.b64decode(MainPass["data"].encode())))
        FPassLock = fernet
    except FileNotFoundError:
        open("mainpass.passlock", "x")
        data = {}
    except InvalidToken:
        showerror(
            "PassLock", "Invalid token, most likely the password is incorrect")


def handle_selection_changed():
    global SelectedIndex, SelectedNameKey
    index = uiMain.listView.selectionModel().currentIndex()
    nameKey = listViewModel.data(index, 0)
    item = findKey(nameKey)
    if item:
        SelectedIndex = index.row()
        SelectedNameKey = nameKey
        uiMain.tbKey.setText(item["NameKey"])
        uiMain.tbU.setText(item["Username"])
        uiMain.tbP.setText(item["Password"])
    
        uiMain.btnEdit.setEnabled(True)
        uiMain.btnDelete.setEnabled(True)
        uiMain.btnCopyU.setEnabled(True)
        uiMain.btnCopyP.setEnabled(True)
        uiMain.btnAdd.setEnabled(False)


def clickAddKey():
    if uiMain.tbKey.text() == "":
        showerror("KeyLocker", "Name Key is Empty")
        return
    Key_ = {
        "NameKey": uiMain.tbKey.text(),
        "Username": uiMain.tbU.text(),
        "Password": uiMain.tbP.text()
    }
    data["Keys"].append(Key_)
    saveMainPass()
    clickClear()
    loadKeys()
    

def clickEdit():
    if SelectedIndex == -1:
        return
    if uiMain.tbKey.text() == "":
        showerror("KeyLocker", "Name Key is Empty")
        return
    Key_ = {
        "NameKey": uiMain.tbKey.text(),
        "Username": uiMain.tbU.text(),
        "Password": uiMain.tbP.text()
    }
    data["Keys"][findIndexKey(SelectedNameKey)] = Key_
    saveMainPass()
    clickClear()
    loadKeys()

def clickDelete():
    global data
    if SelectedIndex == -1 : return
    del(data["Keys"][findIndexKey(SelectedNameKey)])
    saveMainPass()
    clickClear()
    loadKeys()

def clickClear():
    uiMain.cbSPass.setChecked(False)
    uiMain.listView.clearSelection()
    uiMain.tbKey.setText("")
    uiMain.tbU.setText("")
    uiMain.tbP.setText("")
    
    SelectedIndex = -1
    uiMain.btnEdit.setEnabled(False)
    uiMain.btnDelete.setEnabled(False)
    uiMain.btnCopyU.setEnabled(False)
    uiMain.btnCopyP.setEnabled(False)
    uiMain.btnAdd.setEnabled(True)

def findKey(nameKey: str):
    for Key in data["Keys"]:
        if nameKey == Key["NameKey"]:
            return Key
    return False


def findIndexKey(nameKey: str):
    for idx, Key in enumerate(data["Keys"]):
        if nameKey == Key["NameKey"]:
            return idx
    return False

def loadKeys(Keys : list = False):
    listViewModel.clear()
    for Key in Keys if (not Keys == False) else data["Keys"]:
        listViewModel.appendRow(
            QtGui.QStandardItem(Key["NameKey"]))

def clickSearch():
    search = uiMain.tbSearch.text()
    Keys = []
    for Key in data["Keys"]:
        if search in Key["NameKey"]:
            Key["idx"] = findIndexKey(Key["NameKey"])
            Keys.append(Key)
    loadKeys(Keys)
    
def CopyU():
    pyperclip.copy(uiMain.tbU.text())
    

def CopyP():
    pyperclip.copy(uiMain.tbP.text())
    

def stateChanged(state: int):
    print("Change")
    if state == 2:
        uiMain.tbP.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
    else:
        uiMain.tbP.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

def main():
    global data, uiMain, listViewModel
    # Check File Main Pass
    
    # Login
    if not FPassLock:
        login()
        return main()
    
    if not "Keys" in data:
        data["Keys"] = []
        saveMainPass()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    uiMain = UiMain.Ui_Main()
    uiMain.setupUi(MainWindow)

    # Setting
    uiMain.btnEdit.setEnabled(False)
    uiMain.btnDelete.setEnabled(False)
    uiMain.btnCopyU.setEnabled(False)
    uiMain.btnCopyP.setEnabled(False)

    listViewModel = QtGui.QStandardItemModel()
    uiMain.listView.setModel(listViewModel)
    
    uiMain.tbP.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    # Event

    uiMain.listView.selectionModel().selectionChanged.connect(
        handle_selection_changed
    )

    uiMain.btnAdd.clicked.connect(clickAddKey)
    uiMain.btnDelete.clicked.connect(clickDelete)
    uiMain.btnEdit.clicked.connect(clickEdit)
    uiMain.btnClear.clicked.connect(clickClear)
    
    uiMain.btnCopyU.clicked.connect(CopyU)
    uiMain.btnCopyP.clicked.connect(CopyP)
    
    uiMain.cbSPass.stateChanged.connect(stateChanged)
    
    uiMain.btnSearch.clicked.connect(clickSearch)
    
    # End Event

    loadKeys()

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    getMainPass()
    main()
