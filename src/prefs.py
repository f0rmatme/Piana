from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import Operator, AddonPreferences

from pathlib import Path

from .utils.common import setup_logger

from .ui.funcs import has_paks, get_umap_list
from .config import Config


import bpy
import os
import requests

logger = setup_logger(__name__)


def get_map_list():
    maps_data = requests.get("https://gist.githubusercontent.com/luvyana/d5d7b2be0d33f9d213067f06ec681bd8/raw/cd34145908eb2e936065d10f3b9b570c7d5c7353/umaps.json").json()

    maps: list = []
    name: str
    n: int = 0
    for name, value in maps_data.items():
        maps.append(
            (name, name.capitalize(), "", "", n)
        )
        n += 1

    return maps



def update_paks_path(self, context):
    addon_prefs = context.preferences.addons[__package__].preferences

    if has_paks(addon_prefs.paksPath) and os.path.isdir(addon_prefs.exportPath):
        addon_prefs.paths = True
    else:
        addon_prefs.paths = False

def update_export_path(self, context):
    addon_prefs = context.preferences.addons[__package__].preferences

    export_path = Path(addon_prefs.exportPath)
    export_path_config = export_path.joinpath("config.json")

    if export_path_config.exists():
        Config().load(export_path_config)
    else:
        addon_prefs.paksPath = ""

class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__


    debug: bpy.props.BoolProperty(
        name='Debug',
        default=False,
        description="Debug mode"
    )

    paksPath: bpy.props.StringProperty(
        name='Paks Path',
        # default="",
        description="Path to your paks folder",
        subtype='DIR_PATH',
        update=update_paks_path,
    )

    exportPath: bpy.props.StringProperty(
        name='Export Path',
        # CBA with this.
        default="D:\_valorant\\",
        description="Path to your export folder",
        subtype='DIR_PATH',
        update=update_export_path,
    )

    paths: bpy.props.BoolProperty(
        name='Check for Paths',
        default=False,
        description="Path check"
    )

    # Map Importer Settings

    importDecals: bpy.props.BoolProperty(
        name='Import Decals',
        default=False,
        description="Import decals",
        # is_readonly=True
    )

    importLights: bpy.props.BoolProperty(
        name='Import Lights',
        default=False,
        description="Import lights",
        # is_readonly=True

    )

    combineUmaps: bpy.props.BoolProperty(
        name='Combine Umaps',
        default=True,
        description="Combine umaps"
    )

    combineMethod: bpy.props.EnumProperty(
        name='Combine Method',
        default='append',
        items=[
            ('append', 'Append', 'Append makes a full copy of the data into your blend-file, without keeping any reference to the original one.', 'APPEND_BLEND', 0),
            ('link', 'Link', 'Link creates a reference to the data in the source file such that changes made there will be reflected in the referencing file the next time it is reloaded.', "LINK_BLEND", 1)
        ]
    )

    textureControl: bpy.props.EnumProperty(
        name='Texture Control',
        default='pack',
        items=[
            ('pack', 'Pack', 'Packs the textures to the .blend file.', '', 0),
            ('local', 'Local', 'Moves the textures to a new "Textures" folder.', '', 1)
        ]
    )

    selectedMap: bpy.props.EnumProperty(
        name='Selected Map',
        # default="bind",
        items=get_map_list()
    )

    scriptPath: bpy.props.StringProperty(
        name='Script Path',
        default=os.path.dirname(os.path.abspath(__file__)),
        description="Path to your script folder",
        subtype='DIR_PATH'
    )

    usePerfPatch: bpy.props.BoolProperty(
        name='Use PerfPatch',
        default=False,
        description="Huge speed-up, but use it with caution. A restart is recommended after."
    )

    isInjected: bpy.props.BoolProperty(
        name='Is Injected',
        default=False,
        description="IsDLLInjected"
    )


    def draw(self, context):
        layout = self.layout
        
        main_column = layout.column()
        s_column_1 = main_column.column(align=False)

        s_column_1.prop(self, "exportPath")
        s_column_1.prop(self, "paksPath")
        s_column_1.prop(self, "debug")
