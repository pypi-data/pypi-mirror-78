
# import os


from cioc4d.widgets.combo_box_grp import ComboBoxGrp
from cioc4d.collapsible_section import CollapsibleSection



class SoftwareSection(CollapsibleSection):
    
    ORDER = 20

    def __init__(self, dialog):
        self.host_version_widget = None
        self.renderer_widget = None
        super(SoftwareSection, self).__init__(dialog, "Software")

    def build(self):
        self.host_version_widget = ComboBoxGrp(self.dialog, label="Cinema 4D Version")
        self.renderer_widget = ComboBoxGrp(self.dialog, label="Renderer")

    def populate(self):

        host_versions = get_host_versions()
        renderers = get_renderers()

        self.host_version_widget.set_items(host_versions)
        self.host_version_widget.set_by_index(-1)

        self.renderer_widget.set_items(renderers)
        self.renderer_widget.set_by_index(-1)
 
def get_host_versions():
    return ["R17", "R18", "R19", "R20", "R21", "S22", "R22"]


def get_renderers():
    return [
        "standard 22.0",
        "standard 23.0",
        "physical 18.0",
        "physical 20.0",
        "physical 21.0",
        "physical 22.0",
         "arnold 3.1.0.1",
         "arnold 3.2.2.1",
         "arnold 4.0.3.1",
         "vray 23.0.0.1",
         "vray 23.2.0.0",
         "vray 23.2.0.5",
         "vray 24.0.0.3",
         "redshift 1.4.1",
         "redshift 1.4.5",
         "redshift 1.5.0"
         ]
         
         
 