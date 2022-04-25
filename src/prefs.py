from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import Operator, AddonPreferences
import bpy


class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    gamePath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        pass
        # layout = self.layout
        # layout.label(text="This is a preferences view for our add-on")
        # layout.prop(self, "filepath")
        # layout.prop(self, "number")
        # layout.prop(self, "boolean")
