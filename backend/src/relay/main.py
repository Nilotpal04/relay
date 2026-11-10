from fastapi import FastAPI
from relay.api.endpoints import router as endpoints_router

app=FastAPI(title="Relay API", version="1.0.0")
app.include_router(endpoints_router, prefix="/api")

