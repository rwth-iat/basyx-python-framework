from typing import Any, Iterable

from aas_core3.types import Identifiable
from fastapi import APIRouter, Request, HTTPException

from api.server.services.submodel_service import SubmodelService
from api.server.utils.decorator import limited
from sdk.basyx import ObjectStore

from api.server.utils.pagination import Pagination


class SubmodelRouter(Pagination):
    def __init__(self, global_obj_store: ObjectStore[Identifiable]):
        self.router = APIRouter()
        self.obj_store = global_obj_store
        self.service = SubmodelService(global_obj_store)
        self._setup_routes()

    def _setup_routes(self):
        # TODO: Following the swaggerhub documentation this should only return refs (currently not resolvable?)
        # FIXME: Camelcasing?
        @self.router.get("/shells/{aasIdentifier}/submodel-refs")
        @limited()
        async def get_submodel_all(request: Request, aasIdentifier: str) -> Any:
            return self.service.get_all_submodels_as_jsonables(aasIdentifier)

        @self.router.post("/shells/{aasIdentifier}/submodel-refs")
        async def post_submodel(request: Request) -> Any:
            body = await request.json()
            return self.service.add_submodel_from_body(body)

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$metadata")
        async def get_submodel_all_metadata() -> Any:
            # Returns metadata for all submodels, stripped of detailed content
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$reference")
        async def get_submodel_all_reference() -> Any:
            # Returns references for all submodels without full data
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$value")
        async def not_implemented_value() -> Any:
            raise HTTPException(status_code=501, detail="This route is not implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$path")
        async def not_implemented_path() -> Any:
            raise HTTPException(status_code=501, detail="This route is not implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}")
        async def get_submodel(submodel_id: str) -> Any:
            return self.service.get_submodel_jsonable_by_id(submodel_id)

        @self.router.put("/shells/{aasIdentifier}/submodels/{submodelIdentifier}")
        async def put_submodel(submodel_id: str, request: Request) -> Any:
            # Update submodel with given id
            body = await request.json()
            return self.service.update_submodel_by_id(submodel_id, body)

        @self.router.patch("/shells/{aasIdentifier}/submodels/{submodelIdentifier}")
        async def not_implemented_patch_submodel(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not implemented!")

        @self.router.delete("/shells/{aasIdentifier}/submodel-refs")
        async def delete_submodel(submodel_id: str) -> Any:
            return self.service.delete_submodel_by_id(submodel_id)

        # Nested routes for each submodel (PUT/PATCH x $metadata/$value/$reference/$path)
        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$metadata")
        async def get_submodels_metadata(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$metadata")
        async def not_implemented_metadata_patch(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$value")
        async def not_implemented_value_get(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$value")
        async def not_implemented_value_patch(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$reference")
        async def get_submodels_reference(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/$path")
        async def not_implemented_path_get(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements")
        async def get_submodel_submodel_elements(submodel_id: str) -> Any:
            # Get submodel elements
            self.service.get_submodel_elements(submodel_id)

        @self.router.post("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements")
        async def post_submodel_elements(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/$metadata")
        async def get_submodel_submodel_elements_metadata(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/$reference")
        async def get_submodel_submodel_elements_reference(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/$value")
        async def not_implemented_submodel_elements_value(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/$path")
        async def not_implemented_submodel_elements_path(submodel_id: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}")
        async def get_submodel_submodel_elements_id_short_path(submodel_id: str, id_shorts: str) -> Any:
            return self.service.get_submodel_element(submodel_id, id_shorts)

        @self.router.post("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}")
        async def post_submodel_submodel_elements_id_short_path(submodel_id: str, request: Request) -> Any:
            body = await request.json()
            return self.service.post_submodel_element(submodel_id, body)

        @self.router.put("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}")
        async def put_submodel_submodel_elements_id_short_path(submodel_id: str, request: Request) -> Any:
            body = await request.json()
            return self.service.put_submodel_element(submodel_id, body)

        @self.router.patch("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}")
        async def not_implemented_patch_submodel_submodel_elements_id_short_path(submodel_id: str,
                                                                                 id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.delete("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}")
        async def delete_submodel_submodel_elements_id_short_path(submodel_id: str, id_shorts: str) -> Any:
            return self.service.delete_submodel_element(submodel_id, id_shorts)

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$metadata")
        async def get_submodel_submodel_elements_id_short_path_metadata(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$metadata")
        async def not_implemented_metadata_patch(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$reference")
        async def get_submodel_submodel_elements_id_short_path_reference(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value")
        async def not_implemented_value_get(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.patch("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value")
        async def not_implemented_value_patch(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.get("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment")
        async def get_submodel_submodel_element_attachment(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.put("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment")
        async def put_submodel_submodel_element_attachment(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.delete("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment")
        async def delete_submodel_submodel_element_attachment(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/invoke")
        async def not_implemented_invoke(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/invoke/$value")
        async def not_implemented_invoke_value(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/invoke-async")
        async def not_implemented_invoke_async(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        @self.router.post("/shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/invoke-async/$value")
        async def not_implemented_invoke_async_value(submodel_id: str, id_shorts: str) -> Any:
            raise HTTPException(status_code=501, detail="This route is not yet implemented!")

        # FIXME: No updated paths as qualifier endpoints are not present in swaggerhub
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

        # FIXME: Missing based on swaggerhub:
        # - /shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/operation-status/{handleId}
        # - /shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/operation-results/{handleId}
        # - /shells/{aasIdentifier}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/operation-results/{handleId}/$value
