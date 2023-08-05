
import c4d

import cioc4d.const as k
from cioc4d import widgets


class MachinesGroup(object):

    def __init__(self, dialog):

        self.dialog = dialog
        self._build()

    def _build(self):
        with widgets.rounded_group(self.dialog, k.ID_MACHINES_GROUP, title="Machines"):

            widgets.combo_box_grp(
                self.dialog, k.ID_INST_TYPES_COMBOBOX, 
                label="Instance Type",
                 checkbox=True, check_label="Preemptible")

            # widgets.checkbox_grp(
            #     self.dialog, k.ID_PREEMPTIBLE_CHECKBOX, label="Preemptible")

    def populate(self):

        inst_types = [val["description"] for val in get_inst_types()]
        widgets.set_combo_box_content(
            self.dialog, k.ID_INST_TYPES_COMBOBOX, inst_types, 1)
        
        widgets.set_combo_box_check_value(  self.dialog ,  k.ID_INST_TYPES_COMBOBOX, True)  

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
