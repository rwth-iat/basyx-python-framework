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

    def _get_submodel_by_id(self, submodel_id):
        submodel = self.obj_store.get(submodel_id)
        if submodel is None:
            raise HTTPException(status_code=404, detail="Submodel with id " + submodel_id + " not found")
        return submodel

    # Endpoint specific logic
    def get_all_submodels_as_jsonables(self)\
            -> list[bool | int | float | str | list[Any] | MutableMapping[str, Any]]:
        return self._jsonable_submodels(self._get_all_submodels())

    def add_submodel_from_body(self, json):
        submodel = jsonization.submodel_from_jsonable(json)
        try:
            self.obj_store.add(submodel)
        except KeyError as e:
            # TODO: Provide a stacktrace
            # Wenn anders in Spezifikation, Stacktrace in server log
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "Submodel processed"}

    def get_submodel_jsonable_by_id(self, submodel_id: str):
        submodel = self._get_submodel_by_id(submodel_id)
        return jsonization.to_jsonable(submodel)

    def update_submode_by_id(self, submodel_id: str, json):
        submodel = self._get_submodel_by_id(submodel_id)
        new_submodel = jsonization.submodel_from_jsonable(json)
        if submodel.id != new_submodel.id:
            raise HTTPException(403, "Submodel with id " + submodel_id + " does not match")
        # TODO: This cant be right
        self.obj_store.discard(submodel)
        self.obj_store.add(new_submodel)
        return jsonization.to_jsonable(new_submodel)

    def delete_submodel_by_id(self, submodel_id):
        submodel = self._get_submodel_by_id(submodel_id)
        self.obj_store.discard(submodel)
        return {"message": "Submodel with id " + submodel_id + " deleted successfully"}

    def get_submodel_elements(self, submodel_id):
        pass

