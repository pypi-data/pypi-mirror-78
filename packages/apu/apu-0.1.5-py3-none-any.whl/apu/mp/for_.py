""" module builds parallel for loops """

from contextlib import closing
import multiprocessing.pool
from typing import Any, Callable, List, Tuple

def parallel_for(
        loop_callback: Callable[[Any], Any],
        parameters: List[Tuple[Any, ...]],
        nb_threads: int = 8,
) -> List[Any]:
    """Execute a for loop body in parallel
    .. note:: Race-Conditions
        Code executation in parallel can cause into an "race-condition"
        error.

    Arguments:
        loop_callback(Callable): function callback running in the
                                             loop body
        parameters(List[Tuple]): element to execute in parallel

    Returns:
        (List[Any]): list of values

    Examples:
    .. example-code::
        >>> x = lambda x: x ** 2
        >>> parallel_for(x, [y for y in range(10)])
        [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    """
    with closing(multiprocessing.pool.ThreadPool(nb_threads)) as pool:
        return pool.map(loop_callback, parameters)
