from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import random

TEMPLATE_PATH = os.path.join(os.sep, 'alpha', 'templates')
RESOURCE_PATH = os.path.join(TEMPLATE_PATH, 'resources')

alphaapp = FastAPI() # docs_url=None, redoc_url=None, openapi_url=None)
alphaapp.mount('/resources', StaticFiles(directory=RESOURCE_PATH), name='resources')
templates = Jinja2Templates(directory=TEMPLATE_PATH)

def get_random_image(offset):
    path = os.path.join(RESOURCE_PATH, 'img', offset)
    return os.path.join('img', offset, random.choice(next(os.walk(path))[2]))

@alphaapp.get('/', response_class=HTMLResponse)
async def root_get(request: Request):
    imagepath = get_random_image('other')
    return templates.TemplateResponse('notofinterest.html', {
        'request': request,
        'imagepath': imagepath})

@alphaapp.get('/{path_name:path}', response_class=RedirectResponse)
async def catch_all(request: Request, path_name: str):
    return RedirectResponse('/')

