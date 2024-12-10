from typing import Any, MutableMapping

from aas_core3 import jsonization
from aas_core3.types import Submodel
from fastapi import HTTPException

from sdk.basyx import ObjectStore


class SubmodelService:
    def __init__(self, global_object_store: ObjectStore):
        self.obj_store = global_object_store

    # General helper functions
    def _get_all_submodels(self) -> list[Submodel]:
        return [item for item in self.obj_store if isinstance(item, Submodel)]

    def _jsonable_submodels(self, submodels: list[Submodel]) \
            -> list[bool | int | float | str | list[Any] | MutableMapping[str, Any]]:
        return [jsonization.to_jsonable(submodel) for submodel in submodels]

    # Endpoint specific logic
    def get_all_submodels_as_jsonables(self)\
            -> list[bool | int | float | str | list[Any] | MutableMapping[str, Any]]:
        return self._jsonable_submodels(self._get_all_submodels())

    def add_submodel_from_body(self, json):
        submodel = jsonization.submodel_from_jsonable(json)
        try:
            self.obj_store.add(submodel)
        except KeyError as e:
            # TODO: Provide a stacktrace)
            # Wenn anders in Spezifikation, Stacktrace in server log
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "Submodel processed"}

