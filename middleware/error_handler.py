from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

"""
* BaseHTTPMiddleware = Esto nos sirve para manejar los middleware desde una petición.

"""


# Creamos una clase llamada ErrorHandler y hacemos que herede todo lo que tenga BaseHTTPMiddleware
class ErrorHandler(BaseHTTPMiddleware):

    # Se crea una función inicial
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    # Se crea un metodo dispatch para mostrar si hubo una respuesta correcta o un error.
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            # call_next llama al siguiente middleware
            return await call_next(request)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
