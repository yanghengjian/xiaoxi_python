from fastapi import FastAPI
from app.api.text2vec_custom import text2vec_custom as encode
from app.api.weaviate import weaviate as weaviate
from app.core.config import settings

app = FastAPI()

app.include_router(encode.router)
# app.include_router(weaviate.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=1702)
