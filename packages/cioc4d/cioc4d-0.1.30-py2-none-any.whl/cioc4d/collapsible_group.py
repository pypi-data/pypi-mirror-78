
"""
Collapsible Group is a base component for each stacked section of UI 
"""
# import os

import c4d
import abc
# from cioc4d.widgets import groups
# from cioc4d.widgets.combo_box_grp import ComboBoxGrp
# from cioc4d.widgets.text_field_grp import TextFieldGrp

TOGGLE_X = 11
TOGGLE_Y = 7
TOGGLE_SQ_RADIUS = 25


class CollapsibleGroup(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, dialog, title):

        self.group_id = None
        self.vis_group_id = None
        self.collapsed = False
        self.title = title
        self.dialog = dialog

        if self._begin_group():
            self.build()
            self._end_group()
            self.populate()

    @abc.abstractmethod
    def build(self):
        return

    @abc.abstractmethod
    def populate(self):
        return

    def _begin_group(self):

        self.group_id = self.dialog.register()
        title = self.get_titled_toggle()

        # OUTER
        grp = self.dialog.GroupBegin(
            id=self.group_id,
            flags=c4d.BFH_SCALEFIT,
            title=title,
            rows=1,
            cols=1,
            groupflags=0)
        if not grp:
            return

        self.dialog.GroupBorderSpace(4, 4, 4, 4)
        self.dialog.GroupBorder(c4d.BORDER_WITH_TITLE | c4d.BORDER_ROUND)

        # must add an element here to prevent a bug where an empty rounded
        # border grp doesn't know how to display properly
        self.dialog.AddSeparatorH(4)

        # INNER
        self.vis_group_id = self.dialog.register()
        grp = self.dialog.GroupBegin(
            id=self.vis_group_id,
            cols=1,
            flags=c4d.BFH_SCALEFIT,
            groupflags=0)
        if not grp:
            return

        return True

    def _end_group(self):
        self.dialog.GroupEnd()
        self.dialog.GroupEnd()

    def get_titled_toggle(self):
        toggler = "▼" if self.collapsed else "▲"
        return "{} {}".format(toggler, self.title)

    def on_mouse_click(self, msg):

        mousex = msg.GetInt32(c4d.BFM_INPUT_X)
        mousey = msg.GetInt32(c4d.BFM_INPUT_Y)

        dim = self.dialog.GetItemDim(self.group_id)
        xoff = dim["x"]+TOGGLE_X - mousex
        yoff = dim["y"]+TOGGLE_Y - mousey
        if (xoff*xoff)+(yoff*yoff) < TOGGLE_SQ_RADIUS:
            self.toggle()

    def collapse(self):
        self.dialog.HideElement(self.vis_group_id, True)
        self.collapsed = True
        self.dialog.SetString(self.group_id, self.get_titled_toggle())
        self.dialog.LayoutChanged(self.group_id)
        return self.collapsed

    def expand(self):
        self.dialog.HideElement(self.vis_group_id, False)
        self.collapsed = False
        self.dialog.SetString(self.group_id, self.get_titled_toggle())
        self.dialog.LayoutChanged(self.group_id)
        return self.collapsed

    def toggle(self):
        return self.expand() if self.collapsed else self.collapse()
