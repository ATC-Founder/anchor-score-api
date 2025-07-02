from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AnchorScore API is live!"}

@app.get("/healthz")
def health_check():
    return JSONResponse(content={"status": "ok"})
