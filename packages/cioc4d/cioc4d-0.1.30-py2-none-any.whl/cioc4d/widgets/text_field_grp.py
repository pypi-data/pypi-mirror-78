

import c4d
 
from cioc4d.widgets import utils as wutil

class TextFieldGrp(object):
    """A group containing a label, textfield, and optional checkbox.
    
    TODO: Consolidate with HidableTextField.
    """
    def __init__(self, dialog, **kwargs):
        self.dialog = dialog
        self.has_checkbox = kwargs.get("checkbox")
        self.label = kwargs.get("label", "")
        self.check_label = kwargs.get("check_label", "")
        self.helptext = kwargs.get("placeholder")
        self.text_field_id = None
        self.checkbox_id = None

        self._build()

    def _build(self):
        cols = 3 if self.has_checkbox else 2
        with wutil.grid_group(self.dialog, cols=cols):
            wutil.dotted_label(self.dialog, self.label)

            self.text_field_id = self.dialog.register()
            self.dialog.AddEditText(
                self.text_field_id, c4d.BFH_SCALEFIT | c4d.BFV_TOP, editflags=c4d.EDITTEXT_HELPTEXT)

            if self.helptext:
                self.dialog.SetString(
                    self.text_field_id, self.helptext, flags=c4d.EDITTEXT_HELPTEXT)

            if self.has_checkbox:
                self.checkbox_id = self.dialog.register()
                self.dialog.AddCheckbox(
                    self.checkbox_id, c4d.BFH_RIGHT, 0, 0, self.check_label)

    def set_value(self, value):
        self.dialog.SetString(self.text_field_id, value)

    def get_value(self):
        return self.dialog.GetString(self.text_field_id).strip()

    def set_checkbox_value(self, value):
        self.dialog.SetBool(self.checkbox_id, value)

    def get_checkbox_value(self):
        return self.dialog.GetBool(self.checkbox_id)
