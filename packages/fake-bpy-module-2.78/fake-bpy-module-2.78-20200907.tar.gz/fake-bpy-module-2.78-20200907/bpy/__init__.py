import sys
import typing
import bpy.types

from . import ops
from . import types
from . import utils
from . import path
from . import props
from . import app
from . import context

data: 'bpy.types.BlendData' = None
''' Access to Blender's internal data
'''
