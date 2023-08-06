from typing import Any, Dict


class AsDict(object):

    def as_dict(self) -> Dict[str, Any]:
        return {k: getattr(self, k) for k in dir(self) if not k.startswith("_")}
