from fastapi import FastAPI

from routers.auth import router as auth_router

app = FastAPI(title="IntraShip UAM Practice App", version="0.1.0")
app.include_router(auth_router)