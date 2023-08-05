

import c4d
import cioc4d.const as k

from contextlib import contextmanager


@contextmanager
def rounded_group(dialog, **kw):

    if kw.get("title"):
        border_style= c4d.BORDER_WITH_TITLE | c4d.BORDER_ROUND
    else:
        border_style=   c4d.BORDER_ROUND

    grp = dialog.GroupBegin(
        id=dialog.register(),
        flags=c4d.BFH_SCALEFIT,
        title=kw.get("title", ""),
        rows=1,
        cols=1,
        groupflags=0)
    if grp:
        dialog.GroupBorderSpace(4, 4, 4, 4)
        dialog.GroupBorder(border_style)
        yield
    dialog.GroupEnd()

@contextmanager
def grid_group(dialog, **kw):

    grp = dialog.GroupBegin(
        id=dialog.register(),
        flags=c4d.BFH_SCALEFIT,
        rows=kw.get("rows", 1),
        cols=kw.get("cols", 2),
        groupflags=0)
    if grp:
        yield
    dialog.GroupEnd()
 

def combo_box_grp(dialog, name, max_items, **kw):
    label = kw.get("label", "")
    do_checkbox  =kw.get("checkbox")
    cols = 3 if do_checkbox else 2
    check_label=kw.get("check_label", "")

    with grid_group(dialog, cols=cols):

        checkbox_id=dialog.register("{}_checkbox".format(name))
        combo_box_id=dialog.register(name, max_items)

        dialog.AddStaticText(
            id=dialog.register(),
            initw=k.LABEL_WIDTH, inith=0,
            name=label,
            borderstyle=c4d.BORDER_TEXT_DOTTED,
            flags=c4d.BFH_FIT)

        dialog.AddComboBox(combo_box_id, c4d.BFH_SCALEFIT)
        if do_checkbox:
            dialog.AddCheckbox( checkbox_id, c4d.BFH_RIGHT , 0,0,check_label)


def set_combo_box_content(dialog, name,  options, index=None):

    if index < 0:
        index = len(options)-index # from back
    
    widget_id=dialog.registry[name] # should not crash
    first_child_id = widget_id+1
    
    dialog.FreeChildren(widget_id)
    for i, option in enumerate(options):
        dialog.AddChild(widget_id, first_child_id + i, option)
    if index != None:
        set_combo_box_value(dialog, name, index)
 
def set_combo_box_value(dialog, name, index):
    widget_id=dialog.registry[name]
    first_child_id = widget_id+1
    dialog.SetInt32(widget_id, first_child_id+index)
 
def set_combo_box_check_value(dialog, name, value):
    cbname = "{}_checkbox".format(name)
    checkbox_id=dialog.registry[cbname]
    dialog.SetBool(checkbox_id, value)
 


def text_field_grp(dialog, name, **kw):

    with grid_group(dialog, cols=2):

        widget_id=dialog.register(name)
 
        label = kw.get("label", "")
        helptext = kw.get("placeholder")
        text = kw.get("text")

        dialog.AddStaticText(
            dialog.register(),
            initw=k.LABEL_WIDTH,
            inith=0,
            name=label,
            borderstyle=c4d.BORDER_TEXT_DOTTED,
            flags=c4d.BFH_FIT)

        dialog.AddEditText(
            widget_id,
            c4d.BFH_SCALEFIT | c4d.BFV_TOP,
            editflags=c4d.EDITTEXT_HELPTEXT)

        if text:
            dialog.SetString(widget_id, text)

        if helptext:
            dialog.SetString(widget_id, helptext, flags=c4d.EDITTEXT_HELPTEXT)



def set_text_field_value(dialog, name, value):
    widget_id=dialog.registry[name]
    dialog.SetString(widget_id, value)
 
