
import c4d

import cioc4d.const as k


class TmpGroup(object):

    def __init__(self, dialog):

        self.dialog = dialog
        self._build()

    def _build(self):
        grp = self.dialog.GroupBegin(
            id=k.ID_TMP_GROUP, 
            flags=c4d.BFH_SCALEFIT |
            c4d.BFV_SCALEFIT, 
            title="foo", 
            rows=1, 
            cols=1, 
            groupflags=c4d.BORDER_GROUP_IN)
        if grp:
            self.dialog.GroupBorderSpace(5, 5, 5, 5)
            self.dialog.AddUserArea(
                id=k.ID_TMP_INNER, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT)
        self.dialog.GroupEnd()
