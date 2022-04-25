
from typing import Dict, List, Any, TypeVar
from json.encoder import JSONEncoder
import bpy
import os
import json


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.to_dict()


class Config:
    Documentation: str = "https://github.com/Amrsatrio/BlenderUmap/blob/master/README.md"   # Change this later
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
        ys = sc.yina
        ks = sc.kena
        self.ExportPath = ks.exportPath
        self.PaksPath = ks.paksPath
        self.ImportDecals = ys.importDecals
        self.ImportLights = ys.importLights
        self.CombineUmaps = ys.combineUmaps
        self.CombineMethod = ys.combineMethod
        self.TextureControl = ys.textureControl
        self.SelectedMap = ys.selectedMap

    def to_dict(self) -> dict:
        result: dict = {"Documentation": self.Documentation,
                        "PaksPath": self.PaksPath,
                        "ImportDecals": self.ImportDecals,
                        "ImportLights": self.ImportLights,
                        "CombineUmaps": self.CombineUmaps,
                        "CombineMethod": self.CombineMethod,
                        "TextureControl": self.TextureControl,
                        "SelectedMap": self.SelectedMap}

        return result

    def load(self, out=None):  # TODO: load textures
        if not os.path.exists(os.path.join(self.ExportPath, "config.json")):
            return
        with open(os.path.join(self.ExportPath, "config.json"), "r") as f:
            data = json.load(f)
            if out is None:
                out = data

        sc = bpy.context.scene
        ys = sc.yina
        ks = sc.kena
        ks.paksPath = data["PaksPath"]
        ys.importDecals = data["ImportDecals"]
        ys.importLights = data["ImportLights"]
        ys.combineUmaps = data["CombineUmaps"]
        ys.combineMethod = data["CombineMethod"]
        ys.textureControl = data["TextureControl"]
        ys.selectedMap = data["SelectedMap"]

    def dump(self, path):
        with open(os.path.join(path, "config.json"), "w") as f:
            json.dump(self.to_dict(), f, indent=4, cls=MyEncoder)
