from typing import Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = (
            await super().__call__(request)
        )

        if not credentials:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code."
            )

        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=403,
                detail="Invalid authentication scheme."
            )

        user_id = self.verify_jwt(credentials.credentials)

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return user_id

    def verify_jwt(self, jwtoken: str):
        try:
            payload = decode_jwt(jwtoken)
            return payload.get("sub")
        except HTTPException:
            return False
