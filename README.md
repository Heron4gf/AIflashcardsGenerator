# Flashcard Generator API

Microservizio containerizzato per generare flashcard utilizzando OpenAI.

## Prerequisiti

Assicurati di avere nella root del progetto:
1. Un file `.env` contenente `OPENAI_API_KEY=sk-...`
2. Un file `prompt.md` con il system prompt.

## Installazione e Avvio

### 1. Build dell'immagine
```bash
docker build -t flashcard-generator .