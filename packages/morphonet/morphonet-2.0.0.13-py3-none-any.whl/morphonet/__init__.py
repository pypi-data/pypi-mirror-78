# -*- coding: latin-1 -*-
url="ns244.evxonline.net" #Temporary Folder
port=8000
vt_path="Librairies/vt"
#url="morphonet.org"
#url="localhost" #For DB installed in local
    

from . import tools
from .net import Net
from .plot import Plot
from .plugins.MorphoPlugin import MorphoPlugin
from . import ImageHandling
__all__ = [
	'tools',
    'Net',
    'Plot',
    'ImageHandling',
    'MorphoPlugin'
]

