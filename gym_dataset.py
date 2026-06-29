"""
=========================================================================
 GYM & NUTRITION DATASET + AUTO SCHEDULE GENERATOR
=========================================================================
"""

import random

# =========================================================================
# 1. DATASET MAKANAN
# =========================================================================

FOODS = {
    "dada_ayam":        {"kategori": "protein", "protein": 31,  "karbo": 0,   "lemak": 3.6, "kalori": 165, "unit": "100g"},
    "telur_utuh":       {"kategori": "protein", "protein": 6,   "karbo": 0.6, "lemak": 5,   "kalori": 78,  "unit": "1 butir"},
    "putih_telur":      {"kategori": "protein", "protein": 3.6, "karbo": 0.2, "lemak": 0,   "kalori": 17,  "unit": "1 butir"},
    "ikan_salmon":      {"kategori": "protein", "protein": 20,  "karbo": 0,   "lemak": 13,  "kalori": 208, "unit": "100g"},
    "ikan_tuna":        {"kategori": "protein", "protein": 26,  "karbo": 0,   "lemak": 1,   "kalori": 116, "unit": "100g"},
    "ikan_lele":        {"kategori": "protein", "protein": 18,  "karbo": 0,   "lemak": 5,   "kalori": 116, "unit": "100g"},
    "daging_sapi_lean": {"kategori": "protein", "protein": 26,  "karbo": 0,   "lemak": 10,  "kalori": 217, "unit": "100g"},
    "udang":            {"kategori": "protein", "protein": 24,  "karbo": 0.2, "lemak": 0.3, "kalori": 99,  "unit": "100g"},
    "susu_sapi":        {"kategori": "protein", "protein": 3.4, "karbo": 5,   "lemak": 1,   "kalori": 42,  "unit": "100ml"},
    "whey_protein":     {"kategori": "protein", "protein": 24,  "karbo": 3,   "lemak": 1.5, "kalori": 120, "unit": "1 scoop"},
    "greek_yogurt":     {"kategori": "protein", "protein": 10,  "karbo": 4,   "lemak": 0.4, "kalori": 59,  "unit": "100g"},
    "dada_kalkun":      {"kategori": "protein", "protein": 29,  "karbo": 0,   "lemak": 1,   "kalori": 135, "unit": "100g"},
    "ikan_kembung":     {"kategori": "protein", "protein": 22,  "karbo": 0,   "lemak": 10,  "kalori": 190, "unit": "100g"},
    "cottage_cheese":   {"kategori": "protein", "protein": 11,  "karbo": 3.4, "lemak": 4.3, "kalori": 98,  "unit": "100g"},
    "tahu":             {"kategori": "protein", "protein": 8,   "karbo": 2,   "lemak": 4.8, "kalori": 76,  "unit": "100g"},
    "tempe":            {"kategori": "protein", "protein": 19,  "karbo": 9,   "lemak": 11,  "kalori": 193, "unit": "100g"},
    "kacang_almond":    {"kategori": "protein", "protein": 21,  "karbo": 22,  "lemak": 49,  "kalori": 579, "unit": "100g"},
    "edamame":          {"kategori": "protein", "protein": 11,  "karbo": 10,  "lemak": 5,   "kalori": 121, "unit": "100g"},
    "kacang_merah":     {"kategori": "protein", "protein": 9,   "karbo": 23,  "lemak": 0.5, "kalori": 127, "unit": "100g"},
    "nasi_putih":       {"kategori": "karbo",   "protein": 2.7, "karbo": 28,  "lemak": 0.3, "kalori": 130, "unit": "100g"},
    "nasi_merah":       {"kategori": "karbo",   "protein": 2.6, "karbo": 23,  "lemak": 0.9, "kalori": 111, "unit": "100g"},
    "ubi_jalar":        {"kategori": "karbo",   "protein": 1.6, "karbo": 20,  "lemak": 0.1, "kalori": 86,  "unit": "100g"},
    "kentang":          {"kategori": "karbo",   "protein": 2,   "karbo": 17,  "lemak": 0.1, "kalori": 77,  "unit": "100g"},
    "oatmeal":          {"kategori": "karbo",   "protein": 13,  "karbo": 68,  "lemak": 7,   "kalori": 389, "unit": "100g"},
    "roti_gandum":      {"kategori": "karbo",   "protein": 13,  "karbo": 41,  "lemak": 4.2, "kalori": 247, "unit": "100g"},
    "pisang":           {"kategori": "karbo",   "protein": 1.1, "karbo": 23,  "lemak": 0.3, "kalori": 89,  "unit": "1 buah"},
    "quinoa":           {"kategori": "karbo",   "protein": 4.4, "karbo": 21,  "lemak": 1.9, "kalori": 120, "unit": "100g"},
    "jagung":           {"kategori": "karbo",   "protein": 3.3, "karbo": 19,  "lemak": 1.4, "kalori": 96,  "unit": "100g"},
    "alpukat":          {"kategori": "lemak",   "protein": 2,   "karbo": 9,   "lemak": 15,  "kalori": 160, "unit": "100g"},
    "minyak_zaitun":    {"kategori": "lemak",   "protein": 0,   "karbo": 0,   "lemak": 14,  "kalori": 119, "unit": "1 sdm"},
    "kacang_mete":      {"kategori": "lemak",   "protein": 18,  "karbo": 30,  "lemak": 44,  "kalori": 553, "unit": "100g"},
    "brokoli":          {"kategori": "sayur",   "protein": 2.8, "karbo": 7,   "lemak": 0.4, "kalori": 34,  "unit": "100g"},
    "bayam":            {"kategori": "sayur",   "protein": 2.9, "karbo": 3.6, "lemak": 0.4, "kalori": 23,  "unit": "100g"},
    "buncis":           {"kategori": "sayur",   "protein": 1.8, "karbo": 7,   "lemak": 0.1, "kalori": 31,  "unit": "100g"},
    "wortel":           {"kategori": "sayur",   "protein": 0.9, "karbo": 10,  "lemak": 0.2, "kalori": 41,  "unit": "100g"},
    "kembang_kol":      {"kategori": "sayur",   "protein": 1.9, "karbo": 5,   "lemak": 0.3, "kalori": 25,  "unit": "100g"},
    "timun":            {"kategori": "sayur",   "protein": 0.7, "karbo": 3.6, "lemak": 0.1, "kalori": 15,  "unit": "100g"},
    "selada":           {"kategori": "sayur",   "protein": 1.4, "karbo": 2.9, "lemak": 0.2, "kalori": 15,  "unit": "100g"},
    "tomat":            {"kategori": "sayur",   "protein": 0.9, "karbo": 3.9, "lemak": 0.2, "kalori": 18,  "unit": "100g"},
}


# =========================================================================
# 2. DATASET LATIHAN
# =========================================================================

EXERCISES = {
    "dada":     [{"nama": "Bench Press", "set": 4, "rep": "8-10"}, {"nama": "Incline Dumbbell Press", "set": 3, "rep": "10-12"}, {"nama": "Chest Fly", "set": 3, "rep": "12-15"}, {"nama": "Push Up", "set": 3, "rep": "max"}],
    "punggung": [{"nama": "Deadlift", "set": 4, "rep": "6-8"}, {"nama": "Lat Pulldown", "set": 3, "rep": "10-12"}, {"nama": "Barbell Row", "set": 3, "rep": "8-10"}, {"nama": "Pull Up", "set": 3, "rep": "max"}],
    "kaki":     [{"nama": "Squat", "set": 4, "rep": "8-10"}, {"nama": "Leg Press", "set": 3, "rep": "10-12"}, {"nama": "Lunges", "set": 3, "rep": "12 per kaki"}, {"nama": "Leg Curl", "set": 3, "rep": "12-15"}],
    "bahu":     [{"nama": "Overhead Press", "set": 4, "rep": "8-10"}, {"nama": "Lateral Raise", "set": 3, "rep": "12-15"}, {"nama": "Front Raise", "set": 3, "rep": "12-15"}, {"nama": "Shrug", "set": 3, "rep": "12-15"}],
    "lengan":   [{"nama": "Barbell Curl", "set": 3, "rep": "10-12"}, {"nama": "Tricep Pushdown", "set": 3, "rep": "10-12"}, {"nama": "Hammer Curl", "set": 3, "rep": "10-12"}, {"nama": "Dips", "set": 3, "rep": "10-12"}],
    "perut":    [{"nama": "Plank", "set": 3, "rep": "60 detik"}, {"nama": "Hanging Leg Raise", "set": 3, "rep": "12-15"}, {"nama": "Cable Crunch", "set": 3, "rep": "15-20"}, {"nama": "Russian Twist", "set": 3, "rep": "20"}],
    "kardio":   [{"nama": "Treadmill Incline Walk", "set": 1, "rep": "20-30 menit"}, {"nama": "Cycling", "set": 1, "rep": "20-30 menit"}, {"nama": "HIIT Sprint", "set": 1, "rep": "15 menit"}, {"nama": "Jump Rope", "set": 1, "rep": "10 menit"}],
}


# =========================================================================
# 3. DATASET PROGRAM
# =========================================================================

PROGRAMS = {
    "bulking": {
        "deskripsi": "Program penambahan massa otot dengan surplus kalori",
        "alias": ["bulking", "nambah massa", "tambah otot", "massa otot"],
        "kalori_multiplier": 1.15,
        "protein_per_kg": 2.0,
        "karbo_persen": 0.50,
        "lemak_persen": 0.25,
        "meals_per_day": 5,
        "split_latihan": ["dada", "punggung", "kaki", "bahu", "lengan", "perut", None],
    },
    "cutting": {
        "deskripsi": "Program penurunan lemak sambil mempertahankan otot",
        "alias": ["cutting", "turun lemak", "bakar lemak", "kurus"],
        "kalori_multiplier": 0.80,
        "protein_per_kg": 2.2,
        "karbo_persen": 0.35,
        "lemak_persen": 0.30,
        "meals_per_day": 4,
        "split_latihan": ["dada", "punggung", "kardio", "kaki", "bahu", "kardio", None],
    },
    "diet_extreme": {
        "deskripsi": "Defisit kalori agresif untuk penurunan berat badan cepat (jangka pendek)",
        "alias": ["diet extreme", "diet ketat", "turun cepat", "defisit besar"],
        "kalori_multiplier": 0.65,
        "protein_per_kg": 2.4,
        "karbo_persen": 0.25,
        "lemak_persen": 0.30,
        "meals_per_day": 4,
        "split_latihan": ["kardio", "punggung", "kardio", "kaki", "kardio", "perut", None],
    },
    "diet_body_contest": {
        "deskripsi": "Program persiapan kompetisi/kontes body, fokus definisi otot maksimal",
        # PERBAIKAN: alias diperluas supaya mudah ditemukan dengan berbagai cara tanya
        "alias": [
            "diet body contest", "body contest", "kontes binaraga",
            "kompetisi body", "persiapan kontes", "contest prep",
            "body competition", "definisi otot maksimal",
        ],
        "kalori_multiplier": 0.75,
        "protein_per_kg": 2.6,
        "karbo_persen": 0.30,
        "lemak_persen": 0.25,
        "meals_per_day": 6,
        "split_latihan": ["dada", "punggung", "kaki", "bahu", "lengan", "kardio", "perut"],
    },
    "bulking_contest_prep": {
        "deskripsi": (
            "Program HYBRID: bulking bersih + definisi ala body contest. "
            "Surplus kalori kecil supaya lemak tidak menumpuk, protein tinggi "
            "dan kardio rutin supaya otot tetap terlihat definisi."
        ),
        # PERBAIKAN: alias diperluas untuk semua variasi cara tanya user
        "alias": [
            "bulking contest prep", "bulking body contest",
            "bulking sambil body contest", "lean bulk", "clean bulk",
            "bulking sambil definisi", "nambah otot sambil definisi",
            "bulking contest", "hybrid bulking",
        ],
        "kalori_multiplier": 1.07,
        "protein_per_kg": 2.4,
        "karbo_persen": 0.42,
        "lemak_persen": 0.25,
        "meals_per_day": 6,
        "split_latihan": ["dada", "punggung", "kardio", "kaki", "bahu", "lengan", "perut"],
    },
}


# =========================================================================
# 4. FAQ / KNOWLEDGE BASE
# =========================================================================

FAQ_DATA = [
    {
        "tags": ["protein", "berapa banyak", "kebutuhan protein"],
        "jawaban": "Kebutuhan protein harian umumnya 1.6-2.2 g/kg berat badan untuk yang aktif latihan beban. Program cutting atau body contest butuh lebih tinggi, sekitar 2.2-2.6 g/kg.",
    },
    {
        "tags": ["bulking", "nambah otot", "massa otot", "tambah massa"],
        "jawaban": "Bulking adalah fase nambah massa otot dengan surplus kalori (makan lebih dari TDEE), biasanya 10-20% di atas, dikombinasikan latihan beban progresif.",
    },
    {
        "tags": ["cutting", "turun lemak", "bakar lemak"],
        "jawaban": "Cutting adalah fase nurunin lemak dengan defisit kalori (makan kurang dari TDEE), biasanya 15-25% di bawah, sambil jaga protein tinggi biar otot tidak banyak hilang.",
    },
    {
        "tags": ["diet extreme", "diet ketat", "turun cepat", "defisit besar"],
        "jawaban": "Diet extreme pakai defisit kalori agresif sekitar 30-35% di bawah TDEE. Sebaiknya hanya jangka pendek karena risiko kehilangan otot dan kelelahan lebih tinggi.",
    },
    {
        # PERBAIKAN: tag lebih lengkap & spesifik, tidak ada kata "diet" sendirian
        # supaya tidak bertabrakan dengan tag cutting
        "tags": [
            "diet body contest", "body contest", "kontes binaraga",
            "kompetisi body", "persiapan kontes", "contest prep",
        ],
        "jawaban": (
            "Diet body contest adalah program persiapan kompetisi binaraga — "
            "fokus pada definisi otot maksimal dengan protein sangat tinggi (2.4-2.8 g/kg), "
            "defisit kalori terkontrol (~25% di bawah TDEE), makan 6x sehari, "
            "dan latihan intensif hampir setiap hari termasuk kardio rutin."
        ),
    },
    {
        # PERBAIKAN: entri khusus untuk program hybrid — tag sangat spesifik
        "tags": [
            "bulking contest prep", "bulking body contest",
            "bulking sambil body contest", "lean bulk", "clean bulk",
            "bulking sambil definisi", "nambah otot sambil definisi",
            "hybrid bulking",
        ],
        "jawaban": (
            "Program bulking_contest_prep adalah HYBRID antara bulking dan body contest. "
            "Surplus kalori kecil (7%) supaya lemak tidak menumpuk, "
            "protein tinggi 2.4 g/kg seperti standar body contest, "
            "ditambah kardio 2x seminggu. "
            "Cocok untuk yang mau nambah otot tapi tetap terlihat definisi — "
            "bukan bulking 'kotor' yang bikin perut buncit."
        ),
    },
    {
        "tags": ["tdee", "kalori harian", "kebutuhan kalori"],
        "jawaban": "TDEE adalah total kalori yang dibakar tubuh sehari, dihitung dari BMR dikali tingkat aktivitas. Pakai rumus Mifflin-St Jeor untuk estimasinya.",
    },
    {
        "tags": ["rest day", "hari istirahat", "libur latihan"],
        "jawaban": "Rest day penting untuk pemulihan otot. Minimal 1 hari penuh istirahat per minggu supaya otot bisa repair dan mencegah overtraining.",
    },
    {
        "tags": ["protein nabati", "vegetarian", "non daging"],
        "jawaban": "Sumber protein nabati bagus: tahu, tempe, kacang almond, edamame, kacang merah. Kombinasi beberapa sumber membantu lengkapi profil asam amino.",
    },
    {
        "tags": ["kapan makan", "jadwal makan", "frekuensi makan"],
        "jawaban": "Makan 4-6x sehari dengan porsi lebih kecil membantu jaga energi stabil dan distribusi protein merata sepanjang hari.",
    },
    {
        "tags": ["pre workout", "makan sebelum gym", "makan sebelum latihan"],
        "jawaban": "Karbo kompleks seperti oatmeal, nasi merah, atau ubi jalar 1-2 jam sebelum latihan membantu sediakan energi stabil selama sesi gym.",
    },
    {
        "tags": ["kardio", "cardio", "lari", "bakar lemak"],
        "jawaban": "Kardio efektif untuk membakar kalori tambahan. LISS (jalan incline 30 menit) bagus untuk cutting. HIIT lebih efisien waktu tapi lebih melelahkan.",
    },
    {
        "tags": ["suplemen", "whey", "creatine"],
        "jawaban": "Whey protein berguna kalau susah capai target protein dari makanan biasa. Creatine terbukti ilmiah meningkatkan performa dan kekuatan latihan beban.",
    },
]


# =========================================================================
# 5. FUNGSI PENCARIAN — DIPERBAIKI
# =========================================================================

def cari_program(query: str) -> list:
    """
    Cari program yang relevan berdasarkan query.
    PERBAIKAN: memakai alias list di tiap program, bukan hanya nama kuncinya.
    Mengembalikan list nama program yang cocok, diurutkan dari paling spesifik.
    """
    q = query.lower()
    hasil = []

    for nama, data in PROGRAMS.items():
        skor = 0
        # Cek alias — alias yang lebih panjang dapat skor lebih tinggi
        # supaya "diet body contest" lebih prioritas dari sekadar "diet"
        for alias in data.get("alias", []):
            if alias in q:
                skor += len(alias)   # panjang alias = tingkat spesifisitas
        # Cek nama program langsung (dengan/tanpa underscore)
        if nama in q or nama.replace("_", " ") in q:
            skor += len(nama)
        if skor > 0:
            hasil.append((skor, nama))

    hasil.sort(key=lambda x: x[0], reverse=True)
    return [nama for _, nama in hasil]


def cari_faq(query: str, top_n: int = 3) -> list:
    """
    Cari FAQ relevan berdasarkan query.
    PERBAIKAN: tag yang lebih panjang dapat skor lebih tinggi (sama dengan cari_program),
    supaya "diet body contest" lebih prioritas dari sekadar "diet".
    """
    q = query.lower()
    hasil_skor = []

    for entri in FAQ_DATA:
        skor = 0
        for tag in entri["tags"]:
            if tag in q:
                skor += len(tag)   # tag panjang = lebih spesifik = skor lebih tinggi
        if skor > 0:
            hasil_skor.append((skor, entri["jawaban"]))

    hasil_skor.sort(key=lambda x: x[0], reverse=True)
    return [j for _, j in hasil_skor[:top_n]]


def cari_makanan_relevan(query: str, top_n: int = 5) -> list:
    """Cari makanan di FOODS yang namanya relevan dengan query."""
    q = query.lower().replace(" ", "_")
    hasil = []
    for nama, data in FOODS.items():
        if nama in q or q in nama:
            hasil.append((nama, data))
    return hasil[:top_n]


# =========================================================================
# 6. GENERATOR JADWAL
# =========================================================================

HARI_LIST = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


def _hitung_tdee(berat_badan_kg, tinggi_cm=170, usia=22, jenis_kelamin="pria", aktivitas=1.55):
    if jenis_kelamin == "pria":
        bmr = 10 * berat_badan_kg + 6.25 * tinggi_cm - 5 * usia + 5
    else:
        bmr = 10 * berat_badan_kg + 6.25 * tinggi_cm - 5 * usia - 161
    return bmr * aktivitas


def _pilih_makanan(kategori, n=1, exclude=None):
    exclude = exclude or []
    pool = [k for k, v in FOODS.items() if v["kategori"] == kategori and k not in exclude]
    if not pool:
        pool = [k for k, v in FOODS.items() if v["kategori"] == kategori]
    return random.sample(pool, min(n, len(pool)))


def _generate_menu_harian(target_kalori, target_protein, meals_per_day):
    menu = []
    for i in range(meals_per_day):
        komponen = [
            random.choice(_pilih_makanan("protein")),
            random.choice(_pilih_makanan("karbo")),
            random.choice(_pilih_makanan("sayur")),
        ]
        if i % 2 == 0:
            komponen.append(random.choice(_pilih_makanan("lemak")))
        menu.append({
            "waktu_makan": f"Makan ke-{i + 1}",
            "menu": komponen,
            "estimasi_kalori": round(target_kalori / meals_per_day),
            "estimasi_protein_g": round(target_protein / meals_per_day),
        })
    return menu


def generate_weekly_schedule(program, berat_badan_kg, tinggi_cm=170, usia=22,
                              jenis_kelamin="pria", aktivitas=1.55, seed=None):
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
        grup = p["split_latihan"][idx]
        jadwal[hari] = {
            "latihan": {"jenis": grup or "Rest Day", "detail": EXERCISES.get(grup, [])},
            "menu_makan": _generate_menu_harian(target_kalori, target_protein, p["meals_per_day"]),
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
            print(f"   {m['waktu_makan']}: {', '.join(m['menu'])} (~{m['estimasi_kalori']} kkal)")


if __name__ == "__main__":
    hasil = generate_weekly_schedule("bulking_contest_prep", 65, seed=42)
    print_jadwal(hasil)
    print("\nProgram tersedia:", list(PROGRAMS.keys()))