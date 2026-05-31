from fastapi import FastAPI
from app.routers import webhooks

app = FastAPI(title="API Connector Service")

app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])

@app.get("/")
def health_check():
    return {"status": "ok"}
