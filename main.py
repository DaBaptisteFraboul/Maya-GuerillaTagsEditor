from gtag_editor import gui
import importlib

importlib.reload(gui)

win = gui.guerillaTagsEditor()
win.show()