from fastapi import APIRouter

router = APIRouter()

@router.get("news/healthcheck")
def healthcheck():
    return {"status": "healthy"}
