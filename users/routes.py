from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from .schemas import *
from .cruds import *
from core.security import create_access_token
from .dependencies import get_current_user
from typing import List
from .models import User

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate) -> UserResponse:
    existing_user = await authenticate_user(user.username, user.password)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user_obj = await create_user(username=user.username, email=user.email, password=user.password, is_admin=False)
    return user_obj



@router.post("/admin/register", response_model=UserResponse)
async def create_admin(user: UserCreate, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can create new admins")
    
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user_obj = await create_user(
        username=user.username,
        email=user.email,
        password=user.password,
        is_admin=True
    )
    return user_obj


@router.delete('/{id}/')
async def delete_user(id: int, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    
    if current_user.id == id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user.delete()
    return {'status_code': 200, 'success': 'User has been deleted.'}


@router.delete('/admin/{id}/')  # Using DELETE method
async def delete_admin(id: int, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    
    if current_user.id == id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    admin = await User.get_or_none(id=id, is_admin=True)  # Ensure target is admin
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    await admin.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user



@router.get("/agents", response_model=List[UserResponse])
async def agents_list(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Only admins can see agents list')

    agents = await User.filter(is_admin=False).all()
    return agents


@router.get("/agents/{agent_id}", response_model=UserResponse)
async def get_agent(agent_id: int, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    agent = await User.get_or_none(id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent



@router.patch("/agents/{agent_id}", response_model=UserResponse)
async def update_agent(agent_id: int, user_update: UserUpdate, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    
    agent = await User.get_or_none(id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Update fields
    agent.is_verified = user_update.is_verified

    await agent.save()
    return agent



@router.delete("/agents/{agent_id}", status_code=204)
async def delete_agent(agent_id: int, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    
    agent = await User.get_or_none(id=agent_id, is_admin=False)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    await agent.delete()
    return {"detail": "Agent deleted"}




''' User profile routes '''


@router.get("/{user_id}/profile", response_model=UserProfileResponse)
async def read_profile(user_id: int, current_user=Depends(get_current_user)):

    if not current_user:
        raise HTTPException(status_code=403, detail='unauthenticated user!')

    profile = await get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile



@router.delete("/{user_id}/profile")
async def delete_profile(user_id: int, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='only admin can perform this action.')

    success = await delete_user_profile(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="user or profile not found")
    return {"detail": "Profile deleted"}



@router.post("/{user_id}/profile", response_model=UserProfileResponse)
async def create_profile(
    user_id: int,
    profile_data: UserProfileCreate,
    current_user=Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only create your own profile")
    
    created_profile = await create_user_profile(user_id, profile_data.dict())
    
    if not created_profile:
        raise HTTPException(status_code=400, detail="Profile already exists or user not found")
    
    return created_profile


@router.patch("/{user_id}/profile", response_model=UserProfileResponse)
async def update_profile(
    user_id: int,
    profile_data: UserProfileUpdate,
    current_user=Depends(get_current_user)
):

    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only update your own profile")
    
    update_data = profile_data.dict(exclude_unset=True)
    
    # Check if there are any fields to update
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    updated_profile = await update_user_profile(user_id, update_data)
    
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return updated_profile


@router.post("/{user_id}/profile/upload-file", response_model=UserProfileResponse)
async def upload_profile_file(
    user_id: int,
    nid_passport_file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only upload files for your own profile")
    
    # Get existing profile
    profile = await get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Handle file upload
    try:
        file_path = await upload_file(
            file=nid_passport_file,
            file_type="nid_passport",
            allowed_types=['image/', 'application/pdf'],
            max_size_mb=4,
            media_dir='documents'
        )
        
        # Update profile with file path
        profile.nid_passport_file = file_path
        await profile.save(update_fields=['nid_passport_file'])
        
        return profile
    except HTTPException as e:
        raise e


@router.delete("/{user_id}/profile/upload-file", response_model=UserProfileResponse)
async def delete_profile_file(
    user_id: int,
    current_user=Depends(get_current_user)
):
    # Check if user is deleting their own file or is admin
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only delete files for your own profile")
    
    # Get existing profile
    profile = await get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Remove file path
    profile.nid_passport_file = None
    await profile.save()
    
    return profile