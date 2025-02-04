from fastapi import APIRouter

router = APIRouter()

@router.get("auth/healthcheck")
def healthcheck():
    return {"status": "healthy"}
