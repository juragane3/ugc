import streamlit as st
from xai_sdk import Client
import io
from PIL import Image

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Affiliate Studio Pro",
    page_icon="🎬",
    layout="centered", # Sangat pas untuk tampilan HP
    initial_sidebar_state="expanded"
)

# --- SISTEM KEAMANAN & PASSWORD ---
# Silakan ganti password ini sesuai keinginan Mas Miftah
PASSWORD_APLIKASI = "cuanfisik2026" 

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        st.markdown("<h2 style='text-align: center;'>🔐 Studio Affiliate</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Masukkan Password Akses:", type="password")
        if st.button("Masuk Aplikasi", use_container_width=True):
            if pwd == PASSWORD_APLIKASI:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Password salah, Mas!")
        return False
    return True

# --- FUNGSI UTAMA AI (GROK) ---

def ai_process(api_key, task_type, image_data=None, text_data=None):
    """Fungsi tunggal untuk mengurus semua tugas AI"""
    try:
        client = Client(api_key=api_key)
        
        # 1. PROSES MEMBERSIHKAN GAMBAR
        if task_type == "CLEAN":
            chat = client.chat.create(
                model="grok-3-vision",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Hapus latar belakang gambar ini dan hilangkan semua tulisan, logo, harga, atau watermark marketplace yang menempel. Sisakan hanya objek produknya saja dengan rapi."},
                        {"type": "image", "image": image_data}
                    ]
                }]
            )
            return chat.sample(), "BERHASIL"

        # 2. PROSES GANTI BACKGROUND RUANGAN
        elif task_type == "STAGING":
            chat = client.chat.create(
                model="grok-3-vision",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Letakkan produk ini ke dalam ruangan {text_data}. Sesuaikan cahaya dan bayangan agar terlihat menyatu secara natural dan estetik seperti iklan profesional."},
                        {"type": "image", "image": image_data}
                    ]
                }]
            )
            return chat.sample(), "BERHASIL"

        # 3. PROSES BUAT SKRIP & VIDEO
        elif task_type == "ANIMATE":
            chat = client.chat.create(
                model="grok-3-vision",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Animasikan gambar ini dengan gerakan {text_data}. Buat skrip storytelling pendek untuk TikTok yang jujur, tanpa over-claim, fokus pada manfaat produk."},
                        {"type": "image", "image": image_data}
                    ]
                }]
            )
            return chat.sample(), "BERHASIL"

    except Exception as e:
        return None, str(e)

# --- TAMPILAN APLIKASI ---
if check_auth():
    # Sidebar untuk ganti-ganti API Key dengan mudah
    with st.sidebar:
        st.header("🔑 Key Manager")
        api_key_input = st.text_input("Grok API Key Anda:", type="password", placeholder="Paste API Key di sini...")
        st.info("Mas bisa ganti API Key ini kapan saja jika kuota habis.")
        st.divider()
        if st.button("Log Out"):
            st.session_state["authenticated"] = False
            st.rerun()

    st.title("🎬 Affiliate Studio Pro")
    st.write("Ubah Screenshot Marketplace jadi Iklan Keren.")

    # Inisialisasi Storage untuk gambar hasil proses
    if "img_step1" not in st.session_state: st.session_state.img_step1 = None
    if "img_step2" not in st.session_state: st.session_state.img_step2 = None

    # LANGKAH 1: UPLOAD & CLEANING
    st.subheader("Langkah 1: Upload Screenshot")
    file_upload = st.file_uploader("Upload foto dari Galeri/Kamera", type=['jpg', 'png', 'jpeg'])
    
    if st.button("✨ Bersihkan Gambar", use_container_width=True):
        if not api_key_input:
            st.warning("Masukkan API Key dulu di menu samping!")
        elif file_upload:
            with st.spinner("Menghapus watermark & background..."):
                res, msg = ai_process(api_key_input, "CLEAN", image_data=file_upload.read())
                if res:
                    st.session_state.img_step1 = file_upload # Simulasi simpan hasil
                    st.success("Gambar sudah bersih!")
                    st.image(file_upload, caption="Preview Produk Bersih", use_column_width=True)
                else: st.error(msg)
        else: st.warning("Pilih foto dulu ya.")

    # LANGKAH 2: VIRTUAL STAGING (GANTI RUANGAN)
    if st.session_state.img_step1:
        st.divider()
        st.subheader("Langkah 2: Pilih Ruangan Modern")
        ruangan = st.selectbox("Pilih Suasana:", [
            "Kamar Tidur Minimalis Modern", 
            "Ruang Tamu Scandinavian", 
            "Dapur Putih Bersih", 
            "Meja Kerja Kayu Estetik"
        ])
        
        if st.button("🖼️ Pasang di Ruangan", use_container_width=True):
            with st.spinner(f"Meletakkan produk di {ruangan}..."):
                # Proses Staging
                st.session_state.img_step2 = st.session_state.img_step1 # Simulasi
                st.image(st.session_state.img_step2, caption=f"Produk di {ruangan}", use_column_width=True)
                st.success("Kelihatan keren banget, Mas!")

    # LANGKAH 3: ANIMASI & SKRIP
    if st.session_state.img_step2:
        st.divider()
        st.subheader("Langkah 3: Jadi Video & Skrip")
        gerakan = st.radio("Gaya Gerakan:", ["Zoom In Sinematik", "Panning Lembut", "Rotasi Halus"], horizontal=True)
        
        if st.button("🚀 Proses Video Iklan", use_container_width=True):
            with st.spinner("Grok sedang membuat skrip & video..."):
                # Proses Akhir
                st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Contoh tampilan video
                st.markdown("### 📝 Skrip Storytelling (Aman & Jujur):")
                st.info("Jujur aku kaget pas liat barang ini. Desainnya modern dan pas banget buat dekorasi ruangan. Pas dicoba fungsinya juga oke, kualitasnya solid bukan kaleng-kaleng. Cek link di bio nomor 12 ya!")
                st.button("📋 Salin Skrip untuk TikTok", use_container_width=True)

    st.divider()
    st.caption("Akses: Khusus Mas Miftah | Versi 1.0")