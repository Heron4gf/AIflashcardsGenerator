from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from typing import List
from fastapi import FastAPI, HTTPException
import os

load_dotenv()

client = OpenAI()
app = FastAPI()

class FlashCard(BaseModel):
    question: str
    answer: str
    points: int

class FlashcardRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=20)

def read_prompt(file_path: str = "./prompt.md") -> str:
    with open(file_path, "r") as file:
        return file.read()

def generate_flashcard(text: str) -> FlashCard:
    response = client.responses.parse(
        model = os.getenv("OPENAI_MODEL", "gpt-5-nano"),
        input = [
            {
                "role": "system",
                "content": read_prompt()
            },
            {
                "role": "user",
                "content": text
            }
        ],
        text_format = FlashCard
    )
    return response.output_parsed

@app.post("/generate", response_model=List[FlashCard])
def create_flashcards(payload: FlashcardRequest):
    try:
        results = [generate_flashcard(text) for text in payload.texts]
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))