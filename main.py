from fastapi import FastAPI, Request
from ingest import download_and_transcribe
from vectorstore import store_transcript
from llm import query_llm

app = FastAPI()

@app.post("/ingest")
async def ingest_video(request: Request):
    data = await request.json()
    video_id, transcript = download_and_transcribe(data["url"])
    store_transcript(video_id, transcript)
    return {"status": "success", "video_id": video_id}

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    answer = query_llm(data["question"])
    return {"answer": answer}
