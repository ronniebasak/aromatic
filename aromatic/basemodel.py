from pydantic import BaseModel
from typing import (Tuple, Dict, Any)
from pydantic.main import ModelMetaclass, no_type_check
from pydantic.fields import Field as PDField, FieldInfo as PDFieldInfo
from pprint import pprint


# class BaseAromaticMetaClass(ModelMetaclass):
#     @no_type_check
#     def __new__(mcs, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any], **kwargs):
#         is_custom_cls = namespace.get("__module__") != "aromatic.basemodel" \
#                         and namespace.get('__qualname__') not in ["BaseAromaticModel"]
#
#         if is_custom_cls:
#             patched_bases = []
#             for b in bases:
#                 if hasattr(b, "__pydantic_model__"):
#                     patched_bases.append(b.__pydantic_model__)
#                 else:
#                     patched_bases.append(b)
#             bases = tuple(patched_bases)
#
#             if namespace.get("__doc__", None) is None:
#                 namespace["__doc__"] = ""
#             # print("namespace")
#             # pprint(namespace)
#
#             annotations = namespace["__annotations__"]
#         else:
#             pass
#             # print(namespace)
#
#         cls = super().__new__(mcs, name, bases, namespace, **kwargs)
#         return cls


class BaseAromaticModel(BaseModel):
    id: str = ""
    rev: str = ""
    key: str = ""

    def __init__(self, **kwargs: Any):
        super(BaseAromaticModel, self).__init__(**kwargs)

        for key in kwargs:
            if key == '_id':
                self.id = kwargs[key]
            elif key == '_rev':
                self.rev = kwargs[key]
            elif key == '_key':
                self.key = kwargs[key]


    class Meta:
        collection_name: str = ""