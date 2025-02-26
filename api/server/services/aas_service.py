from typing import List, Type, Any, MutableMapping, Union

from aas_core3 import types, jsonization
from aas_core3.types import AssetAdministrationShell
from aas_core3.types import * # TODO: Remove (test input only)
from fastapi import HTTPException

from sdk.basyx import ObjectStore


class AasService:
    def __init__(self, global_object_store: ObjectStore):
        self.obj_store = global_object_store

    # General helper functions
    def _get_all_shells(self) -> List[Type]:
        return self.obj_store.get_identifiables_by_type(AssetAdministrationShell)

    def _jsonable_shells(self, submodels: list[AssetAdministrationShell]) \
            -> list[bool | int | float | str | list[Any] | MutableMapping[str, Any]]:
        return [jsonization.to_jsonable(submodel) for submodel in submodels]

    # Endpoint specific logic
    def get_all_shells_as_jsonable(self) -> List[Union[bool, int, float, str, List[Any], MutableMapping[str, Any]]]:
        return self._jsonable_shells(self._get_all_shells())

    def add_shell_from_body(self, json):
        shell = jsonization.asset_administration_shell_from_jsonable(json)
        try:
            self.obj_store.add(shell)
        except KeyError as e:
            # TODO: Provide a stacktrace
            # Wenn anders in Spezifikation, Stacktrace in server log
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "Shell processed"}
    
    def add_test_input(self):
        aas = AssetAdministrationShell(id="urn:x-test:aas1",
                                       asset_information=AssetInformation(asset_kind=AssetKind.TYPE))

        some_element = Property(
            id_short="some_property",
            value_type=DataTypeDefXSD.INT,
            value="1984"
        )

        another_element = Blob(
            id_short="some_blob",
            content_type="application/octet-stream",
            value=b'\xDE\xAD\xBE\xEF'
        )

        list_element = Blob(
            id_short="list_1",
            content_type="application/octet-stream",
            value=b'\xDE\xAD\xBE\xEF'
        )

        another_list_element = Blob(
            id_short="list_2",
            content_type="application/octet-stream",
            value=b'\xDE\xAD\xBE\xEF'
        )

        element_list = SubmodelElementList(id_short='ExampleSubmodelList',
                                                     type_value_list_element=AASSubmodelElements.
                                                     SUBMODEL_ELEMENT_LIST,
                                                     value=[list_element, another_list_element])

        submodel1 = Submodel(
            id="urn:x-test:submodel1",
            submodel_elements=[
                some_element,
                another_element,
                element_list
            ]
        )
        submodel2 = Submodel(
            id="urn:x-test:submodel2",
            submodel_elements=[
                some_element
            ]
        )

        self.obj_store.add(aas)
