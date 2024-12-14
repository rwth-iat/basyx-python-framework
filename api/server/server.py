from fastapi import FastAPI
import uvicorn

# Import routers
from routes import submodel, aasx_file_server

from sdk.basyx import object_store

app = FastAPI()
prefix = "/api/v3.0"

central_object_store = object_store.ObjectStore()

submodel_router = submodel.SubmodelRouter(central_object_store)
aasx_file_router = aasx_file_server.AasxFileServerRouter(central_object_store)

# Register router
# TODO: This can be done dynamically based on startup params
app.include_router(submodel_router.router, prefix=prefix + "/submodels")
app.include_router(aasx_file_router.router, prefix=prefix + "/aasx")

# Start the server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
