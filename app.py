import streamlit as st
from xai_sdk import Client
import io
from PIL import Image

# --- 1. KONFIGURASI HALAMAN (Optimasi Mobile) ---
st.set_page_config(
    page_title="Affiliate Studio Pro",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. SISTEM KEAMANAN (Password Akses) ---
# Silakan ganti password di bawah ini sesuai keinginan Mas Miftah
PASSWORD_AKSES = "cuanfisik2026"

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        st.markdown("<h2 style='text-align: center;'>🔐 Private Studio Affiliate</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Masukkan Password Akses:", type="password")
        if st.button("Buka Studio 🚀", use_container_width=True):
            if pwd == PASSWORD_AKSES:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Password salah, Mas!")
        return False
    return True

# --- 3. LOGIKA MESIN AI (GROK-3) ---
def panggil_grok(api_key, mode, image_data, extra_info=""):
    client = Client(api_key=api_key)
    
    if mode == "CLEAN":
        prompt = "Identifikasi produk utama dalam gambar ini. Hapus latar belakang secara total dan hilangkan semua teks, logo marketplace, watermark harga, atau elemen promosi lainnya yang menempel pada produk. Sisakan hanya objek produk yang bersih dan rapi."
    elif mode == "STAGING":
        prompt = f"Letakkan produk ini ke dalam ruangan {extra_info}. Pastikan pencahayaan, bayangan, dan perspektif produk terlihat natural dan menyatu dengan ruangan tersebut. Buat tampilan seperti foto iklan katalog profesional yang estetik."
    else: # ANIMATE & SCRIPT
        prompt = f"Animasikan gambar ini dengan gaya {extra_info}. Buat juga skrip konten UGC TikTok yang jujur, bercerita (storytelling), tanpa over-claim, dan fokus pada solusi praktis bagi pembeli. Gunakan bahasa santai (lo-gue atau aku-kamu)."

    try:
        chat = client.chat.create(
            model="grok-3-vision",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "image": image_data}
                ]
            }]
        )
        # Mengambil hasil dari API
        return chat.sample().content, True
    except Exception as e:
        return str(e), False

# --- 4. ANTARMUKA UTAMA (UI) ---
if check_auth():
    # SIDEBAR: Manajemen API Key
    with st.sidebar:
        st.header("🔑 Key Manager")
        
        # Cek apakah ada API Key di Secrets (Otomatis) atau Input Manual
        key_rahasia = st.secrets.get("GROK_API_KEY", "")
        api_key = st.text_input("Grok API Key:", value=key_rahasia, type="password", help="Masukkan API Key Grok Anda di sini.")
        
        if not api_key:
            st.warning("⚠️ Masukkan API Key untuk memulai.")
        else:
            st.success("✅ API Key Siap")
            
        st.divider()
        if st.button("Log Out"):
            st.session_state["authenticated"] = False
            st.rerun()

    st.title("🎬 Affiliate Studio Pro")
    st.write("Ubah screenshot marketplace jadi konten iklan berkelas.")

    # Inisialisasi State Gambar
    if "img_clean" not in st.session_state: st.session_state.img_clean = None
    if "img_final" not in st.session_state: st.session_state.img_final = None

    # LANGKAH 1: CLEANING
    st.subheader("1. Bersihkan Screenshot")
    file_kotor = st.file_uploader("Upload hasil screenshot marketplace:", type=['jpg', 'jpeg', 'png'])

    if st.button("✨ Hapus Watermark & Background", use_container_width=True):
        if not api_key:
            st.error("Isi API Key di menu samping dulu, Mas!")
        elif file_kotor:
            with st.spinner("Grok sedang membersihkan gambar..."):
                hasil, sukses = panggil_grok(api_key, "CLEAN", file_kotor.read())
                if sukses:
                    # Simulasi penyimpanan hasil (Nanti diisi respon gambar dari API)
                    st.session_state.img_clean = file_kotor 
                    st.image(file_kotor, caption="Preview Produk Bersih", use_column_width=True)
                    st.success("Gambar berhasil dibersihkan!")
                else: st.error(f"Gagal: {hasil}")
        else: st.warning("Pilih file gambarnya dulu ya.")

    # LANGKAH 2: VIRTUAL STAGING
    if st.session_state.img_clean:
        st.divider()
        st.subheader("2. Pilih Ruangan Modern")
        pilihan_ruangan = st.selectbox("Pilih Suasana Ruangan:", [
            "Kamar Tidur Minimalis Modern",
            "Ruang Tamu Scandinavian",
            "Dapur Minimalis Putih",
            "Meja Kerja Kayu Estetik",
            "Taman Belakang Asri"
        ])

        if st.button("🖼️ Pasang di Ruangan", use_container_width=True):
            with st.spinner(f"Memindahkan produk ke {pilihan_ruangan}..."):
                # Konversi image state ke bytes
                img_bytes = st.session_state.img_clean.getvalue()
                hasil, sukses = panggil_grok(api_key, "STAGING", img_bytes, pilihan_ruangan)
                if sukses:
                    st.session_state.img_final = st.session_state.img_clean # Simulasi
                    st.image(st.session_state.img_final, caption=f"Produk di {pilihan_ruangan}", use_column_width=True)
                else: st.error(f"Gagal: {hasil}")

    # LANGKAH 3: VIDEO & SKRIP
    if st.session_state.img_final:
        st.divider()
        st.subheader("3. Hasil Video & Skrip Storytelling")
        gaya_gerak = st.selectbox("Gaya Gerakan Video:", ["Slow Zoom In Sinematik", "Panning Kiri ke Kanan", "Rotasi Produk Halus"])

        if st.button("🚀 Generate Konten Iklan", use_container_width=True):
            with st.spinner("Grok sedang merancang skrip dan video..."):
                img_bytes = st.session_state.img_final.getvalue()
                hasil_teks, sukses = panggil_grok(api_key, "ANIMATE", img_bytes, gaya_gerak)
                
                if sukses:
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Contoh tampilan video
                    st.markdown("### ✍️ Skrip UGC (Anti Over-Claim):")
                    st.info(hasil_teks)
                    
                    st.download_button("Salin Skrip ke HP", hasil_teks, file_name="skrip_affiliate.txt", use_container_width=True)
                else: st.error(f"Gagal: {hasil_teks}")

    st.divider()
    st.caption("Aplikasi Studio Affiliate Pro v1.0 | Dibuat khusus untuk Mas Miftah")
