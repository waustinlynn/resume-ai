from uuid import uuid4

from fastapi import APIRouter, status

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_profile():
    return {"id": uuid4()}
