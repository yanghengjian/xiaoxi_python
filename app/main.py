from fastapi import FastAPI
from app.api.v1.endpoints import encode
from app.core.config import settings

app = FastAPI()

app.include_router(encode.router, prefix="/api/v1")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=settings.port)
