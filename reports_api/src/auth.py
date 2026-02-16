import jwt
from jwt import InvalidTokenError, PyJWKClient
from litestar import Request
from litestar.exceptions import HTTPException

from .config import KeycloakConfig


def get_jwks_client(config: KeycloakConfig) -> PyJWKClient:
    return PyJWKClient(config.jwks_url)


def extract_user_id(request: Request, config: KeycloakConfig) -> str:
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = auth_header.replace("Bearer ", "", 1).strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty Bearer token")

    try:
        signing_key = get_jwks_client(config).get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False, "verify_iss": False},
        )
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc

    user_id = payload.get(config.user_claim)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail=f"Token has no '{config.user_claim}' claim",
        )
    return str(user_id)
