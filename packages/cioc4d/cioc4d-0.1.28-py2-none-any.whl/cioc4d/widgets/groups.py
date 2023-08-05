
import c4d
import cioc4d.const as k

from contextlib import contextmanager

@contextmanager
def grid_group(dialog, **kw):
    grp_id = dialog.register()
    grp = dialog.GroupBegin(
        id=grp_id,
        flags=c4d.BFH_SCALEFIT,
        # rows=kw.get("rows", 1),
        cols=kw.get("cols", 2),
        groupflags=0)
    if grp:
        yield grp_id
    dialog.GroupEnd()