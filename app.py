from pydantic import BaseModel, Field, ConfigDict, ValidationError
from openai import AsyncOpenAI
from dotenv import load_dotenv
from typing import List
from fastapi import FastAPI
import os
import json
import logging
import asyncio

load_dotenv()

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
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

def _read_prompt(file_path: str = "./prompt.md") -> str:
    with open(file_path, "r") as file:
        return file.read()

async def _generate_flashcard_async(text: str, max_retries: int = 3) -> FlashCard:
    schema = FlashCard.model_json_schema()
    
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model=os.getenv("MODEL", "gpt-3.5-turbo"),
                messages=[
                    {
                        "role": "system",
                        "content": _read_prompt()
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
            logger.warning(f"Tentativo {attempt + 1}/{max_retries} fallito: {e}")
            continue
        except Exception as e:
             logger.error(f"Errore generico tentativo {attempt + 1}: {e}")
             continue
            
    raise ValueError(f"Fallimento generazione per: {text[:20]}...")

async def _process_batch(texts: List[str]) -> List[FlashCard]:
    tasks = [_generate_flashcard_async(text) for text in texts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    valid_flashcards = []
    for result in results:
        if isinstance(result, FlashCard):
            valid_flashcards.append(result)
        else:
            logger.error(f"Errore nel task: {result}")
    return valid_flashcards

@app.post("/generate", response_model=List[FlashCard])
def create_flashcards(payload: FlashcardRequest):
    return asyncio.run(_process_batch(payload.texts))