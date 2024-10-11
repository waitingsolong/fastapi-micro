from fastapi import APIRouter

router = APIRouter()

@router.get("comments/healthcheck")
def healthcheck():
    return {"status": "healthy"}
