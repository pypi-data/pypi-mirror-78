

# encoding: utf-8
import c4d
from cioc4d.widgets import utils as wutil


class KeyValueHeader(object):
    """A widget containing a label, textfield, and check_box to hide it"""

    def __init__(self, dialog, check_box_label=None):

        self.check_box_label = check_box_label
        self.dialog = dialog
        self.group_id = None

        self.add_button_id = None
        self.name_text_id = None
        self.value_text_id = None
        self.extra_text_id = None

        self._build()

    def _build(self):

        with wutil.grid_group(self.dialog, cols=4) as group_id:
            self.group_id = group_id

            self.add_button_id = self.dialog.register()
            self.dialog.AddButton(
                self.add_button_id, c4d.BFH_FIT, initw=20,  name="Add")

            self.name_text_id = self.dialog.register()
            self.dialog.AddStaticText(
                id=self.name_text_id, initw=215, name="Name",
                borderstyle=c4d.BORDER_TEXT_DOTTED, flags=c4d.BFH_FIT)

            self.value_text_id = self.dialog.register()
            self.dialog.AddStaticText(
                id=self.name_text_id, name="Value",
                borderstyle=c4d.BORDER_TEXT_DOTTED, flags=c4d.BFH_SCALEFIT)

            if self.check_box_label:
                self.extra_text_id = self.dialog.register()
                self.dialog.AddStaticText(
                    id=self.name_text_id, name=self.check_box_label,
                    borderstyle=c4d.BORDER_TEXT_DOTTED, flags=c4d.BFH_FIT | c4d.BFH_RIGHT, initw=40)


class KeyValueWidget(object):
    """A widget containing key/value, textfields, and optional check_box_label"""

    def __init__(self, dialog, *values):

        self.has_check_box = len(values)==3 
        self.dialog = dialog
        self.group_id = None
        self.name_field_id = None
        self.value_field_id = None
        self.extra_checkbox_id = None
        self.delete_btn_id = None
        self._build()
        self.set_values(*values)

    def _build(self):

        with wutil.grid_group(self.dialog, cols=4) as group_id:
            self.group_id = group_id

            self.delete_btn_id = self.dialog.register()
            self.dialog.AddButton(self.delete_btn_id,
                                  c4d.BFH_FIT, initw=20, name='✕')

            self.name_field_id = self.dialog.register()
            self.dialog.AddEditText(
                self.name_field_id, c4d.BFH_FIT | c4d.BFV_TOP, initw=200)

            self.value_field_id = self.dialog.register()
            self.dialog.AddEditText( self.value_field_id, c4d.BFH_SCALEFIT | c4d.BFV_TOP)
            if self.has_check_box:
                self.extra_checkbox_id = self.dialog.register()
                self.dialog.AddCheckbox(
                    self.extra_checkbox_id,  c4d.BFH_FIT | c4d.BFH_RIGHT, initw=35, inith=0, name="")

    def set_values(self, *values):
        self.dialog.SetString(self.name_field_id, values[0])
        self.dialog.SetString(self.value_field_id, values[1])
        if self.has_check_box:
            self.dialog.SetBool(self.extra_checkbox_id, values[2])

    def get_values(self):
        return (
            self.dialog.GetString(self.name_field_id).strip(),
            self.dialog.GetString(self.value_field_id).strip(),
            self.dialog.GetBool(self.extra_checkbox_id) if self.has_check_box else None
        )
