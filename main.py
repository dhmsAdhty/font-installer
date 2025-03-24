import os
import zipfile
import shutil
import streamlit as st
import tempfile
import platform
from pathlib import Path

def is_real_windows():
    """Deteksi apakah benar-benar running di Windows lokal (bukan di cloud)"""
    return platform.system() == "Windows" and os.getenv('LOCALAPPDATA') is not None

def install_fonts_windows(font_path, filename):
    """Fungsi khusus instalasi font di Windows lokal"""
    try:
        fonts_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Windows', 'Fonts')
        os.makedirs(fonts_dir, exist_ok=True)
        
        temp_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'FontInstall')
        os.makedirs(temp_dir, exist_ok=True)
        
        with zipfile.ZipFile(font_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
            installed_fonts = []
            for file in Path(temp_dir).rglob('*'):
                if file.suffix.lower() in ['.ttf', '.otf', '.ttc']:
                    dest = os.path.join(fonts_dir, file.name)
                    shutil.copy2(file, dest)
                    installed_fonts.append(file.name)
            
            return installed_fonts
    except Exception as e:
        st.error(f"Gagal menginstall font: {str(e)}")
        return None
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    st.title("🔄 Font Installer Otomatis")
    
    if is_real_windows():
        st.success("🔍 Mode Windows lokal terdeteksi - instalasi otomatis aktif")
    else:
        st.warning("⚠️ Mode non-Windows - hanya ekstraksi file tersedia")
    
    uploaded_file = st.file_uploader("Unggah file ZIP berisi font", type=['zip'])
    
    if uploaded_file:
        temp_zip = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(temp_zip, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        if is_real_windows():
            # INSTALASI OTOMATIS UNTUK WINDOWS LOKAL
            installed_fonts = install_fonts_windows(temp_zip, uploaded_file.name)
            
            if installed_fonts:
                st.success("🎉 Font berhasil diinstall otomatis!")
                st.markdown(f"""
                **Lokasi instalasi:**  
                `AppData\\Local\\Microsoft\\Windows\\Fonts`
                
                **Langkah selanjutnya:**  
                1. Restart aplikasi yang menggunakan font  
                2. Font siap digunakan
                """)
                
                st.subheader("Font yang terinstall:")
                for font in installed_fonts:
                    st.write(f"✓ {font}")
        else:
            # EKSTRAK SAJA UNTUK NON-WINDOWS
            temp_dir = os.path.join(tempfile.gettempdir(), 'FontExtract')
            os.makedirs(temp_dir, exist_ok=True)
            
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                
                extracted_fonts = []
                for file in Path(temp_dir).rglob('*'):
                    if file.suffix.lower() in ['.ttf', '.otf', '.ttc']:
                        extracted_fonts.append(file.name)
                
                if extracted_fonts:
                    st.info("Font berhasil diekstrak (instalasi manual diperlukan)")
                    
                    # Buat ZIP untuk didownload
                    zip_path = os.path.join(tempfile.gettempdir(), 'extracted_fonts.zip')
                    with zipfile.ZipFile(zip_path, 'w') as zipf:
                        for file in Path(temp_dir).rglob('*'):
                            if file.is_file() and file.suffix.lower() in ['.ttf', '.otf', '.ttc']:
                                zipf.write(file, file.name)
                    
                    with open(zip_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download Font Pack",
                            data=f,
                            file_name="extracted_fonts.zip",
                            mime="application/zip"
                        )
        
        # Bersihkan file temporary
        os.unlink(temp_zip)

if __name__ == "__main__":
    main()