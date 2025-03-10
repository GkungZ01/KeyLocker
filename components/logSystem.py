from datetime import datetime
import os

print("Current Working Directory:", os.getcwd())

class logSystem:
  fileName = ""

  def __init__(self, fileName: str | None = "log.txt") -> None:
    if os.path.exists(fileName):
      os.remove(fileName)
    else:
      open(fileName, "x")
    self.fileName = fileName
  
  def __getTime(self):
    return datetime.now().strftime("%H:%M:%S")
  
  def add(self, tag : str, message : str):
    with open(self.fileName, "a") as f:
      f.write(f"[{self.__getTime()}][{tag}]: {message}\n")
