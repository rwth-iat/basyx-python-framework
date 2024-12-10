from fastapi import FastAPI
import uvicorn
from pygments.lexers import q

# Import routers
from api import submodel

from sdk.basyx import object_store

app = FastAPI()
prefix = "/api/v3.0"

central_object_store = object_store.ObjectStore()

submodel_router = submodel.SubmodelRouter(central_object_store)

# Register router
# TODO: This can be done dynamically based on startup params
app.include_router(submodel_router.router, prefix=prefix + "/submodels")

# Start the server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
