"""mcv OAuth provider for FastMCP.

This module provides a complete mcv OAuth integration that's ready to use
with just a client ID and client secret. It handles all the complexity of
mcv's OAuth flow, token validation, and user management.

Example:
    ```python
    from fastmcp import FastMCP
    from fastmcp.server.auth.providers.mcv import mcvProvider

    # Simple mcv OAuth protection
    auth = mcvProvider(
        client_id="your-mcv-client-id.apps.mcvusercontent.com",
        client_secret="your-mcv-client-secret"
    )

    mcp = FastMCP("My Protected Server", auth=auth)
    ```
"""

from __future__ import annotations

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import httpx
from fastmcp.server.auth import TokenVerifier
from fastmcp.server.auth.auth import AccessToken
from fastmcp.server.auth.oauth_proxy import OAuthProxy
from fastmcp.settings import ENV_FILE
from fastmcp.utilities.auth import parse_scopes
from fastmcp.utilities.logging import get_logger
from fastmcp.utilities.types import NotSet, NotSetT
from key_value.aio.protocols import AsyncKeyValue
from pydantic import AnyHttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.requests import Request

logger = get_logger(__name__)


class mcvProviderSettings(BaseSettings):
    """Settings for mcv OAuth provider."""

    model_config = SettingsConfigDict(
        env_prefix="FASTMCP_SERVER_AUTH_mcv_",
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
    """Complete mcv OAuth provider for FastMCP."""

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
        # FIX 1: Disable consent by default so we can intercept the upstream URL directly
        require_authorization_consent: bool = False,
    ):
        """Initialize mcv OAuth provider."""

        settings = mcvProviderSettings.model_validate(
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
                "client_id is required - set via parameter or FASTMCP_SERVER_AUTH_mcv_CLIENT_ID"
            )
        if not settings.client_secret:
            raise ValueError(
                "client_secret is required - set via parameter or FASTMCP_SERVER_AUTH_mcv_CLIENT_SECRET"
            )

        # Apply defaults
        timeout_seconds_final = settings.timeout_seconds or 10
        allowed_client_redirect_uris_final = settings.allowed_client_redirect_uris

        # Create mcv token verifier
        token_verifier = MCVTokenVerifier(
            timeout_seconds=timeout_seconds_final,
        )

        # Extract secret string from SecretStr
        client_secret_str = (
            settings.client_secret.get_secret_value() if settings.client_secret else ""
        )

        # Allow Claude's OIDC scopes to pass initial validation
        user_scopes = settings.required_scopes or []
        validation_scopes = list(set(user_scopes + ["openid", "email", "profile"]))

        super().__init__(
            upstream_authorization_endpoint="https://www.mycourseville.com/api/oauth/authorize",
            upstream_token_endpoint="https://www.mycourseville.com/api/oauth/access_token",
            upstream_client_id=settings.client_id,
            upstream_client_secret=client_secret_str,
            valid_scopes=validation_scopes,
            token_verifier=token_verifier,
            base_url=settings.base_url,
            redirect_path=settings.redirect_path,
            issuer_url=settings.issuer_url or settings.base_url,
            allowed_client_redirect_uris=allowed_client_redirect_uris_final,
            client_storage=client_storage,
            jwt_signing_key=settings.jwt_signing_key,
            require_authorization_consent=require_authorization_consent,
        )

        logger.debug(
            "Initialized mcv OAuth provider for client %s with scopes: %s",
            settings.client_id,
            validation_scopes,
        )

    async def authorize(self, request: Request, *args, **kwargs) -> str:
        """Intercept the authorize call to force explicit empty scope."""

        url = await super().authorize(request, *args, **kwargs)
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        if "scope" in query_params:
            print(f"DEBUG: Found scopes: {query_params['scope']}")
            del query_params["scope"]
        else:
            print("DEBUG: No scope param found to delete.")

        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed._replace(query=new_query))

        return new_url
