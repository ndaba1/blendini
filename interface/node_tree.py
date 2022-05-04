import bpy
from bpy.types import NodeTree, Node, NodeSocket


class BlendiniTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'BlendiniTreeType'
    # Label for nice name display
    bl_label = "Blendini Editor"
    # Icon identifier
    bl_icon = 'BLENDER'