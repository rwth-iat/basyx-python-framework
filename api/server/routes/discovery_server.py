# router/discovery_router.py
from typing import Any
from fastapi import APIRouter, Request

from basyx import ObjectStore
from aas_core3.types import AssetAdministrationShell
from server.services.discovery_service import DiscoveryService


class DiscoveryRouter:
    def __init__(self, global_obj_store: ObjectStore[AssetAdministrationShell]):
        self.router = APIRouter()
        self.obj_store = global_obj_store
        self.service = DiscoveryService(global_obj_store)
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/")
        async def get_all_aas_ids() -> Any:
            return self.service.get_all_aas_identifiers()

        @self.router.get("/{aas_id}")
        async def get_aas_endpoints(aas_id: str) -> Any:
            return self.service.get_endpoints_for_aas(aas_id)

        @self.router.post("/")
        async def register_aas_entry(request: Request) -> Any:
            body = await request.json()
            return self.service.register_aas_descriptor(body)

        @self.router.delete("/{aas_id}")
        async def delete_aas_entry(aas_id: str) -> Any:
            return self.service.delete_aas_descriptor(aas_id)