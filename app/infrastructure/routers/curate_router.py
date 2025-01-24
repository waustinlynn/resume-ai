from fastapi import APIRouter, Body, status

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def get_resume(
    content: str = Body(..., media_type="text/plain"),
) -> str:
    return content
