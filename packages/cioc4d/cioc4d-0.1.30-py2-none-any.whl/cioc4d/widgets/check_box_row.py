

import c4d
from cioc4d.widgets import utils as wutil


class CheckboxRow(object):
    """A group containing a label, textfield, and optional checkbox"""

    def __init__(self, dialog, *labels, **kw):
        self.dialog = dialog
        self.labels = labels
        self.checkbox_ids = []
        self.num_checkboxes = len(labels)
        self._build(**kw)

    def _build(self, **kw):
        with wutil.grid_group(self.dialog, cols=self.num_checkboxes):
            for label in self.labels:
                this_id = self.dialog.register()
                self.checkbox_ids.append(this_id)
                self.dialog.AddCheckbox(
                    this_id, c4d.BFH_LEFT, 0, 0,  name=label)

 
    def get_value(self, index):
        if index in range(self.num_checkboxes):
            return self.dialog.GetBool(self.checkbox_ids[index]) 

    def set_value(self, value, index):
        if index in range(self.num_checkboxes):
            self.dialog.SetBool(self.checkbox_ids[index]) 

