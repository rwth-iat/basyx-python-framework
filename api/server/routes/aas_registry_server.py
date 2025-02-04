from typing import Any

from aas_core3.types import Identifiable
from fastapi import APIRouter, Request

from api.server.services.aas_registry_server_service import AasRegistryServerService
from sdk.basyx import ObjectStore


class AasRegistryRouter:
    def __init__(self, global_obj_store: ObjectStore[Identifiable]):
        self.router = APIRouter()
        self.obj_store = global_obj_store
        self.service = AasRegistryServerService(global_obj_store)
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/")
        async def GetAllAssetAdministrationShellDescriptors() -> Any:
            return self.service.GetAllAssetAdministrationShellDescriptors()

        @self.router.get("/{aas_descriptor_id}")
        async def GetAssetAdministrationShellDescriptorById(aas_descriptor_id: str) -> Any:
            return self.service.GetAssetAdministrationShellDescriptorById(aas_descriptor_id)

        @self.router.post("/")
        async def PostAssetAdministrationShellDescriptor(request: Request) -> Any:
            body = await request.json()
            return self.service.PostAssetAdministrationShellDescriptor(body)

        @self.router.put("/")
        async def PutAssetAdministrationShellDescriptorById(request: Request) -> Any:
            body = await request.json()
            return self.service.PutAssetAdministrationShellDescriptorById(body)

        @self.router.delete("/{aas_descriptor_id}")
        async def DeleteAssetAdministrationShellDescriptorById(aas_descriptor_id: str) -> Any:
            return self.service.DeleteAssetAdministrationShellDescriptorById(aas_descriptor_id)
