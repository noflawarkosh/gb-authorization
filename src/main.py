from fastapi import FastAPI
from service.router import router

app = FastAPI(title='Authorization service')
app.include_router(router)

