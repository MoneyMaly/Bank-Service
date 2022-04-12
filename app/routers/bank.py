from fastapi import APIRouter, HTTPException, status, Depends
from app.utils.auth_helper import get_current_user


router = APIRouter()


@router.get("/users/me/items/")
async def read_own_items(username: str = Depends(get_current_user), test="test"):
    return [{"item_id": "Foo", "owner": username}] 