# callback from google oAuth2
import base64
import json
import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Response, Request

from api.dependencies import DbSession
from services.oauth_service import oauth_service
from utils.jwt_utils import generate_jwt_token
from repositories.user import UserRepository
from repositories.auth_token import AuthTokenRepository
from repositories.refresh_token import RefreshTokenRepository

log = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google/login")
async def google_login(telegram_user_id: str):
    state = base64.urlsafe_b64encode(json.dumps(telegram_user_id).encode()).decode()

    auth_url = oauth_service.get_authorization_url(state)
    log.info("Redirect URL: {}".format(oauth_service.redirect_uri))

    return {
        "auth_url": auth_url,
    }


@router.get("/google/callback")
async def callback(code: str, state: str, response: Response, db: DbSession):
    try:
        telegram_user_id = json.loads(base64.urlsafe_b64decode(state).decode())
    except Exception as e:
        log.error(e)
        return {"error": "Invalid state"}
    try:
        token_data = await oauth_service.exchange_code_for_token(code)

        user_info = await oauth_service.get_user_info(token_data["access_token"])

        # Generate JWT token
        jwt_token = generate_jwt_token(telegram_user_id, user_info["email"])

        # Save tokens to database
        auth_token_repo = AuthTokenRepository(db)
        refresh_token_repo = RefreshTokenRepository(db)

        # Save access token
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        await auth_token_repo.create_auth_token(
            user_id=telegram_user_id,
            access_token=token_data["access_token"],
            expires_at=expires_at,
        )

        # Save refresh token
        refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        await refresh_token_repo.create_refresh_token(
            user_id=telegram_user_id,
            token=token_data["refresh_token"],
            expires_at=refresh_expires_at,
        )

        # Set refresh token in secure cookie
        response.set_cookie(
            key="refresh_token",
            value=token_data["refresh_token"],
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=30 * 24 * 60 * 60,  # 30 days
        )

        return {
            "access_token": token_data["access_token"],
            "expires_at": token_data["expires_at"],
            "jwt_token": jwt_token,
            "user_info": user_info,
        }
    except Exception as e:
        log.error(e)
        return {"error": "Invalid code"}


@router.post("/refresh")
async def refresh_token(request: Request, response: Response, db: DbSession):
    # Get refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return {"error": "Refresh token not found"}

    # Get user by refresh token
    refresh_token_repo = RefreshTokenRepository(db)
    refresh_token_obj = await refresh_token_repo.get_by_token(refresh_token)
    if not refresh_token_obj:
        return {"error": "Invalid refresh token"}

    # Check if refresh token is expired
    if refresh_token_obj.expires_at < datetime.now(timezone.utc):
        await refresh_token_repo.delete_by_user_id(refresh_token_obj.user_id)
        return {"error": "Refresh token expired"}

    # Refresh access token
    token_data = await oauth_service.refresh_token(refresh_token)

    # Update tokens in database
    user_id = refresh_token_obj.user_id
    auth_token_repo = AuthTokenRepository(db)
    refresh_token_repo = RefreshTokenRepository(db)

    # Update access token
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    await auth_token_repo.update_auth_token(
        user_id=user_id, access_token=token_data["access_token"], expires_at=expires_at
    )

    # Update refresh token
    refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    await refresh_token_repo.update_refresh_token(
        user_id=user_id,
        token=token_data["refresh_token"],
        expires_at=refresh_expires_at,
    )

    # Generate new JWT token
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if user is None:
        return {"error": "User not found"}
    jwt_token = generate_jwt_token(user_id, user.email)

    # Set new refresh token in secure cookie
    response.set_cookie(
        key="refresh_token",
        value=token_data["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=30 * 24 * 60 * 60,  # 30 days
    )

    return {
        "access_token": token_data["access_token"],
        "expires_at": token_data["expires_at"],
        "jwt_token": jwt_token,
    }
