from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance
from gtag_editor import path_utils
from gtag_editor import tag_utils

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import importlib

for modules in [tag_utils,path_utils] :
    importlib.reload(modules)

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
        self.affect_mode = 'selection'
        self.generate_selection_scriptjob()
        self.refresh_tag_list_widget()
        self.setWindowIcon(QtGui.QIcon(path_utils.get_abspath("icons/guerilla_render.png")))
        self.setWindowTitle("Guerilla Tags editor")
        self.setAcceptDrops(True)
        self.materials_taglist = []
        self.obj_list = None
        self.subdiv_taglist = ['s0',
                               's01',
                               's02',
                               's03',
                               's04']
        self.init_materials_taglist()

        print(f'Materials list : {self.materials_taglist}')

    def init_materials_taglist(self):
        for shading_engine in cmds.ls(type = 'shadingEngine'):
            if cmds.sets(shading_engine, query=True):
                for materials in cmds.ls(cmds.listConnections(shading_engine), materials=True):
                    self.materials_taglist.append(materials)


    def import_icons(self):
        self.shared_tag_icon = QtGui.QIcon(path_utils.get_abspath("icons/star.png"))

    def create_widgets(self):
        self.label_title = QtWidgets.QLabel("Tags on selection")

        self.tag_list = QtWidgets.QListWidget()
        self.tag_list.setToolTip("Tags present on the selection")
        self.tag_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tag_list.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.tag_input = QtWidgets.QLineEdit()
        self.tag_input.setToolTip("Guerilla Tags input line edit")
        self.tag_input.setPlaceholderText("Type your GuerillaTags here")

        self.add_tag_buton = QtWidgets.QPushButton('Add tag(s)')
        self.add_tag_buton.setToolTip("Add tags in the line edit to the selected objects")
        self.add_tag_buton.clicked.connect(self.add_gtags)

        self.delete_tag_buton = QtWidgets.QPushButton('Delete tag(s)')
        self.delete_tag_buton.setToolTip("Delete selected tags on the list from the object in the selections")
        self.delete_tag_buton.clicked.connect(self.delete_tags)

        self.replace_tag_buton = QtWidgets.QPushButton('Replace tag(s)')
        self.replace_tag_buton.setToolTip("Replace selected tags in the list with the tags in the line edit")
        self.replace_tag_buton.clicked.connect(self.replace_tags)

        self.merge_selection = QtWidgets.QPushButton('Merge selected tags')
        self.merge_selection.setToolTip("Distribute selected tags to other objects in the selection")
        self.merge_selection.clicked.connect(self.merge_selected_tags)

        self.merge_all_tags = QtWidgets.QPushButton('Merge all')
        self.merge_all_tags.setToolTip("Redistribute all tags on the list to the selection")
        self.merge_all_tags.clicked.connect(self.merge_all)

        self.highlight_shared_tags = QtWidgets.QCheckBox('Highlight shared Tags')
        self.highlight_shared_tags.setToolTip('Highlight tags shared by all objects in the selection')
        self.highlight_shared_tags.setChecked(True)
        self.highlight_shared_tags.clicked.connect(self.refresh_tag_list_widget)

        self.selection_label = QtWidgets.QLabel('Tag mode')

        self.get_children_check = QtWidgets.QCheckBox('Selection children')
        self.get_children_check.clicked.connect(self.set_mode_on_children)
        self.get_children_check.setToolTip("The tools will modify and gather tags from selection's children")
        self.get_children_check.setChecked(False)

        self.get_selection_check = QtWidgets.QCheckBox('Selection')
        self.get_selection_check.clicked.connect(self.set_mode_on_selection)
        self.get_selection_check.setChecked(True)

        self.get_all_check = QtWidgets.QCheckBox('Scene')
        self.get_all_check.clicked.connect(self.set_mode_on_all)
        self.get_all_check.setChecked(False)

        self.tag_materials = QtWidgets.QPushButton('Tag materials')
        self.tag_materials.clicked.connect(self.add_tag_materials)
        self.tag_materials.setToolTip('Set the material name to the object')

        self.option_label = QtWidgets.QLabel('Options')

    def get_taglist_objects(self):
        if self.affect_mode == 'selection' :
            self.obj_list = cmds.ls(selection = True, recursive = False)


    def create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.tags_layout = QtWidgets.QHBoxLayout()
        self.tag_list_layout = QtWidgets.QVBoxLayout()
        self.tags_layout.addLayout(self.tag_list_layout,0)
        self.main_layout.addLayout(self.tags_layout,0)
        self.tag_list_layout.addWidget(self.label_title, 0)
        self.tag_list_layout.addWidget(self.tag_list, 1)
        self.main_layout.addWidget(self.tag_input,1)

        self.tags_buttons_layout = QtWidgets.QVBoxLayout()
        self.tags_layout.addLayout(self.tags_buttons_layout,1)
        self.subdivsion_tag_label = QtWidgets.QLabel('Subdivision Tags')
        self.tags_buttons_layout.addWidget(self.subdivsion_tag_label, 0)
        self.s0_buton = QtWidgets.QPushButton('Tag s0')
        self.s0_buton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.tags_buttons_layout.addWidget(self.s0_buton, 1)
        self.s01_buton = QtWidgets.QPushButton('Tag s01')
        self.s01_buton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.tags_buttons_layout.addWidget(self.s01_buton,2)
        self.s02_buton = QtWidgets.QPushButton('Tag s02')
        self.s02_buton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.tags_buttons_layout.addWidget(self.s02_buton,3)
        self.s03_buton = QtWidgets.QPushButton('Tag s03')
        self.s03_buton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.tags_buttons_layout.addWidget(self.s03_buton,4)
        self.s04_buton = QtWidgets.QPushButton('Tag s04')
        self.s04_buton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.tags_buttons_layout.addWidget(self.s04_buton,5)
        self.tags_buttons_layout.addItem(QtWidgets.QSpacerItem(0,
                                                                 60,
                                                                 QtWidgets.QSizePolicy.Fixed,
                                                                 QtWidgets.QSizePolicy.Expanding))
        for buttons in self.tags_buttons_layout.children():
            buttons.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)


        self.button_layout_one = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.button_layout_one,3)
        self.button_layout_one.addWidget(self.delete_tag_buton)
        self.button_layout_one.addWidget(self.replace_tag_buton)
        self.button_layout_one.addWidget(self.add_tag_buton)

        self.button_layout_two = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.button_layout_two, 4)
        self.button_layout_two.addWidget(self.merge_selection)
        self.button_layout_two.addWidget(self.merge_all_tags)

        self.option_layout = QtWidgets.QVBoxLayout()

        self.tag_mode_layout = QtWidgets.QHBoxLayout()
        self.tag_mode_layout.addWidget(self.get_selection_check, 0)
        self.tag_mode_layout.addWidget(self.get_children_check, 1)
        self.tag_mode_layout.addWidget(self.get_all_check,2)
        #self.option_layout.addWidget(self.selection_label,0)

        self.option_layout.addLayout(self.tag_mode_layout,1)
        self.option_layout.addWidget(self.option_label, 2)

        for widget in self.tag_mode_layout.children():
            widget.setAlignment(QtCore.Qt.AlignBottom)

        self.option_layout.addWidget(self.highlight_shared_tags, 3)
        self.button_layout_two.addWidget(self.tag_materials)
        self.tag_mode_layout.setAlignment(QtCore.Qt.AlignBaseline)
        self.main_layout.setAlignment(QtCore.Qt.AlignBottom)
        self.option_label.setAlignment(QtCore.Qt.AlignBottom)
        self.selection_label.setAlignment(QtCore.Qt.AlignBottom)
        self.main_layout.addLayout(self.option_layout, 5)
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
            if tag_utils.has_gtags_attribute(obj) and not tag_utils.is_gtags_empty(obj):
                obj_tags = tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj))
                for tags in obj_tags :
                    if tags not in tag_list :
                        tag_list.append(tags)
                    else :
                        pass
        for child in children_list :
            if tag_utils.has_gtags_attribute(child) and not tag_utils.is_gtags_empty(child):
                obj_tags = tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(child))
                for tags in obj_tags:
                    if tags not in tag_list:
                        tag_list.append(tags)
                    else:
                        pass
        line_edit_text = tag_utils.convert_gtags_in_string(tag_list)
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
                if not tag_utils.has_gtags_attribute(obj):
                    is_shared = False
                elif tag_utils.is_gtags_empty(obj) :
                    is_shared = False
                elif tag not in tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj)):
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


    def set_mode_on_selection(self):
        self.get_selection_check.setChecked(True)
        self.get_all_check.setChecked(False)
        self.get_children_check.setChecked(False)
        self.affect_mode = 'selection'
        self.label_title.setText('Tags on selection')
        self.refresh_tag_list_widget()

    def set_mode_on_children(self):
        self.get_children_check.setChecked(True)
        self.get_all_check.setChecked(False)
        self.get_selection_check.setChecked(False)
        self.affect_mode = 'children'
        self.label_title.setText('Tags on selection and children')
        self.refresh_tag_list_widget()

    def set_mode_on_all(self):
        self.get_all_check.setChecked(True)
        self.get_selection_check.setChecked(False)
        self.get_children_check.setChecked(False)
        self.affect_mode = 'all'
        self.label_title.setText('Tags on scene objects')
        self.refresh_tag_list_widget()

    def clear_list(self):
        self.tag_list.clear()

    def refresh_tag_list_widget(self):
        tags_to_push = []
        selection = tag_utils.get_clean_selection(self.affect_mode)
        for obj in selection:
            if tag_utils.has_gtags_attribute(obj) and not tag_utils.is_gtags_empty(obj):
                attr = tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj))
                for tags in attr:
                    if tags not in tags_to_push :
                        tags_to_push.append(tags)
        self.tag_list.clear()
        for new_tags in tags_to_push :
            item = QtWidgets.QListWidgetItem(new_tags)
            item.setSizeHint(QtCore.QSize(20, 30))
            self.tag_list.addItem(item)
        if self.highlight_shared_tags.isChecked() and len(selection) > 1 :
            self.check_shared_tags()

    def replace_tags(self):
        selected_tags =[]
        selection = tag_utils.get_clean_selection(self.affect_mode)
        line_edit_tags = tag_utils.convert_gtags_in_list(self.tag_input.text())
        for items in self.tag_list.selectedItems() :
            selected_tags.append(items.text())
        for obj in selection :
            obj_tags = tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj))
            add_tags = False
            for tags in obj_tags :
                if tags in selected_tags :
                    obj_tags.remove(tags)
                    add_tags = True
            if add_tags :
                for tags in line_edit_tags :
                    if not tags in obj_tags :
                        obj_tags.append(tags)
            tag_utils.set_gtags_attribute(obj,tag_utils.convert_gtags_in_string(obj_tags))
        self.refresh_tag_list_widget()

    def delete_tags(self):
        selected_tags = []
        selection = tag_utils.get_clean_selection(self.affect_mode)
        for items in self.tag_list.selectedItems():
            selected_tags.append(items.text())
        for obj in selection:
            old_tags = tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj))
            for tags in selected_tags:
                if tags in old_tags:
                    old_tags.remove(tags)
                else:
                    pass
            tags_replace = tag_utils.convert_gtags_in_string(old_tags)
            tag_utils.set_gtags_attribute(obj, tags_replace)
        self.refresh_tag_list_widget()

    def add_tag_materials(self):

        for obj in tag_utils.get_clean_selection(self.affect_mode) :
            matname = tag_utils.get_obj_material(obj)
            for tags in tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj)):
                if tags == matname:
                    return
                if tags in self.materials_taglist:
                    pass

            matnode = tag_utils.get_obj_material(obj)
            tag_utils.add_gtag_to_attr(obj, matnode)

        self.refresh_tag_list_widget()

    def add_gtags(self):
        """
        Get the Guerilla Tags from line edit and add them to selection
        :return:
        """
        # Check line edit string
        if self.tag_input.text() and not self.tag_input.text().isspace():
            # Get selection
            selection = tag_utils.get_clean_selection(self.affect_mode)
            line_edit_tags = self.tag_input.text()
            new_tags = tag_utils.convert_gtags_in_list(line_edit_tags)
            for obj in selection :
                if not tag_utils.has_gtags_attribute(obj):
                    tag_utils.create_gtags_attribute()
                if tag_utils.is_gtags_empty(obj) :
                    tag_utils.set_gtags_attribute(obj,line_edit_tags)
                else :
                    old_tags = tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj))
                    for tags in new_tags :
                        if tags not in old_tags:
                            tag_utils.add_gtag_to_attr(obj, tags)
                    else :
                        pass

        self.refresh_tag_list_widget()

    def tag_subdiv(self, subidv):
        tag_utils.add_gtag_to_attr()

    def merge_selected_tags(self):
        selected_tags = []
        selection = tag_utils.get_clean_selection(self.affect_mode)
        for items in self.tag_list.selectedItems() :
            selected_tags.append(items.text())
        for obj in selection :
            if not tag_utils.has_gtags_attribute(obj):
                tag_utils.create_gtags_attribute()
            if tag_utils.is_gtags_empty(obj):
                tags = tag_utils.convert_gtags_in_string(selected_tags)
                tag_utils.set_gtags_attribute(obj, tags)
            else:
                old_tags = tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj))
                for tags in selected_tags:
                    if tags not in old_tags:
                        tag_utils.add_gtag_to_attr(obj, tags)
                else:
                    pass

        self.refresh_tag_list_widget()

    def merge_all(self):
        selected_tags = self.get_items_on_list()
        print(selected_tags)
        selection = tag_utils.get_clean_selection(self.affect_mode)
        for obj in selection:
            if not tag_utils.has_gtags_attribute(obj):
                print("pre")
                tag_utils.create_gtags_attribute()
                print("creating attr")
            elif tag_utils.is_gtags_empty(obj):
                tags = tag_utils.convert_gtags_in_string(selected_tags)
                tag_utils.set_gtags_attribute(obj, tags)
            else:
                old_tags = tag_utils.convert_gtags_in_list(tag_utils.get_gtags_attribute(obj))
                for tags in selected_tags:
                    if tags not in old_tags:
                        tag_utils.add_gtag_to_attr(obj, tags)
                else:
                    pass

        self.refresh_tag_list_widget()