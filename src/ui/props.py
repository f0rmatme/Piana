import re
import bpy
import os


from .funcs import has_paks
from ..utils.common import setup_logger


from pathlib import Path
from bpy.types import EnumPropertyItem

import requests

logger = setup_logger(__name__)


