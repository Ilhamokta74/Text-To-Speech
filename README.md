# Text to Speech Bahasa Indonesia (Suara Microsoft Edge)

Skrip `tts_edge.py` mengubah teks bahasa Indonesia menjadi file MP3 memakai suara neural Microsoft Edge lewat paket `edge-tts`. Gratis, tanpa akun, dan ada progress bar saat berjalan.

## Isi folder

| File | Fungsi |
|------|--------|
| `tts_edge.py` | Skrip utama |
| `teks.txt` | Teks yang akan dibacakan (format UTF-8) |
| `hasil.mp3` | Hasil audio (dibuat otomatis) |

## Pemasangan (sekali saja)

1. Pasang Python dari python.org/downloads. Di layar pertama installer, **centang "Add python.exe to PATH"**, lalu klik Install Now.
2. Tutup dan buka lagi Command Prompt atau PowerShell, lalu cek:
   ```
   python --version
   ```
   Kalau muncul pesan Microsoft Store, coba `py --version` dan pakai `py` sebagai pengganti `python` di semua perintah di bawah.
3. Pasang paketnya:
   ```
   python -m pip install edge-tts
   ```

## Cara pakai cepat

1. Simpan teks di `teks.txt`, satu folder dengan `tts_edge.py`.
2. Buka Command Prompt di folder itu, lalu jalankan:
   ```
   python tts_edge.py
   ```
3. Hasilnya `hasil.mp3` dengan suara pria (Ardi).

## Daftar perintah

**Pilih suara**
```
python tts_edge.py --voice ardi
python tts_edge.py --voice gadis
```

**Atur kecepatan, nada, volume**
```
python tts_edge.py --rate=-10%
python tts_edge.py --rate=+15%
python tts_edge.py --pitch=+2Hz
python tts_edge.py --volume=+10%
```

**Ganti file masuk dan keluar**
```
python tts_edge.py --input cerita.txt --output cerita.mp3
python tts_edge.py -i cerita.txt -o cerita.mp3
```

**Teks langsung tanpa file**
```
python tts_edge.py --text "Halo, ini percobaan suara."
```

**Lihat daftar suara Indonesia**
```
python tts_edge.py --list
```

**Kombinasi yang direkomendasikan (narasi santai)**
```
python tts_edge.py --voice gadis --rate=-8% --input teks.txt --output cerita_gadis.mp3
python tts_edge.py --voice ardi --rate=-8% --input teks.txt --output cerita_ardi.mp3
```
Jalankan keduanya, lalu pilih yang paling enak didengar.

## Tabel opsi

| Opsi | Singkat | Default | Keterangan |
|------|---------|---------|------------|
| `--input` | `-i` | `teks.txt` | File teks sumber |
| `--text` | `-t` | - | Teks langsung, mengabaikan `--input` |
| `--output` | `-o` | `hasil.mp3` | Nama file hasil |
| `--voice` | `-v` | `ardi` | `ardi`, `gadis`, atau nama lengkap seperti `id-ID-GadisNeural` |
| `--rate` | - | `+0%` | Kecepatan bicara |
| `--pitch` | - | `+0Hz` | Tinggi rendah nada |
| `--volume` | - | `+0%` | Volume |
| `--list` | - | - | Tampilkan suara Indonesia lalu keluar |

## Progress bar

Saat berjalan, satu baris diperbarui terus di tempat:

```
Menghubungi server Microsoft ...
[##############----------------]  49%      12.0 KB  00:03
```

- Bar dan persen adalah perkiraan dari seberapa banyak teks yang sudah diproses server.
- KB adalah ukuran audio yang sudah diterima.
- Angka terakhir adalah waktu berjalan (menit:detik).
- Persen ditahan di 99% sampai file selesai disimpan.

## Tips biar suara tidak kaku

- Turunkan kecepatan sedikit: `--rate=-8%` sampai `--rate=-12%`.
- Coba kedua suara (Ardi dan Gadis), lalu bandingkan.
- Tulis teks dengan tanda baca lengkap. Titik dan koma memberi jeda yang natural.
- Hindari singkatan dan simbol. Tulis angka dan istilah seperti cara membacanya.

## Mengatasi masalah

| Masalah | Solusi |
|---------|--------|
| `Python was not found` muncul pesan Microsoft Store | Pasang Python dari python.org dengan opsi PATH dicentang, atau matikan alias di Settings > Apps > Advanced app settings > App execution aliases |
| `Paket edge-tts belum terpasang` | Jalankan `python -m pip install edge-tts` |
| `File 'teks.txt' tidak ditemukan` | Buat `teks.txt` di folder yang sama, atau pakai `--text "..."` |
| Error saat memakai `--rate -10%` | Tulis dengan tanda sama dengan: `--rate=-10%` |
| `Gagal membuat audio` | Pastikan internet aktif dan nama suara benar (cek dengan `--list`) |
| Jeda janggal di tengah kalimat | Teks di file terpotong per baris. Gabungkan baris-barisnya menjadi satu paragraf utuh |

## Catatan

- Skrip ini memakai layanan suara online Microsoft lewat paket `edge-tts`, jadi butuh koneksi internet.
- Ini bukan layanan resmi dengan jaminan ketersediaan, jadi kualitas dan ketersediaan suara bisa berubah sewaktu-waktu.
- Cek syarat penggunaan sebelum memakai hasilnya untuk keperluan komersial.
