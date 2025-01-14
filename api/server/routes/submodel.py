from typing import Any

from aas_core3.types import Identifiable
from fastapi import APIRouter, Request, HTTPException

from basyx import ObjectStore
from ..services.submodel_service import SubmodelService


class SubmodelRouter:
    def __init__(self, global_obj_store: ObjectStore[Identifiable]):
        self.router = APIRouter()
        self.obj_store = global_obj_store
        self.service = SubmodelService(global_obj_store)
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/")
        async def get_submodel_all() -> Any:
            return self.service.get_all_submodels_as_jsonables()

        @self.router.post("/")
        async def post_submodel(request: Request) -> Any:
            body = await request.json()
            return self.service.add_submodel_from_body(body)

        @self.router.get("/$metadata")
        async def get_submodel_all_metadata() -> Any:
            # Returns metadata for all submodels, stripped of detailed content
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/$reference")
        async def get_submodel_all_reference() -> Any:
            # Returns references for all submodels without full data
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/$value")
        async def not_implemented_value() -> Any:
            raise HTTPException(status_code=501, detail="This route is not implemented!")

        @self.router.get("/$path")
        async def not_implemented_path() -> Any:
            raise HTTPException(status_code=501, detail="This route is not implemented!")

        @self.router.get("/{submodel_id}")
        async def get_submodel(submodel_id: str) -> Any:
            return self.service.get_submodel_jsonable_by_id(submodel_id)

        @self.router.put("/{submodel_id}")
        async def put_submodel(submodel_id: str, request: Request) -> Any:
            # Update submodel with given id
            body = await request.json()
            return self.service.update_submode_by_id(submodel_id, body)

        @self.router.delete("/{submodel_id}")
        async def delete_submodel(submodel_id: str) -> Any:
            return self.service.delete_submodel_by_id(submodel_id)

        @self.router.patch("/{submodel_id}")
        async def not_implemented_patch_submodel(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not implemented!")

        # Nested routes for each submodel
        @self.router.get("/{submodel_id}/$metadata")
        async def get_submodels_metadata(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/{submodel_id}/$metadata")
        async def not_implemented_metadata_patch(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/$value")
        async def not_implemented_value_get(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/{submodel_id}/$value")
        async def not_implemented_value_patch(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is yet implemented!")

        @self.router.get("/{submodel_id}/$reference")
        async def get_submodels_reference(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/$path")
        async def not_implemented_path_get(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements")
        async def get_submodel_submodel_elements(submodel_id: str) -> Any:
            # Get submodel elements
            self.service.get_submodel_elements(submodel_id)

        @self.router.post("/{submodel_id}/submodel-elements")
        async def post_submodel_elements(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/$metadata")
        async def get_submodel_submodel_elements_metadata(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/$reference")
        async def get_submodel_submodel_elements_reference(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/$value")
        async def not_implemented_submodel_elements_value(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/$path")
        async def not_implemented_submodel_elements_path(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/{id_shorts}")
        async def get_submodel_submodel_elements_id_short_path(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/{submodel_id}/submodel-elements/{id_shorts}")
        async def post_submodel_submodel_elements_id_short_path(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.put("/{submodel_id}/submodel-elements/{id_shorts}")
        async def put_submodel_submodel_elements_id_short_path(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.delete("/{submodel_id}/submodel-elements/{id_shorts}")
        async def delete_submodel_submodel_elements_id_short_path(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/{submodel_id}/submodel-elements/{id_shorts}")
        async def not_implemented_patch_submodel_submodel_elements_id_short_path(submodel_id: str,
                                                                                 id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/{id_shorts}/$metadata")
        async def get_submodel_submodel_elements_id_short_path_metadata(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/{submodel_id}/submodel-elements/{id_shorts}/$metadata")
        async def not_implemented_metadata_patch(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/{id_shorts}/$reference")
        async def get_submodel_submodel_elements_id_short_path_reference(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/{id_shorts}/$value")
        async def not_implemented_value_get(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/{submodel_id}/submodel-elements/{id_shorts}/$value")
        async def not_implemented_value_patch(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/{id_shorts}/attachment")
        async def get_submodel_submodel_element_attachment(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.put("/{submodel_id}/submodel-elements/{id_shorts}/attachment")
        async def put_submodel_submodel_element_attachment(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.delete("/{submodel_id}/submodel-elements/{id_shorts}/attachment")
        async def delete_submodel_submodel_element_attachment(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/{submodel_id}/submodel-elements/{id_shorts}/invoke")
        async def not_implemented_invoke(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/{submodel_id}/submodel-elements/{id_shorts}/invoke/$value")
        async def not_implemented_invoke_value(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/{submodel_id}/submodel-elements/{id_shorts}/invoke-async")
        async def not_implemented_invoke_async(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/{submodel_id}/submodel-elements/{id_shorts}/invoke-async/$value")
        async def not_implemented_invoke_async_value(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/{id_shorts}/qualifiers")
        async def get_submodel_submodel_element_qualifiers(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/{submodel_id}/submodel-elements/{id_shorts}/qualifiers")
        async def post_submodel_submodel_element_qualifiers(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}")
        async def get_submodel_submodel_element_qualifiers_specific(submodel_id: str, id_shorts: str,
                                                                    qualifier_type: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.put("/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}")
        async def put_submodel_submodel_element_qualifiers(submodel_id: str, id_shorts: str,
                                                           qualifier_type: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.delete("/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}")
        async def delete_submodel_submodel_element_qualifiers(submodel_id: str, id_shorts: str,
                                                              qualifier_type: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")
