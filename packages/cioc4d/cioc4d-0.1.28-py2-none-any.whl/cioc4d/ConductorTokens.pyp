
"""
Copyright: Conductor Technologies
Author: Conductor Team

Description:
    - Registers two Tokens.

Compatible:
    - Win / Mac
    - R21
"""
import tempfile
from os.path import expanduser
import os
import c4d

def get_tempdir(_):
    # return tempfile.gettempdir()
    return "/path/to/temp/"


def get_homedir(_):
    # return expanduser("~")
    
    return "/path/to/home/"

if __name__ == "__main__":

    for registeredToken in c4d.modules.tokensystem.GetAllTokenEntries():
        if registeredToken.get("_token") in ["ciotemp", "ciohome"]:
            exit()

    c4d.plugins.RegisterToken(
        "ciotemp", "Conductor: System temp directory", "$ciotemp", get_tempdir)
    c4d.plugins.RegisterToken(
        "ciohome", "Conductor: System home directory", "$ciohome", get_homedir)
