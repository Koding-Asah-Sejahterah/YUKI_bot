import json
import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List

# BARU: Menggunakan aiofiles untuk pembacaan file asinkron
import aiofiles
import requests
from fastapi import Depends, FastAPI, HTTPException, Request
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field

# --- Konfigurasi File ---
API_KEY_FILE = "api_key.txt"
DATABASE_FILE = "knowledge_base.json"

# --- Variabel Global (Akan diinisialisasi oleh lifespan) ---
API_KEY = None
DATA_KNOWLEDGE = []


# --- Model Pydantic ---
# Perbaikan: Menambahkan default=None untuk field yang bisa hilang
class KnowledgeItem(BaseModel):
    # Field ID tetap WAJIB untuk identifikasi
    id: str = Field(description="ID unik data pengetahuan.")

    # Field TITLE dan TEXT diubah agar bisa menerima string kosong jika tidak ada (untuk mengatasi error validasi)
    title: str = Field(default="", description="Judul atau konteks data.")
    text: str = Field(default="", description="Isi teks atau informasi utama.")


# Skema lainnya tetap sama
class QuestionRequest(BaseModel):
    query: str = Field(description="Pertanyaan yang diajukan oleh pengguna.")


class AnswerResponse(BaseModel):
    answer: str = Field(description="Jawaban yang dihasilkan oleh Gemini.")
    context_used: List[str] = Field(
        description="Daftar ID data pengetahuan yang digunakan untuk RAG."
    )
    model_used: str = Field(
        default="gemini-2.5-flash", description="Model Gemini yang digunakan."
    )


# --- Fungsi Lifespan (Mengelola Startup/Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global API_KEY, DATA_KNOWLEDGE

    # 1. Memuat API Key (Sinkron karena ukurannya kecil, TIDAK menggunakan aiofiles)
    try:
        with open(API_KEY_FILE, "r") as f:
            API_KEY = f.read().strip()
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"File '{API_KEY_FILE}' tidak ditemukan. Harap buat file tersebut dan masukkan API Key.",
        )

    # 2. Memuat Database JSON (Asinkron)
    try:
        # Perbaikan: Menggunakan aiofiles
        async with aiofiles.open(DATABASE_FILE, "r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content)

        # Perbaikan Logika: Validasi data pengetahuan menggunakan Pydantic
        # Kami mencoba memuat data. Jika gagal di beberapa item, kita akan log dan mengabaikannya.
        valid_data = []
        for item in data:
            try:
                # Kami mengasumsikan item data Anda memiliki field 'id'.
                # Jika 'id' pun hilang, kami akan menghasilkan ID sementara,
                # tapi ini sangat tidak disarankan untuk data RAG yang sesungguhnya.
                if "id" not in item and "source" in item:
                    item["id"] = item["source"][
                        :10
                    ]  # Ambil 10 karakter pertama dari source sebagai ID sementara

                # Cobalah validasi. Karena title dan text sekarang punya default, ini harusnya berhasil
                valid_data.append(KnowledgeItem(**item).model_dump())
            except Exception as e:
                # Jika validasi gagal (misal field 'id' benar-benar hilang), lewati item ini
                print(
                    f"Peringatan: Gagal memvalidasi item data (Dilewati): {item}. Error: {e}"
                )
                continue

        DATA_KNOWLEDGE = valid_data

        print(
            f" Berhasil memuat {len(DATA_KNOWLEDGE)} baris data pengetahuan (setelah validasi)."
        )

    except FileNotFoundError:
        print(
            f"Peringatan: File '{DATABASE_FILE}' tidak ditemukan. Jawaban hanya berdasarkan pengetahuan umum Gemini."
        )
        DATA_KNOWLEDGE = []

    except Exception as e:
        # Jika terjadi error JSON parsing atau error I/O lainnya
        print(f"Fatal Error saat memuat database JSON: {e}")
        raise HTTPException(
            status_code=500, detail=f"Gagal memuat/memvalidasi database: {e}"
        )

    # Inisialisasi Klien Gemini setelah API Key dimuat
    try:
        app.state.gemini_client = genai.Client(api_key=API_KEY)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Gagal inisialisasi Klien Gemini: {e}"
        )

    # Simpan data pengetahuan ke state aplikasi untuk akses mudah
    app.state.data_knowledge = DATA_KNOWLEDGE

    yield

    print("Aplikasi dimatikan.")


# --- Inisialisasi FastAPI ---
app = FastAPI(
    title="Yuki RAG API",
    description="API untuk menjawab pertanyaan menggunakan Retrieval-Augmented Generation (RAG) dengan Gemini.",
    version="1.0.0",
    lifespan=lifespan,
)


# --- Fungsi Inti Logika Yuki (RAG) ---
# Bagian ini tetap sama karena sudah benar, hanya bergantung pada field text dan title
def retrieve_knowledge(
    query: str, data: List[Dict[str, Any]], top_k: int = 3
) -> List[Dict[str, Any]]:
    # ... (Kode fungsi retrieve_knowledge tetap sama)
    if not data:
        return []

    query_lower = query.lower()

    results = [
        item
        for item in data
        if query_lower in item.get("title", "").lower()
        or query_lower in item.get("text", "").lower()
    ]

    return results[:top_k]


async def generate_rag_answer(client: genai.Client, query: str, context: str):
    # ... (Kode fungsi generate_rag_answer tetap sama)
    MODEL_NAME = "gemini-2.5-flash"

    system_instruction = (
        "Anda adalah asisten AI yang akurat dan berbasis fakta. "
        "Gunakan informasi di dalam tag <KONTEKS> di bawah untuk menjawab pertanyaan. "
        "Jika informasi di dalam <KONTEKS> tidak cukup untuk menjawab, nyatakan bahwa Anda tidak dapat menjawab "
        "berdasarkan informasi yang diberikan, lalu berikan jawaban umum Anda (jika relevan)."
    )

    prompt = (
        f"Pertanyaan pengguna: {query}\n\n"
        f"Berikut adalah data pengetahuan yang diambil (KONTEKS):\n"
        f"<KONTEKS>\n{context}\n</KONTEKS>"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system_instruction),
        )
        return response.text
    except APIError as e:
        raise HTTPException(
            status_code=500, detail=f"Terjadi kesalahan pada API Gemini: {e.message}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Terjadi kesalahan tak terduga: {str(e)}"
        )


# --- Endpoint API ---


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(question: QuestionRequest, request: Request):
    # ... (Kode endpoint ask_question tetap sama)
    client: genai.Client = request.app.state.gemini_client
    knowledge_data: List[Dict[str, Any]] = request.app.state.data_knowledge

    query = question.query

    # 1. Retrieval (Ambil Konteks)
    retrieved_items = retrieve_knowledge(query, knowledge_data, top_k=3)

    context_list = []
    context_ids = []

    if retrieved_items:
        for item in retrieved_items:
            # Karena title dan text mungkin kosong (''), kita tetap bisa menggunakannya.
            context_list.append(f"Judul: {item['title']}\nIsi: {item['text']}")
            context_ids.append(item["id"])

        full_context = "\n\n---\n\n".join(context_list)
    else:
        full_context = "Tidak ada informasi khusus yang ditemukan di basis pengetahuan."

    # 2. Augmented Generation (Pembangkitan Jawaban)
    answer = await generate_rag_answer(client, query, full_context)

    return AnswerResponse(
        answer=answer, context_used=context_ids, model_used="gemini-2.5-flash"
    )
