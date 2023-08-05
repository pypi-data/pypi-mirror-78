
import c4d
from cioc4d.collapsible_section import CollapsibleSection
from cioc4d.widgets.button_row import ButtonRow
from cioc4d.widgets.path_widget import PathWidget
from ciocore.gpath_list import PathList


class AssetsSection(CollapsibleSection):
    ORDER=50
    def __init__(self, dialog):
        self.path_list_grp_id = None
        self.pathlist = PathList()
        self.path_widgets = []
        super(AssetsSection, self).__init__(
            dialog, "Extra Assets", collapse=True)

    def build(self):
        buttons = ["Clear List", "Browse File", "Browse Directory"]
        self.button_row = ButtonRow(
            self.dialog, *buttons)

        self.scroll_id = self.dialog.register()
        self.path_list_grp_id = self.dialog.register()

        scroll_grp = self.dialog.ScrollGroupBegin(
            id=self.scroll_id,
            flags=c4d.BFH_SCALEFIT,
            inith=100,
            scrollflags=c4d.SCROLLGROUP_VERT | c4d.SCROLLGROUP_HORIZ)

        if scroll_grp:
            grp = self.dialog.GroupBegin(
                id=self.path_list_grp_id,
                flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,
                title="",
                cols=1,
                groupflags=0)
            if grp:
                self.dialog.GroupBorderSpace(2, 2, 2, 2)

            self.dialog.GroupEnd()  # manin
        self.dialog.GroupEnd()  # scroll

    def populate(self):
        pass

    def on_plugin_message(self, widget_id, msg):
        button_ids = self.button_row.button_ids

        if widget_id == button_ids[0]:  # clear list
            self.clear_entries()
            return

        if widget_id == button_ids[1]:  # browse file
            fn = c4d.storage.LoadDialog(flags=c4d.FILESELECT_LOAD)
            self.add_entry(fn)
            return

        if widget_id == button_ids[2]:  # browse dir
            fn = c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY)
            self.add_entry(fn)

        path_widget = next(
            (widget for widget in self.path_widgets if widget.delete_btn_id == widget_id), None)
        if path_widget:
            self.remove_entry(path_widget.get_value())

    def clear_entries(self):
        self.pathlist = PathList()
        self._update_widgets()

    def add_entry(self, entry):
        self.pathlist.add(entry.decode("utf8"))
        self._update_widgets()

    def remove_entry(self, entry):
        self.pathlist.remove(entry.decode("utf8"))
        self._update_widgets()

    def _update_widgets(self):
        self.path_widgets = []
        self.dialog.LayoutFlushGroup(self.path_list_grp_id)
        for path in self.pathlist:
            self.path_widgets.append(
                PathWidget(self.dialog, path=path.posix_path()))
        self.dialog.LayoutChanged(self.path_list_grp_id)
