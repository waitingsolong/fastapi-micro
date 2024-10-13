from fastapi import APIRouter

router = APIRouter()

@router.get("users/healthcheck")
def healthcheck():
    return {"status": "healthy"}
