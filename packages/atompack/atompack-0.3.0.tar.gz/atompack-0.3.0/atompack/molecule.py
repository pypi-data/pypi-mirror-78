from typing import List, Tuple

from atompack.atom import Atom
from atompack.bond import Bond
from atompack.topology import Topology


class Molecule(Topology):
    """Representation of a molecule."""

    def __init__(self, atoms: List[Atom], bonds: List[Tuple[int, int, Bond]]) -> None:
        super().__init__()
        for atom in atoms:
            self.insert(atom)
        for i, j, bond in bonds:
            self.connect(i, j, bond=bond)
