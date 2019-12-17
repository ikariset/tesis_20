# Cambio de carpeta a la zona de clases
import os.path
import sys

classes_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/classes/')
sys.path.append(classes_dir)

from classes.RankerTree import RankerTree
from classes.RankerNode import RankerNode
from classes.InvertedIndexFactory import InvertedIndexClass