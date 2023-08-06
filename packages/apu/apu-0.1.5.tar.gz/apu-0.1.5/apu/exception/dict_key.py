""" dictionary key related errors """

class ExistingKey(Exception):
    """ the key allready exists """

class NonExistingKey(Exception):
    """ the key does not exists """

class KeyNotString(Exception):
    """ key type is not String """
