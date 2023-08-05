import os
import c4d
from cioc4d.collapsible_section import CollapsibleSection
from cioc4d.widgets.button_row import ButtonRow
from cioc4d.widgets.path_widget import PathWidget
from ciocore.gpath_list import GLOBBABLE_REGEX, PathList

BG_COLOR = c4d.Vector(0.2, 0.2, 0.2)


class AssetsSection(CollapsibleSection):
    ORDER = 200

    def __init__(self, dialog):
        self.path_list_grp_id = None
        self.pathlist = PathList()
        self.path_widgets = []
        super(AssetsSection, self).__init__(
            dialog, "Extra Assets", collapse=True)

    def build(self):

        self.button_row = ButtonRow(
            self.dialog, "Clear List", "Browse File", "Browse Directory", "Preview")

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

            self.dialog.GroupEnd()  # main
        self.dialog.GroupEnd()  # scroll

        self.dialog.SetDefaultColor(
            self.path_list_grp_id, c4d.COLOR_BG,   BG_COLOR)

    def populate_from_store(self):
        store = self.dialog.store
        self.pathlist = PathList(*(store.assets()))
        self._update_widgets()

    def save_to_store(self):
        store = self.dialog.store
        store.set_assets([p.posix_path() for p in self.pathlist])
        store.commit()

    @property
    def clear_button_id(self):
        return self.button_row.button_ids[0]

    @property
    def browse_file_button_id(self):
        return self.button_row.button_ids[1]

    @property
    def browse_directory_button_id(self):
        return self.button_row.button_ids[2]

    @property
    def preview_button_id(self):
        return self.button_row.button_ids[3]

    def on_plugin_message(self, widget_id, msg):

        # clear list button
        if widget_id == self.clear_button_id:
            self.clear_entries()
         # browse file
        elif widget_id == self.browse_file_button_id:
            fn = c4d.storage.LoadDialog(flags=c4d.FILESELECT_LOAD)
            self.add_entry(fn)
        # browse dir
        elif widget_id == self.browse_directory_button_id:
            fn = c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY)
            self.add_entry(fn)
        else:
            # delete one entry button
            path_widget = next(
                (widget for widget in self.path_widgets if widget.delete_btn_id == widget_id), None)
            if path_widget:
                self.remove_entry(path_widget.get_value())

    def clear_entries(self):
        self.pathlist = PathList()
        self._update_widgets()
        self.save_to_store()

    def add_entry(self, entry):
        self.pathlist.add(entry.decode("utf8"))
        self._update_widgets()
        self.save_to_store()

    def remove_entry(self, entry):
        self.pathlist.remove(entry.decode("utf8"))
        self._update_widgets()
        self.save_to_store()

    def _update_widgets(self):
        self.path_widgets = []
        self.dialog.LayoutFlushGroup(self.path_list_grp_id)
        for path in self.pathlist:
            self.path_widgets.append(
                PathWidget(self.dialog, path=path.posix_path()))
        self.dialog.LayoutChanged(self.path_list_grp_id)
        

    def resolve(self, _, **kwargs):

        if not kwargs.get("with_assets"):
            return {
                "upload_paths":  "Assets are only displayed if you use the Preview button in the Assets section."}

        try:
            return {
                "upload_paths": self.get_upload_paths()
            }
        except ValueError as ex:
            pass

        return {
            "upload_paths":  str(ex)
        }

    def get_preview_affectors(self):
        """
        Only update the preview on explicit button click.

        Collecting assets is potentially expensive as we need to hit the
        filesystem. For this reason, make the user click a button so they know
        what to expect.
        """
        return [self.preview_button_id]

    def get_upload_paths(self):
        # the extra assets
        path_list = _remove_missing_files(self.pathlist)

        document = c4d.documents.GetActiveDocument()
        asset_list = []
        success = c4d.documents.GetAllAssetsNew(
            document, False, '',
            flags=c4d.ASSETDATA_FLAG_WITHCACHES,
            assetList=asset_list)
        if success == c4d.GETALLASSETSRESULT_FAILED:
            raise ValueError("c4d.GetAllAssetsNew gave an error.")
        else:
            path_list.add(*[asset["filename"]
                            for asset in asset_list if asset["exists"]])

        path_list.glob()
        return sorted([p.posix_path() for p in path_list])


def _remove_missing_files(pathlist):
    # NOTE: This is temporary - SHOULD BE HANDLED IN GPathList class. We
    # remove any non-globbable paths that dont exist. We never want the
    # uploader to fail because of missing files. The reason is that the
    # uploader output is not user friendly and its hard to find the
    # culprits. Instead we alert the user about missing files and ask them
    # if they want to continue.
    result = PathList()
    for path in pathlist:
        pp = path.posix_path()
        if GLOBBABLE_REGEX.search(pp):
            result.add(path)
        else:
            if os.path.exists(pp):
                result.add(path)
    return result
