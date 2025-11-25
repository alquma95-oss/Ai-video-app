from fastapi import FastAPI
from pydantic import BaseModel
from googletrans import Translator

app = FastAPI()
translator = Translator()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@app.get("/")
def home():
    return {"message": "Lingua Dub AI Backend Running 🚀"}

@app.post("/translate")
def translate_text(data: TranslationRequest):
    translated = translator.translate(data.text, dest=data.target_language)
    return {
        "original": data.text,
        "translated": translated.text,
        "language": data.target_language
    }
