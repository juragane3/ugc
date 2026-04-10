import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Affiliate Prompt Master", layout="wide")

# --- MASTER TEMPLATE ---
templates = {
    "HOOK": [
        "Nggak nyangka banget nemu barang ini!",
        "Kalian harus lihat ini sebelum kehabisan!",
        "Solusi buat kalian yang punya masalah sama...",
        "Jangan beli barang ini sebelum nonton video ini!",
        "Racun TikTok hari ini, bener-bener worth it!",
        "Pecinta barang unik wajib merapat!"
    ],
    "DETAIL": [
        "Lihat deh teksturnya premium banget.",
        "Bahannya kokoh dan fiturnya lengkap.",
        "Cara pakenya gampang banget, tinggal klik.",
        "Detailnya rapi, kualitasnya di atas rata-rata.",
        "Desainnya elegan banget, cocok buat kado.",
        "Bahannya anti karat dan tahan lama banget."
    ],
    "CTA": [
        "Mumpung promo, cek keranjang kuning!",
        "Stok terbatas, langsung check out!",
        "Link ada di bio atau langsung klik di bawah ya!",
        "Lagi ada gratis ongkir, gercep sekarang!",
        "Harga promo cuma sampai hari ini aja!",
        "Klik icon keranjang kuning sebelum harganya naik!"
    ]
}

st.title("🚀 TikTok Affiliate Master Prompt")
st.write("Buat alur Hook, Detail, dan CTA secara otomatis untuk Grok/AI Video.")

# --- SIDEBAR INPUT ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    produk = st.text_input("Nama Produk:", placeholder="Contoh: Rice Cooker Digital")
    st.divider()
    
    scenes_options = []
    for label in ["HOOK", "DETAIL", "CTA"]:
        st.subheader(f"Scene: {label}")
        narasi = st.selectbox(f"Gaya Narasi {label}:", templates[label], key=f"select_{label}")
        lip_sync = st.checkbox("Aktifkan Lip Sync", value=False, key=f"lip_{label}")
        presenter = st.text_input("Deskripsi Orang:", placeholder="Contoh: Indonesian girl, hijab", key=f"pres_{label}")
        scenes_options.append({"label": label, "narasi": narasi, "lip": lip_sync, "pres": presenter})

# --- DISPLAY AREA ---
if produk:
    all_prompts_list = []
    
    # Grid 3 Kolom untuk Preview
    cols = st.columns(3)
    for i, data in enumerate(scenes_options):
        with cols[i]:
            st.info(f"**SCENE {i+1}: {data['label']}**")
            
            # Membangun Prompt
            orang = data['pres'] if data['pres'] else "Professional Indonesian spokesperson"
            prompt = f"A professional TikTok video for {produk}. "
            
            if data['lip']:
                prompt += f"Visual: A realistic {orang} speaking directly to camera. Script: '{data['narasi']}'. High-fidelity lip-sync. "
            else:
                prompt += f"Visual: High-end cinematic product cinematography focusing on {produk} details and textures. "
            
            prompt += "Lighting: Studio professional. Quality: 4k, 60fps, trending TikTok aesthetic, sharp focus."
            
            st.code(prompt, language="text")
            all_prompts_list.append(f"--- SCENE {i+1} ({data['label']}) ---\n{prompt}")

    # Tombol Master Copy
    st.divider()
    full_text = "\n\n".join(all_prompts_list)
    st.subheader("📋 Master Copy (Semua Scene)")
    st.text_area("Salin semua sekaligus di sini:", value=full_text, height=200)
    st.success("Gunakan ikon di pojok kanan atas setiap kotak untuk menyalin cepat!")

else:
    st.warning("Masukkan Nama Produk di menu samping untuk memulai.")
