from typing import TypeVar, List, Dict, Any

ModelType = TypeVar("ModelType")


def to_list_dict(objects: List[ModelType]) -> List[dict]:
    new_objects = []
    for obj in objects:
        new_objects.append(
            obj.dict())
    return new_objects
