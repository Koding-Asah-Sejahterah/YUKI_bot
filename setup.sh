#!/bin/bash

# YUKI Bot Setup Script
# Script ini membantu setup environment untuk menjalankan YUKI Bot

set -e

echo "=========================================="
echo "  YUKI Bot - Setup Script"
echo "=========================================="
echo ""

# Cek Python version
echo "🔍 Memeriksa versi Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan. Silakan install Python 3.8 atau lebih tinggi."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo "✅ Python version: $PYTHON_VERSION"
echo ""

# Buat virtual environment jika belum ada
if [ ! -d "venv" ]; then
    echo "📦 Membuat virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment berhasil dibuat"
else
    echo "✅ Virtual environment sudah ada"
fi
echo ""

# Aktifkan virtual environment
echo "🔧 Mengaktifkan virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment aktif"
echo ""

# Upgrade pip
echo "⬆️  Mengupgrade pip..."
pip install --upgrade pip --quiet
echo "✅ Pip berhasil diupgrade"
echo ""

# Install dependencies
echo "📥 Menginstall dependencies dari requirements.txt..."
echo "   (Ini mungkin memakan waktu beberapa menit...)"
pip install -r requirements.txt --quiet
echo "✅ Dependencies berhasil diinstall"
echo ""

# Setup api_key.txt
if [ ! -f "api_key.txt" ]; then
    echo "🔑 Setup API Key..."
    if [ -f "api_key.txt.example" ]; then
        cp api_key.txt.example api_key.txt
        echo "⚠️  File api_key.txt telah dibuat dari template."
        echo "   PENTING: Edit file api_key.txt dan masukkan Gemini API Key Anda!"
        echo "   Dapatkan API Key di: https://aistudio.google.com/app/apikey"
    else
        echo "YOUR_GEMINI_API_KEY_HERE" > api_key.txt
        echo "⚠️  File api_key.txt telah dibuat."
        echo "   PENTING: Edit file api_key.txt dan masukkan Gemini API Key Anda!"
        echo "   Dapatkan API Key di: https://aistudio.google.com/app/apikey"
    fi
else
    echo "✅ File api_key.txt sudah ada"
fi
echo ""

# Setup knowledge_base.json
if [ ! -f "knowledge_base.json" ]; then
    echo "📚 Setup Knowledge Base..."
    if [ -f "knowledge_base.json.example" ]; then
        cp knowledge_base.json.example knowledge_base.json
        echo "⚠️  File knowledge_base.json telah dibuat dari template."
        echo "   Edit file ini dan masukkan data pengetahuan Anda!"
    else
        echo '[{"id":"example-1","title":"Example","text":"This is an example knowledge base entry.","source":"setup"}]' > knowledge_base.json
        echo "⚠️  File knowledge_base.json telah dibuat dengan contoh data."
        echo "   Edit file ini dan masukkan data pengetahuan Anda!"
    fi
else
    echo "✅ File knowledge_base.json sudah ada"
fi
echo ""

echo "=========================================="
echo "  ✅ Setup selesai!"
echo "=========================================="
echo ""
echo "📝 Langkah selanjutnya:"
echo "   1. Edit api_key.txt dan masukkan Gemini API Key Anda"
echo "   2. Edit knowledge_base.json dan masukkan data pengetahuan Anda"
echo "   3. Aktifkan virtual environment: source venv/bin/activate"
echo "   4. Jalankan API server: uvicorn api_yuki:app --reload"
echo "      atau CLI version: python3 YUKI.py"
echo ""
echo "📖 Dokumentasi lengkap ada di README.md"
echo ""
