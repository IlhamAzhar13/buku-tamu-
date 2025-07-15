import streamlit as st
import pandas as pd
import cv2
import numpy as np
import os
from datetime import datetime
import base64

# Folder untuk menyimpan foto
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

# Nama file CSV untuk menyimpan data tamu
DATA_FILE = "buku_tamu.csv"

# Fungsi untuk menyimpan data tamu ke file CSV
def save_to_csv(data):
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame([data])
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# Fungsi untuk menambahkan background dari file lokal
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        bg_image = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{bg_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .main-container {{
            background-color: rgba(0, 0, 0, 0.8);
            padding: 20px;
            border-radius: 10px;
            color: white;
        }}
        </style>
        <div class="main-container">
        """,
        unsafe_allow_html=True
    )

# Tambahkan background
add_bg_from_local(r"D:\TESTING KP\Buku Tamu BMKG\background.jpg")

# Halaman Utama atau Daftar Tamu
menu = st.sidebar.selectbox("Menu", ["Form Buku Tamu", "Daftar Tamu"])

if menu == "Form Buku Tamu":
    # Tampilkan logo
    st.image(
        r"D:\TESTING KP\Buku Tamu BMKG\logo.png",
        width=200,
        caption="Stasiun Geofisika Nganjuk",
        use_container_width=False
    )

    # Judul Aplikasi
    st.markdown("<h1 style='text-align: center; color: cyan;'>Buku Tamu Digital</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: lightgreen;'>Selamat Datang di Stasiun Geofisika Nganjuk</h2>", unsafe_allow_html=True)

    # Form Input Buku Tamu
    st.markdown("<h3 style='color: white;'>Formulir Buku Tamu</h3>", unsafe_allow_html=True)
    with st.form(key='guest_form'):
        nama = st.text_input("Nama", placeholder="Masukkan nama lengkap Anda")
        instansi_Jabatan = st.text_input("Instansi/Jabatan", placeholder="Masukkan nama instansi atau jabatan Anda")
        no_telpon = st.text_input("No_Telpon", placeholder="Masukkan no telpon Anda")
        keperluan = st.text_area("Keperluan", placeholder="Tulis keperluan kunjungan Anda")

    # Scan Wajah
        st.markdown("<h4 style='color: white;'>Scan Wajah Anda</h4>", unsafe_allow_html=True)
        image_file = st.camera_input("Ambil Foto Wajah Anda")
        
        submit_button = st.form_submit_button(label="Kirim")
    # Menyimpan Data dan Foto
    if submit_button:
        if nama and instansi_Jabatan and no_telpon and keperluan and image_file:
            img = cv2.imdecode(np.frombuffer(image_file.getvalue(), np.uint8), 1)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            photo_filename = f"{nama.replace(' ', '_')}_{timestamp}.jpg"
            photo_path = os.path.join(PHOTO_DIR, photo_filename)

            cv2.imwrite(photo_path, img)

            new_entry = {
                "Nama": nama,
                "Instansi_Jabatan": instansi_Jabatan,
                "No_telpon": no_telpon,
                "Keperluan": keperluan,
                "Foto": photo_path,
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            save_to_csv(new_entry)
            st.success(f"Terima kasih, {nama}! Data Anda telah berhasil disimpan.")
            st.image(img, caption="Foto Wajah Anda", use_container_width=True)

            st.subheader("Data Tamu")
            st.write(f"**Nama:** {nama}")
            st.write(f"**Instansi_Jabatan:** {instansi_Jabatan}")
            st.write(f"**No_telpon:** {no_telpon}")
            st.write(f"**Keperluan:** {keperluan}")
            st.write(f"**Foto Tersimpan di:** {photo_path}")
        else:
            st.error("Semua kolom dan foto wajib diisi!")

elif menu == "Daftar Tamu":
    # Halaman Daftar Tamu
    st.markdown("<h1 style='text-align: center; color: cyan;'>Daftar Tamu</h1>", unsafe_allow_html=True)
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.dataframe(df)
    else:
        st.write("Belum ada data tamu yang tersimpan.")

# Footer: Dibuat oleh
st.markdown(
    """
    </div>
    <hr style="border:1px solid white;">
    <p style="text-align: center; color: yellow; font-size: 16px;">
        Dibuat oleh: <strong> BMKG Nganjuk dan Mahasiswa KP Fisika'22 UIN Sunan Kalijaga </strong>
    </p>
    """,
    unsafe_allow_html=True
)
