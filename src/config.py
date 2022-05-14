
from typing import Dict, List, Any, TypeVar
from json.encoder import JSONEncoder
import bpy
import os
import json


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.to_dict()


class Config:
    ExportPath: str
    PaksPath: str
    ImportDecals: bool
    ImportLights: bool
    CombineUmaps: bool
    CombineMethod: str
    AssetControl: str
    SelectedMap: str

    def __init__(self) -> None:
        sc = bpy.context.scene
        # ys = sc.yina
        # ks = sc.kena
        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        self.ExportPath = addon_prefs.exportPath
        self.PaksPath = addon_prefs.paksPath
        self.ImportDecals = addon_prefs.importDecals
        self.ImportLights = addon_prefs.importLights
        self.CombineUmaps = addon_prefs.combineUmaps
        self.CombineMethod = addon_prefs.combineMethod
        self.TextureControl = addon_prefs.textureControl
        self.SelectedMap = addon_prefs.selectedMap
        self.Debug = addon_prefs.debug

    def to_dict(self) -> dict:
        result: dict = {
                        "PaksPath": self.PaksPath,
                        "ImportDecals": self.ImportDecals,
                        "ImportLights": self.ImportLights,
                        "CombineUmaps": self.CombineUmaps,
                        "CombineMethod": self.CombineMethod,
                        "TextureControl": self.TextureControl,
                        "SelectedMap": self.SelectedMap,
                        "Debug": self.Debug
                        }

        return result

    def load(self, out=None):  # TODO: load textures
        if not os.path.exists(os.path.join(self.ExportPath, "config.json")):
            return
        with open(os.path.join(self.ExportPath, "config.json"), "r") as f:
            data = json.load(f)
            if out is None:
                out = data

        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        addon_prefs.paksPath = data["PaksPath"]
        addon_prefs.importDecals = data["ImportDecals"]
        addon_prefs.importLights = data["ImportLights"]
        addon_prefs.combineUmaps = data["CombineUmaps"]
        addon_prefs.combineMethod = data["CombineMethod"]
        addon_prefs.textureControl = data["TextureControl"]
        addon_prefs.selectedMap = data["SelectedMap"]
        addon_prefs.debug = data["Debug"]

    def dump(self, path):
        with open(os.path.join(path, "config.json"), "w") as f:
            json.dump(self.to_dict(), f, indent=4, cls=MyEncoder)
