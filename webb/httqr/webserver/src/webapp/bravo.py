from typing import List,Optional
from pydantic import BaseModel
from fastapi import FastAPI,Request,Response,Cookie
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import random
import base64

TEMPLATE_PATH = os.path.join(os.sep, 'bravo', 'templates')
RESOURCE_PATH = os.path.join(TEMPLATE_PATH, 'resources')

bravoapp = FastAPI() # docs_url=None, redoc_url=None, openapi_url=None)
bravoapp.mount('/resources', StaticFiles(directory=RESOURCE_PATH), name='resources')
templates = Jinja2Templates(directory=TEMPLATE_PATH)


def get_random_image(offset, base=None, imgdir=None):
    if base is None: base = RESOURCE_PATH
    if imgdir is None: imgdir = 'img'
    path = os.path.join(base, imgdir, offset)
    return os.path.join(imgdir, offset, random.choice(next(os.walk(path))[2]))


def to_bool(strval, default=True):
    try:
        strval = strval.strip().lower()
        return {'true': True, 'false': False}[strval]
    except:
        return default


class CakeRequest(BaseModel):
    include_flag : bool


class CakeResponse(BaseModel):
    src1:  str
    title1: str
    src2:  str
    title2: str
    src3:  str
    title3: str


def get_flag_src():
    gif_file = os.path.join(RESOURCE_PATH, get_random_image('flags'))
    with open(gif_file, 'rb') as infile:
        gif_data = infile.read()
    flag_path = os.path.join(os.sep, 'bravo', 'flags')
    flag_file = os.path.join(flag_path, random.choice(next(os.walk(flag_path))[2]))
    with open(flag_file, 'rb') as infile:
        flag_data = infile.read()
    result_data = gif_data + flag_data
    result_b64 = base64.b64encode(result_data).decode('ascii')
    return {'src': 'data:image/gif;base64,%s' % result_b64, 'title': 'Unzip me!'}


def cake_response(imgs):
    resp_lst = []
    for ix in range(0, 9, 3):
        resp_lst.append({
            'src1': imgs[ix]['src'],   'title1': imgs[ix]['title'],
            'src2': imgs[ix+1]['src'], 'title2': imgs[ix+1]['title'],
            'src3': imgs[ix+2]['src'], 'title3': imgs[ix+2]['title']
            })
    return resp_lst


def get_cakes(include_flag):
    offset = 'cakes'
    path = os.path.join(RESOURCE_PATH, 'img', offset)
    files = next(os.walk(path))[2]
    random.shuffle(files)
    files = (9 * files)[:9]
    imgs = [{'src': os.path.join('resources', 'img', offset, f), 'title': 'Eat me!'} for f in files]
    if include_flag:
        imgs[0] = get_flag_src()
    random.shuffle(imgs)
    return cake_response(imgs)


# It is intentional that the this method does not support GET.
# Don't forget to set request header Content-Type: application/json
@bravoapp.post('/cakeview', response_model=List[CakeResponse])
async def cakeview_request(request: Request, response: Response, rq_spec: CakeRequest):
    return get_cakes(rq_spec.include_flag)


@bravoapp.get('/tea')
async def bravo_tea(request: Request, do_redirect: Optional[str] = Cookie(None)):
    if to_bool(do_redirect, True):
        response = RedirectResponse('/doonggul-rae-cha')
        response.set_cookie(key='do_redirect', value='true')
        return response

    imagepath = get_random_image('redirect')
    return templates.TemplateResponse('redirect.html', {
        'request': request,
        'imagepath': imagepath})


@bravoapp.get('/doonggul-rae-cha')
async def bravo_doonggul_rae_cha(request: Request, do_redirect: Optional[str] = Cookie(None)):
    if to_bool(do_redirect, True):
        response = RedirectResponse('/cookies')
        response.set_cookie(key='do_redirect', value='true')
        return response

    imagepath = get_random_image('cakes')
    return templates.TemplateResponse('cakes.html', {
        'request': request,
        'imagepath': imagepath})


@bravoapp.get('/cookies')
async def bravo_cookies(request: Request):
    imagepath = get_random_image('cookies')
    return templates.TemplateResponse('cookies.html', {
        'request': request,
        'imagepath': imagepath})


@bravoapp.get('/{path_name:path}', response_class=HTMLResponse)
async def bravo_beverages(request: Request, path_name: str):
    imagepath = get_random_image('unable')
    return templates.TemplateResponse('unable.html', {
        'request': request,
        'imagepath': imagepath},
        status_code=418)

