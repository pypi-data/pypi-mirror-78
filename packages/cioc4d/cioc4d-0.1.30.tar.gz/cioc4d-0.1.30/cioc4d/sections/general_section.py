# -*- coding: utf-8 -*-
import os

import c4d
from cioc4d.sections.collapsible_section import CollapsibleSection
from cioc4d.widgets.combo_box_grp import ComboBoxGrp
from cioc4d.widgets.hidable_text_field_grp import HidableTextFieldGrp
from cioc4d.widgets.text_field_grp import TextFieldGrp
from ciocore import data as coredata
from ciocore.expander import Expander
from ciocore.gpath import Path
from ciocore.gpath_list import PathList

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

        self.destination_widget = HidableTextFieldGrp(
            self.dialog, "Override Destination", placeholder="Path where renders are saved to")

        self.dialog.AddSeparatorH(inith=0)

        self.instance_types_widget = ComboBoxGrp(
            self.dialog, label="Instance Type", checkbox=True,
            check_label="Preemptible")

        self.dialog.Enable(self.takes_widget.combo_box_id, False)

    def populate_from_store(self):

        self.update_combo_items()

        # store is guaranteed to be valid
        store = self.dialog.store

        self.instance_types_widget.set_checkbox_value(store.preemptible())
        self.takes_widget.set_items(TAKE_OPTIONS)
        self.takes_widget.set_by_value(store.takes())
        self.title_widget.set_value(store.title())
        self.destination_widget.set_value(store.destination())
        self.destination_widget.set_visible(store.override_destination())

    def save_to_store(self):
        store = self.dialog.store
        store.set_preemptible(self.instance_types_widget.get_checkbox_value())
        store.set_takes(self.takes_widget.get_selected_value())
        store.set_title(self.title_widget.get_value())
        store.set_destination(self.destination_widget.get_value())
        store.set_override_destination(self.destination_widget.get_visible())
        store.set_instance_type(
            self.instance_types_widget.get_selected_value())
        store.commit()

    def on_plugin_message(self, widget_id, msg):
        if widget_id == self.dialog.foot_grp.connect_button_id:
            self.update_combo_items()
        elif widget_id == self.destination_widget.checkbox_id:
            self.destination_widget.set_visible()
        elif widget_id == self.dialog.section("TaskSection").widget.checkbox_id:
            if self.dialog.section("TaskSection").widget.get_visible():
                self.destination_widget.set_visible(True)

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

        dest_path = Path(self.resolve_destination_path()).posix_path()

        return {
            "job_title": expander.evaluate(self.title_widget.get_value()),
            "output_path": dest_path,
            "project": self.projects_widget.get_selected_value(),
            "instance_type": instance_type["name"] if instance_type else "INVALID",
            "preemptible": self.instance_types_widget.get_checkbox_value()
        }


    
    def set_store_affectors(self):
        """
        collect widget IDs that trigger store update.

        These are usually the same affectors that trigger a preview. However
        this is a special case because we also need to update the store with the
        destination dir state when the user flips the task visibility switch,
        and since the task visibility switch is not in the preview_affectors
        list for this section, we ust append it.

        You may be wondering, why the task toggle id is not in preview_affectors
        here. It's because the whole preview is updated anyway when the task
        toggle changes so its handled in the TaskSection. Store updates on the
        other hand, only write the one sections properties to the store.
        """
        task_widget_toggle_id = self.dialog.section("TaskSection").widget.checkbox_id

        self._store_affectors = self.get_preview_affectors() + [task_widget_toggle_id]

  
  
    def get_preview_affectors(self):
        """
        
        """
        return [
            self.takes_widget.combo_box_id,
            self.title_widget.text_field_id,
            self.projects_widget.combo_box_id,
            self.destination_widget.text_field_id,
            self.destination_widget.checkbox_id,
            self.instance_types_widget.combo_box_id,
            self.instance_types_widget.checkbox_id
        ]

    def resolve_destination_path(self):
        """
        Resolve the destination path in one of 2 ways.

        1. Get the overridden value
        2. Get the common path of image output dirs.


        """
        context = self.dialog.get_context()
        expander = Expander(safe=True, **context)
        value = None
        if self.destination_widget.get_visible():
            value = self.destination_widget.get_value()
            if value:
                value = expander.evaluate(value)
                if Path(value).relative:
                    value = os.path.join(context["docdir"], value)
        if not value:
            value = self._get_common_destination()
        return value

    def _get_common_destination(self):
        """
        Use common path of outputs for destination directory.
        """
        document = c4d.documents.GetActiveDocument()
        render_data = document.GetActiveRenderData()
        doc_path = document.GetDocumentPath()

        out_paths = list(filter(None, [
            _get_image_save_directory(doc_path, render_data),
            _get_multipass_save_directory(doc_path, render_data)
        ]))
        if not out_paths:
            # fallback
            return os.path.join(doc_path, "renders")

        try:
            return PathList(*out_paths).common_path().posix_path()
        except BaseException:
            return os.path.join(doc_path, "renders")


def _get_image_save_directory(doc_path, render_data):
    save_enabled = render_data[c4d.RDATA_GLOBALSAVE]
    do_image_save = render_data[c4d.RDATA_SAVEIMAGE]
    if save_enabled and do_image_save:
        image_path = render_data[c4d.RDATA_PATH]
        if image_path:
            if Path(image_path).relative:
                return Path(os.path.dirname(os.path.join(doc_path, image_path)))
            return Path(os.path.dirname(image_path))


def _get_multipass_save_directory(doc_path, render_data):
    save_enabled = render_data[c4d.RDATA_GLOBALSAVE]
    do_image_save = render_data[c4d.RDATA_MULTIPASS_SAVEIMAGE]
    if save_enabled and do_image_save:
        image_path = render_data[c4d.RDATA_MULTIPASS_FILENAME]
        if image_path:
            if Path(image_path).relative:
                return Path(os.path.dirname(os.path.join(doc_path, image_path)))
            return Path(os.path.dirname(image_path))
