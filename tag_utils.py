import maya.cmds as cmds

# Module related to GuerillaTags attribute and selection


def get_clean_selection(get_children: bool = True) -> list:
    """
    Get a selection with only transforms and direct children transform if checked
    :param get_children:
    :return:
    """
    selection = cmds.ls(selection=True, tr=True)
    if get_children and selection is not None:
        for obj in selection:
            children = cmds.listRelatives(obj)
            if children:
                for child in children:
                    if child not in selection and cmds.nodeType(child) == 'transform':
                        selection.append(child)
    return selection


def get_obj_material(obj: str) -> str:
    shader_groups = cmds.listConnections(cmds.listHistory(obj))
    if shader_groups :
        material = [mat for mat in cmds.ls(cmds.listConnections(shader_groups), materials = True)][0]
        return material

# Tags related functions


def create_gtags_attribute() -> None:
    """
    Create 'GuerillaTags' attribute on selection
    :return:
    """
    cmds.addAttr(longName='GuerillaTags', dataType="string")


def has_gtags_attribute(obj: str) -> bool:
    """
    Check whether GuerillaTags attribute exist on given object
    :param obj:
    :return:
    """
    return cmds.attributeQuery("GuerillaTags", node=obj, exists=True)


def get_gtags_attribute(obj: str) -> str:
    """
    Get GuerillaTags attributes from given object
    :param obj:
    :return: string
    """
    return cmds.getAttr(f'{obj}.GuerillaTags')


def set_gtags_attribute(obj: str, gtags: str) -> None:
    """
    Set GuerillaTags on object
    :param obj:
    :param gtags:
    :return:
    """
    cmds.setAttr(f'{obj}.GuerillaTags', gtags, typ='string')


def convert_gtags_in_list(guerilla_tags: str) -> list:
    """
    Convert Gtags string into a clean list
    :param guerilla_tags:
    :return:
    """
    tags = guerilla_tags.replace(" ", "")
    gtags_list = tags.split(",")
    return gtags_list


def convert_gtags_in_string(guerilla_tags: list) -> str:
    """
    Convert a list of tags into the attribute string
    :param guerilla_tags:
    :return:
    """
    gtags_string = str()
    for tags in guerilla_tags:
        if tags == guerilla_tags[0]:
            gtags_string += tags
        else:
            gtags_string += ', ' + tags
    return gtags_string


def is_gtags_empty(obj) -> bool:
    """
    Check if gtags is empty on object with the GuerillaTags attribute
    :param obj:
    :return:
    """
    if not cmds.getAttr(f'{obj}.GuerillaTags'):
        return True
    else:
        return False


def add_gtag_to_attr(obj: str, tags: str) -> None:
    """
    Add tag to existing GuerillaTags on given object
    :param obj:
    :param tags:
    :return:
    """
    old_tags = get_gtags_attribute(obj)
    if not old_tags:
        new_tags = tags
    else:
        new_tags = old_tags + ', ' + tags
    set_gtags_attribute(obj, new_tags)






