
from flask import Flask, render_template_string

app = Flask(__name__)

# ==========================================
# DATA DASAR SIMULASI (SATUAN: RIBU TON)
# ==========================================

BASE_YEAR = 2023
BASE_PRODUCTION = 326
BASE_FOOD = 2626
OTHER_USE = 86
EXPORT = 8

HTML = r"""
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Soybean Lab — Indonesia</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
:root {
    --forest: #102c20;
    --forest2: #183d2c;
    --green: #2e6746;
    --lime: #d7ef9b;
    --cream: #f4f2e8;
    --gold: #d9ad57;
    --muted: #87958a;
    --white: #fffefa;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    background: #f3f3eb;
    color: var(--forest);
    font-family: 'DM Sans', sans-serif;
    overflow-x: hidden;
}

.page {
    max-width: 1500px;
    margin: auto;
    padding: 25px 4%;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0 28px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    font-size: 13px;
}

.brand-icon {
    width: 39px;
    height: 39px;
    border-radius: 13px;
    background: var(--forest);
    color: var(--lime);
    display: grid;
    place-items: center;
    font-size: 22px;
}

.top-label {
    font-size: 11px;
    color: #78877b;
    letter-spacing: 1.5px;
}

.hero {
    background:
        radial-gradient(circle at 85% 20%, rgba(215,239,155,.18), transparent 26%),
        linear-gradient(115deg, #102c20, #214c34);
    border-radius: 30px;
    min-height: 360px;
    padding: 48px 5%;
    color: white;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
}

.hero-content {
    max-width: 650px;
    position: relative;
    z-index: 2;
}

.eyebrow {
    color: var(--lime);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 18px;
}

.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(38px, 5vw, 65px);
    line-height: 1.08;
    margin: 0 0 18px;
    max-width: 620px;
}

.hero h1 span { color: var(--lime); }

.hero p {
    color: #d0ded2;
    line-height: 1.8;
    font-size: 14px;
    max-width: 490px;
}

.hero-note {
    display: inline-flex;
    gap: 9px;
    align-items: center;
    border: 1px solid #ffffff38;
    background: #ffffff10;
    padding: 11px 17px;
    border-radius: 30px;
    font-size: 11px;
    margin-top: 15px;
}

.hero-art {
    position: absolute;
    right: 7%;
    top: 50%;
    transform: translateY(-50%);
    width: 310px;
    height: 290px;
}

.orbit {
    position: absolute;
    width: 250px;
    height: 250px;
    border: 1px solid #d7ef9b35;
    border-radius: 50%;
    top: 20px;
    left: 25px;
    animation: rotate 24s linear infinite;
}

.orbit:before, .orbit:after {
    content: "";
    position: absolute;
    border: 1px solid #d7ef9b30;
    border-radius: 50%;
    inset: 25px;
}

.orbit:after { inset: 55px; }

.soybean {
    position: absolute;
    font-size: 70px;
    filter: drop-shadow(0 15px 14px #0005);
    animation: float 4s ease-in-out infinite;
}

.bean1 { top: 75px; left: 95px; font-size: 100px; }
.bean2 { top: 20px; right: 20px; font-size: 37px; animation-delay: -1s; }
.bean3 { bottom: 15px; left: 20px; font-size: 45px; animation-delay: -2s; }
.bean4 { bottom: 35px; right: 15px; font-size: 30px; animation-delay: -3s; }

.leaf {
    position: absolute;
    font-size: 55px;
    top: 5px;
    left: 0;
    animation: sway 5s ease-in-out infinite;
}

@keyframes float {
    0%,100% { transform: translateY(0) rotate(-5deg); }
    50% { transform: translateY(-17px) rotate(7deg); }
}
@keyframes rotate { to { transform: rotate(360deg); } }
@keyframes sway {
    0%,100% { transform: rotate(-8deg); }
    50% { transform: rotate(12deg); }
}

.section-heading {
    display: flex;
    justify-content: space-between;
    align-items: end;
    margin: 42px 0 20px;
    gap: 15px;
}

.section-heading h2 {
    font-family: 'Playfair Display', serif;
    font-size: 29px;
    margin: 5px 0;
}

.section-heading p {
    color: #7b897e;
    font-size: 12px;
    margin: 0;
}

.section-tag {
    color: #63816b;
    letter-spacing: 2px;
    font-size: 10px;
    font-weight: 800;
}

.simulation {
    display: grid;
    grid-template-columns: 1.15fr .85fr;
    gap: 20px;
    align-items: stretch;
}

.panel {
    background: var(--white);
    border: 1px solid #e7e8dd;
    border-radius: 23px;
    padding: 27px;
    box-shadow: 0 10px 35px #263b2910;
}

.panel-dark {
    background: var(--forest);
    color: white;
    border: 0;
    position: relative;
    overflow: hidden;
}

.panel-dark:after {
    content: "🌱";
    position: absolute;
    right: -12px;
    bottom: -40px;
    font-size: 145px;
    opacity: .08;
    transform: rotate(-25deg);
}

.panel-title {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
}

.panel-sub {
    font-size: 11px;
    color: #8b988d;
    margin-top: 6px;
}

.year-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 24px 0 12px;
}

.year-number {
    font-family: 'Playfair Display', serif;
    font-size: 67px;
    color: var(--lime);
    line-height: 1;
    transition: .2s;
}

.year-caption {
    font-size: 10px;
    color: #a8bcae;
    letter-spacing: 2px;
}

input[type=range] {
    width: 100%;
    accent-color: #a6ce69;
    cursor: grab;
    margin: 15px 0;
}

input[type=range]:active { cursor: grabbing; }

.range-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #9aab9e;
}

.scenario-title {
    font-size: 11px;
    color: #b8cbbd;
    margin: 27px 0 12px;
}

.scenarios {
    display: flex;
    gap: 9px;
    flex-wrap: wrap;
    position: relative;
    z-index: 2;
}

.scenario-btn {
    border: 1px solid #ffffff35;
    border-radius: 12px;
    background: transparent;
    color: #d5e2d8;
    padding: 12px 19px;
    font-family: inherit;
    font-weight: 700;
    cursor: pointer;
    transition: .25s;
}

.scenario-btn:hover { border-color: var(--lime); }

.scenario-btn.active {
    color: var(--forest);
    background: var(--lime);
    border-color: var(--lime);
    box-shadow: 0 5px 20px #d7ef9b30;
}

.result-panel {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.result-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.live {
    color: #39794c;
    background: #e8f4df;
    border-radius: 30px;
    padding: 7px 11px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1px;
}

.result-big {
    margin: 25px 0 8px;
    font-family: 'Playfair Display', serif;
    font-size: clamp(42px, 5vw, 61px);
    color: #234c32;
    letter-spacing: -2px;
    transition: .3s;
}

.result-caption {
    font-size: 12px;
    color: #819083;
}

.mini-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 23px;
}

.mini-stat {
    padding: 16px;
    background: #f2f4eb;
    border-radius: 15px;
}

.mini-stat span {
    display: block;
    font-size: 10px;
    color: #829083;
    margin-bottom: 7px;
}

.mini-stat strong {
    font-size: 20px;
    color: #244b32;
}

.unit {
    font-size: 10px;
    color: #89958b;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 18px;
}

.metric {
    background: white;
    border-radius: 19px;
    padding: 22px;
    border: 1px solid #e8e9df;
    position: relative;
    overflow: hidden;
    transition: .3s;
}

.metric:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 25px #263b2912;
}

.metric:after {
    content: "";
    width: 75px;
    height: 75px;
    border-radius: 50%;
    position: absolute;
    right: -25px;
    top: -25px;
    background: #e8f1dd;
}

.metric-icon {
    font-size: 23px;
    position: relative;
    z-index: 1;
}

.metric-label {
    color: #819083;
    font-size: 11px;
    margin-top: 13px;
}

.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 700;
    margin-top: 5px;
    color: #234a32;
}

.metric-unit {
    color: #89958a;
    font-size: 10px;
}

.chart-layout {
    display: grid;
    grid-template-columns: 1.5fr .7fr;
    gap: 18px;
}

.chart-panel {
    background: white;
    border: 1px solid #e7e8dd;
    border-radius: 23px;
    padding: 25px;
    min-width: 0;
}

.chart-wrap {
    height: 300px;
    margin-top: 20px;
}

.insight {
    border-radius: 23px;
    padding: 26px;
    background: #e7edda;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.insight-icon { font-size: 34px; }

.insight h3 {
    font-family: 'Playfair Display', serif;
    font-size: 25px;
    margin: 15px 0 8px;
}

.insight p {
    color: #667968;
    line-height: 1.8;
    font-size: 12px;
}

.insight-bottom {
    border-top: 1px solid #cbd8c3;
    padding-top: 15px;
    color: #47634e;
    font-size: 11px;
    line-height: 1.7;
}

.table-panel {
    background: white;
    border: 1px solid #e7e8dd;
    border-radius: 23px;
    padding: 25px;
    overflow: hidden;
}

.table-scroll { overflow-x: auto; }

table {
    border-collapse: collapse;
    width: 100%;
    min-width: 600px;
    margin-top: 20px;
}

th {
    text-align: left;
    padding: 14px 12px;
    background: #f0f3e9;
    color: #627667;
    font-size: 10px;
    letter-spacing: .5px;
}

td {
    padding: 14px 12px;
    border-bottom: 1px solid #edf0e8;
    font-size: 11px;
    color: #425c49;
}

tr.selected-row td {
    background: #edf4e3;
    font-weight: 800;
    color: #244a31;
}

.footer {
    margin: 35px 0 10px;
    padding: 20px 0;
    border-top: 1px solid #dfe4d8;
    display: flex;
    justify-content: space-between;
    color: #879387;
    font-size: 10px;
    gap: 10px;
}

@media(max-width: 850px) {
    .hero-art { opacity: .25; right: -50px; }
    .simulation, .chart-layout { grid-template-columns: 1fr; }
    .metric-grid { grid-template-columns: 1fr; }
    .metric { display: grid; grid-template-columns: 45px 1fr; align-items: center; }
    .metric-icon { grid-row: span 2; }
    .metric-label { margin-top: 0; }
    .metric-value { font-size: 25px; }
}

@media(max-width: 520px) {
    .page { padding: 15px; }
    .hero { padding: 35px 25px; min-height: 330px; }
    .hero h1 { font-size: 39px; }
    .hero-art { transform: translateY(-50%) scale(.7); right: -100px; }
    .panel, .chart-panel, .table-panel { padding: 20px; }
    .year-number { font-size: 55px; }
    .section-heading h2 { font-size: 24px; }
    .footer { flex-direction: column; }
}
</style>
</head>

<body>
<div class="page">

<header class="topbar">
    <div class="brand">
        <div class="brand-icon">🌱</div>
        SOYBEAN LAB
    </div>
    <div class="top-label">INDONESIA · SYSTEM DYNAMICS</div>
</header>

<section class="hero">
    <div class="hero-content">
        <div class="eyebrow">DYNAMIC SYSTEM SIMULATION · 2024—2035</div>
        <h1>Masa Depan <span>Kedelai</span> Indonesia.</h1>
        <p>
            Eksplorasi bagaimana perubahan produksi dan kebutuhan pangan
            memengaruhi ketersediaan kedelai nasional melalui simulasi
            sistem dinamik.
        </p>
        <div class="hero-note">✦ Interactive simulation experience</div>
    </div>

    <div class="hero-art">
        <div class="orbit"></div>
        <div class="leaf">🌿</div>
        <div class="soybean bean1">🫘</div>
        <div class="soybean bean2">🫘</div>
        <div class="soybean bean3">🫘</div>
        <div class="soybean bean4">🫘</div>
    </div>
</section>

<div class="section-heading">
    <div>
        <div class="section-tag">01 / CONTROL CENTER</div>
        <h2>Atur Simulasi</h2>
        <p>Geser tahun dan pilih skenario untuk melihat perubahan.</p>
    </div>
</div>

<section class="simulation">

    <div class="panel panel-dark">
        <div class="panel-title">TIME MACHINE</div>
        <div class="panel-sub">Pilih tahun proyeksi yang ingin diamati</div>

        <div class="year-display">
            <div>
                <div class="year-caption">SIMULATION YEAR</div>
                <div class="year-number" id="yearNumber">2030</div>
            </div>
            <div style="font-size:40px">⏳</div>
        </div>

        <input id="yearSlider" type="range" min="2024" max="2035" value="2030">
        <div class="range-labels">
            <span>2024 · AWAL</span>
            <span>2035 · AKHIR</span>
        </div>

        <div class="scenario-title">PILIH PERTUMBUHAN PRODUKSI</div>
        <div class="scenarios">
            <button class="scenario-btn" data-growth="0">0%</button>
            <button class="scenario-btn active" data-growth="3">+3%</button>
            <button class="scenario-btn" data-growth="5">+5%</button>
        </div>
    </div>

    <div class="panel result-panel">
        <div class="result-top">
            <div class="panel-title">HASIL SIMULASI</div>
            <div class="live">● LIVE RESULT</div>
        </div>

        <div>
            <div class="result-caption">Estimasi impor yang dibutuhkan</div>
            <div class="result-big" id="mainImport">2.588</div>
            <div class="result-caption">Ribu ton kedelai</div>
        </div>

        <div class="mini-stats">
            <div class="mini-stat">
                <span>Produksi nasional</span>
                <strong id="smallProduction">465</strong>
                <div class="unit">Ribu ton</div>
            </div>
            <div class="mini-stat">
                <span>Kebutuhan pangan</span>
                <strong id="smallFood">2.819</strong>
                <div class="unit">Ribu ton</div>
            </div>
        </div>
    </div>
</section>

<div class="section-heading">
    <div>
        <div class="section-tag">02 / SIMULATION OUTPUT</div>
        <h2>Angka yang Berubah</h2>
        <p>Ringkasan kondisi kedelai berdasarkan pilihan simulasi.</p>
    </div>
</div>

<section class="metric-grid">
    <div class="metric">
        <div class="metric-icon">🌾</div>
        <div class="metric-label">PRODUKSI KEDELAI</div>
        <div>
            <div class="metric-value" id="productionCard">465</div>
            <div class="metric-unit">Ribu ton</div>
        </div>
    </div>

    <div class="metric">
        <div class="metric-icon">🍽️</div>
        <div class="metric-label">KEBUTUHAN PANGAN</div>
        <div>
            <div class="metric-value" id="foodCard">2.819</div>
            <div class="metric-unit">Ribu ton</div>
        </div>
    </div>

    <div class="metric">
        <div class="metric-icon">🚢</div>
        <div class="metric-label">IMPOR DIBUTUHKAN</div>
        <div>
            <div class="metric-value" id="importCard">2.588</div>
            <div class="metric-unit">Ribu ton</div>
        </div>
    </div>
</section>

<div class="section-heading">
    <div>
        <div class="section-tag">03 / DATA VISUALIZATION</div>
        <h2>Perjalanan Ketersediaan</h2>
        <p>Bandingkan perkembangan setiap skenario hingga 2035.</p>
    </div>
</div>

<section class="chart-layout">
    <div class="chart-panel">
        <div class="panel-title">PROYEKSI IMPOR KEDELAI</div>
        <div class="panel-sub">Perbandingan kebutuhan impor antar skenario · ribu ton</div>
        <div class="chart-wrap">
            <canvas id="simulationChart"></canvas>
        </div>
    </div>

    <div class="insight">
        <div>
            <div class="insight-icon">🌱</div>
            <h3 id="insightTitle">Produksi Terus Bertumbuh</h3>
            <p id="insightText">
                Skenario pertumbuhan produksi membantu melihat bagaimana
                peningkatan hasil panen dapat mengurangi kebutuhan impor.
            </p>
        </div>
        <div class="insight-bottom" id="insightBottom">
            Gunakan slider untuk mencoba tahun dan skenario yang berbeda.
        </div>
    </div>
</section>

<div class="section-heading">
    <div>
        <div class="section-tag">04 / YEARLY PROJECTION</div>
        <h2>Tabel Proyeksi Tahunan</h2>
        <p>Perhitungan estimasi berdasarkan skenario yang dipilih.</p>
    </div>
</div>

<section class="table-panel">
    <div class="panel-title">RINCIAN HASIL SIMULASI</div>
    <div class="panel-sub">Baris tahun yang sedang dipilih akan disorot otomatis.</div>

    <div class="table-scroll">
        <table>
            <thead>
                <tr>
                    <th>TAHUN</th>
                    <th>PRODUKSI</th>
                    <th>KEBUTUHAN PANGAN</th>
                    <th>IMPOR DIBUTUHKAN</th>
                </tr>
            </thead>
            <tbody id="projectionTable"></tbody>
        </table>
    </div>
</section>

<footer class="footer">
    <span>SOYBEAN LAB · INDONESIA</span>
    <span>Model simulasi berbasis data historis FAOSTAT 2010–2023</span>
</footer>

</div>

<script>
const BASE_PRODUCTION = 326;
const BASE_FOOD = 2626;
const OTHER_USE = 86;
const EXPORT = 8;

let selectedYear = 2030;
let selectedGrowth = 3;
let chart = null;

function formatNumber(value) {
    return Math.round(value).toLocaleString('id-ID');
}

function calculate(year, growth) {
    const t = year - 2023;

    const production = BASE_PRODUCTION * Math.pow(1 + growth / 100, t);
    const food = BASE_FOOD * Math.pow(1.01, t);
    const imports = Math.max(0, food + OTHER_USE + EXPORT - production);

    return { production, food, imports };
}

function animateNumber(element, target) {
    const start = Number(element.dataset.current || 0);
    const duration = 450;
    const startTime = performance.now();

    function update(now) {
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = start + (target - start) * eased;

        element.textContent = formatNumber(value);

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.dataset.current = target;
        }
    }

    requestAnimationFrame(update);
}

function updateMetrics() {
    const result = calculate(selectedYear, selectedGrowth);

    document.getElementById('yearNumber').textContent = selectedYear;

    animateNumber(document.getElementById('mainImport'), result.imports);
    animateNumber(document.getElementById('smallProduction'), result.production);
    animateNumber(document.getElementById('smallFood'), result.food);

    animateNumber(document.getElementById('productionCard'), result.production);
    animateNumber(document.getElementById('foodCard'), result.food);
    animateNumber(document.getElementById('importCard'), result.imports);

    updateInsight(result);
    updateTable();
    updateChartMarker();
}

function updateInsight(result) {
    const title = document.getElementById('insightTitle');
    const text = document.getElementById('insightText');
    const bottom = document.getElementById('insightBottom');

    title.textContent = 'Skenario Produksi +' + selectedGrowth + '%';

    text.textContent =
        'Pada tahun ' + selectedYear +
        ', produksi diperkirakan mencapai ' +
        formatNumber(result.production) +
        ' ribu ton, sementara kebutuhan pangan mencapai ' +
        formatNumber(result.food) +
        ' ribu ton.';

    bottom.textContent =
        'Estimasi kebutuhan impor: ' +
        formatNumber(result.imports) +
        ' ribu ton. Hasil ini mengikuti asumsi model simulasi.';
}

function updateTable() {
    const tbody = document.getElementById('projectionTable');
    tbody.innerHTML = '';

    for (let year = 2024; year <= 2035; year++) {
        const result = calculate(year, selectedGrowth);
        const tr = document.createElement('tr');

        if (year === selectedYear) tr.className = 'selected-row';

        tr.innerHTML = `
            <td>${year}</td>
            <td>${formatNumber(result.production)}</td>
            <td>${formatNumber(result.food)}</td>
            <td>${formatNumber(result.imports)}</td>
        `;

        tbody.appendChild(tr);
    }
}

function buildChart() {
    const labels = [];

    for (let year = 2024; year <= 2035; year++) {
        labels.push(year);
    }

    const datasets = [
        {
            label: 'Produksi tetap 0%',
            data: labels.map(y => calculate(y, 0).imports),
            borderColor: '#9ba99a',
            backgroundColor: '#9ba99a',
            borderDash: [5, 5],
            tension: .35,
            borderWidth: 2,
            pointRadius: 2
        },
        {
            label: 'Produksi +3%',
            data: labels.map(y => calculate(y, 3).imports),
            borderColor: '#3b8055',
            backgroundColor: '#3b8055',
            tension: .35,
            borderWidth: 3,
            pointRadius: 2
        },
        {
            label: 'Produksi +5%',
            data: labels.map(y => calculate(y, 5).imports),
            borderColor: '#d1a64f',
            backgroundColor: '#d1a64f',
            tension: .35,
            borderWidth: 3,
            pointRadius: 2
        }
    ];

    const ctx = document.getElementById('simulationChart');

    chart = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        boxWidth: 7,
                        padding: 18,
                        font: { family: 'DM Sans', size: 10 }
                    }
                },
                tooltip: {
                    backgroundColor: '#102c20',
                    padding: 12,
                    callbacks: {
                        label: context =>
                            context.dataset.label + ': ' +
                            formatNumber(context.raw) + ' ribu ton'
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'DM Sans', size: 10 } }
                },
                y: {
                    beginAtZero: false,
                    grid: { color: '#edf0e8' },
                    ticks: { font: { family: 'DM Sans', size: 10 } }
                }
            },
            animation: {
                duration: 700,
                easing: 'easeOutQuart'
            }
        }
    });
}

function updateChartMarker() {
    if (!chart) return;

    const selectedIndex = selectedYear - 2024;

    chart.data.datasets.forEach((dataset, index) => {
        dataset.pointRadius = chart.data.labels.map((_, i) =>
            i === selectedIndex ? 6 : 2
        );
        dataset.pointHoverRadius = 7;
    });

    chart.update();
}

document.getElementById('yearSlider').addEventListener('input', function() {
    selectedYear = Number(this.value);
    updateMetrics();
});

document.querySelectorAll('.scenario-btn').forEach(button => {
    button.addEventListener('click', function() {
        selectedGrowth = Number(this.dataset.growth);

        document.querySelectorAll('.scenario-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        this.classList.add('active');
        updateMetrics();
    });
});

buildChart();
updateMetrics();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(debug=True)
