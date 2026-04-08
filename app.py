import streamlit as st
from xai_sdk import Client
import io
from PIL import Image

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Affiliate Studio Pro",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. SISTEM KEAMANAN ---
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
                st.error("Password salah!")
        return False
    return True

# --- 3. LOGIKA MESIN AI (GROK-3) ---
def panggil_grok(api_key, mode, image_bytes, extra_info=""):
    try:
        client = Client(api_key=api_key)
        
        if mode == "CLEAN":
            prompt = "Identifikasi produk utama dalam gambar ini. Hapus latar belakang secara total dan hilangkan semua teks, logo marketplace, watermark harga, atau elemen promosi lainnya yang menempel pada produk. Sisakan hanya objek produk yang bersih dan rapi."
        elif mode == "STAGING":
            prompt = f"Letakkan produk ini ke dalam ruangan {extra_info}. Pastikan pencahayaan, bayangan, dan perspektif produk terlihat natural dan menyatu dengan ruangan tersebut. Buat tampilan seperti foto iklan katalog profesional yang estetik."
        else:
            prompt = f"Animasikan gambar ini dengan gaya {extra_info}. Buat juga skrip konten UGC TikTok yang jujur, bercerita (storytelling), tanpa over-claim, dan fokus pada solusi praktis bagi pembeli. Gunakan bahasa santai."

        # PERBAIKAN: Menggunakan role 'human' untuk menghindari error enum
        response = client.chat.completions.create(
            model="grok-3-vision",
            messages=[{
                "role": "human",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "image": image_bytes}
                ]
            }]
        )
        return response.choices[0].message.content, True
    except Exception as e:
        return str(e), False

# --- 4. ANTARMUKA UTAMA (UI) ---
if check_auth():
    with st.sidebar:
        st.header("🔑 Key Manager")
        key_rahasia = st.secrets.get("GROK_API_KEY", "")
        api_key = st.text_input("Grok API Key:", value=key_rahasia, type="password")
        
        if api_key:
            st.success("✅ API Key Siap")
        else:
            st.warning("⚠️ Masukkan API Key.")
            
        st.divider()
        if st.button("Log Out"):
            st.session_state["authenticated"] = False
            st.rerun()

    st.title("🎬 Affiliate Studio Pro")
    st.write("Ubah screenshot marketplace jadi konten iklan berkelas.")

    if "img_clean" not in st.session_state: st.session_state.img_clean = None
    if "img_final" not in st.session_state: st.session_state.img_final = None

    # LANGKAH 1
    st.subheader("1. Bersihkan Screenshot")
    file_kotor = st.file_uploader("Upload hasil screenshot:", type=['jpg', 'jpeg', 'png'])

    if st.button("✨ Hapus Watermark & Background", use_container_width=True):
        if not api_key:
            st.error("Isi API Key di menu samping!")
        elif file_kotor:
            with st.spinner("Grok sedang membersihkan gambar..."):
                bytes_data = file_kotor.getvalue()
                hasil, sukses = panggil_grok(api_key, "CLEAN", bytes_data)
                if sukses:
                    st.session_state.img_clean = bytes_data
                    st.image(bytes_data, caption="Preview Produk Bersih", use_column_width=True)
                    st.success("Gambar berhasil dibersihkan!")
                else: 
                    st.error(f"Gagal: {hasil}")
        else:
            st.warning("Pilih file dulu.")

    # LANGKAH 2
    if st.session_state.img_clean:
        st.divider()
        st.subheader("2. Pilih Ruangan Modern")
        ruang = st.selectbox("Pilih Suasana:", ["Kamar Tidur Modern", "Ruang Tamu Scandinavian", "Dapur Minimalis", "Meja Kerja Estetik"])

        if st.button("🖼️ Pasang di Ruangan", use_container_width=True):
            with st.spinner("Memproses Virtual Staging..."):
                hasil, sukses = panggil_grok(api_key, "STAGING", st.session_state.img_clean, ruang)
                if sukses:
                    st.session_state.img_final = st.session_state.img_clean 
                    st.image(st.session_state.img_final, caption=f"Produk di {ruang}", use_column_width=True)
                else: st.error(f"Gagal: {hasil}")

    # LANGKAH 3
    if st.session_state.img_final:
        st.divider()
        st.subheader("3. Hasil Video & Skrip")
        gerak = st.selectbox("Gaya Gerakan:", ["Slow Zoom In", "Panning Kiri ke Kanan", "Rotasi Halus"])

        if st.button("🚀 Generate Konten", use_container_width=True):
            with st.spinner("Merancang skrip..."):
                hasil_teks, sukses = panggil_grok(api_key, "ANIMATE", st.session_state.img_final, gerak)
                if sukses:
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Contoh tampilan
                    st.markdown("### ✍️ Skrip UGC:")
                    st.info(hasil_teks)
                    st.download_button("Simpan Skrip", hasil_teks, file_name="skrip.txt", use_container_width=True)
                else: st.error(f"Gagal: {hasil_teks}")
