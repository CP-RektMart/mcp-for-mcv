"""Google OAuth provider for FastMCP.

This module provides a complete Google OAuth integration that's ready to use
with just a client ID and client secret. It handles all the complexity of
Google's OAuth flow, token validation, and user management.

Example:
    ```python
    from fastmcp import FastMCP
    from fastmcp.server.auth.providers.google import GoogleProvider

    # Simple Google OAuth protection
    auth = GoogleProvider(
        client_id="your-google-client-id.apps.googleusercontent.com",
        client_secret="your-google-client-secret"
    )

    mcp = FastMCP("My Protected Server", auth=auth)
    ```
"""

from __future__ import annotations

import time

import httpx
from key_value.aio.protocols import AsyncKeyValue
from pydantic import AnyHttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastmcp.server.auth import TokenVerifier
from fastmcp.server.auth.auth import AccessToken
from fastmcp.server.auth.oauth_proxy import OAuthProxy
from fastmcp.settings import ENV_FILE
from fastmcp.utilities.auth import parse_scopes
from fastmcp.utilities.logging import get_logger
from fastmcp.utilities.types import NotSet, NotSetT
from dataclasses import dataclass

logger = get_logger(__name__)

class GoogleProviderSettings(BaseSettings):
    """Settings for Google OAuth provider."""

    model_config = SettingsConfigDict(
        env_prefix="FASTMCP_SERVER_AUTH_GOOGLE_",
        env_file=ENV_FILE,
        extra="ignore",
    )

    client_id: str | None = None
    client_secret: SecretStr | None = None
    base_url: AnyHttpUrl | str | None = None
    issuer_url: AnyHttpUrl | str | None = None
    redirect_path: str | None = None
    required_scopes: list[str] | None = None
    timeout_seconds: int | None = None
    allowed_client_redirect_uris: list[str] | None = None
    jwt_signing_key: str | None = None

    @field_validator("required_scopes", mode="before")
    @classmethod
    def _parse_scopes(cls, v):
        return parse_scopes(v)


class MCVTokenVerifier(TokenVerifier):
    """Token verifier for MyCourseVille OAuth tokens."""

    def __init__(
        self,
        *,
        required_scopes: list[str] | None = None,
        timeout_seconds: int = 10,
    ):
        super().__init__(required_scopes=required_scopes)
        self.timeout_seconds = timeout_seconds

    async def verify_token(self, token: str) -> AccessToken | None:
        """Verify MyCourseVille OAuth token by calling the /users/me endpoint."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                logger.debug("Verifying MyCourseVille token")

                response = await client.get(
                    "https://www.mycourseville.com/api/v1/public/users/me",
                    headers={"Authorization": f"Bearer {token}"},
                )

                if response.status_code != 200:
                    logger.debug(
                        "MyCourseVille token verification failed: %d",
                        response.status_code,
                    )
                    return None

                token_info = response.json()
                user = token_info.get("user", {})

                # Construct AccessToken directly from JSON
                access_token = AccessToken(
                    token=token,
                    client_id="mycourseville",
                    scopes=[],
                    expires_at=None,
                    claims={
                        "id": user.get("id"),
                        "firstname_en": user.get("firstname_en"),
                        "lastname_en": user.get("lastname_en"),
                        "firstname_th": user.get("firstname_th"),
                        "lastname_th": user.get("lastname_th"),
                        "provider": "MyCourseVille",
                    },
                )

                logger.debug("MyCourseVille token verified successfully")
                return access_token

        except httpx.RequestError as e:
            logger.debug("Failed to verify MyCourseVille token: %s", e)
            return None
        except Exception as e:
            logger.debug("MyCourseVille token verification error: %s", e)
            return None


class MCVProvider(OAuthProxy):
    """Complete Google OAuth provider for FastMCP.

    This provider makes it trivial to add Google OAuth protection to any
    FastMCP server. Just provide your Google OAuth app credentials and
    a base URL, and you're ready to go.

    Features:
    - Transparent OAuth proxy to Google
    - Automatic token validation via Google's tokeninfo API
    - User information extraction from Google APIs
    - Minimal configuration required

    Example:
        ```python
        from fastmcp import FastMCP
        from fastmcp.server.auth.providers.google import GoogleProvider

        auth = GoogleProvider(
            client_id="123456789.apps.googleusercontent.com",
            client_secret="GOCSPX-abc123...",
            base_url="https://my-server.com"
        )

        mcp = FastMCP("My App", auth=auth)
        ```
    """

    def __init__(
        self,
        *,
        client_id: str | NotSetT = NotSet,
        client_secret: str | NotSetT = NotSet,
        base_url: AnyHttpUrl | str | NotSetT = NotSet,
        issuer_url: AnyHttpUrl | str | NotSetT = NotSet,
        redirect_path: str | NotSetT = NotSet,
        required_scopes: list[str] | NotSetT = NotSet,
        timeout_seconds: int | NotSetT = NotSet,
        allowed_client_redirect_uris: list[str] | NotSetT = NotSet,
        client_storage: AsyncKeyValue | None = None,
        jwt_signing_key: str | bytes | NotSetT = NotSet,
        require_authorization_consent: bool = True,
    ):
        """Initialize Google OAuth provider.

        Args:
            client_id: Google OAuth client ID (e.g., "123456789.apps.googleusercontent.com")
            client_secret: Google OAuth client secret (e.g., "GOCSPX-abc123...")
            base_url: Public URL where OAuth endpoints will be accessible (includes any mount path)
            issuer_url: Issuer URL for OAuth metadata (defaults to base_url). Use root-level URL
                to avoid 404s during discovery when mounting under a path.
            redirect_path: Redirect path configured in Google OAuth app (defaults to "/auth/callback")

            timeout_seconds: HTTP request timeout for Google API calls
            allowed_client_redirect_uris: List of allowed redirect URI patterns for MCP clients.
                If None (default), all URIs are allowed. If empty list, no URIs are allowed.
            client_storage: Storage backend for OAuth state (client registrations, encrypted tokens).
                If None, a DiskStore will be created in the data directory (derived from `platformdirs`). The
                disk store will be encrypted using a key derived from the JWT Signing Key.
            jwt_signing_key: Secret for signing FastMCP JWT tokens (any string or bytes). If bytes are provided,
                they will be used as is. If a string is provided, it will be derived into a 32-byte key. If not
                provided, the upstream client secret will be used to derive a 32-byte key using PBKDF2.
            require_authorization_consent: Whether to require user consent before authorizing clients (default True).
                When True, users see a consent screen before being redirected to Google.
                When False, authorization proceeds directly without user confirmation.
                SECURITY WARNING: Only disable for local development or testing environments.
        """

        settings = GoogleProviderSettings.model_validate(
            {
                k: v
                for k, v in {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "base_url": base_url,
                    "issuer_url": issuer_url,
                    "redirect_path": redirect_path,
                    "required_scopes": required_scopes,
                    "timeout_seconds": timeout_seconds,
                    "allowed_client_redirect_uris": allowed_client_redirect_uris,
                    "jwt_signing_key": jwt_signing_key,
                }.items()
                if v is not NotSet
            }
        )

        # Validate required settings
        if not settings.client_id:
            raise ValueError(
                "client_id is required - set via parameter or FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID"
            )
        if not settings.client_secret:
            raise ValueError(
                "client_secret is required - set via parameter or FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET"
            )

        # Apply defaults
        timeout_seconds_final = settings.timeout_seconds or 10

        allowed_client_redirect_uris_final = settings.allowed_client_redirect_uris

        # Create Google token verifier
        token_verifier = MCVTokenVerifier(
            timeout_seconds=timeout_seconds_final,
        )

        # Extract secret string from SecretStr
        client_secret_str = (
            settings.client_secret.get_secret_value() if settings.client_secret else ""
        )

        # Initialize OAuth proxy with Google endpoints
        super().__init__(
            upstream_authorization_endpoint="https://www.mycourseville.com/api/oauth/authorize",
            upstream_token_endpoint="https://www.mycourseville.com/api/oauth/access_token",
            upstream_client_id=settings.client_id,
            upstream_client_secret=client_secret_str,
            token_verifier=token_verifier,
            base_url=settings.base_url,
            redirect_path=settings.redirect_path,
            issuer_url=settings.issuer_url
            or settings.base_url,  # Default to base_url if not specified
            allowed_client_redirect_uris=allowed_client_redirect_uris_final,
            client_storage=client_storage,
            jwt_signing_key=settings.jwt_signing_key,
            require_authorization_consent=require_authorization_consent,
        )

        logger.debug(
            "Initialized Google OAuth provider for client %s with scopes: %s",
            settings.client_id,
        )
