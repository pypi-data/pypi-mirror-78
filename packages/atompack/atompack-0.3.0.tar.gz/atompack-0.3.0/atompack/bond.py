from atompack.util import AsDict


class Bond(AsDict):
    """Container to store metadata about a bond between atoms.
    
    Notes:
        Any `kwargs` passed to `__init__()` are dynamically set as instance variables.
    """

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
