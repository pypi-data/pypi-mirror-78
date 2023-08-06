''' iterator design pattern '''
from collections.abc import Iterable, Iterator
from typing import Any, List

class AlphabeticalOrderIterator(Iterator):
    """ Alphabetical ordered collection.
        this class stores the traversal positon at all time
    """

    #`_position` attribute stores the current traversal position.
    _position: int = None

    #`_reverse_order` indicator fot the traversel direction
    _reverse_order: bool = False

    def __init__(self,
                 collection: List[Any] = tuple(),
                 reverse_order: bool = False) -> None:
        """
        the constructor. set the list and the traversal order

        Attributes:
            collection(List[Any]): the collection. default is tuple()
            reverse_order(bool): traverse the collection starting
                                 with the last element
        """
        self._collection = collection
        self._reverse_order = reverse_order
        self._position = -1 if reverse_order else 0

    def __next__(self):
        """ get next element

        Returns:
            (Any): return the next element of collection

        Raises:
            IndexError: end of list
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse_order else 1
        except IndexError:
            raise StopIteration() from IndexError

        return value

class AlphabeticalOrderCollection(Iterable):
    """
    Collection handling a collection with iterator

    Examples:
    ..  example-code:
        >>> liste = AlphabeticalOrderCollection()
        >>> liste.add_item(0)
        >>> liste.add_item(1)
        >>> liste.add_item(2)
        >>> print("\n".join(liste))
        0
        1
        2
        >>> print("\n".join(liste.get_reverse_iterator()), end="")
        2
        1
        0

    """
    def __init__(self, collection: List[Any] = tuple()) -> None:
        """
        iterator constructor

        Arguments:
            collection(List[Any]): a tuple
        """
        self._collection = collection

    def __iter__(self) -> AlphabeticalOrderIterator:
        """
        return an iterator object

        Returns:
            (AlphabeticalOrderIterator): the iterator with alphabetical order
        """
        return AlphabeticalOrderIterator(self._collection)

    def get_reverse_iterator(self) -> AlphabeticalOrderIterator:
        """
        return an iterator object

        Returns:
            (AlphabeticalOrderIterator): the iterator in reversed order
        """
        return AlphabeticalOrderIterator(self._collection, reverse_order=True)

    def add_item(self, item: Any) -> None:
        """
        add an element to the collection

        Attributes:
            item(Any): an item for the collection
        """
        self._collection.append(item)
