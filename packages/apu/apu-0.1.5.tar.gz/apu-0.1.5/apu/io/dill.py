""" dill pickle related functions """
from typing import Any

import dill as pickle

from apu.exception.unsupporteddatatype import UnsupportedDataType


def reconstruct(value: Any) -> str:
    """serialize the data

    Arguments:
        value(Any): object to serialize

    Returns:
        (str): serialized data

    Raises:
        UnsupportedDataType: the data are not serializeable

    """
    try:
        value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
    except pickle.PicklingError as pickle_e:
        raise UnsupportedDataType(
            f"Cannot serialize given data: {value}. Details: {pickle_e}"
        ) from pickle_e
    return value


def load(data: str) -> Any:
    """serialize the data

    Arguments:
        data(str): string to deserialize

    Returns:
        (Any): deserialized data

    Raises:
        UnsupportedDataType: the data are not deserializeable

    """
    try:
        value = pickle.loads(data)
    except pickle.UnpicklingError as upe:
        raise UnsupportedDataType(
            f"Cannot deserialize given data: {data}. Details: {upe}") from upe
    return value
