from pydantic import BaseModel
from typing import (Tuple, Dict, Any)
from pydantic.main import ModelMetaclass, no_type_check


class BaseAromaticMeta(ModelMetaclass):
    @no_type_check
    def __new__(mcs, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any], **kwargs):
        is_custom_cls = namespace.get("__module__") != "aromatic.basemodel" and namespace.get('__qualname__') not in ["BaseAromaticModel"]

        if is_custom_cls:
            patched_bases = []
            for b in bases:
                if hasattr(b, "__pydantic_model__"):
                    patched_bases.append(b.__pydantic_model__)
                else:
                    patched_bases.append(b)
            bases = tuple(patched_bases)

            if namespace.get("__doc__", None) is None:
                namespace["__doc__"] = ""

        cls = super().__new__(mcs, name, bases, namespace, **kwargs)


class BaseAromaticModel(BaseModel, metaclass=BaseAromaticMeta):
    key: str = ""

    class Meta:
        collection_name: str = ""