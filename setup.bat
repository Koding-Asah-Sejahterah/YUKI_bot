@echo off
REM YUKI Bot Setup Script for Windows
REM Script ini membantu setup environment untuk menjalankan YUKI Bot

echo ==========================================
echo   YUKI Bot - Setup Script (Windows)
echo ==========================================
echo.

REM Cek Python version
echo [1/6] Memeriksa versi Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan. Silakan install Python 3.8 atau lebih tinggi.
    echo Download dari: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo [OK] Python ditemukan
echo.

REM Buat virtual environment jika belum ada
if not exist "venv" (
    echo [2/6] Membuat virtual environment...
    python -m venv venv
    echo [OK] Virtual environment berhasil dibuat
) else (
    echo [2/6] Virtual environment sudah ada
)
echo.

REM Aktifkan virtual environment
echo [3/6] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment aktif
echo.

REM Upgrade pip
echo [4/6] Mengupgrade pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip berhasil diupgrade
echo.

REM Install dependencies
echo [5/6] Menginstall dependencies dari requirements.txt...
echo       (Ini mungkin memakan waktu beberapa menit...)
pip install -r requirements.txt --quiet
echo [OK] Dependencies berhasil diinstall
echo.

REM Setup api_key.txt
echo [6/6] Setup konfigurasi...
if not exist "api_key.txt" (
    if exist "api_key.txt.example" (
        copy api_key.txt.example api_key.txt >nul
    ) else (
        echo YOUR_GEMINI_API_KEY_HERE > api_key.txt
    )
    echo [WARNING] File api_key.txt telah dibuat.
    echo           PENTING: Edit file api_key.txt dan masukkan Gemini API Key Anda!
    echo           Dapatkan API Key di: https://aistudio.google.com/app/apikey
) else (
    echo [OK] File api_key.txt sudah ada
)

REM Setup knowledge_base.json
if not exist "knowledge_base.json" (
    if exist "knowledge_base.json.example" (
        copy knowledge_base.json.example knowledge_base.json >nul
    ) else (
        echo [{"id":"example-1","title":"Example","text":"This is an example knowledge base entry.","source":"setup"}] > knowledge_base.json
    )
    echo [WARNING] File knowledge_base.json telah dibuat.
    echo           Edit file ini dan masukkan data pengetahuan Anda!
) else (
    echo [OK] File knowledge_base.json sudah ada
)
echo.

echo ==========================================
echo   [SUCCESS] Setup selesai!
echo ==========================================
echo.
echo Langkah selanjutnya:
echo   1. Edit api_key.txt dan masukkan Gemini API Key Anda
echo   2. Edit knowledge_base.json dan masukkan data pengetahuan Anda
echo   3. Aktifkan virtual environment: venv\Scripts\activate
echo   4. Jalankan API server: uvicorn api_yuki:app --reload
echo      atau CLI version: python YUKI.py
echo.
echo Dokumentasi lengkap ada di README.md
echo.
pause
