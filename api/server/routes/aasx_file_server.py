from typing import Any

from aas_core3.types import Identifiable
from fastapi import APIRouter, Request, HTTPException

from basyx import ObjectStore
from services.aasx_flie_server_service import AasxFileServerService


class AasxFileServerRouter:
    def __init__(self, global_obj_store: ObjectStore[Identifiable]):
        self.router = APIRouter()
        self.obj_store = global_obj_store
        self.service = AasxFileServerService(global_obj_store)
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/")
        async def get_submodel_all() -> Any:
            return self.service.dummy()
