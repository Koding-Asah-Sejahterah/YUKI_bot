# Quick Start Guide - YUKI Bot

## Langkah Cepat untuk Memulai

### 1. Setup Awal (Hanya Sekali)

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```batch
setup.bat
```

### 2. Konfigurasi

Edit dua file berikut:

1. **api_key.txt** - Masukkan Gemini API Key Anda
   - Dapatkan di: https://aistudio.google.com/app/apikey
   
2. **knowledge_base.json** - Masukkan data pengetahuan Anda

### 3. Jalankan Aplikasi

**Opsi A: API Server (untuk integrasi backend)**
```bash
# Aktifkan virtual environment
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Jalankan server
uvicorn api_yuki:app --reload
```

Akses:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

**Opsi B: CLI Version (untuk testing cepat)**
```bash
# Aktifkan virtual environment
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Jalankan CLI
python3 YUKI.py
```

## Troubleshooting

### ❌ uvicorn: command not found

**Solusi:**
```bash
# Aktifkan virtual environment terlebih dahulu
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install ulang dependencies jika perlu
pip install -r requirements.txt
```

### ❌ File 'api_key.txt' tidak ditemukan

**Solusi:**
```bash
# Salin dari template
cp api_key.txt.example api_key.txt

# Edit dan masukkan API Key Anda
nano api_key.txt  # atau editor lain
```

### ❌ Import Error saat menjalankan

**Solusi:**
```bash
# Pastikan virtual environment aktif
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies lengkap
pip install -r requirements.txt
```

## Integrasi dengan Backend

### Request ke API

**Endpoint:** `POST http://localhost:8000/ask`

**Request Body:**
```json
{
  "query": "Pertanyaan Anda"
}
```

**Response:**
```json
{
  "answer": "Jawaban dari Yuki",
  "context_used": ["id-1", "id-2"],
  "model_used": "gemini-2.5-flash"
}
```

### Contoh dengan curl

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "Apa itu YUKI?"}'
```

### Contoh dengan Python

```python
import requests

response = requests.post(
    'http://localhost:8000/ask',
    json={'query': 'Apa itu YUKI?'}
)

print(response.json()['answer'])
```

### Contoh dengan JavaScript

```javascript
const response = await fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'Apa itu YUKI?'})
});

const data = await response.json();
console.log(data.answer);
```

## Dokumentasi Lengkap

Lihat [README.md](README.md) untuk dokumentasi lengkap.
