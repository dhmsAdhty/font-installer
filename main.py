import os
import zipfile
import shutil
from pathlib import Path

def install_fonts(zip_path):
    # Lokasi instalasi font user
    fonts_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'Fonts')
    os.makedirs(fonts_dir, exist_ok=True)
    
    # Folder temporary
    temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'FontInstall')
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        print(f"Mengekstrak: {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Install semua font
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith(('.ttf', '.otf', '.ttc')):
                    src = os.path.join(root, file)
                    dst = os.path.join(fonts_dir, file)
                    shutil.copy2(src, dst)
                    print(f"✓ Berhasil instal: {file}")
        
        print("\nInstalasi selesai! Font akan muncul setelah Anda:")
        print("- Restart aplikasi (Photoshop/Word dll)")
        print("- C:\Users\[Username]\AppData\Local\Microsoft\Windows\Fonts")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Cara pakai: python install_fonts_user.py [file_zip_font]")
    else:
        install_fonts(sys.argv[1])