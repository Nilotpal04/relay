from fastapi import FastAPI
from relay.api.endpoints import router as endpoints_router
from relay.api.webhooks import router as webhooks_router
from relay.api.requests import router as requests_router
from relay.api.websocket import router as websocket_router

app=FastAPI(title="Relay API", version="1.0.0")

app.include_router(endpoints_router, prefix="/api")
app.include_router(webhooks_router, prefix="/api")
app.include_router(requests_router, prefix="/api")
app.include_router(websocket_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

