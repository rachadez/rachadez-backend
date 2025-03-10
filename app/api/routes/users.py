from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_users() -> list[dict]:
    return [{"username": "Rick"}, {"username": "Morty"}]
