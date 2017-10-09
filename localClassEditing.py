# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from osgeo import ogr
import qgis
from utilities import *

from dbf import *

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")

class LocaClassEditing:

    lineLayerName = utilities.pbsname + ': ' +  utilities.subname + '-' + utilities.fedname + '-Line'
    poleLayerName = utilities.pbsname + ': ' +  utilities.subname + '-' + utilities.fedname + '-Pole'
    subLayerName = utilities.pbsname + ': ' +  utilities.subname + '-Substation'
    
