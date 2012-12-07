''' Creates a windows executable with cx_freeze. Run with "python cx_setup build". The package is fairly massive
    right now (~80 MB), partially because it includes extra libraries that are unnecessary, like QT, but one
    must be very careful when removing libraries, as it can cause the whole package to fail. Consequently,
    they are simply left in.
'''

import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "includes":[
        "scipy.sparse.csgraph._validation",
        "scipy.io.matlab.streams",
        "matplotlib.backends.backend_qt4agg"
        ]
    }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Geiger-Counter",
    version = "0.1",
    description = "Geiger-Counter Lab Analysis",
    options = {"build_exe": build_exe_options},
    executables = [Executable("GUI.py", base=base)]
    )