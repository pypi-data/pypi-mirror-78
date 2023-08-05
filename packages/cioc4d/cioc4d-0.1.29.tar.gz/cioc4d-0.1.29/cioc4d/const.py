"""
Contains definitions of common constants.


This file mustr be kept at the same level as the plugin "pyp" file so we can extract the version.
"""
import os
import re
import c4d

LABEL_WIDTH = 180
LABEL_HEIGHT = 14
INT_FIELD_WIDTH = 100
PLUGIN_ID = 1055243 # registered for Conductor at Maxon


C4D_VERSION = int(c4d.GetC4DVersion() / 1000)
 

PLUGIN_DIR = os.path.dirname(__file__)
VERSION = u"dev.999"
try:
    with open(os.path.join(PLUGIN_DIR, "VERSION")) as version_file:
        VERSION = version_file.read().strip()
except BaseException:
    pass


