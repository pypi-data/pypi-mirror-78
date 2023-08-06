""" directory related functions"""

from typing import Any, List

from apu.datastructures.memorywrapper import MemoryWrapper
from apu.dp.null import Null

class Dictionary:
    """ shared Memory dictionary """

    __SHARED_MEMORY = {}

    def __init__(self) -> None:
        """ init shared memory """
        self._dict = Dictionary.__SHARED_MEMORY

    def set(self, key: str, value: Any) -> bool:
        """ set a key value pair into the dictionary

        Arguments:
            key(str): key value has to be string
            value(Any): any value is allowed

        Returns:
            (bool): successful added
        """
        self._dict[key] = value
        return True

    def get(self, key: str) -> Any:
        """ get an dictionary element by key

        Arguments:
            key(str): key pointing to the
                      memory related to it

        Returns:
            (Any): the value or a Null object
        """
        if key in self._dict:
            return self._dict[key]

        return Null()

    def keys(self) -> List[str]:
        """ get  all keys of the data storage

        Returns:
            (List[str]): return a list of strings
        """
        return self._dict.keys()

    def delete(self, key: str) -> None:
        """ delete a key value pair

        Arguments:
            key(str): key pointing to memory position

        """
        del self._dict[key]

    def exists(self, key: str) -> bool:
        """ check if the key is in the list of
            pointers in the memory

        Arguments:
            key(str): pointer to value

        Returns:
            (bool): true if the key is a valid pointer

        """
        return key in self._dict

    def flush(self):
        """ clean the memory """
        self._dict.clear()

    @property
    def all(self) -> dict:
        """ get the whole dict

        Returns:
            (dict): the shared memory dictionary

        """
        return self._dict

class DictionaryWrapper(MemoryWrapper):
    """Dictionary class wrapper class.
       This is used for using Dictionary as a memory.
    """

    def setup(self):
        """ setup the Wrapper with a dictionary object"""
        self._mem = Dictionary()

    def close(self):
        """ close the memory and delete all items"""
        self._mem.flush()

    def set(self, key: str, value: Any) -> bool:
        """ store data to memory

        Arguments:
            key(str): pointer to memory
            value(Any): memory to store

        Returns:
            (bool): True if the memory are set successfull
        """
        data = MemoryWrapper.transform_value_to_pickle(value)
        self._mem.set(key, data)
        return True

    def get(self, key: str) -> Any:
        """get the memory utilizing a reference

        Arguments:
            key(str): key to memory

        Returns:
            (Any): memory or Null-Object
        """
        data = self._mem.get(key)
        if data:
            value = MemoryWrapper.transform_pickle_to_value(data)
        else:
            value = Null()
        return value

    def delete(self, key: str) -> bool:
        """ delete the value related to the pointer

        Arguments:
            key(str): point to memory

        Returns:
            (bool): successfully deleted
        """
        if key in self._mem.keys():
            self._mem.delete(key)
            return True
        return False

    def has(self, key: str) -> bool:
        """ does points contain the key

        Arguments:
            key(str): pointer wo memory

        Returns:
            (bool): True if the pointers contains the key
        """
        return self._mem.exists(key)

    def _get_all(self) -> dict:
        """ the managed memory

        Returns:
            (dict): the whole (serialized data)
        """
        return self._mem.all

    def _restore(self, kv_pairs: dict) -> bool:
        """ map a directory into the memory

        Arguments:
            kv_pairs(dict): dictionary. key can also be bytes

        Returns:
            (bool): True if succeed to store kv_pairs to memory

        """
        self._mem.flush()
        for key, val in kv_pairs.items():
            if isinstance(key, bytes):
                key = key.decode("utf-8")
            self._mem.set(key, val)
        return True
