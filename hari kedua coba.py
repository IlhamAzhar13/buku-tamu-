import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os

# Folder untuk menyimpan foto
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

# Nama file CSV untuk menyimpan data tamu
DATA_FILE = "buku_tamu.csv"

# Fungsi untuk menyimpan data tamu ke file CSV
def save_to_csv(data):
    if not os.path.exists(DATA_FILE):
        # Jika file belum ada, buat file dengan header
        df = pd.DataFrame([data])
        df.to_csv(DATA_FILE, index=False)
    else:
        # Jika file sudah ada, tambahkan data baru
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# Judul Aplikasi
st.markdown("<h1 style='text-align: center;'>Buku Tamu Digital</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Selamat Datang di Stasiun Geofisika Nganjuk</h2>", unsafe_allow_html=True)

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
        photo_path = os.path.join(PHOTO_DIR, photo_filename)

        # Menyimpan foto
        cv2.imwrite(photo_path, img)

        # Data tamu baru
        new_entry = {
            "Nama": nama,
            "Instansi": instansi,
            "Email": email,
            "Pesan": pesan,
            "Foto": photo_path,  # Path ke foto yang disimpan
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
        }

        # Simpan data ke CSV
        save_to_csv(new_entry)

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
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.dataframe(df)
else:
    st.write("Belum ada data tamu yang tersimpan.")
