import os
import zipfile
import shutil
import streamlit as st
from pathlib import Path

def install_fonts(zip_path, original_filename):
    try:
        # Lokasi instalasi font user
        fonts_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'Fonts')
        os.makedirs(fonts_dir, exist_ok=True)
        
        # Folder temporary
        temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'FontInstall')
        os.makedirs(temp_dir, exist_ok=True)
        
        with st.spinner('Sedang mengekstrak font...'):
            st.write(f"Mengekstrak: {original_filename}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Install semua font
            installed_fonts = []
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf', '.ttc')):
                        src = os.path.join(root, file)
                        dst = os.path.join(fonts_dir, file)
                        shutil.copy2(src, dst)
                        installed_fonts.append(file)
            
            if installed_fonts:
                st.success("Instalasi font berhasil!")
                st.write("Font yang terinstal:")
                for font in installed_fonts:
                    st.write(f"✓ {font}")
                
                st.info("\nFont akan muncul setelah Anda:")
                st.write("- Restart aplikasi (Photoshop/Word dll)")
                st.write(f"- Lokasi font: `{fonts_dir}`")
            else:
                st.warning("Tidak ditemukan file font (.ttf/.otf/.ttc) dalam arsip.")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    st.title("📝 Instalasi Font untuk Windows")
    st.markdown("""
    Aplikasi ini memungkinkan Anda menginstal font di Windows **tanpa perlu hak administrator**.
    Font akan diinstal ke folder user lokal (`AppData\\Local\\Microsoft\\Windows\\Fonts`).
    """)
    
    st.warning("""
    **Perhatian:**
    - Hanya instal font dari sumber yang terpercaya
    - Font hanya akan tersedia untuk user yang menginstal
    """)
    
    uploaded_file = st.file_uploader("Unggah file ZIP berisi font", type=['zip'])
    
    if uploaded_file is not None:
        # Simpan file sementara
        temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_zip_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_zip_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        install_fonts(temp_zip_path, uploaded_file.name)
        
        # Hapus file temp
        try:
            os.unlink(temp_zip_path)
        except Exception as e:
            st.warning(f"Gagal menghapus file sementara: {e}")

if __name__ == "__main__":
    main()