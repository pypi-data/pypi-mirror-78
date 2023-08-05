
from ciocore.gpath_list import PathList
import importlib
import c4d

__data__ = None


def data(dialog):
    global __data__

    if __data__:
        return __data__
 
    __data__ = dialog.section("AssetsSection").get_assets_path_list()
 
    return __data__

def clear():
    global __data__
    __data__ = None

 