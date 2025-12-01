from pydantic import Field, field_validator, HttpUrl
from pydantic_settings import BaseSettings
from typing import List, Optional, Literal


class GoogleOAuthSettings(BaseSettings):
    """Настройки Google OAuth для Gmail API"""

    client_id: str = Field(
        ...,
        min_length=1,
        description="Google OAuth Client ID",
    )
    client_secret: str = Field(
        ...,
        min_length=1,
        description="Google OAuth Client Secret",
    )

    redirect_uri: HttpUrl = Field(
        default=HttpUrl("http://localhost:5050/auth/google/callback"),
        description="Redirect URI",
    )

    # Gmail-specific scopes
    scopes: List[str] = Field(
        default_factory=lambda: [
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
        ],
        description="Gmail OAuth scopes",
    )

    # Gmail API endpoints
    gmail_api_uri: HttpUrl = Field(
        default=HttpUrl("https://gmail.googleapis.com/gmail/v1"),
        description="Gmail API base URL",
    )

    auth_uri: HttpUrl = Field(
        default=HttpUrl("https://accounts.google.com/o/oauth2/auth"),
        description="Authorization endpoint",
    )

    token_uri: HttpUrl = Field(
        default=HttpUrl("https://oauth2.googleapis.com/token"),
        description="Token endpoint",
    )

    userinfo_uri: HttpUrl = Field(
        default=HttpUrl("https://www.googleapis.com/oauth2/v3/userinfo"),
        description="UserInfo endpoint",
    )

    # Дополнительные параметры для Gmail
    access_type: Literal["online", "offline"] = Field(
        default="offline",
        description="Для Gmail лучше 'offline' чтобы получить refresh token",
    )
    include_granted_scopes: bool = Field(
        default=True,
    )
    prompt: Optional[str] = Field(
        default="consent",
        description="Для гарантированного получения refresh token",
    )

    @property
    def auth_url(self) -> str:
        """Генерация URL для авторизации с Gmail scopes"""
        from urllib.parse import urlencode

        params = {
            "client_id": self.client_id,
            "redirect_uri": str(self.redirect_uri),
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "access_type": self.access_type,
            "include_granted_scopes": str(self.include_granted_scopes).lower(),
            "prompt": self.prompt or "consent",
        }

        return f"{self.auth_uri}?{urlencode(params)}"

    @field_validator("scopes")
    def validate_gmail_scopes(cls, v):
        """Валидация что включены необходимые scopes для Gmail"""
        required_scopes = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
        ]

        for scope in required_scopes:
            if scope not in v:
                raise ValueError(f"Обязательный scope отсутствует: {scope}")
        return v

    class Config:
        env_prefix = "GOOGLE_OAUTH_"
        case_sensitive = False
        env_file = ".env"
        extra = "ignore"
