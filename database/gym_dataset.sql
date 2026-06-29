-- =========================================================================
-- 1. PEMBUATAN TABEL (DDL)
-- =========================================================================

CREATE TABLE foods (
    id SERIAL PRIMARY KEY,
    key_name VARCHAR(50) UNIQUE NOT NULL,
    kategori VARCHAR(20) NOT NULL,
    protein NUMERIC(5,2) NOT NULL,
    karbo NUMERIC(5,2) NOT NULL,
    lemak NUMERIC(5,2) NOT NULL,
    kalori INTEGER NOT NULL,
    unit VARCHAR(30) NOT NULL
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    kategori VARCHAR(30) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    jml_set INTEGER NOT NULL,
    rep VARCHAR(30) NOT NULL
);

CREATE TABLE programs (
    id SERIAL PRIMARY KEY,
    key_name VARCHAR(50) UNIQUE NOT NULL,
    deskripsi TEXT NOT NULL,
    kalori_multiplier NUMERIC(4,2) NOT NULL,
    protein_per_kg NUMERIC(4,2) NOT NULL,
    karbo_persen NUMERIC(4,2) NOT NULL,
    lemak_persen NUMERIC(4,2) NOT NULL,
    meals_per_day INTEGER NOT NULL,
    split_latihan VARCHAR(20)[] NOT NULL 
);

CREATE TABLE program_aliases (
    id SERIAL PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id) ON DELETE CASCADE,
    alias VARCHAR(100) NOT NULL
);

CREATE TABLE faq_data (
    id SERIAL PRIMARY KEY,
    jawaban TEXT NOT NULL,
    tags TEXT[] NOT NULL 
);

-- Indexing untuk optimasi kecepatan pencarian chatbot
CREATE INDEX idx_foods_kategori ON foods(kategori);
CREATE INDEX idx_exercises_kategori ON exercises(kategori);
CREATE INDEX idx_faq_tags_gin ON faq_data USING gin (tags);


-- =========================================================================
-- 2. MEMASUKKAN DATA (DML / SEEDING)
-- =========================================================================

-- DATA MAKANAN
INSERT INTO foods (key_name, kategori, protein, karbo, lemak, kalori, unit) VALUES
('dada_ayam', 'protein', 31, 0, 3.6, 165, '100g'),
('telur_utuh', 'protein', 6, 0.6, 5, 78, '1 butir'),
('putih_telur', 'protein', 3.6, 0.2, 0, 17, '1 butir'),
('ikan_salmon', 'protein', 20, 0, 13, 208, '100g'),
('ikan_tuna', 'protein', 26, 0, 1, 116, '100g'),
('ikan_lele', 'protein', 18, 0, 5, 116, '100g'),
('daging_sapi_lean', 'protein', 26, 0, 10, 217, '100g'),
('udang', 'protein', 24, 0.2, 0.3, 99, '100g'),
('susu_sapi', 'protein', 3.4, 5, 1, 42, '100ml'),
('whey_protein', 'protein', 24, 3, 1.5, 120, '1 scoop'),
('greek_yogurt', 'protein', 10, 4, 0.4, 59, '100g'),
('dada_kalkun', 'protein', 29, 0, 1, 135, '100g'),
('ikan_kembung', 'protein', 22, 0, 10, 190, '100g'),
('cottage_cheese', 'protein', 11, 3.4, 4.3, 98, '100g'),
('tahu', 'protein', 8, 2, 4.8, 76, '100g'),
('tempe', 'protein', 19, 9, 11, 193, '100g'),
('kacang_almond', 'protein', 21, 22, 49, 579, '100g'),
('edamame', 'protein', 11, 10, 5, 121, '100g'),
('kacang_merah', 'protein', 9, 23, 0.5, 127, '100g'),
('nasi_putih', 'karbo', 2.7, 28, 0.3, 130, '100g'),
('nasi_merah', 'karbo', 2.6, 23, 0.9, 111, '100g'),
('ubi_jalar', 'karbo', 1.6, 20, 0.1, 86, '100g'),
('kentang', 'karbo', 2, 17, 0.1, 77, '100g'),
('oatmeal', 'karbo', 13, 68, 7, 389, '100g'),
('roti_gandum', 'karbo', 13, 41, 4.2, 247, '100g'),
('pisang', 'karbo', 1.1, 23, 0.3, 89, '1 buah'),
('quinoa', 'karbo', 4.4, 21, 1.9, 120, '100g'),
('jagung', 'karbo', 3.3, 19, 1.4, 96, '100g'),
('alpukat', 'lemak', 2, 9, 15, 160, '100g'),
('minyak_zaitun', 'lemak', 0, 0, 14, 119, '1 sdm'),
('kacang_mete', 'lemak', 18, 30, 44, 553, '100g'),
('brokoli', 'sayur', 2.8, 7, 0.4, 34, '100g'),
('bayam', 'sayur', 2.9, 3.6, 0.4, 23, '100g'),
('buncis', 'sayur', 1.8, 7, 0.1, 31, '100g'),
('wortel', 'sayur', 0.9, 10, 0.2, 41, '100g'),
('kembang_kol', 'sayur', 1.9, 5, 0.3, 25, '100g'),
('timun', 'sayur', 0.7, 3.6, 0.1, 15, '100g'),
('selada', 'sayur', 1.4, 2.9, 0.2, 15, '100g'),
('tomat', 'sayur', 0.9, 3.9, 0.2, 18, '100g');

-- DATA LATIHAN
INSERT INTO exercises (kategori, nama, jml_set, rep) VALUES
('dada', 'Bench Press', 4, '8-10'),
('dada', 'Incline Dumbbell Press', 3, '10-12'),
('dada', 'Chest Fly', 3, '12-15'),
('dada', 'Push Up', 3, 'max'),
('punggung', 'Deadlift', 4, '6-8'),
('punggung', 'Lat Pulldown', 3, '10-12'),
('punggung', 'Barbell Row', 3, '8-10'),
('punggung', 'Pull Up', 3, 'max'),
('kaki', 'Squat', 4, '8-10'),
('kaki', 'Leg Press', 3, '10-12'),
('kaki', 'Lunges', 3, '12 per kaki'),
('kaki', 'Leg Curl', 3, '12-15'),
('bahu', 'Overhead Press', 4, '8-10'),
('bahu', 'Lateral Raise', 3, '12-15'),
('bahu', 'Front Raise', 3, '12-15'),
('bahu', 'Shrug', 3, '12-15'),
('lengan', 'Barbell Curl', 3, '10-12'),
('lengan', 'Tricep Pushdown', 3, '10-12'),
('lengan', 'Hammer Curl', 3, '10-12'),
('lengan', 'Dips', 3, '10-12'),
('perut', 'Plank', 3, '60 detik'),
('perut', 'Hanging Leg Raise', 3, '12-15'),
('perut', 'Cable Crunch', 3, '15-20'),
('perut', 'Russian Twist', 3, '20'),
('kardio', 'Treadmill Incline Walk', 1, '20-30 menit'),
('kardio', 'Cycling', 1, '20-30 menit'),
('kardio', 'HIIT Sprint', 1, '15 menit'),
('kardio', 'Jump Rope', 1, '10 menit');

-- DATA PROGRAM
INSERT INTO programs (key_name, deskripsi, kalori_multiplier, protein_per_kg, karbo_persen, lemak_persen, meals_per_day, split_latihan) VALUES
('bulking', 'Program penambahan massa otot dengan surplus kalori', 1.15, 2.0, 0.50, 0.25, 5, ARRAY['dada', 'punggung', 'kaki', 'bahu', 'lengan', 'perut', NULL]),
('cutting', 'Program penurunan lemak sambil mempertahankan otot', 0.80, 2.2, 0.35, 0.30, 4, ARRAY['dada', 'punggung', 'kardio', 'kaki', 'bahu', 'kardio', NULL]),
('diet_extreme', 'Defisit kalori agresif untuk penurunan berat badan cepat (jangka pendek)', 0.65, 2.4, 0.25, 0.30, 4, ARRAY['kardio', 'punggung', 'kardio', 'kaki', 'kardio', 'perut', NULL]),
('diet_body_contest', 'Program persiapan kompetisi/kontes body, fokus definisi otot maksimal', 0.75, 2.6, 0.30, 0.25, 6, ARRAY['dada', 'punggung', 'kaki', 'bahu', 'lengan', 'kardio', 'perut']),
('bulking_contest_prep', 'Program HYBRID: bulking bersih + definisi ala body contest. Surplus kalori kecil supaya lemak tidak menumpuk, protein tinggi dan kardio rutin supaya otot tetap terlihat definisi.', 1.07, 2.4, 0.42, 0.25, 6, ARRAY['dada', 'punggung', 'kardio', 'kaki', 'bahu', 'lengan', 'perut']);

-- DATA ALIAS PROGRAM
INSERT INTO program_aliases (program_id, alias) VALUES
((SELECT id FROM programs WHERE key_name = 'bulking'), 'bulking'),
((SELECT id FROM programs WHERE key_name = 'bulking'), 'nambah massa'),
((SELECT id FROM programs WHERE key_name = 'bulking'), 'tambah otot'),
((SELECT id FROM programs WHERE key_name = 'bulking'), 'massa otot'),
((SELECT id FROM programs WHERE key_name = 'cutting'), 'cutting'),
((SELECT id FROM programs WHERE key_name = 'cutting'), 'turun lemak'),
((SELECT id FROM programs WHERE key_name = 'cutting'), 'bakar lemak'),
((SELECT id FROM programs WHERE key_name = 'cutting'), 'kurus'),
((SELECT id FROM programs WHERE key_name = 'diet_extreme'), 'diet extreme'),
((SELECT id FROM programs WHERE key_name = 'diet_extreme'), 'diet ketat'),
((SELECT id FROM programs WHERE key_name = 'diet_extreme'), 'turun cepat'),
((SELECT id FROM programs WHERE key_name = 'diet_extreme'), 'defisit besar'),
((SELECT id FROM programs WHERE key_name = 'diet_body_contest'), 'diet body contest'),
((SELECT id FROM programs WHERE key_name = 'diet_body_contest'), 'body contest'),
((SELECT id FROM programs WHERE key_name = 'diet_body_contest'), 'kontes binaraga'),
((SELECT id FROM programs WHERE key_name = 'diet_body_contest'), 'kompetisi body'),
((SELECT id FROM programs WHERE key_name = 'diet_body_contest'), 'persiapan kontes'),
((SELECT id FROM programs WHERE key_name = 'diet_body_contest'), 'contest prep'),
((SELECT id FROM programs WHERE key_name = 'diet_body_contest'), 'body competition'),
((SELECT id FROM programs WHERE key_name = 'diet_body_contest'), 'definisi otot maksimal'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'bulking contest prep'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'bulking body contest'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'bulking sambil body contest'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'lean bulk'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'clean bulk'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'bulking sambil definisi'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'nambah otot sambil definisi'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'bulking contest'),
((SELECT id FROM programs WHERE key_name = 'bulking_contest_prep'), 'hybrid bulking');

-- DATA FAQ
INSERT INTO faq_data (jawaban, tags) VALUES
('Kebutuhan protein harian umumnya 1.6-2.2 g/kg berat badan untuk yang aktif latihan beban. Program cutting atau body contest butuh lebih tinggi, sekitar 2.2-2.6 g/kg.', ARRAY['protein', 'berapa banyak', 'kebutuhan protein']),
('Bulking adalah fase nambah massa otot dengan surplus kalori (makan lebih dari TDEE), biasanya 10-20% di atas, dikombinasikan latihan beban progresif.', ARRAY['bulking', 'nambah otot', 'massa otot', 'tambah massa']),
('Cutting adalah fase nurunin lemak dengan defisit kalori (makan kurang dari TDEE), biasanya 15-25% di bawah, sambil jaga protein tinggi biar otot tidak banyak hilang.', ARRAY['cutting', 'turun lemak', 'bakar lemak']),
('Diet extreme pakai defisit kalori agresif sekitar 30-35% di bawah TDEE. Sebaiknya hanya jangka pendek karena risiko kehilangan otot dan kelelahan lebih tinggi.', ARRAY['diet extreme', 'diet ketat', 'turun cepat', 'defisit besar']),
('Diet body contest adalah program persiapan kompetisi binaraga — fokus pada definisi otot maksimal dengan protein sangat tinggi (2.4-2.8 g/kg), defisit kalori terkontrol (~25% di bawah TDEE), makan 6x sehari, dan latihan intensif hampir setiap hari termasuk kardio rutin.', ARRAY['diet body contest', 'body contest', 'kontes binaraga', 'kompetisi body', 'persiapan kontes', 'contest prep']),
('Program bulking_contest_prep adalah HYBRID antara bulking dan body contest. Surplus kalori kecil (7%) supaya lemak tidak menumpuk, protein tinggi 2.4 g/kg seperti standar body contest, ditambah kardio 2x seminggu. Cocok untuk yang mau nambah otot tapi tetap terlihat definisi — bukan bulking kotor yang bikin perut buncit.', ARRAY['bulking contest prep', 'bulking body contest', 'bulking sambil body contest', 'lean bulk', 'clean bulk', 'bulking sambil definisi', 'nambah otot sambil definisi', 'hybrid bulking']),
('TDEE adalah total kalori yang dibakar tubuh sehari, dihitung dari BMR dikali tingkat aktivitas. Pakai rumus Mifflin-St Jeor untuk estimasinya.', ARRAY['tdee', 'kalori harian', 'kebutuhan kalori']),
('Rest day penting untuk pemulihan otot. Minimal 1 hari penuh istirahat per minggu supaya otot bisa repair dan mencegah overtraining.', ARRAY['rest day', 'hari istirahat', 'libur latihan']),
('Sumber protein nabati bagus: tahu, tempe, kacang almond, edamame, kacang merah. Kombinasi beberapa sumber membantu lengkapi profil asam amino.', ARRAY['protein nabati', 'vegetarian', 'non daging']),
('Makan 4-6x sehari dengan porsi lebih kecil membantu jaga energi stabil dan distribusi protein merata sepanjang hari.', ARRAY['kapan makan', 'jadwal makan', 'frekuensi makan']),
('Karbo kompleks seperti oatmeal, nasi merah, atau ubi jalar 1-2 jam sebelum latihan membantu sediakan energi stabil selama sesi gym.', ARRAY['pre workout', 'makan sebelum gym', 'makan sebelum latihan']),
('Kardio efektif untuk membakar kalori tambahan. LISS (jalan incline 30 menit) bagus untuk cutting. HIIT lebih efisien waktu tapi lebih melelahkan.', ARRAY['kardio', 'cardio', 'lari', 'bakar lemak']),
('Whey protein berguna kalau susah capai target protein dari makanan biasa. Creatine terbukti ilmiah meningkatkan performa dan kekuatan latihan beban.', ARRAY['suplemen', 'whey', 'creatine']);