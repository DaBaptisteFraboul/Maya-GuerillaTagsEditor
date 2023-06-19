import gui
import importlib

importlib.reload(gui)

def execute():
    win = gui.guerillaTagsEditor()
    win.show()
