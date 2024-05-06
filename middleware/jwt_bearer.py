from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # super() es la función superior que en este caso sería HTTPBearer y tiene un método llamado .__call__() que hace la solicitud de forma asíncrona.
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@admin.com":
            raise HTTPException(status_code=403, detail="credentials invalid")
