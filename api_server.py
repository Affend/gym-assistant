from fastapi import FastAPI
from pydantic import BaseModel
import requests
from gym_dataset import bangun_konteks   # pakai dataset kamu sendiri

app = FastAPI()

# Format request yang diterima server
class ChatRequest(BaseModel):
    pertanyaan: str
    program: str = None   # opsional, misal "bulking" atau "cutting"

@app.post("/chat")
def chat(req: ChatRequest):
    # 1. RETRIEVE — ambil data relevan dari dataset
    konteks = bangun_konteks(req.pertanyaan)

    # 2. AUGMENT — susun pesan ke LLM
    system_prompt = (
        "Kamu asisten gym & nutrisi yang ramah dan santai. "
        "Jawab berdasarkan data referensi yang diberikan saja."
    )
    pesan = f"Data referensi:\n{konteks}\n\nPertanyaan: {req.pertanyaan}"

    # 3. GENERATE — kirim ke Ollama (LLM lokal kamu sendiri)
    response = requests.post("http://localhost:11434/api/chat", json={
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": pesan}
        ],
        "stream": False
    })

    jawaban = response.json()["message"]["content"]
    return {"jawaban": jawaban}

# Endpoint bonus: generate jadwal otomatis
@app.post("/jadwal")
def jadwal(program: str, berat_badan: float):
    from gym_dataset import generate_weekly_schedule
    hasil = generate_weekly_schedule(program=program, berat_badan_kg=berat_badan)
    return hasil