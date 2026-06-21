from fastapi import APIRouter, Depends

from src.core.security import get_current_user


router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("")
def protected_route(user: dict = Depends(get_current_user)):
    return {
        "message": "Protected route access granted",
        "user": user,
    }
