

import c4d

from cioc4d.widgets.hidable_text_field_grp import HidableTextFieldGrp
from cioc4d.sections.collapsible_section import CollapsibleSection

class TaskSection(CollapsibleSection):

    ORDER = 50

    def __init__(self, dialog):
        self.widget = None
        super(TaskSection, self).__init__(dialog, "Task Template", collapse=True)

    def build(self):
        self.widget = HidableTextFieldGrp(self.dialog, label="Override Template", placeholder="Task command template")



    def populate_from_store(self):
        store = self.dialog.store
        self.widget.set_value(store.task_template())
        self.widget.set_visible(store.override_task_template())

    def save_to_store(self):
        store = self.dialog.store
        store.set_task_template(self.widget.get_value())
        store.set_override_task_template(self.widget.get_visible())
        store.commit()

         
    def get_preview_affectors(self):
        return [self.widget.text_field_id, self.widget.checkbox_id]

    
    def on_plugin_message(self, widget_id, msg):
    
        if widget_id == self.widget.checkbox_id:
            self.widget.set_visible()

        if widget_id in self._store_affectors:
            self.save_to_store()