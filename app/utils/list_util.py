from typing import TypeVar, List

ModelType = TypeVar("ModelType")


def to_list_dict(objects: List[ModelType], un_selects: List[str] = None) -> List[dict]:
    new_objects = []
    for obj in objects:
        new_objects.append(
            obj.dict(un_selects=un_selects))
    return new_objects
