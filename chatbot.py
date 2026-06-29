"""
=========================================================================
 CHATBOT GYM & NUTRISI — RAG + FastAPI / Ollama / Anthropic
=========================================================================
CARA PAKAI:
  Mode demo (tanpa API, langsung bisa dicoba):
      python3 chatbot.py

  Mode Ollama (gratis, LLM lokal — install Ollama dulu):
      set CHAT_MODE=ollama          (Windows PowerShell)
      python3 chatbot.py

  Mode FastAPI (server kamu sendiri — jalankan api_server.py dulu):
      set CHAT_MODE=fastapi         (Windows PowerShell)
      python3 chatbot.py

  Mode Anthropic (butuh API key):
      set ANTHROPIC_API_KEY=sk-ant-xxx
      python3 chatbot.py
=========================================================================
"""

import os
import sys
import requests as req

from gym_dataset import (
    cari_faq,
    cari_makanan_relevan,
    PROGRAMS,
    generate_weekly_schedule,
)

# =========================================================================
# KONFIGURASI — ubah di sini kalau mau ganti mode
# =========================================================================
CHAT_MODE      = os.environ.get("CHAT_MODE", "anthropic")  # anthropic | ollama | fastapi
OLLAMA_URL     = "http://localhost:11434/api/chat"
OLLAMA_MODEL   = "llama3.2"
FASTAPI_URL    = "http://localhost:8000/chat"


# =========================================================================
# SYSTEM PROMPT — di sinilah "kepribadian" chatbot diatur
# =========================================================================
# BAGIAN INI YANG BISA KAMU UBAH untuk variasi bahasa yang lebih hidup.
# Claude/LLM akan generate jawaban sesuai instruksi di sini secara otomatis.

SYSTEM_PROMPT = """
Kamu adalah asisten gym & nutrisi bernama "GymBot" yang ramah, santai, dan
bicara seperti teman gym yang sudah berpengalaman.

Gaya bicara:
- Variatif dan natural — jangan selalu mulai dengan pola yang sama
- Kadang santai ("nah bro", "oke jadi gini", "gue saranin"), kadang lebih serius
  tergantung pertanyaannya
- Boleh pakai analogi sederhana biar mudah dipahami
- Kalau ada pilihan program, bantu user mikir mana yang cocok buat kondisi mereka
- Singkat dan to the point — tidak perlu bertele-tele

Aturan:
- Jawab HANYA berdasarkan data referensi yang diberikan
- Kalau data tidak cukup, jujur bilang "belum ada di database saya"
- Jangan pernah jawab di luar topik gym, nutrisi, dan kesehatan olahraga
"""


# =========================================================================
# FUNGSI RETRIEVAL (RETRIEVE)
# =========================================================================

def bangun_konteks(query: str) -> str:
    """Kumpulkan data relevan dari dataset berdasarkan pertanyaan user."""
    bagian = []

    faq = cari_faq(query, top_n=3)
    if faq:
        bagian.append("Referensi FAQ:\n" + "\n".join(f"- {f}" for f in faq))

    makanan = cari_makanan_relevan(query, top_n=5)
    if makanan:
        baris = [
            f"- {nama}: {d['protein']}g protein, {d['karbo']}g karbo, "
            f"{d['lemak']}g lemak, {d['kalori']} kkal per {d['unit']}"
            for nama, d in makanan
        ]
        bagian.append("Data gizi makanan:\n" + "\n".join(baris))

    for nama_prog, data_prog in PROGRAMS.items():
        if nama_prog.replace("_", " ") in query.lower() or nama_prog in query.lower():
            bagian.append(
                f"Detail program '{nama_prog}': {data_prog['deskripsi']}. "
                f"Protein target: {data_prog['protein_per_kg']} g/kg. "
                f"Split latihan: {', '.join(g or 'rest' for g in data_prog['split_latihan'])}."
            )

    return "\n\n".join(bagian) if bagian else "Tidak ada data spesifik di dataset untuk pertanyaan ini."


# =========================================================================
# FUNGSI GENERATE — 3 MODE
# =========================================================================

def _via_anthropic(query: str, konteks: str) -> str:
    """Mode Anthropic API (butuh API key)."""
    try:
        import anthropic
    except ImportError:
        return "Package 'anthropic' belum terinstall. Jalankan: pip install anthropic"

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "ANTHROPIC_API_KEY belum di-set. Coba mode lain: set CHAT_MODE=ollama"

    client = anthropic.Anthropic(api_key=api_key)
    pesan = f"Data referensi:\n{konteks}\n\nPertanyaan: {query}"
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": pesan}],
    )
    return response.content[0].text


def _via_ollama(query: str, konteks: str) -> str:
    """Mode Ollama — LLM gratis yang jalan di komputer sendiri."""
    pesan = f"Data referensi:\n{konteks}\n\nPertanyaan: {query}"
    try:
        response = req.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system",  "content": SYSTEM_PROMPT},
                {"role": "user",    "content": pesan},
            ],
            "stream": False,
        }, timeout=60)
        return response.json()["message"]["content"]
    except req.exceptions.ConnectionError:
        return "Ollama tidak bisa dihubungi. Pastikan Ollama sudah jalan (ketik: ollama serve)"


def _via_fastapi(query: str, konteks: str) -> str:
    """Mode FastAPI — kirim ke api_server.py yang kamu jalankan sendiri."""
    try:
        response = req.post(FASTAPI_URL, json={"pertanyaan": query}, timeout=60)
        return response.json()["jawaban"]
    except req.exceptions.ConnectionError:
        return (
            "API server tidak bisa dihubungi di localhost:8000. "
            "Pastikan api_server.py sudah jalan di terminal lain: uvicorn api_server:app --reload"
        )


def jawab(query: str) -> str:
    """
    Fungsi utama chatbot.
    RETRIEVE → AUGMENT → GENERATE
    """
    konteks = bangun_konteks(query)

    if CHAT_MODE == "ollama":
        return _via_ollama(query, konteks)
    elif CHAT_MODE == "fastapi":
        return _via_fastapi(query, konteks)
    else:
        return _via_anthropic(query, konteks)


# =========================================================================
# MODE DEMO (tanpa LLM) — cukup tampilkan hasil retrieval
# =========================================================================

def demo_tanpa_api():
    print("=" * 65)
    print("MODE DEMO — menampilkan data yang ditemukan di dataset")
    print("Ketik 'exit' untuk keluar")
    print("=" * 65)
    while True:
        query = input("\nPertanyaan kamu: ").strip()
        if query.lower() in ("exit", "quit", "q"):
            break
        if not query:
            continue
        konteks = bangun_konteks(query)
        print("\n--- Data relevan dari dataset ---")
        print(konteks)


# =========================================================================
# CHAT LOOP UTAMA
# =========================================================================

def chat_loop():
    mode_label = {
        "anthropic": "Anthropic API (Claude)",
        "ollama":    f"Ollama lokal ({OLLAMA_MODEL})",
        "fastapi":   "FastAPI server lokal",
    }.get(CHAT_MODE, CHAT_MODE)

    print("=" * 65)
    print(f"GYMBOT — Mode: {mode_label}")
    print("Ketik 'jadwal <program> <berat>' untuk generate jadwal")
    print("Contoh: jadwal bulking_contest_prep 70")
    print("Ketik 'exit' untuk keluar")
    print("=" * 65)

    while True:
        try:
            query = input("\nKamu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break

        if query.lower() in ("exit", "quit", "q"):
            print("Sampai jumpa!")
            break
        if not query:
            continue

        # Shortcut: generate jadwal otomatis
        if query.lower().startswith("jadwal "):
            parts = query.split()
            if len(parts) == 3:
                try:
                    hasil = generate_weekly_schedule(
                        program=parts[1],
                        berat_badan_kg=float(parts[2])
                    )
                    from gym_dataset import print_jadwal
                    print_jadwal(hasil)
                    continue
                except (ValueError, KeyError) as e:
                    print(f"GymBot: {e}")
                    continue

        jawaban = jawab(query)
        print(f"\nGymBot: {jawaban}")


# =========================================================================
# ENTRY POINT
# =========================================================================

if __name__ == "__main__":
    api_key_ada   = bool(os.environ.get("ANTHROPIC_API_KEY"))
    mode_eksplisit = "CHAT_MODE" in os.environ

    if not api_key_ada and not mode_eksplisit:
        print("Info: API key & CHAT_MODE tidak di-set, menjalankan mode demo...\n")
        demo_tanpa_api()
    else:
        chat_loop()
