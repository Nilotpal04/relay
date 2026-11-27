from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from relay.models.user import User
from relay.schemas.auth import RegisterRequest
from relay.core.security import hash_password

async def register_user_service(
        session: AsyncSession,
        payload: RegisterRequest
) -> User:
    normalize_email = payload.email.lower()
    normalize_username = payload.username.lower()

    result = await session.execute(
        select(User).where(
            or_(
                User.email == normalize_email,
                User.username == normalize_username
            )
        )
    )
    existing_users = result.scalars().all()

    email_exists = any(user.email == normalize_email for user in existing_users)
    username_exists = any(user.username == normalize_username for user in existing_users)

    if email_exists and username_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email and username are both already taken"
        )
    elif email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    elif username_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )

    hashed_pw = hash_password(payload.password)

    new_user = User(
        name=payload.name,
        username=normalize_username,
        email=normalize_email,
        hashed_password=hashed_pw,
        is_active=True
    )

    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already exists"
        )

    return new_user
