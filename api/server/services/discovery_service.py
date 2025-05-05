# services/discovery_service.py
from typing import Any, List, MutableMapping

from aas_core3.types import ConceptDescription
from aas_core3 import jsonization
from basyx import ObjectStore
from server.utils.error_handling import CustomErrorResponse


class DiscoveryService:
    def __init__(self, global_object_store: ObjectStore):
        self.obj_store = global_object_store

    def get_all_aas_identifiers(self) -> List[str]:
        descriptors = self.obj_store.get_identifiables_by_type(ConceptDescription)
        return [desc.id for desc in descriptors]

    def get_endpoints_for_aas(self, aas_id: str) -> List[str]:
        try:
            descriptor = self.obj_store.get_identifiable(aas_id)
        except KeyError as e:
            raise CustomErrorResponse(status_code=404, exception=e)
        return [endpoint.value for endpoint in descriptor.is_case_of[0].keys]

    def register_aas_descriptor(self, json: MutableMapping[str, Any]) -> Any:
        descriptor = jsonization.concept_description_from_jsonable(json)
        try:
            self.obj_store.add(descriptor)
        except KeyError as e:
            raise CustomErrorResponse(status_code=400, exception=e)
        return {"message": "AAS descriptor registered"}

    def delete_aas_descriptor(self, aas_id: str) -> Any:
        try:
            self.obj_store.delete(aas_id)
        except KeyError as e:
            raise CustomErrorResponse(status_code=404, exception=e)
        return {"message": "AAS descriptor deleted"}
