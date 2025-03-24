import os
import zipfile
import shutil
import streamlit as st
import tempfile
import platform
from pathlib import Path

def install_fonts_windows(font_path, filename):
    """Fungsi khusus untuk instalasi font di Windows"""
    try:
        # Path khusus Windows
        fonts_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Windows', 'Fonts')
        os.makedirs(fonts_dir, exist_ok=True)
        
        # Ekstrak dan install
        with zipfile.ZipFile(font_path, 'r') as zip_ref:
            with st.spinner(f'Menginstall {filename}...'):
                # Ekstrak ke folder temporary
                temp_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'FontInstall')
                os.makedirs(temp_dir, exist_ok=True)
                zip_ref.extractall(temp_dir)
                
                # Proses instalasi
                installed = []
                for file in Path(temp_dir).rglob('*'):
                    if file.suffix.lower() in ['.ttf', '.otf', '.ttc']:
                        shutil.copy2(file, os.path.join(fonts_dir, file.name))
                        installed.append(file.name)
                
                return installed
    except Exception as e:
        st.error(f"Gagal menginstall font: {str(e)}")
        return None
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def extract_fonts_non_windows(font_path, filename):
    """Fungsi untuk ekstrak font di non-Windows"""
    try:
        temp_dir = os.path.join(tempfile.gettempdir(), 'FontExtract')
        os.makedirs(temp_dir, exist_ok=True)
        
        with zipfile.ZipFile(font_path, 'r') as zip_ref:
            with st.spinner(f'Mengekstrak {filename}...'):
                zip_ref.extractall(temp_dir)
                
                # List semua font yang diekstrak
                fonts = []
                for file in Path(temp_dir).rglob('*'):
                    if file.suffix.lower() in ['.ttf', '.otf', '.ttc']:
                        fonts.append(file.name)
                
                return temp_dir, fonts
    except Exception as e:
        st.error(f"Gagal mengekstrak font: {str(e)}")
        return None, None

def main():
    st.title("🚀 Font Installer Otomatis")
    st.markdown("""
    **Aplikasi untuk menginstall font secara otomatis di Windows**  
    *Untuk pengguna non-Windows, font akan diekstrak untuk instalasi manual*
    """)
    
    uploaded_file = st.file_uploader("Unggah file ZIP berisi font", type=['zip'])
    
    if uploaded_file:
        # Simpan file zip sementara
        temp_zip = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(temp_zip, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        if platform.system() == "Windows":
            # Instalasi otomatis untuk Windows
            installed_fonts = install_fonts_windows(temp_zip, uploaded_file.name)
            
            if installed_fonts:
                st.success("✅ Font berhasil diinstall!")
                st.markdown("""
                **Langkah selanjutnya:**
                1. Restart aplikasi (Photoshop/Word/etc)
                2. Font akan tersedia di semua aplikasi
                """)
                
                st.subheader("Font yang terinstall:")
                for font in installed_fonts:
                    st.write(f"- {font}")
        else:
            # Ekstrak saja untuk non-Windows
            extract_dir, extracted_fonts = extract_fonts_non_windows(temp_zip, uploaded_file.name)
            
            if extracted_fonts:
                st.warning("""
                ⚠️ Sistem Anda bukan Windows
                **Silakan install font secara manual:**
                1. Download file font di bawah
                2. Buka file font
                3. Klik "Install" di preview font
                """)
                
                st.subheader("Font yang diekstrak:")
                for font in extracted_fonts:
                    st.write(f"- {font}")
                
                # Buat ZIP untuk didownload
                zip_path = os.path.join(tempfile.gettempdir(), 'extracted_fonts.zip')
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for file in Path(extract_dir).rglob('*'):
                        if file.is_file():
                            zipf.write(file, file.name)
                
                with open(zip_path, 'rb') as f:
                    st.download_button(
                        label="📥 Download Font",
                        data=f,
                        file_name="extracted_fonts.zip",
                        mime="application/zip"
                    )
        
        # Bersihkan file temporary
        os.unlink(temp_zip)

if __name__ == "__main__":
    main()