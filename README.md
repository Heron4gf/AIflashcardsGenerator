# AI Flashcards Generator

Containerized microservice based on FastAPI and OpenAI to automatically generate flashcards from input texts.

## Installation

### 1. Clone the repository
```bash
git clone [https://github.com/Heron4gf/AIflashcardsGenerator](https://github.com/Heron4gf/AIflashcardsGenerator)
cd AIflashcardsGenerator

```

### 2. Build the Docker image
```bash
docker build -t flashcard-generator .
```

### 3. Run the container
You must pass your OpenAI API key and the desired model as environment variables.

```bash
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY="sk-..." \
  -e OPENAI_MODEL="gpt-4o" \
  flashcard-generator

```

## API Documentation
### `POST /generate` Endpoint

Generates a list of flashcards based on the provided texts.

**URL:** `http://localhost:8000/generate`
**Content-Type:** `application/json`

**Request Body:**

```json
{
  "texts": [
    "Text for flashcard 1",
    "Text for flashcard 2",
    ...
  ]
}
```

| Parameter | Type | Description |
| --- | --- | --- |
| `texts` | `List[str]` | List of 1 to 20 text strings to process. |

**Response:**
Returns a JSON list of flashcard objects.

```json
[
  {
    "question": "Generated question?",
    "answer": "Generated answer...",
    "points": 1
  }
]
```

## Usage Example
### Linux/macOS/PowerShell
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["What is Python?", "Explain Docker"]}'
```

### Windows Command Prompt (cmd)
```cmd
curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d "{\"texts\": [\"What is Python?\", \"Explain Docker\"]}"
