from fastapi import APIRouter


router = APIRouter(tags=["example"])

@router.get("/")
def hello_world():
    return { "msg": "Hello World" }
