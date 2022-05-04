# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Blendini",
    "author" : "Victor Ndaba",
    "description" : "Introduces a procedural houdini-like workflow to blender",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 1),
    "location" : "Editors > Blendini",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.types import NodeTree, Node, NodeSocket, Panel, Menu

C = bpy.context
D = bpy.data

# Implementation of custom nodes from Python


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MyCustomTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomTreeType'
    # Label for nice name display
    bl_label = "Blendini"
    # Icon identifier
    bl_icon = 'BLENDER'

class ObjectButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"


class OBJECT_PT_context_object(ObjectButtonsPanel, Panel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.use_pin_id:
            layout.template_ID(space, "pin_id")
        else:
            row = layout.row()
            row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')

class ShaderSocket(NodeSocket):
    bl_idname = 'ShaderSocket'
    bl_label = 'Shader socket'

# Custom socket type
class MyCustomSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomSocketType'
    # Label for nice name display
    bl_label = "Custom Node Socket"

    # Enum items list
    my_items = (
        ('DOWN', "Down", "Where your feet are"),
        ('UP', "Up", "Where your head should be"),
        ('LEFT', "Left", "Not right"),
        ('RIGHT', "Right", "Not left"),
    )

    my_enum_prop: bpy.props.EnumProperty(
        name="Direction",
        description="Just an example",
        items=my_items,
        default='UP',
    )

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "my_enum_prop", text=text)
            

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MyCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'CustomTreeType'

class ObjectDataNode(Node, MyCustomTreeNode):
    '''A more usable node'''
    bl_idname = 'ObjectNodeType'
    bl_label = 'Object'

    Name: bpy.props.StringProperty(default="Object Node")

    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        # layout.label(text="Node settings")
        layout.prop(self, "Name")
        row = layout.row()
        row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        # my_string_prop button will only be visible in the sidebar
        layout.prop(self, "Name")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return self.Name

# Derived from the Node base type.
class MyCustomNode(Node, MyCustomTreeNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomNodeType'
    # Label for nice name display
    bl_label = 'Geometry'
    # Icon identifier
    bl_icon = 'OBJECT_DATA'

    bl_options = {'REGISTER', 'UNDO'}

    Name: bpy.props.StringProperty()

    def init(self, context):
        print("ONInit")
        self.inputs.new('NodeSocketShader', "Shader")
        self.inputs.new('CustomSocketType', "Geo Data")
        self.outputs.new('NodeSocketColor', "Output")

        print(repr(self.Name))
        bpy.ops.mesh.primitive_cube_add()
        self.Name = C.active_object.name

    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print(repr(self.Name))
        print("Removing node ", self, ", Goodbye!")
        obj = bpy.data.objects[self.Name]
        D.objects.remove(obj)


    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.label(text="Object Data")
        # layout.prop(self, "Name")
        row = layout.row()
        row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')
        row.template_ID(context.scene.objects, "active", filter='AVAILABLE')

        layout = self.layout

        snode = context.space_data
        id_from = snode.id_from

        row.template_ID(id_from, "active_material", new="material.new")
    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        # my_string_prop button will only be visible in the sidebar
        layout.prop(self, "Name")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return self.Name

#######################################################################








#######################################################################



### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type


class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'CustomTreeType'


# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory('GEOMTERY', "Geometry", items=[
        # our basic node
        NodeItem("CustomNodeType", label='Cube', settings={
        }),
        NodeItem("CustomNodeType", label='Torus', settings={
        }),
        NodeItem("CustomNodeType", label='Sphere', settings={
        }),
    ]),
    # MyNodeCategory('OBJECTNODES', "Objects", items=[
    #     NodeItem("ObjectNodeType")
    # ]),
    # MyNodeCategory('OTHERNODES', "Other Nodes", items=[
    #     # the node item can have additional settings,
    #     # which are applied to new nodes
    #     # NOTE: settings values are stored as string expressions,
    #     # for this reason they should be converted to strings using repr()
    #     NodeItem("CustomNodeType", label="Node A", settings={
    #         "my_string_prop": repr("Lorem ipsum dolor sit amet"),
    #         "my_float_prop": repr(1.0),
    #     }),
    #     NodeItem("CustomNodeType", label="Node B", settings={
    #         "my_string_prop": repr("consectetur adipisicing elit"),
    #         "my_float_prop": repr(2.0),
    #     }),
    # ]),
]

classes = (
    MyCustomTree,
    MyCustomSocket,
    MyCustomNode,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
