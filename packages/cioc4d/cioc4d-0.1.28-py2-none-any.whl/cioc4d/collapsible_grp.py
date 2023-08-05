
"""
Collapsible Group is a base class for each stacked section of UI 
"""
# import os

import c4d
import abc

TOGGLE_W = 100
TOGGLE_X = 11
TOGGLE_Y = 7

TOGGLE_DIST = 5
DEFAULT_TEXT = 191/255.0
COLLAPSED_COLOR = c4d.Vector(0.5, DEFAULT_TEXT, 1)
EXPANDED_COLOR = c4d.Vector(1, DEFAULT_TEXT, DEFAULT_TEXT)
DEFAULT_COLOR = c4d.Vector(DEFAULT_TEXT, DEFAULT_TEXT, DEFAULT_TEXT)


class CollapsibleSection(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def ORDER(self):
        pass

    @classmethod
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in c.all_subclasses()]
        )
        
    def __init__(self, dialog, title, collapse=False):

        self.group_id = None
        self.vis_group_id = None
        self.separator_id = None
        self.collapsed = None
        self.title = title
        self.dialog = dialog

        # Build the UI
        if not self._begin_group():
            return
        self.build()
        self._end_group()

        self.collapse() if collapse else self.expand()

    @abc.abstractmethod
    def build(self):
        return

    @abc.abstractmethod
    def populate(self):
        return

    def on_plugin_message(self, widget_id, msg):
        pass

    def on_core_message(self, msg_id, msg):
        pass

    def on_message(self, msg_id, msg):
        if msg_id == c4d.BFM_INPUT:
            self.on_mouse_click(msg)

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

        # must add an element here (with ID) to prevent a bug where an empty
        # rounded border grp doesn't know how to display properly
        self.separator_id = self.dialog.register()
        self.dialog.AddStaticText(self.separator_id, c4d.BFH_SCALEFIT, inith=4)

        # INNER
        self.vis_group_id = self.dialog.register()
        grp = self.dialog.GroupBegin(
            id=self.vis_group_id,
            cols=1,
            flags=c4d.BFH_SCALEFIT,
            groupflags=0)
        if not grp:
            return

        self.dialog.SetDefaultColor(
            self.vis_group_id, c4d.COLOR_TEXT,   DEFAULT_COLOR)

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
        group_dim = self.dialog.GetItemDim(self.group_id)
        y = (group_dim["y"]+TOGGLE_Y) - mousey
        if abs(y) > TOGGLE_DIST:
            return
        x = (group_dim["x"]+TOGGLE_X) - mousex
        if x > TOGGLE_DIST:
            return
        x = mousex - (group_dim["x"]+TOGGLE_X + TOGGLE_W)
        if x > TOGGLE_DIST:
            return
        self.toggle()

    def collapse(self):
        self.dialog.HideElement(self.vis_group_id, True)
        self.dialog.HideElement(self.separator_id, False)
        self.collapsed = True
        self.dialog.SetString(self.group_id, self.get_titled_toggle())
        self.dialog.SetDefaultColor(
            self.group_id, c4d.COLOR_TEXT,   COLLAPSED_COLOR)
        self.dialog.LayoutChanged(self.group_id)
        return self.collapsed

    def expand(self):
        self.dialog.HideElement(self.vis_group_id, False)
        self.dialog.HideElement(self.separator_id, True)

        self.collapsed = False
        self.dialog.SetString(self.group_id, self.get_titled_toggle())
        self.dialog.SetDefaultColor(
            self.group_id, c4d.COLOR_TEXT,   EXPANDED_COLOR)
        self.dialog.LayoutChanged(self.group_id)
        return self.collapsed

    def toggle(self):
        return self.expand() if self.collapsed else self.collapse()
