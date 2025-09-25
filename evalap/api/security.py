from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from evalap.api.config import ADMIN_TOKENS, USER_TOKENS

# Security scheme for Bearer tokens
security = HTTPBearer()


async def admin_only(x_evalap_admin: str = Header(default=None)):
    if ADMIN_TOKENS and x_evalap_admin not in ADMIN_TOKENS:
        raise HTTPException(
            status_code=401, detail="Unauthorized: Please contact an admin to perform this request."
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify the bearer token and return the user if valid.
    This function assumes your authentication system already exists.
    """
    if not USER_TOKENS:
        # Allow if no user tokens are given at startup
        return "ok"

    token = credentials.credentials
    try:
        return USER_TOKENS[token]
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
