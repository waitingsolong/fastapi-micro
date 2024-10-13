from fastapi import APIRouter

router = APIRouter()

@router.get("media/healthcheck")
def healthcheck():
    return {"status": "healthy"}
