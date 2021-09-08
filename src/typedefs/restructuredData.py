from typing import List,TypedDict

class IRestructuredObj(TypedDict):
    columnNo: int
    data: List[float]

class IRestructuredObjList(TypedDict):
    restructuredObjList : List[IRestructuredObj]

