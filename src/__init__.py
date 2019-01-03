# Cambio de carpeta a la zona de clases
import os.path
import sys

mango_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/classes/')
sys.path.append(mango_dir)
