from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai
from pydantic import BaseModel, Field
from retrieval import find_chunks


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@app.post("/api/chat")
def chat(request: ChatRequest):
    # Find paragraphs related to the question in backend/data/*.txt
    chunks = find_chunks(request.question)
    if not chunks:
        return {
            "answer": "자료에서 관련 내용을 찾지 못했습니다.",
            "sources": [],
        }

    # Put the file name in front of each paragraph so the model knows the source
    context = "\n\n".join(f"[{c['source']}]\n{c['text']}" for c in chunks)
    prompt = f"""Answer the question using only the materials below.
Each paragraph starts with its file name in [brackets].
If the answer is not in the materials, say that it cannot be found.
Answer in the same language as the question.

Materials:
{context}

Question: {request.question}"""

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )
    # Unique file names, in the order they were found
    sources = list(dict.fromkeys(c["source"] for c in chunks))
    return {"answer": interaction.output_text, "sources": sources}
