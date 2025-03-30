import os
import zipfile
import shutil
import tempfile
import platform
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def install_fonts(zip_path):
    """Fungsi instalasi font di Windows"""
    try:
        # Path instalasi font Windows
        fonts_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Windows', 'Fonts')
        os.makedirs(fonts_dir, exist_ok=True)
        
        # Folder temporary
        temp_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'FontInstall')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Ekstrak ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
            installed_fonts = []
            for file in Path(temp_dir).rglob('*'):
                if file.suffix.lower() in ['.ttf', '.otf', '.ttc']:
                    dest = os.path.join(fonts_dir, file.name)
                    shutil.copy2(file, dest)
                    installed_fonts.append(file.name)
            
            return installed_fonts
    except Exception as e:
        raise e
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def select_file():
    """GUI untuk memilih file"""
    root = tk.Tk()
    root.withdraw()  # Sembunyikan window utama
    
    file_path = filedialog.askopenfilename(
        title="Pilih file ZIP berisi font",
        filetypes=[("ZIP files", "*.zip")]
    )
    
    return file_path

def main():
    # Buat GUI sederhana
    root = tk.Tk()
    root.title("Font Installer for Windows")
    root.geometry("500x400")
    
    def on_install():
        file_path = select_file()
        if file_path:
            try:
                installed = install_fonts(file_path)
                if installed:
                    message = "Font berhasil diinstall:\n\n" + "\n".join(f"✓ {f}" for f in installed)
                    message += "\n\nLokasi: AppData\\Local\\Microsoft\\Windows\\Fonts"
                    message += "\n\nRestart aplikasi untuk melihat font baru"
                    messagebox.showinfo("Sukses", message)
                else:
                    messagebox.showwarning("Peringatan", "Tidak ditemukan font yang valid dalam file ZIP")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menginstall font:\n{str(e)}")
    
    # UI Elements
    tk.Label(
        root, 
        text="Font Installer for Windows",
        font=("Arial", 16, "bold")
    ).pack(pady=20)
    
    tk.Label(
        root,
        text="Aplikasi ini akan menginstall font ke sistem Windows Anda\nTanpa perlu hak administrator",
        wraplength=400
    ).pack(pady=10)
    
    tk.Button(
        root,
        text="Pilih File ZIP Font",
        command=on_install,
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10,
        font=("Arial", 12)
    ).pack(pady=30)
    
    tk.Label(
        root,
        text="Pastikan file ZIP berisi file font (.ttf/.otf)",
        font=("Arial", 9)
    ).pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()