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

from .interface.node_tree import BlendiniNodeTree, MyCustomNode, MyCustomSocket, node_categories
from .nodes.Groups.node_group import BlendiniNodeGroup, BDN_OT_AddBasicNodeGroup


import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

classes = (
    BDN_OT_AddBasicNodeGroup,
    BlendiniNodeTree,
    BlendiniNodeGroup,
    MyCustomNode,
    MyCustomSocket,
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