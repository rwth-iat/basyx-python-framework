from typing import Any

from aas_core3.types import Identifiable
from fastapi import APIRouter, Request

from server.services.submodel_registry_server_service import SubmodelRegistryServerService
from basyx import ObjectStore


class SubmodelRegistryRouter:
    def __init__(self, global_obj_store: ObjectStore[Identifiable]):
        self.router = APIRouter()
        self.obj_store = global_obj_store
        self.service = SubmodelRegistryServerService(global_obj_store)
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/")
        async def GetAllSubmodelDescriptors() -> Any:
            return self.service.GetAllSubmodelDescriptors()

        @self.router.get("/{submodel_id}")
        async def GetSubmodelDescriptorById(submodel_id: str) -> Any:
            return self.service.GetSubmodelDescriptorById(submodel_id)

        @self.router.post("/")
        async def PostSubmodelDescriptor(request: Request) -> Any:
            body = await request.json()
            return self.service.PostSubmodelDescriptor(body)

        @self.router.put("/")
        async def PutSubmodelDescriptorById(request: Request) -> Any:
            body = await request.json()
            return self.service.PutSubmodelDescriptorById(body)

        @self.router.delete("/{submodel_id}")
        async def DeleteSubmodelDescriptorById(submodel_id: str) -> Any:
            return self.service.DeleteSubmodelDescriptorById(submodel_id)
