import bpy

from bpy.props import StringProperty, IntProperty, CollectionProperty, BoolProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel
from .ui.funcs import *



class ListItem(bpy.types.PropertyGroup):
    """Group of properties representing an item in the list."""
    name: StringProperty(name="Name", description="A name for this item", default="Untitled")
    random_prop: BoolProperty(name="Any other property you want", description="", default=True)


class MY_UL_List(UIList):
    """Demo UIList."""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        custom_icon = 'OBJECT_DATAMODE'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon=custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon=custom_icon)



        # row = layout.row()
        # row.template_list("MY_UL_List", "The_List", scene,
        #                   "my_list", scene, "list_index")

        # row = layout.row()
        # row.operator('my_list.new_item', text='Add')
        # row.operator('my_list.delete_item', text='Remove')
        # # row.operator('my_list.move_item', text='UP').direction = 'UP'
        # # row.operator('my_list.move_item', text='DOWN').direction = 'DOWN'

        # if scene.list_index >= 0 and scene.my_list:
        #     item = scene.my_list[scene.list_index]

        #     row = layout.row()
        #     row.prop(item, "name")
        #     row.prop(item, "random_prop")





class LIST_OT_NewItem(Operator):
    """Add a new item to the list."""

    bl_idname = "my_list.new_item"
    bl_label = "Add a new item"

    def execute(self, context):
        context.scene.my_list.add()

        return{'FINISHED'}


class LIST_OT_DeleteItem(Operator):
    """Delete the selected item from the list."""

    bl_idname = "my_list.delete_item"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.scene.my_list

    def execute(self, context):
        my_list = context.scene.my_list
        index = context.scene.list_index

        my_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(my_list) - 1)

        return{'FINISHED'}

def register():

    bpy.types.Scene.my_list = CollectionProperty(type=ListItem)
    bpy.types.Scene.list_index = IntProperty(name="Index for my_list",
                                             default=0)


# def unregister():


#     # bpy.utils.unregister_class(ListItem)
#     del bpy.types.Scene.my_list
#     del bpy.types.Scene.list_index


if __name__ == "__main__":
    register()
