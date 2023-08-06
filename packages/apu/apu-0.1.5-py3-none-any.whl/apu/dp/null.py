""" null objects do nothing only marking the position as null"""

class Null:
    """ Null Object implementation

        This class ignores all parameters parsed to the object
        on creation.
        The created instances do nothing and mark an object
        nor nothing
    """
    def __init__(self, *args, **kargs) -> None:
        """ Ignore the function call """
        return None

    def __call__(self, *args, **kwargs):
        """ Ignore the function call """
        return self

    def __getattr__(self, name):
        """ Ignore the function call """
        return self

    def __setattr__(self, name, value):
        """ Ignore the function call """
        return self

    def __delattr__(self, name):
        """ Ignore the function call """
        return self

    def __repr__(self) -> str:
        """ string representation

        Returns:
            (str): the String \"<Null>\"

        Examples:
        ..  example-code:
            >>> n = Null()
            >>> repr(n)
            <Null>

        """
        return "<Null>"

    def __str__(self) -> str:
        """ string representation

        Returns:
            (str): the String \"Null\"

        Examples:
        ..  example-code:
            >>> n = Null()
            >>> str(n)
            Null
        """
        return "Null"
