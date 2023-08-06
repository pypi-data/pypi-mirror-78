import copy

import numpy as np

from atompack.util import AsDict


class Atom(AsDict):
    """Container to store metadata about a single atom.
    
    Notes:
        Any `kwargs` passed to `__init__()` are dynamically set as instance variables.

    Args:
        position: Position vector in 3D cartesian space.

    Example:
        >>> from atompack.atom import Atom
        >>> import numpy as np
        >>> 
        >>> atom = Atom(np.zeros(3), charge=-2)
        >>> assert atom.charge == -2
    """

    def __init__(self, position: np.ndarray, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._position = position

    @property
    def position(self) -> np.ndarray:
        """Returns a copy of the atom's position vector."""
        return copy.deepcopy(self._position)
