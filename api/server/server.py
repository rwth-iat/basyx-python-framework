import uvicorn
from fastapi import FastAPI

from api.server.routes import submodel, aasx_file_server, aas_registry_server, submodel_registry_server, aas
from sdk.basyx import object_store

app = FastAPI()
prefix = "/api/v3.0"

central_object_store = object_store.ObjectStore()

aas_router = aas.AasRouter(central_object_store)
submodel_router = submodel.SubmodelRouter(central_object_store)
aasx_file_router = aasx_file_server.AasxFileServerRouter(central_object_store)
aas_registry_router = aas_registry_server.AasRegistryRouter(central_object_store)
submodel_registry_router = submodel_registry_server.SubmodelRegistryRouter(central_object_store)

# Register router
# TODO: This can be done dynamically based on startup params
app.include_router(submodel_router.router, prefix=prefix)
app.include_router(aasx_file_router.router, prefix=prefix)
app.include_router(aas_registry_router.router, prefix=prefix + "/blub")
app.include_router(submodel_registry_router.router, prefix=prefix)
# FIXME: Collision issues
app.include_router(aas_router.router, prefix=prefix + "/test")

# Start the server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
