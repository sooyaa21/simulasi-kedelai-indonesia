
from flask import Flask, render_template_string, request
import pickle

app = Flask(__name__)

with open("model_kedelai.pkl", "rb") as f:
    model = pickle.load(f)

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Simulasi Kedelai Indonesia</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f3f7f1;
    margin: 0;
    padding: 30px;
    color: #26352a;
}
.container {
    max-width: 850px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 14px;
}
h1 { color: #28643b; }
select, button {
    padding: 12px;
    width: 100%;
    margin: 10px 0 20px;
    border-radius: 8px;
}
button {
    background: #28643b;
    color: white;
    border: none;
    cursor: pointer;
}
.results {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
}
.card {
    background: #edf5ed;
    padding: 18px;
    border-radius: 10px;
}
.value {
    font-size: 23px;
    font-weight: bold;
    color: #28643b;
}
</style>
</head>
<body>
<div class="container">
<h1>Simulasi Ketersediaan Kedelai Indonesia</h1>
<p>Simulasi produksi, kebutuhan pangan, dan kebutuhan impor tahun 2024–2035.</p>

<form method="POST">
<label>Skenario Produksi</label>
<select name="skenario">
{% for nama in skenario %}
<option value="{{ nama }}" {% if nama == pilihan %}selected{% endif %}>{{ nama }}</option>
{% endfor %}
</select>

<label>Tahun Proyeksi</label>
<select name="tahun">
{% for t in range(2024, 2036) %}
<option value="{{ t }}" {% if t == tahun %}selected{% endif %}>{{ t }}</option>
{% endfor %}
</select>

<button type="submit">Jalankan Simulasi</button>
</form>

{% if hasil %}
<h2>Hasil Simulasi Tahun {{ tahun }}</h2>
<div class="results">
<div class="card">Produksi<div class="value">{{ hasil.produksi }} ribu ton</div></div>
<div class="card">Kebutuhan Pangan<div class="value">{{ hasil.pangan }} ribu ton</div></div>
<div class="card">Impor Dibutuhkan<div class="value">{{ hasil.impor }} ribu ton</div></div>
</div>
<p>Skenario: {{ pilihan }}</p>
{% endif %}

<p><small>Catatan: Hasil merupakan simulasi berdasarkan asumsi model, bukan ramalan pasti.</small></p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    skenario = model["skenario"]
    pilihan = request.form.get("skenario", "Kondisi Tetap")
    tahun = int(request.form.get("tahun", 2035))

    growth = skenario[pilihan]
    n = tahun - 2023

    produksi = model["produksi_awal"] * (1 + growth) ** n
    pangan = model["pangan_awal"] * (
        1 + model["pertumbuhan_pangan"]
    ) ** n

    impor = max(
        0,
        pangan + model["penggunaan_lain"] +
        model["ekspor"] - produksi
    )

    hasil = {
        "produksi": f"{produksi:,.2f}",
        "pangan": f"{pangan:,.2f}",
        "impor": f"{impor:,.2f}"
    }

    return render_template_string(
        HTML,
        skenario=skenario,
        pilihan=pilihan,
        tahun=tahun,
        hasil=hasil
    )

if __name__ == "__main__":
    app.run(debug=True)
