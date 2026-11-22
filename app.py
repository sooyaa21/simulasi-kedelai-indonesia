import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle

st.set_page_config(
    page_title="Simulasi Kedelai Indonesia",
    page_icon="🌱",
    layout="wide"
)

with open("model_kedelai.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🌱 Simulasi Ketersediaan Kedelai Indonesia")
st.write(
    "Simulasi produksi, kebutuhan pangan, dan kebutuhan impor "
    "kedelai Indonesia periode 2024–2035."
)

st.sidebar.header("Pengaturan Simulasi")

skenario = st.sidebar.selectbox(
    "Pilih skenario produksi",
    list(model["skenario"].keys())
)

tahun = st.sidebar.slider(
    "Pilih tahun proyeksi",
    2024, 2035, 2035
)

n = tahun - 2023
pertumbuhan = model["skenario"][skenario]

produksi = model["produksi_awal"] * (1 + pertumbuhan) ** n
pangan = model["pangan_awal"] * (
    1 + model["pertumbuhan_pangan"]
) ** n

impor = max(
    0,
    pangan + model["penggunaan_lain"] +
    model["ekspor"] - produksi
)

st.subheader(f"Hasil Simulasi Tahun {tahun}")

col1, col2, col3 = st.columns(3)

col1.metric("Produksi", f"{produksi:,.2f} ribu ton")
col2.metric("Kebutuhan Pangan", f"{pangan:,.2f} ribu ton")
col3.metric("Impor Dibutuhkan", f"{impor:,.2f} ribu ton")

st.info(f"Skenario yang dipilih: {skenario}")

data = []

for nama, growth in model["skenario"].items():
    for t in range(2024, tahun + 1):
        periode = t - 2023
        p = model["produksi_awal"] * (1 + growth) ** periode
        k = model["pangan_awal"] * (
            1 + model["pertumbuhan_pangan"]
        ) ** periode
        i = max(
            0,
            k + model["penggunaan_lain"] +
            model["ekspor"] - p
        )
        data.append({
            "Tahun": t,
            "Skenario": nama,
            "Produksi": p,
            "Kebutuhan Pangan": k,
            "Impor Dibutuhkan": i
        })

df = pd.DataFrame(data)

st.subheader("Grafik Proyeksi Kebutuhan Impor")

fig, ax = plt.subplots(figsize=(10, 5))

for nama in model["skenario"]:
    bagian = df[df["Skenario"] == nama]
    ax.plot(
        bagian["Tahun"],
        bagian["Impor Dibutuhkan"],
        marker="o",
        label=nama
    )

ax.set_xlabel("Tahun")
ax.set_ylabel("Impor (1000 ton)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.subheader("Tabel Hasil Simulasi")
st.dataframe(
    df[df["Tahun"] == tahun].round(2),
    use_container_width=True
)

st.caption(
    "Catatan: Hasil merupakan simulasi berdasarkan asumsi model, "
    "bukan ramalan pasti."
)
