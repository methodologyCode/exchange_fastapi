import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder

from utils import get_currencies

app = FastAPI()
templates = Jinja2Templates(directory="templates")
path_to_static = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=path_to_static), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_form_page(request: Request):
    currencies = await get_currencies()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "currencies": currencies
    })


@app.post("/", response_class=HTMLResponse)
async def get_currencies_page(request: Request):
    currencies = await get_currencies()
    form = await request.form()
    result = jsonable_encoder(form)
    from_amount = result["from-amount"]
    from_curr = result["from-curr"]
    to_curr = result["to-curr"]
    converted_amount = round((currencies[to_curr] / currencies[from_curr]) * float(from_amount), 2)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "currencies": currencies,
        'from_curr': from_curr,
        'to_curr': to_curr,
        'from_amount': from_amount,
        'converted_amount': converted_amount
    })

