

# encoding: utf-8
import c4d
from cioc4d.widgets import utils as wutil


class MetadataHeader(object):
    """A widget containing a label, textfield, and check_box to hide it"""

    def __init__(self, dialog):

        self.dialog = dialog
        self.group_id = None

        self.add_button_id = None
        self.name_text_id = None
        self.value_text_id = None

        self._build()

    def _build(self):

        with wutil.grid_group(self.dialog, cols=3) as group_id:
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


class MetadataWidget(object):
    """A widget containing a label, textfield, and check_box to hide it"""

    def __init__(self, dialog, values=("", "", True)):

        self.dialog = dialog
        self.group_id = None
        self.name_field_id = None
        self.value_field_id = None
        self.delete_btn_id = None
        self._build()
        self.set_values(values)

    def _build(self):

        with wutil.grid_group(self.dialog, cols=3) as group_id:
            self.group_id = group_id

            self.delete_btn_id = self.dialog.register()
            self.dialog.AddButton(self.delete_btn_id,
                                  c4d.BFH_FIT, initw=20, name='✕')

            self.name_field_id = self.dialog.register()
            self.dialog.AddEditText(
                self.name_field_id, c4d.BFH_FIT | c4d.BFV_TOP, initw=200)

            self.value_field_id = self.dialog.register()
            self.dialog.AddEditText(
                self.value_field_id, c4d.BFH_SCALEFIT | c4d.BFV_TOP)


    def set_values(self, values):
        self.dialog.SetString(self.name_field_id, values[0])
        self.dialog.SetString(self.value_field_id, values[1])

    def get_values(self):
        return (
            self.dialog.GetString(self.name_field_id).strip(),
            self.dialog.GetString(self.value_field_id).strip()
        )
