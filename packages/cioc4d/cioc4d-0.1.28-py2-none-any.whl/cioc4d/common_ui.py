

import c4d
import cioc4d.const as k


def set_combobox_content(dialog, widget_id,  options, index=None):
    #child_base_name = self.WIDGET_TO_OPTIONS_MAP[widget_name]
    first_child_id = widget_id+1
    dialog.FreeChildren(widget_id)
    for i, option in enumerate(options):
        dialog.AddChild(widget_id, first_child_id + i, option)
    if index != None:
        set_combobox_value(dialog, widget_id, index)


def set_combobox_value(dialog, widget_id, index):
    #child_base_name = self.WIDGET_TO_OPTIONS_MAP[widget_name]
    dialog.SetInt32(widget_id, widget_id+1+index)


def create_labeled_text_field(dialog, widget_id, **kw):


    label = kw.get("label", "")
    helptext = kw.get("placeholder")
    text = kw.get("text")

    dialog.AddStaticText(
        widget_id+1,
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
        dialog.SetString(widget_id, text )
    
    if helptext:
        dialog.SetString( widget_id, helptext,flags=c4d.EDITTEXT_HELPTEXT)
        