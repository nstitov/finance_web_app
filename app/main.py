from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import categories, dashboard, transactions
from app.services.filters import to_datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.state.templates = Jinja2Templates(directory="app/templates")
app.state.templates.env.filters["to_datetime"] = to_datetime


app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "Finance App API"}
