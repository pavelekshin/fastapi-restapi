import argparse
import asyncio

from src.auth.schemas import AdminUser
from src.auth.security import hash_password
from src.auth.service import get_user_by_email
from src.database import auth_user, fetch_one


async def create_auth_admin_user(user: AdminUser):
    if await get_user_by_email(user.email):
        raise ValueError(f"User with email {user.email} already exist")

    insert_superuser = (
        auth_user.insert()
        .values(
            {
                "email": user.email,
                "password": hash_password(user.password),
                "is_admin": user.is_admin,
            }
        )
        .returning(auth_user)
    )

    return await fetch_one(insert_superuser)


async def run():
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("--email", "-e", dest="email", type=str)
    parser.add_argument("--password", "-p", dest="password", type=str)
    args = parser.parse_args()

    admin_user = AdminUser(email=args.email, password=args.password)

    if not await create_auth_admin_user(admin_user):
        raise ValueError(f"{admin_user.email} not created!")


asyncio.run(run())
