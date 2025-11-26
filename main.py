from fastapi import FastAPI
from pydantic import BaseModel
from deep_translator import GoogleTranslator

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@app.get("/")
def home():
    return {"message": "AI Video Dub Backend Running 🚀"}

@app.post("/translate")
def translate_text(data: TranslationRequest):
    translated = GoogleTranslator(
        target=data.target_language
    ).translate(data.text)

    return {
        "original": data.text,
        "translated": translated,
        "language": data.target_language
    }
