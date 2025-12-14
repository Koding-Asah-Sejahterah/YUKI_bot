# YUKI BOT WITH RAG API (Retrieval-Augmented Generation)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688)](https://fastapi.tiangolo.com/)

Yuki RAG API adalah sistem *chatbot* canggih yang dibangun menggunakan **FastAPI** dan memanfaatkan model bahasa besar **Gemini 2.5 Flash**. Tujuannya adalah memberikan jawaban yang akurat dan terkonteks berdasarkan basis pengetahuan kustom.

Proyek ini mengimplementasikan pola **Retrieval-Augmented Generation (RAG)**, di mana kemampuan generatif AI diperkuat oleh data kustom yang tersimpan dalam *database* lokal (`knowledge_base.json`).

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
* Kunci API Google AI (Gemini API Key).

### 1. Kloning Repositori

```bash
git clone [URL-REPOSitori-ANDA]
cd YUKI-ac465e61f72dda0eaa0189d793ef46b35a74a083
