
import os

import c4d
 
from cioc4d.widgets.combo_box_grp import ComboBoxGrp
from cioc4d.widgets.text_field_grp import TextFieldGrp
from cioc4d.collapsible_section import CollapsibleSection


class GeneralSection(CollapsibleSection):


    ORDER = 10

    def __init__(self, dialog):
        self.takes_widget = None
        self.title_widget = None
        self.projects_widget = None
        self.destination_widget = None
        self.instance_types_widget = None
      
      
        super(GeneralSection, self).__init__(dialog, "General")

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
            self.dialog, label="Instance Type", check_box=True,
            check_label="Preemptible")

    def populate(self):

        projects = get_projects()
        take_options = ["Current", "Marked", "Main"]

        self.takes_widget.set_items(take_options)
        self.takes_widget.set_by_index(-1)

        self.projects_widget.set_items(projects)
        self.projects_widget.set_by_index(-1)

        self.title_widget.set_value("C4D <docname> <take>")

        renders_path = os.path.join(
            c4d.documents.GetActiveDocument().GetDocumentPath(), "renders")
        self.destination_widget.set_value(renders_path)

        inst_types = [val["description"] for val in get_inst_types()]

        self.instance_types_widget.set_items(inst_types)
        self.instance_types_widget.set_by_index(3)  # last
        self.instance_types_widget.set_check_box_value(True)  # last

    def on_plugin_message(self, evt, msg):
        pass

def get_projects():
    return ["default", "fishAttack", "harryPotter",
            "leagueOfGentlemen", "fawltyTowers"]


def get_inst_types():
    return [{u'cores': 2,
             u'description': u'2 core, 8GB Mem',
             u'memory': 8.0,
             u'name': u'm5.large'},
            {u'cores': 4,
             u'description': u'4 core, 16GB Mem',
             u'memory': 16.0,
             u'name': u'm5.xlarge'},
            {u'cores': 8,
             u'description': u'8 core, 32GB Mem',
             u'memory': 32.0,
             u'name': u'm5.2xlarge'},
            {u'cores': 16,
             u'description': u'16 core, 64GB Mem',
             u'memory': 64.0,
             u'name': u'm5.4xlarge'},
            {u'cores': 32,
             u'description': u'32 core, 128GB Mem',
             u'memory': 128.0,
             u'name': u'm5.8xlarge'},
            {u'cores': 48,
             u'description': u'48 core, 192GB Mem',
             u'memory': 192.0,
             u'name': u'm5.12xlarge'},
            {u'cores': 64,
             u'description': u'64 core, 256GB Mem',
             u'memory': 256.0,
             u'name': u'm5.16xlarge'},
            {u'cores': 72,
             u'description': u'72 core, 144GB Mem',
             u'memory': 144.0,
             u'name': u'c5.18xlarge'},
            {u'cores': 96,
             u'description': u'96 core, 384GB Mem',
             u'memory': 384.0,
             u'name': u'm5.24xlarge'}]
