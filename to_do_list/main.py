from fastapi import FastAPI, Request, Response
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


# create session with db for each request
# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         request.state.db = SessionLocal()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()  # session always will be closed
#     return response
