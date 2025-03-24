import os
import zipfile
import shutil
import streamlit as st
import tempfile
import platform

def get_system_paths():
    """Mendapatkan path yang sesuai dengan sistem operasi"""
    if platform.system() == "Windows":
        return {
            'fonts_dir': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Windows', 'Fonts'),
            'temp_dir': os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'FontInstall')
        }
    else:
        return {
            'fonts_dir': os.path.join(tempfile.gettempdir(), 'Fonts'),
            'temp_dir': os.path.join(tempfile.gettempdir(), 'FontInstall')
        }

def install_fonts(zip_path, original_filename):
    try:
        paths = get_system_paths()
        fonts_dir = paths['fonts_dir']
        temp_dir = paths['temp_dir']
        
        os.makedirs(fonts_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        
        with st.spinner('Sedang mengekstrak font...'):
            st.write(f"Mengekstrak: {original_filename}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            installed_fonts = []
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf', '.ttc')):
                        src = os.path.join(root, file)
                        dst = os.path.join(fonts_dir, file)
                        shutil.copy2(src, dst)
                        installed_fonts.append(file)
            
            if installed_fonts:
                st.success("Proses ekstraksi font berhasil!")
                st.write("Font yang ditemukan:")
                for font in installed_fonts:
                    st.write(f"✓ {font}")
                
                if platform.system() == "Windows":
                    st.info("""
                    Instalasi font berhasil di sistem Windows!
                    Font akan muncul setelah:
                    1. Restart aplikasi (Photoshop/Word dll)
                    2. Lokasi font: `{}`
                    """.format(fonts_dir))
                else:
                    st.warning("""
                    [Untuk Pengguna Windows]
                    Silakan download font yang telah diekstrak dan instal manual:
                    1. Buka folder Fonts di Windows
                    2. Drag & drop file font ke folder tersebut
                    
                    Lokasi font yang diekstrak: `{}`
                    """.format(fonts_dir))
            else:
                st.warning("Tidak ditemukan file font (.ttf/.otf/.ttc) dalam arsip.")
    
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    st.title("📝 Font Installer (Windows)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://i.imgur.com/JtQ8FJo.png", width=150)
    with col2:
        st.markdown("""
        Aplikasi instalasi font untuk Windows
        - Tanpa perlu hak administrator
        - Instal hanya untuk user saat ini
        """)
    
    st.warning("""
    **Penting:**
    - Aplikasi ini bekerja penuh hanya di Windows
    - Di platform lain, font hanya akan diekstrak
    - Hanya gunakan font dari sumber terpercaya
    """)
    
    uploaded_file = st.file_uploader("Unggah file ZIP berisi font", type=['zip'])
    
    if uploaded_file is not None:
        temp_zip_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        
        with open(temp_zip_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        install_fonts(temp_zip_path, uploaded_file.name)
        
        try:
            os.unlink(temp_zip_path)
        except Exception as e:
            st.warning(f"Gagal menghapus file sementara: {e}")

if __name__ == "__main__":
    main()