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

def save_to_csv(data):
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame([data])
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# Tambahkan CSS untuk background dan estetika
def add_custom_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #004080;
            color: white;
            font-family: Arial, sans-serif;
        }
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_custom_styles()

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Form Buku Tamu", "Daftar Tamu"])

if menu == "Form Buku Tamu":
    st.image("logo.png", width=200, caption="Stasiun Geofisika Nganjuk", use_container_width=False)
    
    st.markdown("<div class='title'>Buku Tamu Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Selamat Datang di Stasiun Geofisika Nganjuk</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Formulir Buku Tamu")
    with st.form(key='guest_form'):
        nama = st.text_input("Nama", placeholder="Masukkan nama lengkap Anda")
        instansi = st.text_input("Instansi/Jabatan", placeholder="Masukkan nama instansi/jabatan Anda")
        email = st.text_input("No_Telpon", placeholder="Masukkan No_Telpon Anda")
        pesan = st.text_area("Keperluan", placeholder="Tulis keperluan kunjungan Anda")
        submit_button = st.form_submit_button(label="Kirim")
    
    st.subheader("Scan Wajah Anda")
    image_file = st.camera_input("Ambil Foto Wajah Anda")
    
    if submit_button:
        if nama and instansi and email and pesan and image_file:
            img = cv2.imdecode(np.frombuffer(image_file.getvalue(), np.uint8), 1)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            photo_filename = f"{nama.replace(' ', '_')}_{timestamp}.jpg"
            photo_path = os.path.join(PHOTO_DIR, photo_filename)
            cv2.imwrite(photo_path, img)
            
            new_entry = {
                "Nama": nama,
                "Instansi/Jabatan": instansi,
                "No_Telpon": email,
                "Pesan": pesan,
                "Foto": photo_path,
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            save_to_csv(new_entry)
            st.success(f"Terima kasih, {nama}! Data Anda telah berhasil disimpan.")
            st.image(img, caption="Foto Wajah Anda", use_container_width=True)
            
            st.subheader("Data Tamu")
            st.write(f"**Nama:** {nama}")
            st.write(f"**Instansi\Jabatan:** {instansi}")
            st.write(f"**Email:** {email}")
            st.write(f"**Pesan:** {pesan}")
            st.write(f"**Foto Tersimpan di:** {photo_path}")
        else:
            st.error("Semua kolom dan foto wajib diisi!")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Daftar Tamu":
    st.markdown("<div class='title'>Daftar Tamu</div>", unsafe_allow_html=True)
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.dataframe(df)
        
        if st.button("Hapus Semua Data"):
            os.remove(DATA_FILE)
            st.warning("Semua data tamu telah dihapus!")
    else:
        st.write("Belum ada data tamu yang tersimpan.")

# Footer
st.markdown(
    """
    <hr style="border:1px solid white;">
    <p style="text-align: center; color: white; font-size: 16px;">
        Dibuat oleh: <strong>Mahasiswa KP Fisika'22 UIN Sunan Kalijaga Yogyakarta</strong>
    </p>
    """,
    unsafe_allow_html=True
)
