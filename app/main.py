from fastapi import FastAPI
from app.api.text2vec_custom import text2vec_custom as encode
from app.api.weaviate import weaviate as weaviate
from app.api.chat import knowledge_ik_index_controller as knowledge_ik_index_controller
from app.core.config import settings

app = FastAPI()

app.include_router(encode.router)
app.include_router(weaviate.router)
app.include_router(knowledge_ik_index_controller.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=settings["port"])
