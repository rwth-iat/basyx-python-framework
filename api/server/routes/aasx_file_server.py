from typing import Any

from aas_core3.types import Identifiable
from fastapi import APIRouter, Request, HTTPException

from basyx import ObjectStore
from ..services.aasx_flie_server_service import AasxFileServerService


class AasxFileServerRouter:
    def __init__(self, global_obj_store: ObjectStore[Identifiable]):
        self.router = APIRouter()
        self.obj_store = global_obj_store
        self.service = AasxFileServerService(global_obj_store)
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/")
        async def GetAllAASXPackageIds() -> Any:
            return self.service.GetAllAASXPackageIds()

        @self.router.get("/{aasx_package_id}")
        async def GetAASXByPackageId(aasx_package_id: str) -> Any:
            return self.service.GetAASXByPackageId(aasx_package_id)

        @self.router.post("/")
        async def PostAASXPackage(request: Request) -> Any:
            body = await request.json()
            return self.service.PostAASXPackage(body)

        @self.router.put("/")
        async def PutAASXByPackageId(request: Request) -> Any:
            body = await request.json()
            return self.service.PutAASXByPackageId(body)

        @self.router.delete("/{aasx_package_id}")
        async def DeleteAASXByPackageId(aasx_package_id: str) -> Any:
            return self.service.DeleteAASXByPackageId(aasx_package_id)
        