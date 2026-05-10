from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.api import categories, transactions
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.state.templates = Jinja2Templates(directory="app/templates")


app.include_router(categories.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": "Finance App API"}
