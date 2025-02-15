from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *
from tkinter.messagebox import *
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from PyQt5 import QtGui, QtWidgets

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


fernet_lock: Fernet = ""
main_password = {}
password_data = {}

random.seed(random.random())

def show_password_dialog():
    """
    แสดงหน้าต่างสำหรับกรอกรหัสผ่าน
    returns: str - รหัสผ่านที่ผู้ใช้กรอก หรือ string ว่างถ้าผู้ใช้ยกเลิก
    """
    dialog_window = Tk()
    tkM.SetGeometry(dialog_window, "500x100", True)
    tkM.NotReSize(dialog_window)
    
    # ใช้ list เพื่อเก็บสถานะการปิดหน้าต่าง
    dialog_result = [False]
    # เพิ่มตัวแปรเก็บสถานะการแสดงรหัสผ่าน
    show_password = [False]
    
    def handle_dialog_close():
        """จัดการเมื่อผู้ใช้ปิดหน้าต่าง"""
        dialog_result[0] = False
        dialog_window.destroy()
    
    def handle_submit():
        """จัดการเมื่อผู้ใช้กดยืนยัน"""
        dialog_result[0] = True
        dialog_window.destroy()
    
    def handle_select_all(event):
        event.widget.event_generate("<<SelectAll>>")
        return "break"
    
    # เพิ่มฟังก์ชันสำหรับสลับการแสดงรหัสผ่าน
    def toggle_password_visibility():
        show_password[0] = not show_password[0]
        password_entry.config(show="" if show_password[0] else "*")
    
    # กำหนดชื่อหน้าต่างตามสถานะ
    if "salt" in main_password:
        dialog_window.title("KeyLocker | Login")
    else:
        dialog_window.title("KeyLocker | New Password")
    
    password_var = StringVar()
    
    # สร้าง UI elements
    input_frame = Frame(dialog_window, pady=15)
    input_frame.pack()
    
    label = Label(input_frame, text='Enter Password:', font=('Arial', 11))
    label.pack(side='left', padx=5)
    
    password_entry = Entry(
        input_frame, 
        width=40, 
        show="*", 
        textvariable=password_var,
        font=('Arial', 11),
        )
    password_entry.pack(side='left', padx=5)
    password_entry.focus_set()
    password_entry.bind('<Return>', lambda _: handle_submit())
    
    show_password_button = Button(
        input_frame, 
        text="👁", 
        width=3,
        height=1,
        command=toggle_password_visibility,
        font=('Arial', 11),
        )
    show_password_button.pack(side='left', padx=5)
    
    button_frame = Frame(dialog_window, pady=10)
    button_frame.pack()
    
    submit_button = Button(button_frame, text="Submit", font=('Arial', 10))
    submit_button.pack(side='left', padx=5)
    submit_button.bind('<Button-1>', lambda _: handle_submit())
    
    cancel_button = Button(button_frame, text="Cancel", font=('Arial', 10))
    cancel_button.pack(side='right', padx=5)
    cancel_button.bind('<Button-1>', lambda _: handle_dialog_close())
    
    # จัดการการปิดหน้าต่าง
    dialog_window.protocol("WM_DELETE_WINDOW", handle_dialog_close)
    dialog_window.grab_set()
    
    dialog_window.bind('<Control-a>', handle_select_all)
    
    # เพิ่ม focus อีกครั้งหลังจากสร้าง UI เสร็จ
    dialog_window.lift()
    dialog_window.focus_force()
    
    dialog_window.wait_window(dialog_window)
    
    return password_var.get() if dialog_result[0] else ""

def get_main_password():
    global main_password
    if os.path.exists("mainpass.passlock"):
        password_file = open("mainpass.passlock", "r+").read()
        if password_file:
            try:
                main_password = json.loads(password_file)
            except json.decoder.JSONDecodeError:
                showerror("PassLock", "File is not json")
                exit(1)
    else:
        open("mainpass.passlock", "x")


def generate_salt(size=16):
    return secrets.token_bytes(size)


def get_salt(password: str):
    return generate_salt(random.randint(1, 16))


def derive_key(password, salt):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def get_key(password):
    global main_password
    # get salt
    salt: bytes

    if "salt" in main_password:
        salt = base64.b64decode(main_password["salt"].encode())
    else:
        salt = get_salt(password)
        main_password["salt"] = base64.b64encode(salt).decode()
        save_main_password()

    # generate the key from the salt and the password
    derived_key = derive_key(password, salt)
    # encode it using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)


def save_main_password():
    global password_data, main_password

    if fernet_lock:
        main_password['data'] = base64.b64encode(
            fernet_lock.encrypt(json.dumps(password_data).encode())).decode()
    with open("mainpass.passlock", "w") as file_data:
        file_data.write(json.dumps(main_password))


def login():
    global password_data, fernet_lock
    password = show_password_dialog()

    if not password:
        sys.exit(1)

    fernet = Fernet(get_key(
        hashlib.sha256(password.encode()).hexdigest()))

    try:
        password_data = {} if "data" not in main_password else json.loads(
            fernet.decrypt(base64.b64decode(main_password["data"].encode())))
        fernet_lock = fernet
    except FileNotFoundError:
        open("mainpass.passlock", "x")
        password_data = {}
    except InvalidToken:
        showerror(
            "KeyLocker", "Invalid password")


def handle_selection_changed():
    global selected_index, selected_key_name
    index = ui_main.listView.selectionModel().currentIndex()
    key_name = list_view_model.data(index, 0)
    item = find_key(key_name)
    if item:
        selected_index = index.row()
        selected_key_name = key_name
        ui_main.tbKey.setText(item["NameKey"])
        ui_main.tbU.setText(item["Username"])
        ui_main.tbP.setText(item["Password"])
    
        ui_main.btnEdit.setEnabled(True)
        ui_main.btnDelete.setEnabled(True)
        ui_main.btnCopyU.setEnabled(True)
        ui_main.btnCopyP.setEnabled(True)
        ui_main.btnAdd.setEnabled(False)


def add_key():
    if ui_main.tbKey.text() == "":
        showerror("KeyLocker", "Name Key is Empty")
        return
    new_key = {
        "NameKey": ui_main.tbKey.text(),
        "Username": ui_main.tbU.text(),
        "Password": ui_main.tbP.text()
    }
    password_data["Keys"].append(new_key)
    save_main_password()
    clear_form()
    load_keys()

def edit_key():
    if selected_index == -1:
        return
    if ui_main.tbKey.text() == "":
        showerror("KeyLocker", "Name Key is Empty")
        return
    updated_key = {
        "NameKey": ui_main.tbKey.text(),
        "Username": ui_main.tbU.text(),
        "Password": ui_main.tbP.text()
    }
    password_data["Keys"][find_key_index(selected_key_name)] = updated_key
    save_main_password()
    clear_form()
    load_keys()

def delete_key():
    global password_data
    if selected_index == -1: return
    del(password_data["Keys"][find_key_index(selected_key_name)])
    save_main_password()
    clear_form()
    load_keys()

def clear_form():
    ui_main.cbSPass.setChecked(False)
    ui_main.listView.clearSelection()
    ui_main.tbKey.setText("")
    ui_main.tbU.setText("")
    ui_main.tbP.setText("")
    
    global selected_index
    selected_index = -1
    ui_main.btnEdit.setEnabled(False)
    ui_main.btnDelete.setEnabled(False)
    ui_main.btnCopyU.setEnabled(False)
    ui_main.btnCopyP.setEnabled(False)
    ui_main.btnAdd.setEnabled(True)

def find_key(nameKey: str):
    for Key in password_data["Keys"]:
        if nameKey == Key["NameKey"]:
            return Key
    return False


def find_key_index(nameKey: str):
    for idx, Key in enumerate(password_data["Keys"]):
        if nameKey == Key["NameKey"]:
            return idx
    return False

def load_keys(Keys : list = False):
    list_view_model.clear()
    for Key in Keys if (not Keys == False) else password_data["Keys"]:
        list_view_model.appendRow(
            QtGui.QStandardItem(Key["NameKey"]))

def search_keys():
    search_text = ui_main.tbSearch.text()
    found_keys = []
    for key in password_data["Keys"]:
        if search_text in key["NameKey"]:
            key["idx"] = find_key_index(key["NameKey"])
            found_keys.append(key)
    load_keys(found_keys)
    
def copy_username():
    pyperclip.copy(ui_main.tbU.text())
    

def copy_password():
    pyperclip.copy(ui_main.tbP.text())
    

def stateChanged(state: int):
    if state == 2:
        ui_main.tbP.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
    else:
        ui_main.tbP.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

def main():
    global password_data, ui_main, list_view_model
    # Check File Main Pass
    
    # Login
    if not fernet_lock:
        login()
        return main()
    
    if "Keys" not in password_data:
        password_data["Keys"] = []
        save_main_password()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui_main = UiMain.Ui_Main()
    ui_main.setupUi(MainWindow)

    # Setting
    ui_main.btnEdit.setEnabled(False)
    ui_main.btnDelete.setEnabled(False)
    ui_main.btnCopyU.setEnabled(False)
    ui_main.btnCopyP.setEnabled(False)

    list_view_model = QtGui.QStandardItemModel()
    ui_main.listView.setModel(list_view_model)
    
    # เพิ่มการตั้งค่าฟอนต์สำหรับ listView
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(11)
    ui_main.listView.setFont(font)
    
    ui_main.tbP.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    # Event

    ui_main.listView.selectionModel().selectionChanged.connect(
        handle_selection_changed
    )

    ui_main.btnAdd.clicked.connect(add_key)
    ui_main.btnDelete.clicked.connect(delete_key)
    ui_main.btnEdit.clicked.connect(edit_key)
    ui_main.btnClear.clicked.connect(clear_form)
    
    ui_main.btnCopyU.clicked.connect(copy_username)
    ui_main.btnCopyP.clicked.connect(copy_password)
    
    ui_main.cbSPass.stateChanged.connect(stateChanged)
    
    ui_main.btnSearch.clicked.connect(search_keys)
    
    # End Event

    load_keys()

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    get_main_password()
    main()
