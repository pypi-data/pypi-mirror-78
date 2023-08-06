""" apu.dp.backboard implementation """

import json
import os

from typing import Callable, Any, List

from apu.datastructures.dictionary import DictionaryWrapper
from apu.exception.dict_key import ExistingKey, NonExistingKey, KeyNotString
from apu.exception.noteditable import NotEditable
from apu.exception.directory import NonExistingDirectory
from apu.exception.io import UnsafeLoading


class MetaInfo:
    """ additional information and data manipulation utilizing callbacks """
    def __init__(self, read_only: bool = True):
        """ are the values read only

        Arguments:
            read_only(bool): set the value data to read_only
        """
        self.read_only = read_only
        self._callback = list()

    def __call__(self, value: Any):
        """ call all callback functions on given value

        Arguments:
            value(Any): value to run with the callbacks
        """
        for call_back in self._callback:
            call_back(value)

    @property
    def callback(self) -> List[Callable[[Any], Any]]:
        """ get the callbacks

        Returns:
            (List[Callable[[Any], Any]]): list of all callbacks
        """
        return self._callback

    @callback.setter
    def callback(self, callback: Callable[[Any], Any]):
        """ add a new callback to the list of callbacks

        Arguments:
            callback(Callable[[Any], Any]): callable structure
        """
        self._callback.append(callback)

    def del_callback(self, callback: Callable[[Any], Any]):
        """ get one callback if the callback is in the list

        Arguments:
            callback(Callable[[Any], Any]): callable structure
        """
        if callback in self._callback:
            self._callback.remove(callback)

    def clean(self):
        """ delete all callbacks """
        del self._callback[:]


class Blackboard:
    """a shared memory structure to handover information
       in different objects"""
    def __init__(self):
        self._memory_wrapper = DictionaryWrapper()
        self._meta_info = {}

    def close(self):
        """ delete the meta information and close the memory"""
        del self._meta_info
        self._memory_wrapper.close()

    def set(self, key: str, value: Any, read_only: bool = False) -> bool:
        """ set the memory related to the reference key

        Arguments:
            key(str): reference
            value(Any): memory value
            read_only(bool): store the data read only?

        Returns:
            (bool): True if the memory could be placed

        Raises:
            KeyNotString: the reference key is not a string
            ExistingKey: the reference key is already set
        """
        if not isinstance(key, str):
            raise KeyNotString(
                f"Blackboard data `key` {key} should be `str` type.")

        if key in self._meta_info:
            raise ExistingKey("Given `key` already exists in blackboard")

        if self._memory_wrapper.set(key, value):
            self._meta_info[key] = MetaInfo(read_only=read_only)
            return True
        return False

    def get(self, key: str) -> Any:
        """ get the memory

        Arguments:
            key(str): reference key

        Returns:
            (Any): memory value

        Raises:
            NonExistingKey: key does not exists
        """
        if key not in self._meta_info:
            raise NonExistingKey
        return self._memory_wrapper.get(key)

    def update(self, key: str, value: Any) -> bool:
        """ change the memory

        Arguments:
            key(str): reference key
            value(Any): Memory value

        Returns:
            (bool): true if the data are places successfully

        Raises:
            NonExistingKey: key does not exists
            NotEditable: the memory is read only
        """
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        if meta_info.read_only:
            raise NotEditable("Cannot update read-only data")

        if self._memory_wrapper.set(key, value):
            meta_info.callback(value)
            return True
        return False

    def drop(self, key: str) -> bool:
        """ drop memory with pointer

        Arguments:
            key(str): pointer to memory

        Returns:
            (bool): Ture if the drop was successful

        Raises:
            NonExistingKey: key to memory is unknown

        """
        if key not in self._meta_info:
            raise NonExistingKey

        if self._memory_wrapper.delete(key):
            meta_info = self._meta_info[key]
            meta_info.clear_callbacks()
            del self._meta_info[key]
            return True
        return False

    def clear(self):
        """ clean the memory for all reference keys"""
        for key in self.keys(in_list=True):
            self.drop(key)

    def keys(self, in_list: bool = False) -> List[str]:
        """ get a list of all reference keys

        Arguments:
            in_list(bool): as a python list

        Returns:
            List[str]: an iterator or python list object

        """
        if in_list:
            return list(self._meta_info.keys())
        return self._meta_info.keys()

    def register_callback(self, key: str,
                          callback: Callable[[Any], Any]) -> int:
        """ register a callback on the memory values

        Arguments:
            key(str): reference key
            callback(Callable[[Any], Any]): callback function

        Returns:
            int: python id Object

        Raises:
            NonExistingKey: the key does not exists
        """
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        meta_info.add_callback(callback)
        return id(callback)

    def remove_callback(self, key: str, callback: Callable[[Any], Any]) -> int:
        """ remove the callback from the memory

        Arguments:
            key(str): reference key
            callback(Callable[[Any], Any]): delete this callback

        Returns:
            int: python object id

        Raises:
            NonExistingKey: key does not exists
        """
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        meta_info.remove_callback(callback)
        return id(callback)

    def clear_callbacks(self, key: str):
        """ clear the callback

        Arguments:
            key(str): reference key

        Raises:
            NonExistingKey: key does not exists
        """
        if key not in self._meta_info:
            raise NonExistingKey
        meta_info = self._meta_info[key]
        meta_info.clear_callbacks()

    def save(self, dir_path: str = './.blackboard'):
        """ save the blackboard

        Arguments:
            dir_path(str): file path
        """
        if not os.path.exists(dir_path):
            os.mkdir(dir_path, 0o755)
        blackboard_file_path = os.path.join(dir_path, '.blackboard.pickle')
        meta_info_file_path = os.path.join(dir_path, '.blackboard.meta')
        self._memory_wrapper.save(blackboard_file_path)
        self._save_meta_info(meta_info_file_path)

    def load(self, dir_path: str = './.blackboard', safe: bool = True):
        """ load the data from blackboard file

        Arguments:
            dir_path(str): filepath
            safe(bool): load safe

        Raises:
            UnsafeLoading: unsafe loading
            NonExistingDirectory: path does not exists
        """
        if self.keys(in_list=True):
            if safe:
                raise UnsafeLoading
            self.clear()
        if os.path.exists(dir_path):
            blackboard_file_path = os.path.join(dir_path, '.blackboard.pickle')
            meta_info_file_path = os.path.join(dir_path, '.blackboard.meta')
            self._memory_wrapper.load(blackboard_file_path)
            self._load_meta_info(meta_info_file_path)
        else:
            raise NonExistingDirectory

    def _save_meta_info(self, file_path: str):
        """store additional meta information in json file

        Arguments:
            file_path(str): file path

        """
        saved_meta_info = {}
        for key, meta_info in self._meta_info.items():
            read_only = meta_info.read_only
            saved_meta_info[key] = read_only
        with open(file_path, 'w') as outfile:
            json.dump(saved_meta_info, outfile)

    def _load_meta_info(self, file_path: str):
        """load the meta information from file

        Arguments:
            file_path: path to meta file
        """
        with open(file_path, 'r') as infile:
            saved_meta_info = json.load(infile)
        if self._meta_info:
            self._meta_info.clear()
        for key, read_only in saved_meta_info.items():
            self._meta_info[key] = MetaInfo(read_only=read_only)
