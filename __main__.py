import os
import sys

fpath = os.path.join(os.path.dirname(__file__), "")
sys.path.append(fpath)

fpath = os.path.join(os.path.dirname(__file__), "src")
sys.path.append(fpath)

fpath = os.path.join(os.path.dirname(__file__), "src/Tiled_utils")
sys.path.append(fpath)

from src.Game import Game


if __name__ == "__main__":
    Game()
