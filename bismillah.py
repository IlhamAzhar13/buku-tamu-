import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os
import base64

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
        """,
        unsafe_allow_html=True
    )

# Tambahkan background
add_bg_from_local("background.jpg")

# Menampilkan logo
st.image("logo.png", width=200, caption="Stasiun Geofisika Nganjuk")

# Judul Aplikasi
st.markdown("<h1 style='text-align: center; color: white;'>Buku Tamu Digital</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Selamat Datang di Stasiun Geofisika Nganjuk</h2>", unsafe_allow_html=True)

# Form Input Buku Tamu
st.subheader("Formulir Buku Tamu")
with st.form(key='guest_form'):
    nama = st.text_input("Nama", placeholder="Masukkan nama lengkap Anda")
    instansi = st.text_input("Instansi", placeholder="Masukkan nama instansi Anda")
    email = st.text_input("Email", placeholder="Masukkan email Anda")
    pesan = st.text_area("Pesan", placeholder="Tulis pesan atau tujuan kunjungan Anda")
    submit_button = st.form_submit_button(label="Kirim")

# Scan Wajah
st.subheader("Scan Wajah Anda")
image_file = st.camera_input("Ambil Foto Wajah Anda")

# Menyimpan Data dan Foto
if submit_button:
    if nama and instansi and email and pesan and image_file:
        # Mengambil gambar dari kamera
        img = cv2.imdecode(np.frombuffer(image_file.getvalue(), np.uint8), 1)

        # Membuat nama file untuk foto
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_filename = f"{nama.replace(' ', '_')}_{timestamp}.jpg"
        photo_path = os.path.join("photos", photo_filename)

        # Menyimpan foto
        os.makedirs("photos", exist_ok=True)
        cv2.imwrite(photo_path, img)

        # Data tamu baru
        new_entry = {
            "Nama": nama,
            "Instansi": instansi,
            "Email": email,
            "Pesan": pesan,
            "Foto": photo_path,
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Simpan data ke CSV
        DATA_FILE = "buku_tamu.csv"
        if not os.path.exists(DATA_FILE):
            pd.DataFrame([new_entry]).to_csv(DATA_FILE, index=False)
        else:
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

        # Menampilkan pesan sukses
        st.success(f"Terima kasih, {nama}! Data Anda telah berhasil disimpan.")
        st.image(img, caption="Foto Wajah Anda", use_column_width=True)

        # Menampilkan ringkasan data tamu
        st.subheader("Data Tamu")
        st.write(f"**Nama:** {nama}")
        st.write(f"**Instansi:** {instansi}")
        st.write(f"**Email:** {email}")
        st.write(f"**Pesan:** {pesan}")
        st.write(f"**Foto Tersimpan di:** {photo_path}")
    else:
        st.error("Semua kolom dan foto wajib diisi!")

# Menampilkan Data Buku Tamu
st.subheader("Data Buku Tamu")
DATA_FILE = "buku_tamu.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.dataframe(df)
else:
    st.write("Belum ada data tamu yang tersimpan.")
