"""
=========================================================================
 GYMBOT API SERVER — FastAPI mandiri tanpa LLM eksternal
=========================================================================
CARA JALANKAN (Terminal 1):
    python3 -m uvicorn api_server:app --reload --port 8000

CARA TEST browser:
    http://localhost:8000/docs
=========================================================================
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gym_dataset import (
    cari_faq, cari_program, cari_makanan_relevan,
    generate_weekly_schedule, PROGRAMS, FOODS,
)

app = FastAPI(
    title="GymBot API",
    description="API chatbot gym & nutrisi — mandiri tanpa LLM eksternal",
    version="2.1.0",
)


class ChatRequest(BaseModel):
    pertanyaan: str

class ChatResponse(BaseModel):
    jawaban: str
    program_ditemukan: list = []

class JadwalRequest(BaseModel):
    program: str
    berat_badan_kg: float
    tinggi_cm: float = 170
    usia: int = 22
    jenis_kelamin: str = "pria"


def _format_makanan(nama, data):
    return (
        f"{nama.replace('_', ' ').title()}: "
        f"{data['protein']}g protein, {data['karbo']}g karbo, "
        f"{data['lemak']}g lemak, {data['kalori']} kkal per {data['unit']}"
    )


def _jawab_dari_dataset(pertanyaan: str) -> tuple:
    """
    Mesin jawaban rule-based.
    Return: (jawaban: str, program_ditemukan: list)

    URUTAN PRIORITAS:
    1. Program spesifik (pakai cari_program() yang sudah diperbaiki)
    2. Makanan spesifik
    3. FAQ umum
    4. Daftar program / makanan
    5. Sapaan
    6. Fallback
    """
    q = pertanyaan.lower().strip()

    # ------------------------------------------------------------------
    # 1. CEK PROGRAM — pakai cari_program() yang berbasis alias & skor
    # ------------------------------------------------------------------
    program_cocok = cari_program(q)
    if program_cocok:
        # Ambil program paling relevan (skor tertinggi)
        nama = program_cocok[0]
        data = PROGRAMS[nama]
        split_str = ", ".join(g or "istirahat" for g in data["split_latihan"])
        surplus_info = "surplus" if data["kalori_multiplier"] > 1 else "defisit"
        persen = abs(round((data["kalori_multiplier"] - 1) * 100))
        jawaban = (
            f"Program {nama.replace('_', ' ').upper()}:\n"
            f"{data['deskripsi']}\n\n"
            f"Target kalori  : {surplus_info} {persen}% dari TDEE kamu\n"
            f"Target protein : {data['protein_per_kg']} g per kg berat badan\n"
            f"Frekuensi makan: {data['meals_per_day']}x sehari\n"
            f"Split latihan  : {split_str}\n\n"
            f"Mau generate jadwal mingguan lengkap?\n"
            f"Ketik: jadwal {nama} <berat_badan>"
        )
        return jawaban, program_cocok

    # ------------------------------------------------------------------
    # 2. CEK MAKANAN SPESIFIK
    # ------------------------------------------------------------------
    makanan = cari_makanan_relevan(q, top_n=5)
    if makanan:
        if len(makanan) == 1:
            nama, data = makanan[0]
            return (
                f"Info gizi {nama.replace('_', ' ').title()}:\n"
                f"- Protein : {data['protein']}g\n"
                f"- Karbo   : {data['karbo']}g\n"
                f"- Lemak   : {data['lemak']}g\n"
                f"- Kalori  : {data['kalori']} kkal per {data['unit']}\n"
                f"- Kategori: {data['kategori']}"
            ), []
        baris = [_format_makanan(n, d) for n, d in makanan]
        return "Data gizi makanan:\n" + "\n".join(baris), []

    # ------------------------------------------------------------------
    # 3. CEK FAQ UMUM
    # ------------------------------------------------------------------
    faq = cari_faq(q, top_n=1)
    if faq:
        return faq[0], []

    # ------------------------------------------------------------------
    # 4. DAFTAR PROGRAM
    # ------------------------------------------------------------------
    if any(k in q for k in ["program apa", "pilihan program", "list program", "program tersedia", "ada program apa"]):
        baris = [
            f"- {nama.replace('_', ' ').upper()}: {data['deskripsi']}"
            for nama, data in PROGRAMS.items()
        ]
        return "Program yang tersedia:\n" + "\n".join(baris), []

    # ------------------------------------------------------------------
    # 5. DAFTAR MAKANAN PER KATEGORI
    # ------------------------------------------------------------------
    kategori_map = {"protein": "protein", "karbo": "karbo", "karbohidrat": "karbo",
                    "lemak": "lemak", "sayur": "sayur", "sayuran": "sayur"}
    for kata, kat in kategori_map.items():
        if kata in q and any(w in q for w in ["apa saja", "list", "daftar", "contoh"]):
            makanan_kat = [_format_makanan(n, d) for n, d in FOODS.items() if d["kategori"] == kat]
            return f"Sumber {kat} dalam database:\n" + "\n".join(makanan_kat), []

    # ------------------------------------------------------------------
    # 6. SAPAAN
    # ------------------------------------------------------------------
    if any(k in q for k in ["halo", "hai", "hello", "hi", "selamat pagi", "selamat sore"]):
        return (
            "Halo! Saya GymBot, asisten gym & nutrisi kamu.\n"
            "Tanya apa saja soal program, makanan, atau nutrisi.\n"
            "Contoh: 'apa itu diet body contest?', 'protein dada ayam berapa?'"
        ), []

    # ------------------------------------------------------------------
    # 7. FALLBACK
    # ------------------------------------------------------------------
    return (
        "Pertanyaan itu belum ada di database saya.\n"
        "Coba tanya soal:\n"
        "- Program: bulking, cutting, diet body contest, bulking contest prep, diet extreme\n"
        "- Gizi makanan: 'protein dada ayam', 'kalori oatmeal'\n"
        "- Topik gym: 'apa itu tdee', 'kapan makan sebelum latihan'\n"
        "- Generate jadwal: 'jadwal bulking 70'"
    ), []


# =========================================================================
# ENDPOINT
# =========================================================================

@app.get("/")
def root():
    return {
        "status": "GymBot API aktif",
        "versi": "2.1.0",
        "docs": "http://localhost:8000/docs",
        "program_tersedia": list(PROGRAMS.keys()),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.pertanyaan.strip():
        raise HTTPException(status_code=400, detail="Pertanyaan tidak boleh kosong")
    jawaban, program_cocok = _jawab_dari_dataset(req.pertanyaan)
    return ChatResponse(jawaban=jawaban, program_ditemukan=program_cocok)


@app.post("/jadwal")
def buat_jadwal(req: JadwalRequest):
    try:
        return generate_weekly_schedule(
            program=req.program,
            berat_badan_kg=req.berat_badan_kg,
            tinggi_cm=req.tinggi_cm,
            usia=req.usia,
            jenis_kelamin=req.jenis_kelamin,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/program")
def list_program():
    return {
        nama: {"deskripsi": data["deskripsi"], "alias": data.get("alias", [])}
        for nama, data in PROGRAMS.items()
    }


@app.get("/makanan/{nama}")
def info_makanan(nama: str):
    nama_lower = nama.lower()
    if nama_lower not in FOODS:
        mirip = [k for k in FOODS if nama_lower in k or k in nama_lower]
        detail = f"Mungkin maksudnya: {mirip}" if mirip else f"'{nama}' tidak ada di database"
        raise HTTPException(status_code=404, detail=detail)
    return {"nama": nama_lower, **FOODS[nama_lower]}


@app.get("/makanan")
def list_makanan(kategori: str = None):
    if kategori:
        hasil = {k: v for k, v in FOODS.items() if v["kategori"] == kategori}
        if not hasil:
            raise HTTPException(status_code=404,
                detail=f"Kategori '{kategori}' tidak ada. Pilihan: protein, karbo, lemak, sayur")
        return hasil
    return FOODS