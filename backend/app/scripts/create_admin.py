import argparse
import asyncio

from sqlalchemy import select

from app.db import async_session_factory
from app.models.user import User, UserRole
from app.security import hash_password


async def create_admin(email: str, password: str) -> None:
    async with async_session_factory() as db:
        existing = await db.execute(select(User).where(User.email == email))
        if existing.scalar_one_or_none() is not None:
            print(f"User {email} already exists")
            return

        db.add(
            User(
                email=email,
                hashed_password=hash_password(password),
                role=UserRole.ADMIN.value,
            )
        )
        await db.commit()
        print(f"Created admin user {email}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an admin user")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()
    asyncio.run(create_admin(args.email, args.password))


if __name__ == "__main__":
    main()
