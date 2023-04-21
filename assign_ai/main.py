from arel import HotReloadMiddleware as HotReload
from db import init_db
from fastapi import FastAPI
from routes import hackathons, submission, users

app = FastAPI()
app.add_middleware(HotReload)

app.include_router(users.router)
app.include_router(hackathons.router)
app.include_router(submission.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def read_root():
    return {"message": "Hackathon Hive!"}
