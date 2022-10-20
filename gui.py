from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import os

# Misc functions

def  get_abspath(relative_path):
    path_base = os.path.dirname(__file__)
    path = os.path.join(path_base, relative_path)
    path = path.replace('\\','/')
    return path


def get_clean_selection(get_children = True):
    selection = cmds.ls(selection=True, tr=True)
    if get_children and selection is not None :
        for obj in selection :
            children = cmds.listRelatives(obj)
            if children :
                for child in children :
                    if child not in selection and cmds.nodeType(child) == 'transform' :
                        selection.append(child)
    return selection


# Tags related functions


def create_gtags_attribute(object:str):
    cmds.addAttr(longName='GuerillaTags',dataType = "string")


def has_gtags_attribute(object : str) -> bool:
    """
    Check wether GuerillaTags attribute exist on given object
    :param object:
    :return:
    """
    return cmds.attributeQuery("GuerillaTags", node =object, exists=True)


def get_gtags_attribute(object:str) -> None:
    return cmds.getAttr(f'{object}.GuerillaTags')


def set_gtags_attribute(object, gtags :str):
    cmds.setAttr(f'{object}.GuerillaTags', gtags,typ='string')


def convert_gtags_in_list(guerilla_tags : str) -> list:
    """
    Convert Gtags string into a list
    :param guerilla_tags:
    :return:
    """
    tags = guerilla_tags.replace(" ", "")
    gtags_list = tags.split(",")
    return gtags_list


def convert_gtags_in_string(guerilla_tags : list) -> str:
    """
    Convert a list of tags into the attribute string
    :param guerilla_tags:
    :return:
    """
    gtags_string = str()
    for tags in guerilla_tags :
        if tags == guerilla_tags[0]:
            gtags_string += tags
        else :
            gtags_string += ', ' + tags
    return gtags_string


def is_gtags_empty(object):
    if not cmds.getAttr(f'{object}.GuerillaTags') :
        return True
    else :
        return False


def add_gtag_to_attr(object:str, tags:str):
    old_tags = get_gtags_attribute(object)
    if not old_tags :
        new_tags = tags
    else :
        new_tags = old_tags+ ', ' + tags
    set_gtags_attribute(object, new_tags)


# UI related stuff
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class guerillaTagsEditor(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(guerillaTagsEditor, self).__init__(parent)
        self.import_icons()
        self.create_widgets()
        self.create_layout()
        self.generate_selection_scriptjob()
        self.refresh_tag_list_widget()
        self.setWindowIcon(QtGui.QIcon(get_abspath("icons/guerilla_render.png")))
        self.setWindowTitle("Guerilla Tags editor")
        self.setAcceptDrops(True)

    def import_icons(self):
        self.shared_tag_icon = QtGui.QIcon(get_abspath("icons/star.png"))

    def create_widgets(self):
        self.label_title = QtWidgets.QLabel("Tags on selection")

        self.tag_list = QtWidgets.QListWidget()
        self.tag_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.tag_input = QtWidgets.QLineEdit()
        self.tag_input.setPlaceholderText("Type your GuerillaTags here")

        self.add_tag_buton = QtWidgets.QPushButton('Add tag(s)')
        self.add_tag_buton.clicked.connect(self.add_gtags)

        self.delete_tag_buton = QtWidgets.QPushButton('Delete tag(s)')
        self.delete_tag_buton.clicked.connect(self.delete_tags)

        self.replace_tag_buton = QtWidgets.QPushButton('Replace tag(s)')
        self.replace_tag_buton.clicked.connect(self.replace_tags)

        self.merge_selection = QtWidgets.QPushButton('Merge selected tags')
        self.merge_selection.clicked.connect(self.merge_selected_tags)

        self.merge_all_tags = QtWidgets.QPushButton('Merge all')
        self.merge_all_tags.clicked.connect(self.merge_all)

        self.highlight_shared_tags = QtWidgets.QCheckBox('Highlight shared Tags')
        self.highlight_shared_tags.setChecked(True)
        self.highlight_shared_tags.clicked.connect(self.refresh_tag_list_widget)

        self.get_children_check = QtWidgets.QCheckBox('Affect selection direct children')
        self.get_children_check.setChecked(True)

    def create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.label_title, 0)
        self.main_layout.addWidget(self.tag_list, 1)
        self.main_layout.addWidget(self.tag_input,2)
        self.button_layout_one = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.button_layout_one,3)
        self.button_layout_one.addWidget(self.delete_tag_buton)
        self.button_layout_one.addWidget(self.replace_tag_buton)
        self.button_layout_one.addWidget(self.add_tag_buton)
        self.button_layout_two = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.button_layout_two, 4)
        self.button_layout_two.addWidget(self.merge_selection)
        self.button_layout_two.addWidget(self.merge_all_tags)
        self.main_layout.addWidget(self.highlight_shared_tags, 5)
        self.main_layout.addWidget(self.get_children_check, 6)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else :
            event.ignore()

    def dropEvent(self,event):
        data = event.mimeData().text()
        list = data.split('\n')
        children_list = []
        tag_list = []
        for obj in list:
            if self.get_children_check.isChecked():
                children = cmds.listRelatives(obj)
                if children:
                    for child in children:
                        if child not in children_list and cmds.nodeType(child) == 'transform':
                            children_list.append(child)
            if has_gtags_attribute(obj) and not is_gtags_empty(obj):
                obj_tags = convert_gtags_in_list(get_gtags_attribute(obj))
                for tags in obj_tags :
                    if tags not in tag_list :
                        tag_list.append(tags)
                    else :
                        pass
        for child in children_list :
            if has_gtags_attribute(child) and not is_gtags_empty(child):
                obj_tags = convert_gtags_in_list(get_gtags_attribute(child))
                for tags in obj_tags:
                    if tags not in tag_list:
                        tag_list.append(tags)
                    else:
                        pass
        line_edit_text = convert_gtags_in_string(tag_list)
        self.tag_input.setText(line_edit_text)

    def generate_selection_scriptjob(self):
        self.script_job = cmds.scriptJob(event =['SelectionChanged', self.refresh_tag_list_widget], protected=False)

    def closeEvent(self, event):
        print("Closing Gtags editor event")
        cmds.scriptJob(kill = self.script_job)
        event.accept()

    def check_shared_tags(self):
        """
        Modify widget if their tag is shared with all selection
        :return:
        """
        list_widget_items = []
        selection = cmds.ls(selection=True,tr = True)
        for i in range(self.tag_list.count()):

            list_widget_items.append(self.tag_list.item(i))

        for items in list_widget_items:
            is_shared = True
            tag = items.text()
            for obj in selection:
                if not has_gtags_attribute(obj):
                    is_shared = False
                elif is_gtags_empty(obj) :
                    is_shared = False
                elif tag not in convert_gtags_in_list(get_gtags_attribute(obj)):
                    is_shared=False
            if is_shared:
                items.setIcon(self.shared_tag_icon)
            else :
                items.setIcon(QtGui.QIcon())

    def add_item_to_list(self):
        item = QtWidgets.QListWidgetItem("Hello")
        item.setIcon(self.all_icons)
        item.setSizeHint(QtCore.QSize(20, 30))
        self.tag_list.addItem(item)

    def get_items_on_list(self):
        """
        Get the list of tags on the list widget
        :return:
        """
        print(f"Number of items : {self.tag_list.count()}")
        list_widget_items = []
        for i in range(self.tag_list.count()):
            list_widget_items.append(self.tag_list.item(i).text())
        return list_widget_items

    def clear_list(self):
        self.tag_list.clear()

    def refresh_tag_list_widget(self):
        tags_to_push = []
        for obj in get_clean_selection(self.get_children_check.isChecked()):
            if has_gtags_attribute(obj) and not is_gtags_empty(obj):
                attr = convert_gtags_in_list(get_gtags_attribute(obj))
                for tags in attr:
                    if tags not in tags_to_push :
                        tags_to_push.append(tags)
        self.tag_list.clear()
        for new_tags in tags_to_push :
            item = QtWidgets.QListWidgetItem(new_tags)
            item.setSizeHint(QtCore.QSize(20, 30))
            self.tag_list.addItem(item)
        if self.highlight_shared_tags.isChecked() and len(get_clean_selection(self.get_children_check.isChecked())) > 1 :
            self.check_shared_tags()

    def replace_tags(self):
        selected_tags =[]
        selection = get_clean_selection(self.get_children_check.isChecked())
        line_edit_tags = convert_gtags_in_list(self.tag_input.text())
        for items in self.tag_list.selectedItems() :
            selected_tags.append(items.text())
        for obj in selection :
            obj_tags = convert_gtags_in_list(get_gtags_attribute(obj))
            add_tags = False
            for tags in obj_tags :
                if tags in selected_tags :
                    obj_tags.remove(tags)
                    add_tags = True
            if add_tags :
                for tags in line_edit_tags :
                    if not tags in obj_tags :
                        obj_tags.append(tags)
            set_gtags_attribute(obj,convert_gtags_in_string(obj_tags))
        self.refresh_tag_list_widget()

    def delete_tags(self):
        selected_tags = []
        selection = cmds.ls(selection = True)
        for items in self.tag_list.selectedItems() :
            selected_tags.append(items.text())
        for obj in selection:
            old_tags = convert_gtags_in_list(get_gtags_attribute(obj))
            for tags in selected_tags:
                if tags in old_tags:
                    old_tags.remove(tags)
                else:
                    pass
            tags_replace = convert_gtags_in_string(old_tags)
            set_gtags_attribute(obj, tags_replace)
        self.refresh_tag_list_widget()

    def add_gtags(self):
        """
        Get the Guerilla Tags from line edit and add them to selection
        :return:
        """
        # Check line edit string
        if self.tag_input.text() and not self.tag_input.text().isspace():
            # Get selection
            selection = get_clean_selection(self.get_children_check.isChecked())
            line_edit_tags = self.tag_input.text()
            new_tags = convert_gtags_in_list(line_edit_tags)
            for obj in selection :
                if not has_gtags_attribute(obj):
                    create_gtags_attribute(obj)
                if is_gtags_empty(obj) :
                    set_gtags_attribute(obj,line_edit_tags)
                else :
                    old_tags = convert_gtags_in_list(get_gtags_attribute(obj))
                    no_tag = False
                    for tags in new_tags :
                        if tags not in old_tags:
                            add_gtag_to_attr(obj, tags)
                    else :
                        pass

        self.refresh_tag_list_widget()

    def merge_selected_tags(self):
        selected_tags = []
        for items in self.tag_list.selectedItems() :
            selected_tags.append(items.text())
        for obj in get_clean_selection(self.get_children_check.isChecked()):
            if not has_gtags_attribute(obj):
                create_gtags_attribute(obj)
            if is_gtags_empty(obj):
                tags = convert_gtags_in_string(selected_tags)
                set_gtags_attribute(obj, tags)
            else:
                old_tags = convert_gtags_in_list(get_gtags_attribute(obj))
                for tags in selected_tags:
                    if tags not in old_tags:
                        add_gtag_to_attr(obj, tags)
                else:
                    pass

        self.refresh_tag_list_widget()

    def merge_all(self):
        selected_tags = self.get_items_on_list()
        print(selected_tags)
        for obj in get_clean_selection(self.get_children_check.isChecked()):
            if not has_gtags_attribute(obj):
                print("pre")
                create_gtags_attribute(obj)
                print("creating attr")
            elif is_gtags_empty(obj):
                tags = convert_gtags_in_string(selected_tags)
                set_gtags_attribute(obj, tags)
            else:
                old_tags = convert_gtags_in_list(get_gtags_attribute(obj))
                for tags in selected_tags:
                    if tags not in old_tags:
                        add_gtag_to_attr(obj, tags)
                else:
                    pass

        self.refresh_tag_list_widget()
