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
You must pass your API key, Base URL, and the desired model as environment variables.

```bash
docker run -d -p 8000:8000 \
  -e BASE_URL="https://api.groq.com/openai/v1" \
  -e API_KEY="your-api-key" \
  -e MODEL="gpt-3.5-turbo" \
  flashcard-generator

```

### 4. (Optional) Run with Docker Compose
You can also run the service with `docker-compose.yml`.

```bash
docker compose up --build -d
```

The service reads these environment variables:

| Variable | Description | Default |
| --- | --- | --- |
| `BASE_URL` | OpenAI-compatible API base URL | `http://localhost:8000` (from compose file) |
| `API_KEY` | API key for the selected provider | _none_ |
| `MODEL` | Model name used for generation | `gpt-5-nano` (compose) / `gpt-3.5-turbo` (app fallback) |

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
    "answer": "Generated answer..."
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
