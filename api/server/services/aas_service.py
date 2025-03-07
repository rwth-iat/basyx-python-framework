from typing import List, Type, Any, MutableMapping, Union

from aas_core3 import types, jsonization
from aas_core3.types import AssetAdministrationShell
from fastapi import HTTPException

from basyx import ObjectStore


class AasService:
    def __init__(self, global_object_store: ObjectStore):
        self.obj_store = global_object_store

    # General helper functions
    def _get_all_shells(self) -> List[Type]:
        # FIXME: Type issues. Should this be casted to List[AAS]?
        return self.obj_store.get_identifiables_by_type(AssetAdministrationShell)

    def _get_shell_by_id(self, aas_identifier) -> AssetAdministrationShell:
        shell = self.obj_store.get(aas_identifier)
        if shell is None or not isinstance(shell, AssetAdministrationShell):
            raise HTTPException(status_code=404, detail="Submodel with id " + aas_identifier + " not found")
        return shell

    def _jsonable_shells(self, submodels: List[AssetAdministrationShell]) \
            -> List[Union[bool, int, float, str, List[Any], MutableMapping[str, Any]]]:
        return [jsonization.to_jsonable(submodel) for submodel in submodels]

    # Endpoint specific logic
    def get_all_shells_as_jsonable(self) -> List[Union[bool, int, float, str, List[Any], MutableMapping[str, Any]]]:
        return self._jsonable_shells(self._get_all_shells())

    def get_shell_jsonable_by_id(self, aas_identifier):
        shell = self._get_shell_by_id(aas_identifier)
        return jsonization.to_jsonable(shell)

    def add_shell_from_body(self, json):
        shell = jsonization.asset_administration_shell_from_jsonable(json)
        try:
            self.obj_store.add(shell)
        except KeyError as e:
            # TODO: Provide a stacktrace
            # Wenn anders in Spezifikation, Stacktrace in server log
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "Shell processed"}

    def delete_shell_by_id(self, aas_identifier):
        shell = self._get_shell_by_id(aas_identifier)
        self.obj_store.discard(shell)
        return {"message": "AssetAdministrationShell with id " + aas_identifier + " deleted successfully"}
