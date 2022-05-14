from cgitb import text
import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty, BoolProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel


# All Todo

class ListItem(PropertyGroup):
    """Group of properties representing an item in the list."""

    name: StringProperty(
        name="Name",
        description="A name for this item",
        default="Untitled"
    )

    random_prop: BoolProperty(
        name="",
        description="",
        default=True
    )


class MY_UL_List(UIList):
    """Demo UIList."""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        custom_icon = 'OBJECT_DATAMODE'
        

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "random_prop")
            layout.label(text=item.name)


        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.prop(item, "random_prop")
            layout.label(text="", icon=custom_icon)


class LIST_OT_NewItem(Operator):
    """Add a new item to the list."""

    bl_idname = "my_list.new_item"
    bl_label = "Add a new item"

    def execute(self, context):
        context.scene.my_list.add()

        return{'FINISHED'}



def register():

    #     bpy.utils.register_class(ListItem)
    #     bpy.utils.register_class(MY_UL_List)
    #     bpy.utils.register_class(LIST_OT_NewItem)
    #     bpy.utils.register_class(LIST_OT_DeleteItem)
    #     bpy.utils.register_class(LIST_OT_MoveItem)
    #     bpy.utils.register_class(PT_ListExample)

    bpy.types.Scene.my_list = CollectionProperty(type=ListItem)
    bpy.types.Scene.list_index = IntProperty(name="Index for my_list",
                                             default=0)


def unregister():

    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index

#     bpy.utils.unregister_class(ListItem)
#     bpy.utils.unregister_class(MY_UL_List)
#     bpy.utils.unregister_class(LIST_OT_NewItem)
#     bpy.utils.unregister_class(LIST_OT_DeleteItem)
#     bpy.utils.unregister_class(LIST_OT_MoveItem)
#     bpy.utils.unregister_class(PT_ListExample)


if __name__ == "__main__":
    register()
