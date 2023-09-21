import gui
import importlib

importlib.reload(gui)


def execute():
    print("Updated")
    win = gui.guerillaTagsEditor()
    win.show()
