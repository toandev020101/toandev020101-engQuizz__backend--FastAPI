from typing import TypeVar, List, Dict, Any

ModelType = TypeVar("ModelType")


def to_list_dict(objects: List[ModelType], un_selects: List[str] = None,
                 relationship_levels: Dict[str, bool] = None) -> List[dict]:
    new_objects = []
    for obj in objects:
        new_objects.append(
            obj.dict(un_selects=un_selects, relationship_levels=relationship_levels))
    return new_objects
