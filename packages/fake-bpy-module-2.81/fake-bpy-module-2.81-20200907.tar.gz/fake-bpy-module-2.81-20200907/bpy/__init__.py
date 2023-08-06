import sys
import typing
import bpy.types

from . import types
from . import ops
from . import utils
from . import context
from . import app
from . import path
from . import props

data: 'bpy.types.BlendData' = None
''' Access to Blender's internal data
'''
