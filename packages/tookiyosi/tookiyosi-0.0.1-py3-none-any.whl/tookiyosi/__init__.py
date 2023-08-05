# tookiyosi main

__title__ = "Tooki Yosi"
__version__ = "0.0.1"

from .errors import *
import os
import warnings
import webbrowser


def creeper():
    try:
        import winsound
        path = os.path.dirname(errors.__file__)  # getting the directory of the package itself (where __init__.py is)
        path = path + "/creeper.wav"
        winsound.PlaySound(path, winsound.SND_FILENAME)
    except Exception as e:
        raise e


def freevbucks():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", new=2, autoraise=True)


class Eyylona:
    def __init__(self, y_amount, universe=None):
        try:
            if int(y_amount) >= 2:
                self.y_amount = int(y_amount)
                name = "E"
                i = 0
                while i < self.y_amount:
                    name = name + "y"
                    i = i + 1
                name = name + "lona"
                self.name = str(name)
            else:
                raise CosmicUniverseError("Eyylona needs to have at least 2 Y's.")
        except Exception as e:
            raise e
        if universe:
            try:
                if int(universe) == 7:
                    raise CosmicUniverseError("There is already an Eyylona on universe #7! Two eyylons would cause the universe to explode.")
                if int(universe) < 1 or int(universe) > 101:
                    raise ValueError("The universe number is invalid! It must be a number between 1-101.")
                self.universe = int(universe)
            except Exception as e:
                raise e
        else:
            self.universe = None

    def set_y_amount(self, y_amount):
        try:
            if int(y_amount) >= 2:
                self.y_amount = int(y_amount)
                name = "E"
                i = 0
                while i < self.y_amount:
                    name = name + "y"
                    i = i + 1
                name = name + "lona"
                self.name = str(name)
            else:
                raise CosmicUniverseError("Eyylona needs to have at least 2 Y's.")
        except Exception as e:
            raise e

    def setuniverse(self, universe):
        try:
            if int(universe) == 7:
                warnings.warn("Could not set universe: There is already an Eyylona on universe #7! Two eyylons would cause the universe to explode.")
            elif int(universe) < 1 or int(universe) > 101:
                warnings.warn("Could not set universe: The universe number is invalid! It must be a number between 1-101.")
            else:
                self.universe = int(universe)
        except Exception as e:
            if universe is None:
                self.universe = None
            else:
                warnings.warn("Could not set universe: " + str(type(e)) + ": " + str(e))
