from pathlib import Path
import math
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_XLSX = BASE_DIR / "data" / "Data_Mining_KKN.xlsx"
FEATURES = ["Usia", "BMI", "Glukosa", "Tekanan Darah", "Riwayat Keluarga"]

st.set_page_config(page_title="SPK KNN - Data Mining KKN", page_icon="📊", layout="wide")
st.title("📊 Sistem Pendukung Keputusan — Metode K-Nearest Neighbors (KNN)")
st.write("Aplikasi pembelajaran untuk mengklasifikasikan data pasien berdasarkan dataset Excel. Hasil bukan diagnosis medis.")

@st.cache_data
def load_default(path):
    # Dataset tugas memiliki judul pada baris ketiga.
    raw = pd.read_excel(path, header=2)
    raw.columns = [str(c).strip() for c in raw.columns]
    required = ["Pasien", *FEATURES, "Kelas"]
    missing = [c for c in required if c not in raw.columns]
    if missing:
        raise ValueError("Kolom tidak ditemukan di Excel: " + ", ".join(missing))
    data = raw[required].copy()
    data["Pasien"] = data["Pasien"].astype(str).str.strip()
    for col in FEATURES:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data["Kelas"] = data["Kelas"].astype(str).str.strip()
    data = data.dropna(subset=["Pasien", *FEATURES, "Kelas"])
    data = data[data["Kelas"].isin(["Rendah", "Tinggi"])]
    if data.empty:
        raise ValueError("Tidak ditemukan baris dataset dengan kelas Rendah/Tinggi.")
    return data.reset_index(drop=True)

uploaded = st.sidebar.file_uploader("Opsional: unggah file Excel dataset", type=["xlsx", "xls"])
try:
    if uploaded is not None:
        raw = pd.read_excel(uploaded, header=2)
        raw.columns = [str(c).strip() for c in raw.columns]
        needed = ["Pasien", *FEATURES, "Kelas"]
        if any(c not in raw.columns for c in needed):
            st.sidebar.error("Format Excel tidak sesuai. Gunakan file Data_Mining_KKN.xlsx yang disertakan.")
            st.stop()
        data = raw[needed].copy()
        data["Pasien"] = data["Pasien"].astype(str).str.strip()
        for c in FEATURES:
            data[c] = pd.to_numeric(data[c], errors="coerce")
        data["Kelas"] = data["Kelas"].astype(str).str.strip()
        data = data.dropna(subset=["Pasien", *FEATURES, "Kelas"])
        data = data[data["Kelas"].isin(["Rendah", "Tinggi"])].reset_index(drop=True)
    else:
        data = load_default(DEFAULT_XLSX)
except Exception as e:
    st.error(f"Gagal membaca dataset: {e}")
    st.stop()

st.subheader("1. Dataset latihan")
st.caption(f"Jumlah data valid: {len(data)} pasien")
st.dataframe(data, use_container_width=True, hide_index=True)

st.subheader("2. Masukkan data pasien baru")
with st.form("form_prediksi"):
    c1, c2, c3 = st.columns(3)
    with c1:
        usia = st.number_input("Usia (tahun)", min_value=1, max_value=120, value=42, step=1)
        bmi = st.number_input("BMI", min_value=1.0, max_value=100.0, value=28.5, step=0.1)
    with c2:
        glukosa = st.number_input("Glukosa", min_value=1.0, max_value=1000.0, value=130.0, step=1.0)
        tekanan = st.number_input("Tekanan darah", min_value=1.0, max_value=400.0, value=128.0, step=1.0)
    with c3:
        riwayat_label = st.selectbox("Riwayat keluarga", ["Tidak ada (0)", "Ada (1)"])
        k = st.number_input("Nilai K (jumlah tetangga)", min_value=1, max_value=len(data), value=min(3, len(data)), step=1)
        metode = st.selectbox("Perhitungan jarak", ["Euclidean (sesuai lembar Excel)", "Euclidean dengan normalisasi"])
    submitted = st.form_submit_button("🔎 Hitung Prediksi", type="primary")

if submitted:
    new_values = [float(usia), float(bmi), float(glukosa), float(tekanan), 1.0 if riwayat_label.endswith("1)") else 0.0]
    matrix = data[FEATURES].astype(float).copy()
    query = pd.Series(new_values, index=FEATURES, dtype=float)
    if metode == "Euclidean dengan normalisasi":
        mins = matrix.min()
        spans = (matrix.max() - mins).replace(0, 1)
        matrix_calc = (matrix - mins) / spans
        query_calc = (query - mins) / spans
    else:
        matrix_calc = matrix
        query_calc = query
    distances = []
    for idx, row in matrix_calc.iterrows():
        distance = math.sqrt(sum((float(row[f]) - float(query_calc[f])) ** 2 for f in FEATURES))
        distances.append(distance)
    result = data.copy()
    result["Jarak"] = distances
    result = result.sort_values("Jarak", ascending=True).reset_index(drop=True)
    neighbors = result.head(int(k))
    votes = neighbors["Kelas"].value_counts()
    max_votes = votes.max()
    winners = sorted(votes[votes == max_votes].index.tolist())
    prediction = winners[0] if len(winners) == 1 else neighbors.iloc[0]["Kelas"]

    st.subheader("3. Hasil prediksi")
    st.success(f"Kelas hasil KNN: **{prediction}**")
    st.caption(f"Prediksi berdasarkan {int(k)} tetangga terdekat menggunakan {metode.lower()}.")
    st.subheader("4. Tetangga terdekat")
    st.dataframe(neighbors[["Pasien", *FEATURES, "Kelas", "Jarak"]].round({"BMI": 2, "Jarak": 4}), use_container_width=True, hide_index=True)
    st.subheader("5. Urutan seluruh jarak")
    st.dataframe(result[["Pasien", "Kelas", "Jarak"]].round({"Jarak": 4}), use_container_width=True, hide_index=True)
    st.subheader("6. Ringkasan perhitungan")
    st.write("Rumus Euclidean: jarak = √(Σ(nilai fitur data latihan − nilai fitur pasien baru)²).")
    st.write("Jumlah suara kelas tetangga:")
    st.dataframe(votes.rename("Jumlah suara").rename_axis("Kelas").reset_index(), hide_index=True, use_container_width=True)
    csv = result.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ Unduh hasil perhitungan (CSV)", data=csv, file_name="hasil_knn.csv", mime="text/csv")

with st.expander("Catatan penggunaan"):
    st.markdown("- File Excel bawaan ada di folder `data/` dan akan dibaca otomatis.\n- Pilih K sesuai kebutuhan tugas; nilai awal K = 3.\n- Mode Euclidean sesuai lembar Excel memakai nilai asli fitur, sehingga skala glukosa lebih berpengaruh pada jarak. Mode normalisasi disediakan sebagai opsi tambahan.\n- Ini hanya contoh klasifikasi untuk pembelajaran, bukan alat diagnosis atau pengganti tenaga kesehatan.")
