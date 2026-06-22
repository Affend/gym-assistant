"""
=========================================================================
 GYM & NUTRITION DATASET + AUTO SCHEDULE GENERATOR
=========================================================================
Dataset ini berisi:
1. FOODS        -> daftar makanan & kandungan gizi per porsi
2. EXERCISES    -> daftar latihan per grup otot
3. PROGRAMS     -> definisi program (Bulking, Cutting, Diet Extreme,
                   Diet Body Contest) lengkap dengan target makro & split
4. generate_weekly_schedule() -> fungsi untuk generate jadwal mingguan
   otomatis (latihan + menu makan) berdasarkan program & berat badan user

Cara pakai cepat (lihat juga bagian __main__ di paling bawah):

    from gym_dataset import generate_weekly_schedule

    jadwal = generate_weekly_schedule(program="bulking", berat_badan_kg=65)
    for hari, isi in jadwal.items():
        print(hari, isi)
=========================================================================
"""

import random

# =========================================================================
# 1. DATASET MAKANAN
# =========================================================================
# Nilai gizi adalah perkiraan per 100 gram (atau per unit untuk telur),
# berdasarkan estimasi nutrisi umum yang banyak dipakai di Indonesia.
# protein, karbo, lemak dalam gram | kalori dalam kkal

FOODS = {
    # --- Sumber Protein Hewani ---
    "dada_ayam":        {"kategori": "protein", "protein": 31, "karbo": 0,  "lemak": 3.6, "kalori": 165, "unit": "100g"},
    "telur_utuh":       {"kategori": "protein", "protein": 6,  "karbo": 0.6,"lemak": 5,   "kalori": 78,  "unit": "1 butir"},
    "putih_telur":      {"kategori": "protein", "protein": 3.6,"karbo": 0.2,"lemak": 0,   "kalori": 17,  "unit": "1 butir"},
    "ikan_salmon":      {"kategori": "protein", "protein": 20, "karbo": 0,  "lemak": 13,  "kalori": 208, "unit": "100g"},
    "ikan_tuna":        {"kategori": "protein", "protein": 26, "karbo": 0,  "lemak": 1,   "kalori": 116, "unit": "100g"},
    "ikan_lele":        {"kategori": "protein", "protein": 18, "karbo": 0,  "lemak": 5,   "kalori": 116, "unit": "100g"},
    "daging_sapi_lean": {"kategori": "protein", "protein": 26, "karbo": 0,  "lemak": 10,  "kalori": 217, "unit": "100g"},
    "udang":            {"kategori": "protein", "protein": 24, "karbo": 0.2,"lemak": 0.3, "kalori": 99,  "unit": "100g"},
    "susu_sapi":        {"kategori": "protein", "protein": 3.4,"karbo": 5,  "lemak": 1,   "kalori": 42,  "unit": "100ml"},
    "whey_protein":     {"kategori": "protein", "protein": 24, "karbo": 3,  "lemak": 1.5, "kalori": 120, "unit": "1 scoop"},
    "greek_yogurt":     {"kategori": "protein", "protein": 10, "karbo": 4,  "lemak": 0.4, "kalori": 59,  "unit": "100g"},

    # --- Sumber Protein Nabati ---
    "tahu":             {"kategori": "protein", "protein": 8,  "karbo": 2,  "lemak": 4.8, "kalori": 76,  "unit": "100g"},
    "tempe":            {"kategori": "protein", "protein": 19, "karbo": 9,  "lemak": 11,  "kalori": 193, "unit": "100g"},
    "kacang_almond":    {"kategori": "protein", "protein": 21, "karbo": 22, "lemak": 49,  "kalori": 579, "unit": "100g"},
    "edamame":          {"kategori": "protein", "protein": 11, "karbo": 10, "lemak": 5,   "kalori": 121, "unit": "100g"},

    # --- Sumber Karbohidrat ---
    "nasi_putih":       {"kategori": "karbo", "protein": 2.7, "karbo": 28, "lemak": 0.3, "kalori": 130, "unit": "100g"},
    "nasi_merah":       {"kategori": "karbo", "protein": 2.6, "karbo": 23, "lemak": 0.9, "kalori": 111, "unit": "100g"},
    "ubi_jalar":        {"kategori": "karbo", "protein": 1.6, "karbo": 20, "lemak": 0.1, "kalori": 86,  "unit": "100g"},
    "kentang":          {"kategori": "karbo", "protein": 2,   "karbo": 17, "lemak": 0.1, "kalori": 77,  "unit": "100g"},
    "oatmeal":          {"kategori": "karbo", "protein": 13,  "karbo": 68, "lemak": 7,   "kalori": 389, "unit": "100g"},
    "roti_gandum":      {"kategori": "karbo", "protein": 13,  "karbo": 41, "lemak": 4.2, "kalori": 247, "unit": "100g"},
    "pisang":           {"kategori": "karbo", "protein": 1.1, "karbo": 23, "lemak": 0.3, "kalori": 89,  "unit": "1 buah"},

    # --- Sumber Lemak Sehat ---
    "alpukat":          {"kategori": "lemak", "protein": 2,   "karbo": 9,  "lemak": 15,  "kalori": 160, "unit": "100g"},
    "minyak_zaitun":    {"kategori": "lemak", "protein": 0,   "karbo": 0,  "lemak": 14,  "kalori": 119, "unit": "1 sdm"},
    "kacang_mete":      {"kategori": "lemak", "protein": 18,  "karbo": 30, "lemak": 44,  "kalori": 553, "unit": "100g"},

    # --- Sayur & Serat ---
    "brokoli":          {"kategori": "sayur", "protein": 2.8, "karbo": 7,  "lemak": 0.4, "kalori": 34,  "unit": "100g"},
    "bayam":            {"kategori": "sayur", "protein": 2.9, "karbo": 3.6,"lemak": 0.4, "kalori": 23,  "unit": "100g"},
    "buncis":           {"kategori": "sayur", "protein": 1.8, "karbo": 7,  "lemak": 0.1, "kalori": 31,  "unit": "100g"},
    "wortel":           {"kategori": "sayur", "protein": 0.9, "karbo": 10, "lemak": 0.2, "kalori": 41,  "unit": "100g"},
    "kembang_kol":      {"kategori": "sayur", "protein": 1.9, "karbo": 5,  "lemak": 0.3, "kalori": 25,  "unit": "100g"},
    "timun":            {"kategori": "sayur", "protein": 0.7, "karbo": 3.6,"lemak": 0.1, "kalori": 15,  "unit": "100g"},
    "selada":           {"kategori": "sayur", "protein": 1.4, "karbo": 2.9,"lemak": 0.2, "kalori": 15,  "unit": "100g"},
    "tomat":            {"kategori": "sayur", "protein": 0.9, "karbo": 3.9,"lemak": 0.2, "kalori": 18,  "unit": "100g"},

    # --- Tambahan Protein ---
    "dada_kalkun":      {"kategori": "protein", "protein": 29, "karbo": 0,  "lemak": 1,   "kalori": 135, "unit": "100g"},
    "ikan_kembung":     {"kategori": "protein", "protein": 22, "karbo": 0,  "lemak": 10,  "kalori": 190, "unit": "100g"},
    "cottage_cheese":   {"kategori": "protein", "protein": 11, "karbo": 3.4,"lemak": 4.3, "kalori": 98,  "unit": "100g"},
    "kacang_merah":     {"kategori": "protein", "protein": 9,  "karbo": 23, "lemak": 0.5, "kalori": 127, "unit": "100g"},

    # --- Tambahan Karbo ---
    "quinoa":           {"kategori": "karbo", "protein": 4.4, "karbo": 21, "lemak": 1.9, "kalori": 120, "unit": "100g"},
    "jagung":           {"kategori": "karbo", "protein": 3.3, "karbo": 19, "lemak": 1.4, "kalori": 96,  "unit": "100g"},
}


# =========================================================================
# 2. DATASET LATIHAN (EXERCISES)
# =========================================================================
# Dikelompokkan berdasarkan grup otot, setiap latihan punya target rep
# range yang bisa disesuaikan tujuan (massa, kekuatan, definisi)

EXERCISES = {
    "dada": [
        {"nama": "Bench Press", "set": 4, "rep": "8-10"},
        {"nama": "Incline Dumbbell Press", "set": 3, "rep": "10-12"},
        {"nama": "Chest Fly", "set": 3, "rep": "12-15"},
        {"nama": "Push Up", "set": 3, "rep": "max"},
    ],
    "punggung": [
        {"nama": "Deadlift", "set": 4, "rep": "6-8"},
        {"nama": "Lat Pulldown", "set": 3, "rep": "10-12"},
        {"nama": "Barbell Row", "set": 3, "rep": "8-10"},
        {"nama": "Pull Up", "set": 3, "rep": "max"},
    ],
    "kaki": [
        {"nama": "Squat", "set": 4, "rep": "8-10"},
        {"nama": "Leg Press", "set": 3, "rep": "10-12"},
        {"nama": "Lunges", "set": 3, "rep": "12 per kaki"},
        {"nama": "Leg Curl", "set": 3, "rep": "12-15"},
    ],
    "bahu": [
        {"nama": "Overhead Press", "set": 4, "rep": "8-10"},
        {"nama": "Lateral Raise", "set": 3, "rep": "12-15"},
        {"nama": "Front Raise", "set": 3, "rep": "12-15"},
        {"nama": "Shrug", "set": 3, "rep": "12-15"},
    ],
    "lengan": [
        {"nama": "Barbell Curl", "set": 3, "rep": "10-12"},
        {"nama": "Tricep Pushdown", "set": 3, "rep": "10-12"},
        {"nama": "Hammer Curl", "set": 3, "rep": "10-12"},
        {"nama": "Dips", "set": 3, "rep": "10-12"},
    ],
    "perut": [
        {"nama": "Plank", "set": 3, "rep": "60 detik"},
        {"nama": "Hanging Leg Raise", "set": 3, "rep": "12-15"},
        {"nama": "Cable Crunch", "set": 3, "rep": "15-20"},
        {"nama": "Russian Twist", "set": 3, "rep": "20"},
    ],
    "kardio": [
        {"nama": "Treadmill Incline Walk", "set": 1, "rep": "20-30 menit"},
        {"nama": "Cycling", "set": 1, "rep": "20-30 menit"},
        {"nama": "HIIT Sprint", "set": 1, "rep": "15 menit"},
        {"nama": "Jump Rope", "set": 1, "rep": "10 menit"},
    ],
}


# =========================================================================
# 3. DATASET PROGRAM (Bulking, Cutting, Diet Extreme, Diet Body Contest)
# =========================================================================
# - kalori_multiplier : pengali dari TDEE (Total Daily Energy Expenditure)
# - protein_per_kg     : gram protein per kg berat badan
# - karbo_persen / lemak_persen : porsi sisa kalori dari karbo & lemak
# - split_latihan      : urutan grup otot per hari (7 hari, None = rest day)
# - meals_per_day       : jumlah makan per hari

PROGRAMS = {
    "bulking": {
        "deskripsi": "Program penambahan massa otot dengan surplus kalori",
        "kalori_multiplier": 1.15,       # surplus 15% dari TDEE
        "protein_per_kg": 2.0,
        "karbo_persen": 0.50,
        "lemak_persen": 0.25,
        "meals_per_day": 5,
        "split_latihan": ["dada", "punggung", "kaki", "bahu", "lengan", "perut", None],
    },
    "cutting": {
        "deskripsi": "Program penurunan lemak sambil mempertahankan otot",
        "kalori_multiplier": 0.80,       # defisit 20% dari TDEE
        "protein_per_kg": 2.2,
        "karbo_persen": 0.35,
        "lemak_persen": 0.30,
        "meals_per_day": 4,
        "split_latihan": ["dada", "punggung", "kardio", "kaki", "bahu", "kardio", None],
    },
    "diet_extreme": {
        "deskripsi": "Defisit kalori agresif untuk penurunan berat badan cepat (jangka pendek, awasi kondisi tubuh)",
        "kalori_multiplier": 0.65,       # defisit 35% dari TDEE
        "protein_per_kg": 2.4,
        "karbo_persen": 0.25,
        "lemak_persen": 0.30,
        "meals_per_day": 4,
        "split_latihan": ["kardio", "punggung", "kardio", "kaki", "kardio", "perut", None],
    },
    "diet_body_contest": {
        "deskripsi": "Program persiapan kompetisi/kontes body, fokus definisi otot maksimal",
        "kalori_multiplier": 0.75,
        "protein_per_kg": 2.6,
        "karbo_persen": 0.30,
        "lemak_persen": 0.25,
        "meals_per_day": 6,
        "split_latihan": ["dada", "punggung", "kaki", "bahu", "lengan", "kardio", "perut"],
    },
}


# =========================================================================
# 3B. FAQ / KNOWLEDGE BASE (untuk chatbot RAG)
# =========================================================================
# Setiap entri punya "tags" supaya gampang dicari berdasarkan kata kunci
# pertanyaan user. Ini yang nanti jadi "sumber referensi" yang dikirim
# ke LLM saat menjawab pertanyaan user.

FAQ_DATA = [
    {
        "tags": ["protein", "berapa banyak", "kebutuhan protein"],
        "jawaban": "Kebutuhan protein harian umumnya 1.6-2.2 gram per kg berat badan untuk orang yang aktif latihan beban. Untuk program cutting atau diet body contest, protein bisa dinaikkan ke 2.2-2.6 g/kg supaya massa otot tetap terjaga saat defisit kalori."
    },
    {
        "tags": ["bulking", "nambah otot", "massa otot"],
        "jawaban": "Bulking adalah fase menambah massa otot dengan cara makan di surplus kalori (lebih banyak dari kebutuhan harian), biasanya 10-20% di atas TDEE, dikombinasikan dengan latihan beban progresif."
    },
    {
        "tags": ["cutting", "turun lemak", "diet"],
        "jawaban": "Cutting adalah fase menurunkan lemak tubuh dengan defisit kalori (makan lebih sedikit dari kebutuhan harian), biasanya 15-25% di bawah TDEE, sambil mempertahankan asupan protein tinggi agar otot tidak banyak hilang."
    },
    {
        "tags": ["diet extreme", "turun cepat", "defisit besar"],
        "jawaban": "Diet extreme menggunakan defisit kalori yang lebih agresif (sekitar 30-35% di bawah TDEE) untuk penurunan berat badan cepat. Ini sebaiknya hanya dilakukan jangka pendek dan dengan pengawasan, karena risiko kehilangan massa otot dan kelelahan lebih tinggi."
    },
    {
        "tags": ["body contest", "kompetisi", "kontes binaraga"],
        "jawaban": "Program diet body contest dirancang untuk persiapan kompetisi, fokus pada definisi otot maksimal dengan protein sangat tinggi (2.4-2.8 g/kg), defisit kalori terkontrol, dan latihan intensif hampir setiap hari termasuk kardio."
    },
    {
        "tags": ["tdee", "kalori harian", "kebutuhan kalori"],
        "jawaban": "TDEE (Total Daily Energy Expenditure) adalah estimasi total kalori yang dibakar tubuh dalam sehari, dihitung dari BMR (Basal Metabolic Rate) dikalikan tingkat aktivitas. Rumus umum yang dipakai adalah Mifflin-St Jeor."
    },
    {
        "tags": ["rest day", "hari istirahat", "libur latihan"],
        "jawaban": "Rest day penting untuk pemulihan otot. Idealnya minimal 1 hari penuh istirahat per minggu, atau di sela-sela jika baru mulai latihan, supaya otot punya waktu memperbaiki diri dan mencegah overtraining."
    },
    {
        "tags": ["sumber protein nabati", "vegetarian", "non daging"],
        "jawaban": "Sumber protein nabati yang baik antara lain tahu, tempe, kacang almond, edamame, dan kacang merah. Kombinasi beberapa sumber nabati membantu memenuhi profil asam amino lengkap."
    },
    {
        "tags": ["kapan makan", "jadwal makan", "frekuensi makan"],
        "jawaban": "Frekuensi makan bisa disesuaikan preferensi, umumnya 4-6 kali sehari dengan porsi lebih kecil membantu menjaga energi stabil dan distribusi protein merata sepanjang hari, terutama untuk program bulking dan body contest."
    },
    {
        "tags": ["karbo sebelum latihan", "pre workout", "makan sebelum gym"],
        "jawaban": "Karbohidrat kompleks seperti oatmeal, nasi merah, atau ubi jalar 1-2 jam sebelum latihan membantu menyediakan energi yang stabil selama sesi gym."
    },
]


def cari_faq(query: str, top_n: int = 3):
    """
    Pencarian sederhana berbasis kata kunci (keyword matching) di FAQ_DATA.
    Ini adalah bentuk paling dasar dari 'retrieval' dalam RAG.

    Parameters
    ----------
    query : str
        Pertanyaan dari user
    top_n : int
        Jumlah maksimal hasil relevan yang dikembalikan

    Returns
    -------
    list[str] : daftar jawaban FAQ yang paling relevan dengan query
    """
    query_lower = query.lower()
    hasil_skor = []

    for entri in FAQ_DATA:
        skor = sum(1 for tag in entri["tags"] if tag in query_lower)
        if skor > 0:
            hasil_skor.append((skor, entri["jawaban"]))

    hasil_skor.sort(key=lambda x: x[0], reverse=True)
    return [jawaban for _, jawaban in hasil_skor[:top_n]]


def cari_makanan_relevan(query: str, top_n: int = 5):
    """Cari makanan di FOODS yang namanya disebut/mirip dengan query."""
    query_lower = query.lower().replace(" ", "_")
    hasil = []
    for nama, data in FOODS.items():
        if nama in query_lower or query_lower in nama:
            hasil.append((nama, data))
    return hasil[:top_n]


# =========================================================================
# 4. FUNGSI GENERATOR JADWAL OTOMATIS
# =========================================================================

HARI_LIST = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


def _hitung_tdee(berat_badan_kg, tinggi_cm=170, usia=22, jenis_kelamin="pria", aktivitas=1.55):
    """
    Estimasi TDEE memakai rumus Mifflin-St Jeor.
    aktivitas: 1.2 (jarang olahraga) - 1.9 (sangat aktif)
    """
    if jenis_kelamin == "pria":
        bmr = 10 * berat_badan_kg + 6.25 * tinggi_cm - 5 * usia + 5
    else:
        bmr = 10 * berat_badan_kg + 6.25 * tinggi_cm - 5 * usia - 161
    return bmr * aktivitas


def _pilih_makanan(kategori, n=1, exclude=None):
    """Pilih n makanan acak dari kategori tertentu."""
    exclude = exclude or []
    pool = [k for k, v in FOODS.items() if v["kategori"] == kategori and k not in exclude]
    if not pool:
        pool = [k for k, v in FOODS.items() if v["kategori"] == kategori]
    return random.sample(pool, min(n, len(pool)))


def _generate_menu_harian(target_kalori, target_protein, meals_per_day):
    """
    Membuat menu harian sederhana yang mendekati target kalori & protein,
    dibagi rata ke sejumlah meals_per_day.
    """
    menu = []
    kalori_per_meal = target_kalori / meals_per_day
    protein_per_meal = target_protein / meals_per_day

    for i in range(meals_per_day):
        protein_food = random.choice(_pilih_makanan("protein", 1))
        karbo_food = random.choice(_pilih_makanan("karbo", 1))
        sayur_food = random.choice(_pilih_makanan("sayur", 1))

        komponen = [protein_food, karbo_food, sayur_food]
        # Tambahkan lemak sehat di sebagian meal
        if i % 2 == 0:
            komponen.append(random.choice(_pilih_makanan("lemak", 1)))

        menu.append({
            "waktu_makan": f"Makan ke-{i + 1}",
            "menu": komponen,
            "estimasi_kalori": round(kalori_per_meal),
            "estimasi_protein_g": round(protein_per_meal),
        })

    return menu


def generate_weekly_schedule(
    program: str,
    berat_badan_kg: float,
    tinggi_cm: float = 170,
    usia: int = 22,
    jenis_kelamin: str = "pria",
    aktivitas: float = 1.55,
    seed: int = None,
):
    """
    Generate jadwal mingguan (latihan + menu makan) secara otomatis.

    Parameters
    ----------
    program : str
        Salah satu dari: "bulking", "cutting", "diet_extreme", "diet_body_contest"
    berat_badan_kg : float
        Berat badan user dalam kg
    tinggi_cm, usia, jenis_kelamin, aktivitas : opsional, untuk hitung TDEE
    seed : int, opsional
        Untuk hasil menu yang konsisten/reproducible

    Returns
    -------
    dict : jadwal per hari (Senin-Minggu), masing-masing berisi
           latihan & menu makan beserta ringkasan target gizi
    """
    if program not in PROGRAMS:
        raise ValueError(f"Program '{program}' tidak ditemukan. Pilihan: {list(PROGRAMS.keys())}")

    if seed is not None:
        random.seed(seed)

    p = PROGRAMS[program]
    tdee = _hitung_tdee(berat_badan_kg, tinggi_cm, usia, jenis_kelamin, aktivitas)
    target_kalori = round(tdee * p["kalori_multiplier"])
    target_protein = round(berat_badan_kg * p["protein_per_kg"])

    jadwal = {}
    for idx, hari in enumerate(HARI_LIST):
        grup_otot = p["split_latihan"][idx]

        if grup_otot is None:
            latihan_hari = {"jenis": "Rest Day / Recovery", "detail": []}
        else:
            latihan_hari = {"jenis": grup_otot, "detail": EXERCISES.get(grup_otot, [])}

        menu_hari = _generate_menu_harian(target_kalori, target_protein, p["meals_per_day"])

        jadwal[hari] = {
            "latihan": latihan_hari,
            "menu_makan": menu_hari,
            "target_kalori_harian": target_kalori,
            "target_protein_harian_g": target_protein,
        }

    return {
        "program": program,
        "deskripsi_program": p["deskripsi"],
        "tdee_estimasi": round(tdee),
        "target_kalori_harian": target_kalori,
        "target_protein_harian_g": target_protein,
        "jadwal_mingguan": jadwal,
    }


def print_jadwal(hasil):
    """Helper untuk mencetak hasil generate_weekly_schedule() secara rapi."""
    print("=" * 70)
    print(f"PROGRAM: {hasil['program'].upper()}")
    print(f"Deskripsi : {hasil['deskripsi_program']}")
    print(f"TDEE Estimasi      : {hasil['tdee_estimasi']} kkal")
    print(f"Target Kalori/Hari : {hasil['target_kalori_harian']} kkal")
    print(f"Target Protein/Hari: {hasil['target_protein_harian_g']} g")
    print("=" * 70)

    for hari, isi in hasil["jadwal_mingguan"].items():
        print(f"\n--- {hari} ---")
        print(f"Latihan: {isi['latihan']['jenis']}")
        for ex in isi["latihan"]["detail"]:
            print(f"   - {ex['nama']}: {ex['set']} set x {ex['rep']}")

        print("Menu Makan:")
        for m in isi["menu_makan"]:
            menu_str = ", ".join(m["menu"])
            print(f"   {m['waktu_makan']}: {menu_str} (~{m['estimasi_kalori']} kkal, ~{m['estimasi_protein_g']}g protein)")


# =========================================================================
# CONTOH PENGGUNAAN
# =========================================================================
if __name__ == "__main__":
    # Contoh: generate jadwal bulking untuk user dengan berat 65 kg
    hasil = generate_weekly_schedule(
        program="bulking",
        berat_badan_kg=65,
        tinggi_cm=170,
        usia=22,
        jenis_kelamin="pria",
        seed=42,
    )
    print_jadwal(hasil)

    print("\n\nProgram tersedia:", list(PROGRAMS.keys()))
