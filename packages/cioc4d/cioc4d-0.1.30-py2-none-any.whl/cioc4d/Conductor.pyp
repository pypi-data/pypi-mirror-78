import os
import sys

CIO_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, CIO_DIR)

from cioc4d.conductor_dialog import ConductorDialog
import cioc4d.const as k
import c4d



class ConductorRender(c4d.plugins.CommandData):
    dialog = None
    def Execute(self, doc):
        if self.dialog is None:
            self.dialog = ConductorDialog()

        return self.dialog.Open(
            dlgtype=c4d.DLG_TYPE_ASYNC,
            pluginid=k.PLUGIN_ID,
            defaulth=800,
            defaultw=480)

    def RestoreLayout(self, sec_ref):
        if self.dialog is None:
            self.dialog = ConductorDialog()
        return self.dialog.Restore(pluginid=k.PLUGIN_ID, secret=sec_ref)


def enhance_main_menu():

    mainMenu = c4d.gui.GetMenuResource("M_EDITOR")
    menu = c4d.BaseContainer()
    menu.InsData(c4d.MENURESOURCE_SUBTITLE, "Conductor")
    menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_1055243")
    menu.InsData(c4d.MENURESOURCE_SEPERATOR, True)

    submenu = c4d.BaseContainer()
    submenu.InsData(c4d.MENURESOURCE_SUBTITLE, "Utilities")
    menu.InsData(c4d.MENURESOURCE_SUBMENU, submenu)
    mainMenu.InsData(c4d.MENURESOURCE_STRING, menu)


def PluginMessage(the_id, data):
    if the_id == c4d.C4DPL_BUILDMENU:
        enhance_main_menu()


if __name__ == "__main__":
    cr_icon = c4d.bitmaps.BaseBitmap()
    cr_icon.InitWith(os.path.join(
        k.PLUGIN_DIR, 'res', 'conductorRender_30x30.png'))
    c4d.WriteConsole("Conductor plugin loading...")
    success = c4d.plugins.RegisterCommandPlugin(
        id=k.PLUGIN_ID,
        str="Conductor Render",
        info=0,
        icon=cr_icon,
        help='Render scene using Conductor cloud service',
        dat=ConductorRender())

    if not success:
        c4d.WriteConsole("Couldn't register Conductor plugin.")
    c4d.WriteConsole("Conductor plugin loaded.")
