from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

home_router = APIRouter()

home_router.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates(directory="template")


# change tags
@home_router.get("/", tags=["home"], response_class=HTMLResponse)
def home_page(request: Request):
    return template.TemplateResponse(request=request, name="index.html")
