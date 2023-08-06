""" apu.exception: anton python utils excaptions module """

__version__ = (0, 0, 1)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from apu.exception.dict_key import ExistingKey, NonExistingKey, KeyNotString
from apu.exception.directory import NonExistingDirectory
from apu.exception.io import UnsafeLoading
from apu.exception.noteditable import NotEditable
from apu.exception.readwrongfile import ReadWrongFile
from apu.exception.unsupporteddatatype import UnsupportedDataType

__all__ = [
    "ExistingKey",
    "NonExistingKey",
    "KeyNotString",
    "NonExistingDirectory",
    "UnsafeLoading",
    "NotEditable",
    "ReadWrongFile",
    "UnsupportedDataType",
]
