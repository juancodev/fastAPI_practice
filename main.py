from fastapi import FastAPI
from config.database import engine, Base
from middleware.error_handler import ErrorHandler
from router.movie import movie_router
from router.auth import auth_router
from router.home import home_router

"""
* HTMLResponse = useful for send HTML response to the browser.
* JSONResponse = useful for send JSON response to the client.
* Path = useful for send a limit and offset in params.
* Query = useful for query in route
* Status = useful for all status code.
* HTTPException = useful for send error Message and don't stop the app.
* Request = util para la solicitud que vamos a requerir desde la petición
* jsonable_encoder = nos sirve para convertir la respuesta del modelo de la clase en respuesta json
"""
# instance of The Class FastAPI
app = FastAPI()

# title of my application and docs
app.title = "My app with FastAPI"

# version of my API
# app.version = "0.0.1"

# use middleware in all the app for handle error.
app.add_middleware(ErrorHandler)

# include all routing of our app
app.include_router(home_router)
app.include_router(movie_router)
app.include_router(auth_router)

# create database
Base.metadata.create_all(bind=engine)
