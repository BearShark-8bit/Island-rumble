"""pytiles is a Python module that provides classes and functions for working with tiled maps provided by Tiled"""


import os, sys, inspect

cmd_folder = os.path.realpath(
    os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
)

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(
    os.path.abspath(
        os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "tile")
    )
)

if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

cmd_subfolder = os.path.realpath(
    os.path.abspath(
        os.path.join(
            os.path.split(inspect.getfile(inspect.currentframe()))[0], "structures"
        )
    )
)

if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import tile
import structures
from loadTileGroup import loadTileGroup
