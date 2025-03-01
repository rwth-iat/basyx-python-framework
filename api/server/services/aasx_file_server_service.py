from typing import Any, MutableMapping, List, Union

from aas_core3.types import AssetAdministrationShell
from aas_core3 import jsonization
from fastapi import HTTPException

from basyx import ObjectStore


class AasxFileServerService:
    def __init__(self, global_object_store: ObjectStore):
        self.obj_store = global_object_store

    def get_all_aasx_package_ids(self) -> list[str]:
        return [item.id for item in self.obj_store if isinstance(item, AssetAdministrationShell)]

    def get_aasx_by_package_id(self, package_id) \
            -> list[bool | int | float | str | list[Any] | MutableMapping[str, Any]]:
        aasx_package = self.obj_store.get_identifiable(package_id)
        assert isinstance(aasx_package, AssetAdministrationShell)
        return jsonization.to_jsonable(aasx_package)

    def post_aasx_package(self, json):
        aasx_package = jsonization.asset_administration_shell_from_jsonable(json)
        try:
            self.obj_store.add(aasx_package)
        except KeyError as e:
            # TODO: Provide a stacktrace
            # Wenn anders in Spezifikation, Stacktrace in server log
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "AASX package processed"}

    def put_aasx_by_package_id(self, json):
        aasx_package = jsonization.asset_administration_shell_from_jsonable(json)
        try:
            self.obj_store.delete(aasx_package.id)  # should there be an exception if there is no aasx_package to
            # update?
            self.obj_store.add(aasx_package)
        except KeyError as e:
            # TODO: Provide a stacktrace
            # Wenn anders in Spezifikation, Stacktrace in server log
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "AASX package updated"}

    def delete_aasx_by_package_id(self, package_id):
        try:
            self.obj_store.delete(package_id)  # should there be an exception if there is no aasx_package to delete?
        except KeyError as e:
            # TODO: Provide a stacktrace
            # Wenn anders in Spezifikation, Stacktrace in server log
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "AASX package deleted"}
