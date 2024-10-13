from fastapi import APIRouter

router = APIRouter()

@router.get("matches/healthcheck")
def healthcheck():
    return {"status": "healthy"}
