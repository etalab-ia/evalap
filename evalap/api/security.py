from fastapi import Header, HTTPException

from evalap.api.config import ADMIN_TOKENS


async def admin_only(x_eg1_admin: str = Header(default=None)):
    if ADMIN_TOKENS and x_eg1_admin not in ADMIN_TOKENS:
        raise HTTPException(status_code=401, detail="Unauthorized: Please contact an admin to perform this request.")
