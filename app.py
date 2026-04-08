import streamlit as st
import requests
import base64
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Affiliate Studio Pro",
    page_icon="🎬",
    layout="centered"
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

# --- 3. LOGIKA MESIN AI (DIRECT API CALL) ---
def panggil_grok_direct(api_key, mode, image_bytes, extra_info=""):
    # Encode gambar ke base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    if mode == "CLEAN":
        prompt = "Hapus latar belakang secara total dan hilangkan semua teks, logo marketplace, watermark harga. Sisakan hanya objek produk yang bersih dan rapi."
    elif mode == "STAGING":
        prompt = f"Letakkan produk ini ke dalam ruangan {extra_info} yang estetik dan profesional."
    else:
        prompt = f"Buat skrip TikTok storytelling yang jujur dan tanpa over-claim untuk produk ini."

    payload = {
        "model": "grok-3-vision",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'], True
    except Exception as e:
        return str(e), False

# --- 4. ANTARMUKA UTAMA (UI) ---
if check_auth():
    with st.sidebar:
        st.header("🔑 Key Manager")
        key_rahasia = st.secrets.get("GROK_API_KEY", "")
        api_key = st.text_input("Grok API Key:", value=key_rahasia, type="password")
        if api_key: st.success("✅ API Key Siap")
        if st.button("Log Out"):
            st.session_state["authenticated"] = False
            st.rerun()

    st.title("🎬 Affiliate Studio Pro")

    if "img_clean" not in st.session_state: st.session_state.img_clean = None

    st.subheader("1. Bersihkan Screenshot")
    file_kotor = st.file_uploader("Upload hasil screenshot:", type=['jpg', 'jpeg', 'png'])

    if st.button("✨ Hapus Watermark & Background", use_container_width=True):
        if not api_key:
            st.error("Isi API Key di menu samping!")
        elif file_kotor:
            with st.spinner("Grok sedang bekerja..."):
                bytes_data = file_kotor.getvalue()
                hasil, sukses = panggil_grok_direct(api_key, "CLEAN", bytes_data)
                if sukses:
                    st.session_state.img_clean = bytes_data
                    st.image(bytes_data, caption="Produk Siap Pakai", use_column_width=True)
                    st.success("Proses Berhasil!")
                else: 
                    st.error(f"Gagal: {hasil}")
        else:
            st.warning("Pilih file dulu.")

    # Bagian Skrip
    if st.session_state.img_clean:
        st.divider()
        if st.button("🚀 Buat Skrip Iklan Jujur", use_container_width=True):
            with st.spinner("Menyusun kata-kata..."):
                hasil_teks, sukses = panggil_grok_direct(api_key, "ANIMATE", st.session_state.img_clean)
                if sukses:
                    st.info(hasil_teks)
