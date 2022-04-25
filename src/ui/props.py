import re
import bpy
import os

from .config import Config
from .funcs import has_paks
from ..utils.common import setup_logger


from pathlib import Path
from bpy.types import EnumPropertyItem

import requests

logger = setup_logger(__name__)


def update_export_path(self, context):
    sc = context.scene
    kena = sc.kena
    yina = sc.yina

    export_path = Path(kena.exportPath)
    export_path_config = export_path.joinpath("config.json")
    if export_path_config.exists():
        logger.info("Loading config from: {}".format(export_path_config))
        Config().load(export_path_config)
    else:
        kena.paksPath = ""


def update_paks_path(self, context):
    sc = context.scene
    kena = sc.kena
    yina = sc.yina
    # logger.info(kena.paksPath)

    if has_paks(kena.paksPath) and os.path.isdir(kena.exportPath):
        kena.paths = True
    else:
        kena.paths = False


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
        # print(a,b)

    return maps


def get_umap_list(self, context, map_name) -> list:
    maps_data = requests.get("https://gist.githubusercontent.com/luvyana/d5d7b2be0d33f9d213067f06ec681bd8/raw/cd34145908eb2e936065d10f3b9b570c7d5c7353/umaps.json").json()
    return maps_data[map_name]


class ValorantSettings(bpy.types.PropertyGroup):

    paksPath: bpy.props.StringProperty(
        name='Paks Path',
        default="",
        description="Path to your paks folder",
        subtype='DIR_PATH',
        update=update_paks_path,
    )

    exportPath: bpy.props.StringProperty(
        name='Export Path',
        default="",
        description="Path to your export folder",
        subtype='DIR_PATH',
        update=update_export_path
    )

    paths: bpy.props.BoolProperty(
        name='Check for Paths',
        default=False,
        description="Path check"
    )


class MapImporterSettings(bpy.types.PropertyGroup):

    importDecals: bpy.props.BoolProperty(
        name='Import Decals',
        default=False,
        description="Import decals"
    )

    importLights: bpy.props.BoolProperty(
        name='Import Lights',
        default=False,
        description="Import lights"
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
