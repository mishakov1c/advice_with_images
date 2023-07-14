import json
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from webapp.constants import BORED_ENDPOINT, UNSPLASH_ENDPOINT
from webapp.config import ACCESS_KEY

app = FastAPI(title='AmuzeMe')
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="webapp/templates")


def get_bored_activity() -> str:
    try:
        response = requests.get(BORED_ENDPOINT).json()
        if response:
            return response.get('activity')
        else:
            raise HTTPException(
                status_code=500,
                detail='Не удалось получить совет.',
            )
    except requests.RequestException:
        raise HTTPException(
            status_code=500,
            detail='Ошибка при выполнении запроса к API Bored.',
        )


def get_unsplash_picture(query: str) -> str:
    try:
        unsplash_url = f'{UNSPLASH_ENDPOINT}?query={query}&client_id={ACCESS_KEY}'
        unsplash_response = requests.get(unsplash_url)
        data = json.loads(unsplash_response.text)

        if 'results' in data and len(data['results']):
            return data['results'][0]['urls']['small']
        else:
            raise HTTPException(
                status_code=500,
                detail='Не удалось получить ссылку на изображение.',
            )
    except requests.RequestException:
        raise HTTPException(
            status_code=500,
            detail='Ошибка при выполнении запроса к API Unsplash.',
        )


@app.get("/", response_class=HTMLResponse)
def get_advice(request: Request):
    try:
        activity = get_bored_activity()
        picture_link = get_unsplash_picture(activity)

        return templates.TemplateResponse(
            'index.html',
            {
                'request': request,
                'activity': activity,
                'picture_link': picture_link
            }
        )
    except HTTPException as exception:
        return {'message': str(exception)}
