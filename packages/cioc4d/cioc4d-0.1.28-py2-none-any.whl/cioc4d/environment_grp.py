
import c4d
from cioc4d.collapsible_section import CollapsibleSection
from cioc4d.widgets.key_value_widget import KeyValueHeader, KeyValueWidget


class EnvironmentSection(CollapsibleSection):
    ORDER=60
    def __init__(self, dialog):
        self.list_grp_id = None
        self.widgets = []
        super(EnvironmentSection, self).__init__(
            dialog, "Extra Environment", collapse=False)

    def build(self):
        self.header_row = KeyValueHeader(self.dialog, check_box_label="Excl")

        self.list_grp_id = self.dialog.register()

        self.dialog.GroupBegin(
            id=self.list_grp_id,
            flags=c4d.BFH_SCALEFIT,
            title="",
            cols=1,
            groupflags=0)

        self.dialog.GroupEnd()  # manin

    def populate(self):
        pass

    def on_plugin_message(self, widget_id, msg):
        if widget_id == self.header_row.add_button_id:  # clear list
            self.add_entry()
            return

        if self.remove_entry(widget_id):
            return

    def add_entry(self):

        values = [widget.get_values() for widget in self.widgets]
        values.append(("", "", True))
        self._update_widgets(values)

    def remove_entry(self, widget_id):
        keep_widgets = [
            w for w in self.widgets if w.delete_btn_id != widget_id]
        if len(keep_widgets) < len(self.widgets):

            values = [widget.get_values() for widget in keep_widgets]
            self._update_widgets(values)
            return True
        return False

    def _update_widgets(self, values):
        self.widgets = []
        self.dialog.LayoutFlushGroup(self.list_grp_id)
        for value_tuple in values:
            self.widgets.append(
                KeyValueWidget(self.dialog, *value_tuple))
        self.dialog.LayoutChanged(self.list_grp_id)
