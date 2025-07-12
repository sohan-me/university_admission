from .models import User, UserProfile
from core.security import get_password_hash, verify_password
import shutil
from pathlib import Path
from tortoise.exceptions import DoesNotExist
from .schemas import *
from fastapi import UploadFile, HTTPException
import uuid





async def upload_file(
    file: UploadFile, 
    file_type: str = "document",
    allowed_types: list = None,
    max_size_mb: int = 5,
    media_dir: str = None
) -> str:
    
    MEDIA_DIR = Path(f'media/{media_dir}/')
    MEDIA_DIR.mkdir(exist_ok=True)
  
    if not file:
        return None
    
    # Default allowed types if not specified
    if allowed_types is None:
        allowed_types = ['image/', 'application/pdf']
    
    # Validate file type
    if not any(file.content_type.startswith(allowed_type) for allowed_type in allowed_types):
        raise HTTPException(
            status_code=400, 
            detail=f"Only {', '.join(allowed_types)} files are allowed"
        )
    
    # Validate file size (convert MB to bytes)
    max_size_bytes = max_size_mb * 1024 * 1024
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=400, 
            detail=f"File size must be less than {max_size_mb}MB"
        )
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    filename = f"{file_type}_{uuid.uuid4()}.{file_extension}"
    file_path = MEDIA_DIR / filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    return str(file_path)


async def get_user_by_username(username: str):
    return await User.get_or_none(username=username)


async def get_user_by_id(id: int):
    return await User.get_or_none(id=id)


async def create_user(username: str, email: str, password: str, is_admin: bool = False):
    user = await User.create(
        username=username,
        email=email,
        password_hash=get_password_hash(password),
        is_admin=is_admin,
        is_verified=False
    )
    return user



async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if user and verify_password(password, user.password_hash):
        return user
    return None




''' User profile CRUD'''




async def get_user_profile(user_id: int):
    user = await User.get_or_none(id=user_id).prefetch_related("profile")
    if not user:
        return None

    # If user exists but has no profile
    if not hasattr(user, "profile") or user.profile is None:
        return None

    return user.profile



async def delete_user_profile(user_id: int):
    try:
        user = await User.get_or_none(id=user_id).prefetch_related('profile')
        if not user:
            return None

        if not hasattr(user, 'profile') or user.profile is None:
            return None
        
        await user.profile.delete()
        return True
    except DoesNotExist:
        return False


async def create_user_profile(user_id: int, profile_data: dict):
    user = await User.get_or_none(id=user_id)
    if not user:
        return None
    
    # Check if profile already exists
    existing_profile = await get_user_profile(user_id)
    if existing_profile:
        return None  # Profile already exists
    
    profile = await UserProfile.create(user=user, **profile_data)
    return profile


async def update_user_profile(user_id: int, profile_data: dict):
    profile = await get_user_profile(user_id)
    if not profile:
        return None
    
    # Update only provided fields
    for field, value in profile_data.items():
        if value is not None:
            setattr(profile, field, value)
    
    await profile.save()
    return profile