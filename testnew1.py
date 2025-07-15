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
DATA_FILE = r"D:\TESTING KP\Buku Tamu BMKG\buku_tamu.csv"

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
        </style>
        <div class="main-container">
        """,
        unsafe_allow_html=True
    )

# Tambahkan background
add_bg_from_local(r"D:\TESTING KP\Buku Tamu BMKG\new2.jpeg")

# Halaman Utama atau Daftar Tamu
menu = st.sidebar.selectbox("Menu", ["Form Buku Tamu", "Daftar Tamu"])

if menu == "Form Buku Tamu":
    col1, col2, col3 =  st.columns([1,0.5,1])
    with col2:
        st.image(
            r"D:\TESTING KP\Buku Tamu BMKG\logo.png",
            width=100,
            use_container_width=False
        )

    st.markdown("<h1 style='text-align: center; color: White;'>Buku Tamu Digital</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: White;'>Selamat Datang di Stasiun Geofisika Nganjuk</h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: white;'>Formulir Buku Tamu</h3>", unsafe_allow_html=True)
    with st.form(key='guest_form'):
        nama = st.text_input("Nama", placeholder="Masukkan nama lengkap Anda", key="nama")
        instansi_Jabatan = st.text_input("Instansi/Jabatan", placeholder="Masukkan nama instansi atau jabatan Anda", key="instansi")
        no_telpon = st.text_input("No_Telpon", placeholder="Masukkan no telpon Anda", key="no_telpon")
        keperluan = st.text_area("Keperluan", placeholder="Tulis keperluan kunjungan Anda", key="keperluan")

        st.markdown("<h4 style='color: white;'>Scan Wajah Anda</h4>", unsafe_allow_html=True)
        image_file = st.camera_input("Ambil Foto Wajah Anda", key="foto")

        col1, col2, col3 = st.columns([1,0.3,1])
        with col2:
            submit_button = st.form_submit_button(label="Kirim")

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

            # Reset dengan reload halaman
            st.rerun()
        else:
            st.error("Semua kolom dan foto wajib diisi!")

elif menu == "Daftar Tamu":
    st.markdown("<h1 style='text-align: center; color: White;'>Daftar Tamu</h1>", unsafe_allow_html=True)
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.dataframe(df)
    else:
        st.write("Belum ada data tamu yang tersimpan.")

# Footer
st.markdown(
    """
    </div>
    <hr style="border:1px solid white;">
    <p style="text-align: center; color: white; font-size: 16px;">
        Dibuat oleh: <strong>Stasiun Geofisika Nganjuk X Fisika'22 UM</strong>
    </p>
    """,
    unsafe_allow_html=True
)
