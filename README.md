# YUKI BOT WITH RAG API (Retrieval-Augmented Generation)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688)](https://fastapi.tiangolo.com/)

Yuki RAG API adalah sistem *chatbot* canggih yang dibangun menggunakan **FastAPI** dan memanfaatkan model bahasa besar **Gemini 2.5 Flash**. Tujuannya adalah memberikan jawaban yang akurat dan terkonteks berdasarkan basis pengetahuan kustom.

Proyek ini mengimplementasikan pola **Retrieval-Augmented Generation (RAG)**, di mana kemampuan generatif AI diperkuat oleh data kustom yang tersimpan dalam *database* lokal (`knowledge_base.json`).

> 🚀 **Ingin langsung mulai?** Lihat [QUICK_START.md](QUICK_START.md) untuk panduan singkat!

## Fitur Kunci

* **RAG Implementation:** Menjamin jawaban AI didukung oleh sumber data spesifik milik perusahaan/proyek.
* **Gemini 2.5 Flash:** Menggunakan model Google yang cepat dan efisien untuk pemrosesan bahasa alami dan latensi rendah.
* **FastAPI Framework:** Menyediakan *interface* API yang *asynchronous*, performa tinggi, dan dilengkapi dengan dokumentasi interaktif otomatis (Swagger UI).
* **Filtering Konten:** Menerapkan *filtering* awal untuk mengambil potongan konteks yang paling relevan secara efisien, menghemat biaya token dan waktu pemrosesan.

## Arsitektur dan Cara Kerja RAG

Sistem RAG ini bekerja dalam tiga fase saat menerima permintaan POST pada *endpoint* `/yuki/ask`:

1.  **Retrieval (Pengambilan):** Sistem memproses pertanyaan pengguna dan mengidentifikasi kata kunci relevan. Kata kunci ini digunakan untuk memindai `knowledge_base.json` dan mengambil potongan teks yang paling relevan (dibatasi oleh `max_context`).
2.  **Augmentation (Penguatan):** Potongan konteks yang diambil digabungkan dengan pertanyaan asli pengguna untuk membentuk **Prompt Final**. Prompt ini bertindak sebagai instruksi tegas kepada Gemini untuk menggunakan data konteks sebagai sumber kebenaran utama. 
3.  **Generation (Generasi):** Prompt Final dikirim ke **Gemini 2.5 Flash API**. Jawaban yang dihasilkan dikembalikan kepada pengguna dalam format JSON melalui *endpoint* FastAPI.

## Persiapan dan Setup

### Prasyarat

* Python 3.8 atau lebih tinggi
* Kunci API Google AI (Gemini API Key) - [Dapatkan di sini](https://aistudio.google.com/app/apikey)

### 1. Kloning Repositori

```bash
git clone https://github.com/Koding-Asah-Sejahterah/YUKI_bot.git
cd YUKI_bot
```

### 2. Setup Otomatis (Direkomendasikan)

Kami menyediakan script setup otomatis untuk memudahkan instalasi:

**Untuk Linux/Mac:**
```bash
./setup.sh
```

**Untuk Windows:**
```batch
setup.bat
```

Script ini akan:
- Membuat virtual environment
- Menginstall semua dependencies
- Membuat file konfigurasi (api_key.txt, knowledge_base.json)

Setelah menjalankan script, Anda hanya perlu mengedit `api_key.txt` dan `knowledge_base.json` sesuai kebutuhan.

### 2. Setup Manual (Alternatif)

Jika Anda lebih suka setup secara manual, ikuti langkah-langkah berikut:

#### 2.1. Buat Virtual Environment (Disarankan)

```bash
# Membuat virtual environment
python3 -m venv venv

# Mengaktifkan virtual environment
# Untuk Linux/Mac:
source venv/bin/activate

# Untuk Windows:
venv\Scripts\activate
```

#### 2.2. Instalasi Dependencies

```bash
pip install -r requirements.txt
```

**Catatan:** Jika terjadi error saat instalasi, coba upgrade pip terlebih dahulu:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2.3. Konfigurasi API Key

Buat file `api_key.txt` di direktori root proyek dan masukkan Gemini API Key Anda:

```bash
# Salin file contoh
cp api_key.txt.example api_key.txt

# Edit file dan masukkan API Key Anda
# Gunakan text editor favorit Anda (nano, vim, vscode, dll)
nano api_key.txt
```

Isi file `api_key.txt` dengan API Key Anda (tanpa tanda kutip atau spasi tambahan):
```
YOUR_GEMINI_API_KEY_HERE
```

#### 2.4. Persiapan Knowledge Base

Buat file `knowledge_base.json` yang berisi data pengetahuan kustom Anda:

```bash
# Salin file contoh
cp knowledge_base.json.example knowledge_base.json

# Edit file dan masukkan data pengetahuan Anda
nano knowledge_base.json
```

Format `knowledge_base.json`:
```json
[
  {
    "id": "unique-id-1",
    "title": "Judul Data",
    "text": "Konten atau informasi yang akan digunakan sebagai konteks",
    "source": "sumber-data"
  }
]
```

**Alternatif:** Anda dapat menggunakan Jupyter Notebook `Datapreparation.ipynb` untuk mempersiapkan data pengetahuan Anda.

## Cara Menjalankan Aplikasi

### Opsi 1: Menjalankan FastAPI Server (API Endpoint)

Untuk menjalankan API server dengan FastAPI dan uvicorn:

```bash
# Pastikan virtual environment sudah diaktifkan
uvicorn api_yuki:app --host 0.0.0.0 --port 8000 --reload
```

Server akan berjalan di `http://localhost:8000`

**Mengakses Dokumentasi API:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Menggunakan API:**

```bash
# Contoh request menggunakan curl
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "Apa itu YUKI?"}'
```

### Opsi 2: Menjalankan CLI Version

Untuk menjalankan versi command-line interaktif:

```bash
python3 YUKI.py
```

Program akan meminta input pertanyaan dan menampilkan jawaban langsung di terminal.

## Mengintegrasikan dengan Backend

Jika Anda ingin menggunakan endpoint AI ini dari backend aplikasi lain:

1. **Pastikan API server berjalan** (gunakan Opsi 1 di atas)

2. **Gunakan endpoint `/ask`** dengan method POST:
   - URL: `http://localhost:8000/ask`
   - Method: `POST`
   - Content-Type: `application/json`
   - Body:
     ```json
     {
       "query": "Pertanyaan Anda di sini"
     }
     ```

3. **Contoh integrasi dengan JavaScript (fetch):**
   ```javascript
   const response = await fetch('http://localhost:8000/ask', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({
       query: 'Apa itu YUKI?'
     })
   });
   
   const data = await response.json();
   console.log(data.answer);
   ```

4. **Contoh integrasi dengan Python (requests):**
   ```python
   import requests
   
   response = requests.post(
       'http://localhost:8000/ask',
       json={'query': 'Apa itu YUKI?'}
   )
   
   data = response.json()
   print(data['answer'])
   ```

## Troubleshooting

### Error: "uvicorn: command not found"

Ini berarti uvicorn belum terinstal. Solusi:

1. Pastikan Anda sudah mengaktifkan virtual environment
2. Install dependencies dengan `pip install -r requirements.txt`
3. Atau install uvicorn secara manual: `pip install uvicorn`

### Error: "File 'api_key.txt' tidak ditemukan"

Pastikan Anda sudah membuat file `api_key.txt` dan mengisi dengan Gemini API Key yang valid.

### Error: "File 'knowledge_base.json' tidak ditemukan"

Pastikan Anda sudah membuat file `knowledge_base.json` dengan format yang benar (lihat contoh di atas).
