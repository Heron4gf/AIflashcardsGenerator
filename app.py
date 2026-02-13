from pydantic import BaseModel, Field, ConfigDict, ValidationError
from openai import OpenAI
from dotenv import load_dotenv
from typing import List
from fastapi import FastAPI
import os
import json
import logging

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
app = FastAPI()

class FlashCard(BaseModel):
    model_config = ConfigDict(extra="forbid") 
    question: str
    answer: str

class FlashcardRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=20)

def read_prompt(file_path: str = "./prompt.md") -> str:
    with open(file_path, "r") as file:
        return file.read()

def generate_flashcard(text: str, max_retries: int = 3) -> FlashCard:
    schema = FlashCard.model_json_schema()
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=os.getenv("MODEL", "gpt-5-nano"),
                messages=[
                    {
                        "role": "system",
                        "content": read_prompt()
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "FlashCard",
                        "schema": schema,
                        "strict": True
                    }
                }
            )
            
            content = response.choices[0].message.content
            return FlashCard.model_validate_json(content)
            
        except (ValidationError, json.JSONDecodeError) as e:
            logger.warning(f"Validazione fallita (tentativo {attempt + 1}/{max_retries}): {e}")
            continue
            
    raise ValueError(f"Impossibile generare una flashcard valida per '{text[:30]}...' dopo {max_retries} tentativi")

@app.post("/generate", response_model=List[FlashCard])
def create_flashcards(payload: FlashcardRequest):
    results = []
    
    for text in payload.texts:
        try:
            flashcard = generate_flashcard(text)
            results.append(flashcard)
        except Exception as e:
            logger.error(f"Errore generazione: {e}")
            continue
    
    return results