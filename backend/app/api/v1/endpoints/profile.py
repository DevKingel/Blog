from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import get_user_by_id, update_user
from app.db.session import get_session
from app.schemas.profile import ProfileRead, ProfileUpdate

router = APIRouter()


@router.get("/", response_model=ProfileRead)
async def get_current_user_profile(
    user_id: UUID,  # In a real implementation, this would come from the token
    db: AsyncSession = Depends(get_session),
) -> ProfileRead:
    """
    Get current user's profile.
    Note: In a real implementation, the user_id would be extracted from the JWT token.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ProfileRead(**user.__dict__)


@router.put("/", response_model=ProfileRead)
async def update_current_user_profile(
    *,
    user_id: UUID,  # In a real implementation, this would come from the token
    profile_update: ProfileUpdate,
    db: AsyncSession = Depends(get_session),
) -> ProfileRead:
    """
    Update current user's profile.
    Note: In a real implementation, the user_id would be extracted from the JWT token.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Filter out None values
    update_data = profile_update.dict(exclude_unset=True)
    updated_user = await update_user(db, user_id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return ProfileRead(**updated_user.__dict__)
