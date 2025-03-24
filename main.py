import os
import zipfile
import shutil
import streamlit as st
import tempfile
import platform
from pathlib import Path

def get_install_path():
    """Mendapatkan path instalasi yang sesuai dengan OS"""
    if platform.system() == "Windows":
        return os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Windows', 'Fonts')
    else:
        return os.path.join(tempfile.gettempdir(), 'FontCache')

def install_fonts(font_path, filename):
    try:
        fonts_dir = get_install_path()
        os.makedirs(fonts_dir, exist_ok=True)
        
        # Folder temporary untuk ekstraksi
        temp_dir = os.path.join(tempfile.gettempdir(), 'FontInstall')
        os.makedirs(temp_dir, exist_ok=True)
        
        with zipfile.ZipFile(font_path, 'r') as zip_ref:
            with st.spinner(f'Memproses {filename}...'):
                zip_ref.extractall(temp_dir)
                
                installed_fonts = []
                for file in Path(temp_dir).rglob('*'):
                    if file.suffix.lower() in ['.ttf', '.otf', '.ttc']:
                        dest = os.path.join(fonts_dir, file.name)
                        shutil.copy2(file, dest)
                        installed_fonts.append(file.name)
                
                return fonts_dir, installed_fonts
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    st.title("📁 Font Installer Universal")
    
    # Peringatan untuk non-Windows
    if platform.system() != "Windows":
        st.warning("""
        ⚠️ Fitur instalasi otomatis hanya tersedia untuk Windows
        Anda dapat mengekstrak dan mendownload font untuk instalasi manual
        """)
    
    st.markdown("""
    **Fitur:**
    - ✔️ Auto-install font di Windows
    - ✔️ Ekstrak font untuk platform lain
    - ✔️ Support file ZIP berisi banyak font
    """)
    
    uploaded_file = st.file_uploader("Unggah file ZIP berisi font", type=['zip'])
    
    if uploaded_file:
        # Simpan file sementara
        temp_zip = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(temp_zip, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        fonts_dir, installed_fonts = install_fonts(temp_zip, uploaded_file.name)
        
        if installed_fonts:
            if platform.system() == "Windows":
                st.success("🎉 Font berhasil diinstall!")
                st.markdown(f"""
                **Lokasi instalasi:**  
                `{fonts_dir}`
                
                **Langkah selanjutnya:**  
                1. Restart aplikasi (Photoshop/Word/etc)  
                2. Font akan tersedia untuk digunakan
                """)
            else:
                st.info("""
                Font berhasil diekstrak! Silakan download untuk instalasi manual:
                """)
                
                # Buat ZIP dari font yang diekstrak
                zip_path = os.path.join(tempfile.gettempdir(), 'fonts_to_install.zip')
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for font in installed_fonts:
                        zipf.write(os.path.join(fonts_dir, font), font)
                
                # Tombol download
                with open(zip_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Font Pack",
                        data=f,
                        file_name="fonts_to_install.zip",
                        mime="application/zip"
                    )
                
                st.markdown("""
                **Cara instalasi manual:**
                1. Ekstrak file ZIP yang didownload
                2. Untuk Windows:
                   - Klik kanan masing-masing file font
                   - Pilih "Install"
                3. Untuk Mac:
                   - Buka Font Book
                   - Drag file font ke aplikasi
                4. Untuk Linux:
                   - Salin file ke ~/.fonts atau /usr/share/fonts
                """)
            
            st.subheader("Daftar Font:")
            cols = st.columns(3)
            for i, font in enumerate(installed_fonts):
                cols[i % 3].write(f"🔠 {font}")
        
        # Bersihkan file sementara
        os.unlink(temp_zip)

if __name__ == "__main__":
    main()