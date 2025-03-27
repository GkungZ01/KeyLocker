from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *
from tkinter.messagebox import *
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from PyQt5 import QtGui, QtWidgets

import modules.tkinterMore as tkM
import base64
import secrets
import os
import json
import hashlib
import random
import sys
import ui.main as UiMain
import pyperclip
import ctypes
from modules.logSystem import logSystem


fernet_lock: Fernet = ""
main_password = {}
password_data = {}
temp_list = {}
file_path = "mainpass.passlock"
selected_index = -1
selected_key = ""
devMode = False

# Config

version = "1.0.1"

random.seed(random.random())

_logSystem = logSystem()

log = _logSystem.add


def show_password_dialog():
    """
    แสดงหน้าต่างสำหรับกรอกรหัสผ่าน
    returns: str - รหัสผ่านที่ผู้ใช้กรอก หรือ string ว่างถ้าผู้ใช้ยกเลิก
    """
    dialog_window = Tk()
    tkM.SetGeometry(dialog_window, "500x100", True)
    tkM.NotReSize(dialog_window)
    tkM.setIcon(dialog_window, "assets/icons/icon_by_icons8.com.ico")

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
    
    password_entry.focus_set()

    dialog_window.wait_window(dialog_window)

    return password_var.get() if dialog_result[0] else ""


def get_main_password():
    global main_password
    log("INFO", "Check File Main Pass")
    if os.path.exists(file_path):
        password_file = open(file_path, "r").read()
        if password_file:
            try:
                main_password = json.loads(password_file)
                log("INFO", "File Main Pass found and loaded")
            except json.decoder.JSONDecodeError:
                log("ERROR", "File Main Pass is not json")
                showerror("PassLock", "File is not json")
                exit(1)
    else:
        log("INFO", "File Main Pass not found")
        log("INFO", "Create File Main Pass")
        open(file_path, "x")


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


def generate_id_key():
    return secrets.token_hex(16)


def _get_key():
    key = generate_id_key()
    if (key in password_data["Keys"]):
        return _get_key()
    return key


def fix_keys() -> dict:
    keys = password_data["Keys"]
    _keys = {}

    for key in keys:
        _keys.update({_get_key(): key})
    return _keys


def save_main_password():
    log("INFO", "Save Main Password")
    global password_data, main_password

    if fernet_lock:
        main_password['data'] = base64.b64encode(
            fernet_lock.encrypt(json.dumps(password_data).encode())).decode()
    with open(file_path, "w") as file_data:
        file_data.write(json.dumps(main_password))


def login():
    global password_data, fernet_lock
    password = show_password_dialog()

    if not password:
        log("INFO", "Exit Program")
        sys.exit(1)

    fernet = Fernet(get_key(
        hashlib.sha256(password.encode()).hexdigest()))

    try:
        password_data = {} if "data" not in main_password else json.loads(
            fernet.decrypt(base64.b64decode(main_password["data"].encode())))
        fernet_lock = fernet
    except FileNotFoundError:
        open(file_path, "x")
        password_data = {}
    except InvalidToken:
        showerror(
            "KeyLocker", "Invalid password")


def handle_selection_changed():
    global selected_index, selected_key
    index = ui_main.listView.selectionModel().currentIndex()
    selected_index = index.row()
    ui_main.btnClearSelection.setEnabled(selected_index >= 0)
    if (selected_index >= 0):
        items = temp_list if temp_list else password_data["Keys"]
        item = list(items.values())[selected_index]
        selected_key = list(items.keys())[selected_index]
        ui_main.tbKey.setText(item["NameKey"])
        ui_main.tbU.setText(item["Username"])
        ui_main.tbP.setText(item["Password"])

        ui_main.btnEdit.setEnabled(True)
        ui_main.btnDelete.setEnabled(True)
        ui_main.btnCopyU.setEnabled(True)
        ui_main.btnCopyP.setEnabled(True)
        ui_main.btnAdd.setEnabled(False)

        ui_main.btnClearForm.setEnabled(False)


def add_key():
    global password_data
    if ui_main.tbKey.text() == "":
        showerror("KeyLocker", "Name Key is Empty")
        return

    new_key = {_get_key(): {
        "NameKey": ui_main.tbKey.text(),
        "Username": ui_main.tbU.text(),
        "Password": ui_main.tbP.text()
    }}
    
    password_data["Keys"].update(new_key)
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
    password_data["Keys"][selected_key] = updated_key
    if temp_list:
        if selected_key in temp_list:
            temp_list[selected_key] = updated_key
    save_main_password()
    clear_form()
    load_keys()


def delete_key():
    global password_data
    if selected_index == -1:
        return
    del (password_data["Keys"][selected_key])
    save_main_password()
    clear_form()
    load_keys()


def clear_form():
    ui_main.tbKey.setText("")
    ui_main.tbU.setText("")
    ui_main.tbP.setText("")


def clear_selection():
    global selected_index

    ui_main.btnClearForm.setEnabled(True)
    ui_main.btnAdd.setEnabled(True)
    ui_main.btnEdit.setEnabled(False)
    ui_main.btnDelete.setEnabled(False)
    ui_main.btnCopyU.setEnabled(False)
    ui_main.btnCopyP.setEnabled(False)

    ui_main.listView.selectionModel().clearCurrentIndex()
    ui_main.listView.selectionModel().clearSelection()

    clear_form()


def clear_search():
    global temp_list
    ui_main.tbSearch.setText("")
    temp_list = {}
    load_keys()


def find_key_index(nameKey: str):
    for idx, Key in enumerate(password_data["Keys"]):
        if nameKey == Key["NameKey"]:
            return idx
    return False


def load_keys():
    log("INFO", "Load Keys")
    list_view_model.clear()
    for _, value in temp_list.items() if temp_list else password_data["Keys"].items():
        list_view_model.appendRow(
            QtGui.QStandardItem(value["NameKey"]))


def search_keys():
    global temp_list
    log("INFO", "Search Keys")
    temp_list = {}
    search_text = ui_main.tbSearch.text()
    for key, value in password_data["Keys"].items():
        if search_text.lower() in value["NameKey"].lower():
            temp_list.update({key: value})
    if not temp_list:
        showerror("KeyLocker", "Key Not Found")
    load_keys()


def copy_username():
    pyperclip.copy(ui_main.tbU.text())


def copy_password():
    pyperclip.copy(ui_main.tbP.text())


def stateChanged(state: int):
    if state == 2:
        ui_main.tbP.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
    else:
        ui_main.tbP.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)


def show_about():
    showinfo("KeyLocker", "Version: " + version)


def main():
    global password_data, ui_main, list_view_model
    # Check File Main Pass

    # Login
    if not fernet_lock:
        log("INFO", "Login")
        login()
        return main()

    if "Keys" not in password_data:
        password_data["Keys"] = []
        save_main_password()

    log("INFO", "Start GUI")
    # GUI
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui_main = UiMain.Ui_KeyLocker()
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
    ui_main.btnClearForm.clicked.connect(clear_form)
    ui_main.btnClearSelection.clicked.connect(clear_selection)

    ui_main.btnCopyU.clicked.connect(copy_username)
    ui_main.btnCopyP.clicked.connect(copy_password)

    ui_main.cbSPass.stateChanged.connect(stateChanged)

    ui_main.btnSearch.clicked.connect(search_keys)
    ui_main.btnClearSearch.clicked.connect(clear_search)

    ui_main.actionAbout.triggered.connect(show_about)
    
    ui_main.tbSearch.returnPressed.connect(search_keys)

    # End Event

    if (type(password_data["Keys"]) == list):
        log("INFO", "Fix Keys")
        password_data["Keys"] = fix_keys()
        save_main_password()

    load_keys()

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    if "-dev" in sys.argv[1:]:
        devMode = True
    log("INFO", "Start Program")
    log("INFO", "Check Access File Main Pass")
    # ตรวจสอบว่าโปรแกรมมีสิทธิ์ในการอ่านและเขียนไฟล์หรือไม่
    if not os.access(os.getcwd(), os.R_OK) and not os.access(os.getcwd(), os.W_OK):
        # ตรวจสอบว่าโปรแกรมกำลังทำงานในโหมด Administrator หรือไม่
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # ถ้าไม่ได้รันในโหมด Administrator ให้เรียกใช้โปรแกรมใหม่ในโหมด Administrator
            ctypes.windll.shell32.ShellExecuteW(
                # hwnd: handle ของหน้าต่าง (None = หน้าต่างปัจจุบัน)
                None,
                "runas",       # operation: "runas" คือคำสั่งให้รันในโหมด Administrator
                sys.executable,  # file: path ของไฟล์ Python interpreter
                # parameters: arguments ที่ส่งเข้ามาในโปรแกรม
                " ".join(sys.argv),
                # directory: directory เริ่มต้น (None = directory ปัจจุบัน)
                None,
                1             # show command: 1 = แสดงหน้าต่างปกติ
            )
            sys.exit()        # ออกจากโปรแกรมหลังจากเรียกใช้ในโหมด Administrator

    get_main_password()
    main()
