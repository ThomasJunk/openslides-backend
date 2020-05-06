from typing import Any, Dict, List, Union

Filter = Union["And", "Or", "Not", "FilterOperator"]


class FilterOperator:
    def __init__(self, field: str, value: Any, operator: str) -> None:
        self.field = field
        self.value = value
        self.operator = operator

    def to_dict(self) -> Dict[str, Any]:
        return {"field": self.field, "value": self.value, "operator": self.operator}


class And:
    def __init__(self, value: List[Filter]) -> None:
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        raise


class Or:
    def __init__(self, value: List[Filter]) -> None:
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        raise


class Not:
    def __init__(self, value: Filter) -> None:
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        raise
