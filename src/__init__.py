# Cambio de carpeta a la zona de clases
import sys, os.path
mango_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/classes/')
sys.path.append(mango_dir)
from classes import RankerTree, RankerNode