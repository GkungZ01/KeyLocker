import ctypes
from datetime import datetime
import os
import sys

class logSystem:
  fileName = ""
  nosave = False

  def __init__(self, fileName: str = "log.txt", nosave: bool = False) -> None:
    self.nosave = nosave
    if os.path.exists(fileName):
      os.remove(fileName)
    else:
      if os.access(os.getcwd(), os.X_OK):
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
      open(fileName, "x")
    self.fileName = fileName
  
  def __getTime(self):
    return datetime.now().strftime("%H:%M:%S")
  
  def add(self, tag : str, message : str):
    if not self.nosave:
      with open(self.fileName, "a") as f:
        f.write(f"[{self.__getTime()}][{tag}]: {message}\n")
