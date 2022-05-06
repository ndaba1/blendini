import bpy


def create_basic_node_group(context, operator, group_name):
    bpy.context.scene.use_nodes = True

    base_group = bpy.data.node_groups.new(group_name, 'BlendiniNodeTree')

    group_in = base_group.nodes.new('NodeGroupInput')
    group_in.location = (-200, 0)
    base_group.inputs.new('NodeSocketFactor', 'Input')

    group_out = base_group.nodes.new('NodeGroupOutput')
    group_out.location = (200, 0)
    base_group.inputs.new('NodeSocketColor', 'Output')

    link = base_group.links.new

    link(group_in.outputs[0], group_out.inputs[0])

    return base_group


class BDN_OT_AddBasicNodeGroup(bpy.types.Operator):
    bl_idname = "bdn.add_basic_node_group"
    bl_label = "Adds a basic node group"

    def execute(self, context):
        custom_node_name = "Basic Group"
        my_group = create_basic_node_group(self, context, custom_node_name)
        test_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        test_node.node_tree = bpy.data.node_groups[my_group.name]
        test_node.use_custom_color = True
        test_node.color = (0.5, 0.4, 0.2)

        return {'FINISHED'}


class BlendiniNodeGroup(bpy.types.Node):
    bl_idname = 'BlendiniNodeGroup'
    bl_label = "Blendini Node Group"
    bl_icon = 'NODE_TREE'
    is_sn = True

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.label(text="Node settings")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "I am a custom node"