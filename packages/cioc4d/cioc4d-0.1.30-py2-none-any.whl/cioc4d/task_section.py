

import c4d

from cioc4d.widgets.text_field_grp import TextFieldGrp
from cioc4d.collapsible_section import CollapsibleSection

class TaskSection(CollapsibleSection):

    ORDER = 50

    def __init__(self, dialog):
        self.widget = None
        super(TaskSection, self).__init__(dialog, "Tasks", collapse=True)

    def build(self):
        self.widget = TextFieldGrp(self.dialog, label="Template")

    def populate_from_store(self):
        self.widget.set_value(self.dialog.store.task_template())

    def save_to_store(self):
        store = self.dialog.store
        store.set_task_template(self.widget.get_value())
        store.commit()

         
    def get_preview_affectors(self):
        return [self.widget.text_field_id]
    
    def on_plugin_message(self, widget_id, msg):
        if widget_id in self._store_affectors:
            self.save_to_store()