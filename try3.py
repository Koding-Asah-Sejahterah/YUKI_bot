import requests
import json
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

# Inisialisasi Rich Console
console = Console()

# --- 1. SETUP & LOAD DATA ---
api_key_file = "api_key.txt"
database_file = "knowledge_base.json"

console.print(Panel.fit("[bold cyan] YUKI [/bold cyan]", border_style="cyan"))

# Cek API Key
try:
    api_key = open(api_key_file).read().strip()
except FileNotFoundError:
    console.print(f"[bold red] Error: File '{api_key_file}' tidak ditemukan![/bold red]")
    exit()

# Load Database JSON (Hasil dari Notebook)
data_knowledge = []
try:
    with console.status("[bold green]Membaca database pengetahuan...[/bold green]", spinner="dots"):
        with open(database_file, "r", encoding="utf-8") as f:
            data_knowledge = json.load(f)
    console.print(f"[green] Berhasil memuat {len(data_knowledge)} baris data pengetahuan.[/green]")
except FileNotFoundError:
    console.print(f"[bold red] Error: File '{database_file}' tidak ditemukan![/bold red]")
    console.print("[yellow] Tips: Jalankan dulu notebook data preparation yang tadi kita buat.[/yellow]")
    exit()

# --- 2. INPUT USER ---
pertanyaan_user = console.input("\n[bold yellow]Kamu mau tanya apa ke Yuki? : [/bold yellow]")

# --- 3. FILTERING / SEARCH ENGINE SEDERHANA ---
# Kita cari data di JSON yang mengandung kata kunci dari pertanyaan user
# Tujuannya: Agar prompt tidak kepenuhan data yang tidak relevan.

stopwords = ['apa', 'itu', 'yang', 'di', 'ke', 'dari', 'bagaimana', 'cara', 'aku', 'mau', 'bisa', 'tolong']
kata_kunci = [k.lower() for k in pertanyaan_user.split() if k.lower() not in stopwords]

if not kata_kunci: # Fallback jika user cuma ketik stopwords
    kata_kunci = pertanyaan_user.lower().split()

context_relevan = ""
jumlah_relevan = 0

console.print(f"[dim] Mencari info tentang: {kata_kunci}[/dim]")

for item in data_knowledge:
    # item['content'] adalah teks yang sudah kita bersihkan di notebook
    isi_teks = item['content'].lower()

    # Cek apakah ADA kata kunci yang muncul di baris data ini
    if any(k in isi_teks for k in kata_kunci):
        context_relevan += f"\n--- REFERENSI DARI {item['source']} ---\n"
        context_relevan += item['content'] + "\n"
        jumlah_relevan += 1

if jumlah_relevan > 0:
    console.print(f"[bold green] Ditemukan {jumlah_relevan} poin data yang relevan![/bold green]\n")
else:
    console.print("[bold red]Tidak ditemukan data spesifik di file JSON.[/bold red] Yuki akan menjawab pakai pengetahuan umum.")

# --- 4. SIAPKAN REQUEST KE GEMINI ---
endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
headers = {"Content-type": "application/json"}

prompt_final = f"""
Peran: Kamu adalah asisten AI bernama Yuki.
Tugas: Jawab pertanyaan user dengan ramah dan informatif.
Gunakan data konteks di bawah ini sebagai sumber kebenaran utama.
Jika di konteks ada jawabannya, sebutkan sumbernya (nama filenya).

Data Konteks:
{context_relevan}

Pertanyaan User: {pertanyaan_user}
"""

payload = {"contents": [{"parts": [{"text": prompt_final}]}]}

# --- 5. KIRIM & TAMPILKAN ---
try:
    with console.status("[bold magenta]Yuki sedang berpikir...[/bold magenta]", spinner="dots"):
        response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        respon_data = response.json()
        try:
            jawaban_raw = respon_data["candidates"][0]["content"]["parts"][0]["text"]
            md_jawaban = Markdown(jawaban_raw)
            console.print(Panel(md_jawaban, title="[bold cyan] JAWABAN YUKI[/bold cyan]", border_style="cyan"))
        except KeyError:
            console.print("[bold red]Format respon API aneh.[/bold red]")
    else:
        console.print(f"[bold red]Error API: {response.status_code}[/bold red]")
        console.print(response.text)

except Exception as e:
    console.print(f"[bold red]Terjadi kesalahan koneksi: {e}[/bold red]")
