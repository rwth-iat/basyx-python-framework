from typing import Any

from fastapi import APIRouter


router = APIRouter()

@router.get("/aas")
async def get_all_aas() -> Any:
    return {"message": ""}


@router.get("/aas/{aas_id}")
async def get_aas_by_id(aas_id: str) -> Any:
    return {"message": ""}


@router.post("/aas")
async def create_aas() -> Any:
    return {"message": ""}


@router.delete("/aas/{aas_id}")
async def delete_aas(aas_id: str) -> Any:
    return {"message": ""}
