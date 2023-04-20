from routes import users,hackathons
from fastapi import FastAPI
from db import init_db
from arel import HotReloadMiddleware as HotReload

app = FastAPI()
app.add_middleware(HotReload)

app.include_router(users.router)
app.include_router(hackathons.router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"Hello": "World!"}



