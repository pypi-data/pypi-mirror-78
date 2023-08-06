""" apu.datastructure.memorywrapper """

import abc
from typing import Any
import dill as pickle

from apu.dp.null import Null
from apu.exception.readwrongfile import ReadWrongFile
from apu.io.dill import reconstruct, load


class MemoryWrapper:
    """ wrap the memory and setup steps.
        future change to additional wrapper
    """
    def __init__(self, **kwargs):
        """ init the object """
        self._mem = None
        self._config = kwargs
        self.setup()

    @abc.abstractmethod
    def setup(self):
        """ memory setup """

    @abc.abstractmethod
    def close(self):
        """ set the Pointer to Null """
        self._mem = Null()

    @abc.abstractmethod
    def set(self, key: str, value: Any) -> bool:
        """ set a key to the memory value
        Arguments:
            key(str): string typed key
            value(Any): memory object

        Return:
            (bool): true if successfull stored
        """
        return True

    @abc.abstractmethod
    def get(self, key: str) -> Any:
        """ get the memory value by string

        Arguments:
            key(str): pointer to memory object

        Returns:
            (Any): memory object

        """
        return Null()

    @abc.abstractmethod
    def delete(self, key: str) -> bool:
        """ delete the memory object

        Arguments:
            key(str): pointer to memory object

        Returns:
            (bool): true if successfull deleted
        """

        return True

    @abc.abstractmethod
    def has(self, key: str) -> bool:
        """ has pointer to memory?

        Arguments:
            key(str): request key

        Returns:
            (bool): True if the pointer is in memory
        """
        return False

    @abc.abstractmethod
    def _get_all(self) -> dict:
        """ get the whole managed memory
        Returns:
            (dict): get all serialized data in the blackboard
        """
        return dict()

    @abc.abstractmethod
    def _restore(self, kv_pairs):
        """
        Arguments:
            ky_pairs(dict): key value pairs

        Returns:
            (bool): true if the key value pair is successfully stored
        """
        return True

    @staticmethod
    def transform_value_to_pickle(value: Any) -> str:
        """ serialize an object

        Arguments:
            value(Any): the memory

        Returns:
            (str): serialized object
        """
        return reconstruct(value)

    @staticmethod
    def transform_pickle_to_value(data: str) -> Any:
        """ deserialize object

        Arguments:
            data(str): serialized value

        Returns:
            (Any): deserialized Data

        """
        return load(data)

    def save(self, file_path: str) -> bool:
        """ store the memory to file

        Arguments:
            file_path(str): the path to the fail containing the memory

        Returns:
            (bool): True if the storage was successful
        """
        whole_data = self._get_all()
        with open(file_path, 'wb') as outfile:
            pickle.dump(whole_data, outfile, protocol=pickle.HIGHEST_PROTOCOL)
        return True

    def load(self, file_path: str) -> bool:
        """ load the data from file

        Arguments:
            file_path(str): the path to the fail containing the memory

        Returns:
            (bool): True if the storage was successful
        """
        with open(file_path, 'rb') as infile:
            read_data = pickle.load(infile)
        if not isinstance(read_data, dict):
            raise ReadWrongFile(
                f"File contents must be dictionary data: {read_data}")
        self._restore(read_data)
        return True
