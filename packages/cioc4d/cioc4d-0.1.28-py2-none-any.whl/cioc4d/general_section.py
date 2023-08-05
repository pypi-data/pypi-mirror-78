
import os

import c4d
from ciocore import data as coredata
from cioc4d.widgets.combo_box_grp import ComboBoxGrp
from cioc4d.widgets.text_field_grp import TextFieldGrp
from cioc4d.collapsible_section import CollapsibleSection
 
TAKE_OPTIONS = ["Current", "Marked", "Main"]


class GeneralSection(CollapsibleSection):

    ORDER = 10

    def __init__(self, dialog):
        self.takes_widget = None
        self.title_widget = None
        self.projects_widget = None
        self.destination_widget = None
        self.instance_types_widget = None

        super(GeneralSection, self).__init__(dialog, "General", collapse=False)

    def build(self):

        self.takes_widget = ComboBoxGrp(self.dialog, label="Takes")

        self.title_widget = TextFieldGrp(
            self.dialog, label="Job Title", placeholder="Title in Conductor dashboard")

        self.projects_widget = ComboBoxGrp(
            self.dialog, label="Conductor Project")

        self.destination_widget = TextFieldGrp(
            self.dialog, label="Destination Path", placeholder="Path where renders are saved to")

        self.dialog.AddSeparatorH(inith=0)

        self.instance_types_widget = ComboBoxGrp(
            self.dialog, label="Instance Type", checkbox=True,
            check_label="Preemptible")

    def populate_from_store(self):

        self.update_combo_items()

        # store is guaranteed to be valid
        store = self.dialog.store
        preemptible = store.preemptible()
        print "Preemptible = ", preemptible
        self.instance_types_widget.set_checkbox_value(store.preemptible())
        self.takes_widget.set_items(TAKE_OPTIONS)
        self.takes_widget.set_by_value(store.takes())
        self.title_widget.set_value(store.title())
        self.destination_widget.set_value(store.destination())

    def save_to_store(self):
        store = self.dialog.store
        store.set_preemptible(self.instance_types_widget.get_checkbox_value())
        store.set_takes(self.takes_widget.get_selected_value())
        store.set_title(self.title_widget.get_value())
        store.set_destination(self.destination_widget.get_value())
        store.set_instance_type(
            self.instance_types_widget.get_selected_value())
        store.commit()

    def on_plugin_message(self, widget_id, msg):
        if widget_id == self.dialog.foot_grp.connect_button_id:
            self.update_combo_items()

        # should this be done with a call to super? 
        if widget_id in self._store_affectors:
            self.save_to_store()


    def update_combo_items(self):
        if coredata.valid():
            store = self.dialog.store
            projects = coredata.data()["projects"]
            inst_types = coredata.data()["instance_types"]
            self.projects_widget.set_items(
                projects, default_value=store.project())
            self.instance_types_widget.set_items(
                [val["description"] for val in inst_types], default_value=store.instance_type())
        else:
            self.projects_widget.set_items(["-- Not Connected --"])
            self.instance_types_widget.set_items(["-- Not Connected --"])

    def get_selected_instance_type(self):
        if not coredata.valid():
            return
        inst_types = coredata.data()["instance_types"]
        description = self.instance_types_widget.get_selected_value()
        return next((it for it in inst_types if it["description"] == description), None)

    def resolve(self, expander, **kwargs):
        instance_type = self.get_selected_instance_type()

        result = {
            "job_title": expander.evaluate(self.title_widget.get_value()),
            "output_path": expander.evaluate(self.destination_widget.get_value()),
            "project": self.projects_widget.get_selected_value(),
            "instance_type": instance_type["name"] if instance_type else "INVALID",
        }
        return result

    def get_preview_affectors(self):
        return [
            self.takes_widget.combo_box_id,
            self.title_widget.text_field_id,
            self.projects_widget.combo_box_id,
            self.destination_widget.text_field_id,
            self.instance_types_widget.combo_box_id,
            self.instance_types_widget.checkbox_id
        ]
