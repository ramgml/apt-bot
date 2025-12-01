"""Google OAuth 2.0 service for APT Bot."""
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
from google_auth_oauthlib.flow import Flow

from core.config import settings


class OAuthService:
    """Google OAuth 2.0 service."""

    def __init__(self) -> None:
        """Initialize OAuth service."""
        self.client_id = settings.google.client_id
        self.client_secret = settings.google.client_secret
        self.redirect_uri = settings.google.redirect_uri
        self.scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/gmail.send",
        ]

    def get_authorization_url(self, state: str) -> str:
        """
        Get Google OAuth authorization URL.

        Args:
            state: State parameter for CSRF protection

        Returns:
            Authorization URL
        """
        flow = Flow.from_client_config(
            {
                "installed": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri],
                }
            },
            scopes=self.scopes,
            state=state,
            redirect_uri=self.redirect_uri,
        )
        auth_url, _ = flow.authorization_url(prompt="consent")
        return auth_url

    async def exchange_code_for_token(self, code: str) -> dict[str, Any]:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from Google

        Returns:
            Token data with access_token, refresh_token, expires_at
        """
        flow = Flow.from_client_config(
            {
                "installed": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri],
                }
            },
            scopes=self.scopes,
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials

        return {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(seconds=3600)
                if credentials.expiry is None
                else datetime.fromtimestamp(
                    credentials.expiry, tz=timezone.utc
                )
            ),
        }

    async def get_user_info(self, access_token: str) -> dict[str, Any]:
        """
        Get user info from Google using access token.

        Args:
            access_token: Google access token

        Returns:
            User info (email, name, etc.)
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Google refresh token

        Returns:
            New token data
        """
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data=data,
            )
            response.raise_for_status()
            token_data = response.json()

        return {
            "access_token": token_data["access_token"],
            "refresh_token": refresh_token,
            "expires_at": (
                datetime.now(timezone.utc)
                + timedelta(seconds=token_data.get("expires_in", 3600))
            ),
        }


# Create a singleton instance
oauth_service = OAuthService()
