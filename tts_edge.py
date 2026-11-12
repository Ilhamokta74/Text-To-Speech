import argparse
import asyncio
import sys
import time
from pathlib import Path

try:
    import edge_tts
except ImportError:
    sys.exit("Paket edge-tts belum terpasang. Jalankan: python -m pip install edge-tts")

VOICES = {
    "ardi": "id-ID-ArdiNeural",    # pria
    "gadis": "id-ID-GadisNeural",  # wanita
}


async def list_voices() -> None:
    voices = await edge_tts.list_voices()
    for v in voices:
        if v["Locale"].lower().startswith("id-"):
            print(f'{v["ShortName"]}  ({v["Gender"]})')


BAR_WIDTH = 30


def render_progress(done: int, total: int, received: int, elapsed: float, final: bool = False) -> None:
    """Tampilkan baris progres yang ditimpa terus (satu baris saja)."""
    kb = received / 1024
    mm, ss = divmod(int(elapsed), 60)
    if done > 0 or final:
        pct = 1.0 if final else min(done / total, 0.99)
        filled = int(pct * BAR_WIDTH)
        bar = "#" * filled + "-" * (BAR_WIDTH - filled)
        line = f"[{bar}] {pct * 100:3.0f}%  {kb:8.1f} KB  {mm:02d}:{ss:02d}"
    else:
        line = f"Menerima audio...  {kb:8.1f} KB  {mm:02d}:{ss:02d}"
    sys.stdout.write("\r" + line + "    ")
    sys.stdout.flush()


async def synthesize(text: str, voice: str, rate: str, pitch: str, volume: str, output: Path) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)

    total_chars = max(len(text), 1)
    spoken_chars = 0   # estimasi seberapa banyak teks yang sudah diproses server
    received = 0       # jumlah byte audio yang sudah diterima
    start = time.time()

    print("Menghubungi server Microsoft ...")
    with open(output, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
                received += len(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                spoken_chars += len(chunk.get("text", "")) + 1
            render_progress(spoken_chars, total_chars, received, time.time() - start)

    render_progress(spoken_chars, total_chars, received, time.time() - start, final=True)
    sys.stdout.write("\n")
    sys.stdout.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description="Text to speech bahasa Indonesia (Microsoft Edge).")
    parser.add_argument("--input", "-i", default="teks.txt", help="file teks sumber (default: teks.txt)")
    parser.add_argument("--text", "-t", help="teks langsung, mengabaikan --input")
    parser.add_argument("--output", "-o", default="hasil.mp3", help="nama file hasil (default: hasil.mp3)")
    parser.add_argument("--voice", "-v", default="ardi",
                        help="ardi, gadis, atau nama suara lengkap seperti id-ID-GadisNeural")
    parser.add_argument("--rate", default="+0%", help="kecepatan, contoh --rate=-10%% atau --rate=+15%%")
    parser.add_argument("--pitch", default="+0Hz", help="nada, contoh --pitch=+2Hz")
    parser.add_argument("--volume", default="+0%", help="volume, contoh --volume=+10%%")
    parser.add_argument("--list", action="store_true", help="tampilkan daftar suara Indonesia lalu keluar")
    args = parser.parse_args()

    if args.list:
        asyncio.run(list_voices())
        return

    if args.text:
        text = args.text
    else:
        path = Path(args.input)
        if not path.exists():
            sys.exit(f"File '{path}' tidak ditemukan. Buat file itu dulu, atau pakai --text \"...\".")
        text = path.read_text(encoding="utf-8").strip()

    if not text:
        sys.exit("Teks kosong, tidak ada yang dibacakan.")

    voice = VOICES.get(args.voice.lower(), args.voice)
    output = Path(args.output)

    print(f"Membuat audio dengan suara {voice} ...")
    try:
        asyncio.run(synthesize(text, voice, args.rate, args.pitch, args.volume, output))
    except Exception as exc:
        sys.exit(f"\nGagal membuat audio: {exc}\nPastikan koneksi internet aktif dan nama suara benar.")

    print(f"Selesai: {output.resolve()}")


if __name__ == "__main__":
    main()