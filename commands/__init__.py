from users.models import User
from core.security import get_password_hash

async def create_superuser():
    existing_admin = await User.get_or_none(username="admin")
    if existing_admin:
        print("[INFO] Superuser already exists")
        return

    print("[INFO] Creating initial superuser...")
    await User.create(
        username="admin",
        email="admin@example.com",
        password_hash=get_password_hash("adminpassword"),
        is_admin=True
    )
    print("[INFO] Superuser created: username=admin, password=adminpassword")


