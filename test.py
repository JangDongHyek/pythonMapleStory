import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
import db
import time
import lib
import os
import gsl
import globals
import gml
import init


init.Init()
asd = gml.getMinimapSize(True)
users = gsl.pixelseSerarch([asd['start_x'],asd['start_y'],asd['end_x'],asd['end_y']], globals.minimap_user,6)
print(users)