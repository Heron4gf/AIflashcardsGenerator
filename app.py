from pydantic import BaseModel, Field, ConfigDict, ValidationError
from openai import OpenAI
from dotenv import load_dotenv
from typing import List
from fastapi import FastAPI, HTTPException
import os
import json
import logging

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
app = FastAPI()


class FlashCard(BaseModel):
    model_config = ConfigDict(extra="forbid") 
    
    question: str
    answer: str
    points: int


class FlashcardRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=20)


def read_prompt(file_path: str = "./prompt.md") -> str:
    with open(file_path, "r") as file:
        return file.read()


def generate_flashcard(text: str) -> FlashCard:
    schema = FlashCard.model_json_schema()
    
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "gpt-oss-20b"),
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


@app.post("/generate", response_model=List[FlashCard])
def create_flashcards(payload: FlashcardRequest):
    results = []
    
    for text in payload.texts:
        try:
            flashcard = generate_flashcard(text)
            results.append(flashcard)
        except (ValidationError, json.JSONDecodeError) as e:
            # Flashcard non valida: logga e continua
            logger.warning(f"Flashcard scartata per testo: '{text[:50]}...' - Errore: {e}")
            continue
        except Exception as e:
            # Per altri errori (es. API down), puoi decidere se saltare o propagare
            logger.error(f"Errore imprevisto per testo: '{text[:50]}...' - {e}")
            continue
    
    return results
