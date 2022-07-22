from fastapi import FastAPI
from .db import Base
from .views import router

app = FastAPI()

app.include_router(router=router, prefix='/todo')


@app.on_event("startup")
async def startup():
    await Base.connect()


@app.on_event("shutdown")
async def shutdown():
    await Base.disconnect()
