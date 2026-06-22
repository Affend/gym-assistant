"""
=========================================================================
 CHATBOT GYM & NUTRISI (RAG SEDERHANA)
=========================================================================
File ini adalah contoh chatbot yang memakai dataset di gym_dataset.py
sebagai sumber referensi (knowledge base), lalu mengirim pertanyaan
user + referensi tersebut ke LLM (Claude) untuk dijawab secara natural.

Konsep RAG (Retrieval-Augmented Generation) di sini sangat sederhana:
1. RETRIEVE : cari data relevan dari dataset (FAQ_DATA, FOODS, PROGRAMS)
   berdasarkan pertanyaan user
2. AUGMENT  : gabungkan data relevan itu ke dalam prompt
3. GENERATE : kirim ke LLM, LLM jawab berdasarkan data yang diberikan

CARA PAKAI:
1. Pastikan sudah install package "anthropic":
       pip install anthropic
2. Set API key Anthropic sebagai environment variable:
       export ANTHROPIC_API_KEY="sk-ant-xxxxxxxx"     (Mac/Linux)
       setx ANTHROPIC_API_KEY "sk-ant-xxxxxxxx"        (Windows, lalu buka terminal baru)
3. Jalankan:
       python3 chatbot.py
4. Ketik pertanyaan, contoh: "apa itu bulking?" atau "menu untuk cutting apa saja?"
   Ketik "exit" untuk keluar.

CATATAN: Kalau belum punya API key / belum mau pakai API dulu, jalankan
mode "tanpa API" di bagian bawah file ini (lihat fungsi demo_tanpa_api())
yang hanya menampilkan hasil retrieval mentah tanpa LLM.
=========================================================================
"""

import os
from gym_dataset import (
    cari_faq,
    cari_makanan_relevan,
    PROGRAMS,
    generate_weekly_schedule,
)


def bangun_konteks(query: str) -> str:
    """
    Tahap RETRIEVE + AUGMENT.
    Mengumpulkan semua data relevan dari dataset berdasarkan pertanyaan
    user, lalu menyusunnya jadi teks konteks yang akan dikirim ke LLM.
    """
    bagian_konteks = []

    # 1. Cari di FAQ
    faq_hasil = cari_faq(query, top_n=3)
    if faq_hasil:
        bagian_konteks.append("Referensi FAQ:\n" + "\n".join(f"- {f}" for f in faq_hasil))

    # 2. Cari makanan yang disebut di pertanyaan
    makanan_hasil = cari_makanan_relevan(query, top_n=5)
    if makanan_hasil:
        baris_makanan = [
            f"- {nama}: {d['protein']}g protein, {d['karbo']}g karbo, "
            f"{d['lemak']}g lemak, {d['kalori']} kkal per {d['unit']}"
            for nama, d in makanan_hasil
        ]
        bagian_konteks.append("Data gizi makanan terkait:\n" + "\n".join(baris_makanan))

    # 3. Cari nama program yang disebut (bulking, cutting, dll)
    for nama_program, data_program in PROGRAMS.items():
        if nama_program.replace("_", " ") in query.lower() or nama_program in query.lower():
            bagian_konteks.append(
                f"Detail program '{nama_program}': {data_program['deskripsi']}. "
                f"Target protein {data_program['protein_per_kg']} g/kg berat badan, "
                f"split latihan: {', '.join(g or 'rest' for g in data_program['split_latihan'])}."
            )

    if not bagian_konteks:
        return "Tidak ada data spesifik yang cocok di dataset untuk pertanyaan ini."

    return "\n\n".join(bagian_konteks)


def tanya_llm_dengan_konteks(query: str, konteks: str) -> str:
    """
    Tahap GENERATE.
    Mengirim pertanyaan + konteks ke Claude API, lalu mengembalikan jawaban.
    Membutuhkan package 'anthropic' dan ANTHROPIC_API_KEY.
    """
    try:
        import anthropic
    except ImportError:
        return (
            "Package 'anthropic' belum terinstall. Jalankan dulu:\n"
            "    pip install anthropic\n"
            "Atau coba mode tanpa API dengan menjalankan demo_tanpa_api()."
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return (
            "ANTHROPIC_API_KEY belum di-set. Set dulu environment variable-nya, "
            "atau coba mode tanpa API dengan demo_tanpa_api()."
        )

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "Kamu adalah asisten gym & nutrisi yang ramah dan membantu. "
        "Jawab pertanyaan user HANYA berdasarkan data referensi yang diberikan. "
        "Jika data referensi tidak cukup untuk menjawab, katakan dengan jujur "
        "bahwa informasinya belum ada di dataset. Jawab dalam Bahasa Indonesia "
        "dengan singkat dan jelas."
    )

    user_message = f"Data referensi:\n{konteks}\n\nPertanyaan user: {query}"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    return response.content[0].text


def demo_tanpa_api():
    """
    Mode demo TANPA perlu API key — hanya menampilkan hasil retrieval
    mentah dari dataset. Berguna untuk memastikan logic pencarian data
    sudah jalan benar sebelum sambung ke LLM.
    """
    print("=" * 70)
    print("MODE DEMO TANPA API (hanya menampilkan hasil retrieval dataset)")
    print("Ketik 'exit' untuk keluar")
    print("=" * 70)

    while True:
        query = input("\nPertanyaan kamu: ").strip()
        if query.lower() == "exit":
            break
        if not query:
            continue

        konteks = bangun_konteks(query)
        print("\n--- Data relevan yang ditemukan di dataset ---")
        print(konteks)


def chat_loop():
    """Loop chatbot interaktif lewat terminal, memakai LLM (butuh API key)."""
    print("=" * 70)
    print("CHATBOT GYM & NUTRISI")
    print("Ketik 'exit' untuk keluar")
    print("=" * 70)

    while True:
        query = input("\nKamu: ").strip()
        if query.lower() == "exit":
            print("Sampai jumpa!")
            break
        if not query:
            continue

        konteks = bangun_konteks(query)
        jawaban = tanya_llm_dengan_konteks(query, konteks)
        print(f"\nBot: {jawaban}")


if __name__ == "__main__":
    # Cek otomatis: kalau API key belum di-set, jalankan mode demo dulu
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY belum di-set, menjalankan mode demo tanpa API...\n")
        demo_tanpa_api()
    else:
        chat_loop()
