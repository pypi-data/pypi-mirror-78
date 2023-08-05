import os
import c4d
from cioc4d.sections.collapsible_section import CollapsibleSection
from cioc4d.widgets.button_row import ButtonRow
from cioc4d.widgets.path_widget import PathWidget
from ciocore.gpath_list import GLOBBABLE_REGEX, PathList
from ciocore.gpath import Path
from cioc4d import const as k

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
            self.dialog, "Clear List", "Browse File", "Browse Directory", label="Actions")
            
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

    # @property
    # def preview_button_id(self):
    #     return self.button_row.button_ids[3]

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
                "upload_paths":  "Assets are only shown here if you use the Show Assets button above."}
        try:
            return {
                "upload_paths": self.get_upload_paths()
            }
        except ValueError as ex:
            pass

        return {
            "upload_paths":  str(ex)
        }
 

    def get_upload_paths(self):
        return sorted([p.posix_path() for p in self.get_assets_path_list()])


    def get_assets_path_list(self):
        # the extra assets
        # copy

        document = c4d.documents.GetActiveDocument()

        path_list= PathList(*self.pathlist) 

        # Called remove_missing here because its cheaper to do it while the list
        # is small. The scraped assets have an exists field anyway.
        path_list.remove_missing()

        if k.C4D_VERSION < 22:
            docfile = Path(os.path.join( 
                document.GetDocumentPath(), document.GetDocumentName()
                )).posix_path()

            asset_list = c4d.documents.GetAllAssets(document, False, '')
            path_list.add(*[asset["filename"]  for asset in asset_list if asset["exists"]  ] )
            path_list.add(docfile)
        else:
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
        return path_list
        


  