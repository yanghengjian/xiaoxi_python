from sentence_transformers import SentenceTransformer
from app.core.config import settings

class Vectorizer:
    def __init__(self):
        self.model = SentenceTransformer(settings['model_path'])

    def encode(self, text: str):
        encoded_vector = self.model.encode([text], normalize_embeddings=True, convert_to_tensor=False)[0]
        return encoded_vector

vectorizer = Vectorizer()
