import sys
import typing
import bpy.types

from . import types
from . import ops
from . import app
from . import context
from . import props
from . import utils
from . import path

data: 'bpy.types.BlendData' = None
''' Access to Blender's internal data
'''
