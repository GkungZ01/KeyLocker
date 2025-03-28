import tkinter
import os
import tkinter.ttk


def SetGeometry(app: tkinter.Tk | tkinter.Toplevel, geometry: str, CenterScreen: bool = False):

    if not CenterScreen:
        app.geometry(geometry)
        return

    size = tuple(int(_) for _ in geometry.split('+')[0].split('x'))

    x = int((app.winfo_screenwidth() / 2) - (size[0] / 2))
    y = int((app.winfo_screenheight() / 2) - (size[1] / 2))

    app.geometry(f"+{x}+{y}")


def CenterScreen(app: tkinter.Tk | tkinter.Toplevel):
    size = tuple(int(_) for _ in app.geometry().split('+')[0].split('x'))

    x = int((app.winfo_screenwidth() / 2) - (size[0] / 2))
    y = int((app.winfo_screenheight() / 2) - (size[1] / 2))

    app.geometry(f"+{x}+{y}")


def NotReSize(app: tkinter.Tk | tkinter.Toplevel):
    app.resizable(width=False, height=False)


def setIcon(app: tkinter.Tk | tkinter.Toplevel, icon_path: str):
    if not icon_path:
        return
    if os.path.exists(icon_path):
        if os.path.splitext(icon_path)[1] == ".ico":
            app.iconbitmap(icon_path)
        else:
            ph = tkinter.PhotoImage(file=icon_path)
            app.iconphoto(False,ph)
