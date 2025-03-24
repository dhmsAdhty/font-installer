# **Font Installer untuk Windows (Tanpa Admin)** 🚀

Skrip Python untuk meng-unzip dan menginstal font **tanpa perlu hak akses Administrator**, font akan terinstal hanya untuk user saat ini.

## 📌 **Fitur Utama**
- ✅ Instal font hanya untuk user yang login
- ✅ Tidak memerlukan hak admin sama sekali
- ✅ Support format TTF, OTF, TTC
- ✅ Auto-clean file temporary

## 🛠 **Cara Pakai**
1. Jalankan dengan:
```cmd
python main.py "C:\Users\[Username]\Downloads\font_kamu.zip"
```

## 📂 **Lokasi Font**
Font akan terinstal di:
```
C:\Users\[Username]\AppData\Local\Microsoft\Windows\Fonts
```

## 💡 **Catatan Penting**
1. Font hanya tersedia untuk user yang menginstal
2. Tidak perlu restart komputer
3. Jika font tidak muncul:
   - Restart aplikasi (Photoshop/Word dll)
   - Atau logoff & login kembali

## 🚨 **Jika Ada Masalah**
1. Pastikan Python sudah terinstal
2. Cek path file zip benar
3. Pastikan file zip tidak corrupt
