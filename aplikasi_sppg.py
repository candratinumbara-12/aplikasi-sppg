import base64
from datetime import date, time
import streamlit as st
from fpdf import FPDF

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Aplikasi SPPG - Checklist Laporan PDF",
    page_icon="📋",
    layout="wide",
)

# Inisialisasi Session State
if "data_laporan" not in st.session_state:
    st.session_state.data_laporan = None
if "html_download_button" not in st.session_state:
    st.session_state.html_download_button = None
if "dapur_aktif" not in st.session_state:
    st.session_state.dapur_aktif = "SPPG Paseh Cigentur"

# ==========================================
# 2. CLASS PDF & GENERATOR
# ==========================================
class PDFChecklistResmi(FPDF):
    def header(self):
        self.set_font("Arial", "B", 10)
        self.cell(
            0,
            6,
            "CHECKLIST MONITORING DAN EVALUASI OPERASIONAL SPPG",
            0,
            1,
            "C",
        )
        self.set_font("Arial", "I", 8)
        self.cell(
            0,
            4,
            "Program Badan Gizi Nasional (BGN) - Standard Operating Procedure",
            0,
            1,
            "C",
        )
        self.line(10, 20, 200, 20)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(
            0,
            10,
            f"Halaman {self.page_no()}/{{nb}} - Dokumen Resmi Operasional SPPG",
            0,
            0,
            "C",
        )


def generate_pdf(d):
    pdf = PDFChecklistResmi()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", "", 8)

    col_w = 95
    row_h = 5

    # Header Identitas Dapur & Tim
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w, row_h, f"Nama SPPG: {d.get('nama_sppg')}", 1, 0, "L")
    pdf.cell(
        col_w, row_h, f"Pengawas Keuangan (PLOK): {d.get('plok')}", 1, 1, "L"
    )

    pdf.cell(col_w, row_h, f"Kepala SPPG: {d.get('kepala_sppg')}", 1, 0, "L")
    pdf.cell(col_w, row_h, f"Pengawas Gizi (Plog): {d.get('plog')}", 1, 1, "L")

    pdf.cell(col_w, row_h, f"Tanggal: {d.get('tanggal')}", 1, 0, "L")
    pdf.cell(
        col_w, row_h, f"Asisten Lapangan: {d.get('asisten_lapangan')}", 1, 1, "L"
    )

    pdf.cell(col_w, row_h, f"Jam Mulai Zoom: {d.get('jam_zoom')}", 1, 0, "L")
    pdf.cell(col_w, row_h, f"Chef: {d.get('chef')}", 1, 1, "L")
    pdf.ln(3)

    def print_section(title):
        pdf.set_fill_color(220, 230, 242)
        pdf.set_font("Arial", "B", 9)
        pdf.cell(0, 6, title, 1, 1, "L", fill=True)
        pdf.set_font("Arial", "", 8)

    # I. DATA UMUM
    print_section("I. DATA UMUM")
    pdf.cell(0, 5, "1. JUMLAH PENERIMA MANFAAT & SERTIFIKASI", 0, 1, "L")
    pdf.cell(
        0,
        4,
        f"   - PM Peserta Didik: Terdata ({d.get('pm_didik_potensi')}) | Dilayani Hari Ini ({d.get('pm_didik_dilayani')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - PM 3B (Bumil/Balita): Terdata ({d.get('pm_3b_potensi')}) | Dilayani Hari Ini ({d.get('pm_3b_dilayani')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Total PM Dilayani: {int(d.get('pm_didik_dilayani', 0)) + int(d.get('pm_3b_dilayani', 0))}",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Sertifikat SLHS: {d.get('sertif_slhs')} | Sertifikat Halal: {d.get('sertif_halal')} | Sertifikat BNSP Chef: {d.get('sertif_bnsp')}",
        0,
        1,
        "L",
    )

    pdf.cell(0, 5, "2. AIR BERSIH", 0, 1, "L")
    pdf.cell(
        0,
        4,
        f"   - Air Minum: {d.get('air_minum_sumber')} | pH: {d.get('air_minum_ph')} | Tgl/Jam Ambil: {d.get('air_minum_tgljam')}",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Air Masak: {d.get('air_masak_sumber')} | pH: {d.get('air_masak_ph')} | Tgl/Jam Ambil: {d.get('air_masak_tgljam')}",
        0,
        1,
        "L",
    )

    pdf.cell(0, 5, "3. KONDISI RUANGAN", 0, 1, "L")
    pdf.cell(
        0,
        4,
        f"   - Termometer Berfungsi: {d.get('ruang_termo')} (Ket: {d.get('ruang_termo_ket')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Suhu Ruangan Sesuai (25-30 deg C): {d.get('ruang_suhu')} (Suhu Terkini: {d.get('suhu_terkini')} deg C)",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Kebersihan Ruangan: {d.get('ruang_bersih')} (Catatan: {d.get('ruang_bersih_ket')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Insect Killer Berfungsi: {d.get('insect_killer')} (Jumlah Berfungsi: {d.get('insect_killer_unit')} unit)",
        0,
        1,
        "L",
    )
    pdf.ln(2)

    # II. PENERIMAAN & PENYIMPANAN BAHAN BAKU
    print_section("II. PENERIMAAN DAN PENYIMPANAN BAHAN BAKU")
    pdf.cell(0, 4, "1. Spesifikasi Bahan Baku (Penerimaan):", 0, 1, "L")
    for kat in [
        "Karbohidrat",
        "Protein Hewani",
        "Protein Nabati",
        "Buah",
        "Sayur",
    ]:
        k = kat.lower().replace(" ", "_")
        pdf.cell(
            0,
            4,
            f"   - {kat}: Jml ({d.get(f'bb_{k}_jml')}) | Kualitas ({d.get(f'bb_{k}_kual')}) | Jam ({d.get(f'bb_{k}_jam')}) | Penerima ({d.get(f'bb_{k}_nama')})",
            0,
            1,
            "L",
        )

    pdf.cell(
        0, 4, "2. Suhu Bahan Baku Beku & Ruang Penyimpanan:", 0, 1, "L"
    )
    pdf.cell(
        0,
        4,
        f"   - Beku 1: {d.get('beku1_nama')} ({d.get('beku1_suhu')} deg C, Jam {d.get('beku1_jam')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Beku 2: {d.get('beku2_nama')} ({d.get('beku2_suhu')} deg C, Jam {d.get('beku2_jam')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Suhu Chiller: {d.get('suhu_chiller')} deg C (Jam {d.get('jam_chiller')}) | Suhu Freezer: {d.get('suhu_freezer')} deg C (Jam {d.get('jam_freezer')})",
        0,
        1,
        "L",
    )

    pdf.cell(0, 4, "3. Bahan Makanan & Rotasi:", 0, 1, "L")
    pdf.cell(
        0,
        4,
        f"   - Pencucian Pakai Sumber Air di Atas: {d.get('cuci_air_sesuai')} (Sumber: {d.get('sumber_air_cuci')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Tahu Disimpan di Chiller: {d.get('tahu_chiller')} (Suhu Chiller: {d.get('tahu_suhu_chiller')} deg C)",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Rotasi FIFO/FEFO: {d.get('fifo_fefo')} (Ket: {d.get('fifo_ket')})",
        0,
        1,
        "L",
    )
    pdf.ln(2)

    # III. PERSIAPAN, PENGOLAHAN DAN PENDINGINAN
    print_section("III. PERSIAPAN, PENGOLAHAN DAN PENDINGINAN")
    pdf.cell(
        0,
        4,
        f"1. Higiene Tim Persiapan: Sakit ({d.get('p_sakit')}) | APD ({d.get('p_apd')}) | CTPS ({d.get('p_ctps')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"2. Persiapan: SOP Prohe ({d.get('p_sop_prohe')}) | Bahan Berbau/Lendir ({d.get('p_bahan_rusak')}) | Kendala ({d.get('p_kendala')})",
        0,
        1,
        "L",
    )

    pdf.cell(0, 4, "3. Status Menu Rawan Hari Ini:", 0, 1, "L")
    pdf.cell(
        0,
        4,
        f"   - Ikan/Seafood: {d.get('mr_ikan')} | Ayam Bersantan: {d.get('mr_ayam_santan')}",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Ayam Suwir/Olahan Ulang: {d.get('mr_ayam_suwir')} | Telur Dadar: {d.get('mr_telur')} | Susu: {d.get('mr_susu')}",
        0,
        1,
        "L",
    )

    pdf.cell(
        0,
        4,
        f"4. Higiene Tim Pengolahan: Sakit ({d.get('o_sakit')}) | APD ({d.get('o_apd')}) | CTPS ({d.get('o_ctps')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"5. Pengolahan: Matang Sempurna ({d.get('o_matang')}) | Suhu Matang ({d.get('o_suhu_matang')} deg C, Jam {d.get('o_jam_matang')}) | SOP ({d.get('o_sop')}) | Kendala ({d.get('o_kendala')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"6. Pendinginan: Ruang Steril ({d.get('dingin_ruang')}) | Suhu Diukur ({d.get('dingin_suhu')} deg C) | Nasi >2 jam Ruang ({d.get('nasi_suhu_ruang')})",
        0,
        1,
        "L",
    )
    pdf.ln(2)

    # IV. PEMORSIAN DAN DISTRIBUSI
    print_section("IV. PEMORSIAN DAN DISTRIBUSI")
    pdf.cell(
        0,
        4,
        f"1. Pemorsian: Gizi & URT Sesuai ({d.get('pors_gizi')}) | Suhu Pemorsian ({d.get('pors_suhu')} deg C)",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Quality Control / Organoleptik: Oleh ({d.get('qc_oleh')}), Jam ({d.get('qc_jam')}), Hasil ({d.get('qc_hasil')})",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Sample Menu Simpan (2 Sampel): {d.get('sampel_2menu')} | Kendala: {d.get('pors_kendala')}",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Sisa Makanan Pemorsian: Nasi ({d.get('sisa_nasi')} kg), Prohe ({d.get('sisa_prohe')} kg), Prona ({d.get('sisa_prona')} kg), Sayur ({d.get('sisa_sayur')} kg), Buah ({d.get('sisa_buah')} kg)",
        0,
        1,
        "L",
    )

    pdf.cell(
        0,
        4,
        f"2. Alat & Tempat: Alat Terpisah ({d.get('alat_pisah')}) | Meja/Alat Bersih ({d.get('meja_bersih')}) | Bebas Bocor/Genangan ({d.get('sanitasi_fisik')})",
        0,
        1,
        "L",
    )

    pdf.cell(0, 4, "3. Rantai Distribusi:", 0, 1, "L")
    pdf.cell(
        0,
        4,
        f"   - Jam Selesai Masak: {d.get('jam_selesai_masak')} | Jam Berangkat: {d.get('jam_berangkat')} | Jam Sampai: {d.get('jam_sampai')} | Jam Konsumsi: {d.get('jam_konsumsi')}",
        0,
        1,
        "L",
    )
    pdf.cell(
        0,
        4,
        f"   - Label/Segel Ompreng: {d.get('label_segel')} | Suhu Bagikan (Panas: {d.get('suhu_dist_panas')} deg C / Dingin: {d.get('suhu_dist_dingin')} deg C)",
        0,
        1,
        "L",
    )
    pdf.cell(0, 4, f"   - Kendala Distribusi: {d.get('dist_kendala')}", 0, 1, "L")
    pdf.ln(2)

    # V. TEMUAN & KEPUTUSAN
    print_section("V. TEMUAN & KEPUTUSAN FINAL")
    pdf.cell(0, 4, f"Temuan Operasional: {d.get('temuan_khusus')}", 0, 1, "L")
    pdf.set_font("Arial", "B", 9)
    pdf.cell(0, 5, f"KEPUTUSAN FINAL: {d.get('keputusan_final')}", 0, 1, "L")
    pdf.set_font("Arial", "I", 8)
    pdf.cell(
        0,
        4,
        "Kontak Darurat: PSC 119 WA +62 8777 7591097 | pheoc.indonesia@kemkes.go.id",
        0,
        1,
        "L",
    )

    out = pdf.output()
    if isinstance(out, str):
        return out.encode("latin1")
    return bytes(out)


# ==========================================
# 3. ANTARMUKA STREAMLIT (UI)
# ==========================================
st.title("📋 Sistem Checklist Monitoring & PDF Generator SPPG")
st.caption("Aplikasi Input Laporan Harian Dapur SPPG - Badan Gizi Nasional")

st.session_state.dapur_aktif = st.text_input(
    "Unit Dapur / SPPG:", value=st.session_state.dapur_aktif
)

with st.form("form_presisi_pdf"):
    st.subheader("1. Identitas Tim & Jadwal")
    c1, c2 = st.columns(2)
    with c1:
        f_kepala = st.text_input("Kepala SPPG", "Candra Tinumbara")
        f_plok = st.text_input("Pengawas Keuangan (PLOK)", "Asep")
        f_plog = st.text_input("Pengawas Gizi (Plog)", "Rina")
    with c2:
        f_asisten = st.text_input("Asisten Lapangan", "Budi")
        f_chef = st.text_input("Chef", "Dedi")
        f_tanggal = st.date_input("Tanggal Operasional", date.today())
        # PERBAIKAN: Menggunakan objek time(07, 00) bukan date.today()
        f_jam_zoom = st.time_input("Jam Mulai Zoom", time(7, 0))

    st.subheader("2. Data Umum & Air Bersih")
    c3, c4 = st.columns(2)
    with c3:
        f_pm_d_pot = st.number_input(
            "PM Didik (Terdata)", min_value=0, value=300
        )
        f_pm_d_dil = st.number_input(
            "PM Didik (Dilayani Hari Ini)", min_value=0, value=300
        )
        f_pm_3b_pot = st.number_input(
            "PM 3B Bumil/Balita (Terdata)", min_value=0, value=50
        )
        f_pm_3b_dil = st.number_input(
            "PM 3B Bumil/Balita (Dilayani)", min_value=0, value=50
        )
    with c4:
        f_slhs = st.selectbox("Sertifikat SLHS", ["Ada", "Tidak Ada/Proses"])
        f_halal = st.selectbox("Sertifikat Halal", ["Ada", "Tidak Ada/Proses"])
        f_bnsp = st.selectbox("Sertifikat BNSP Chef", ["Ada", "Tidak Ada"])

    st.markdown("**Air Bersih & Masak**")
    ca, cb = st.columns(2)
    with ca:
        f_air_m_src = st.text_input("Sumber Air Minum", "Depot Isi Ulang / RO")
        f_air_m_ph = st.text_input("pH Air Minum", "7.0")
        f_air_m_tgl = st.text_input("Tgl/Jam Ambil Air Minum", "05:00 WIB")
    with cb:
        f_air_k_src = st.text_input("Sumber Air Masak", "PDAM / Sumur Terfilter")
        f_air_k_ph = st.text_input("pH Air Masak", "6.8")
        f_air_k_tgl = st.text_input("Tgl/Jam Ambil Air Masak", "04:30 WIB")

    st.markdown("**Ruangan & Sanitasi**")
    cr1, cr2 = st.columns(2)
    with cr1:
        f_ruang_termo = st.selectbox("Termometer Berfungsi", ["Ya", "Tidak"])
        f_ruang_termo_ket = st.text_input("Keterangan Termometer", "Kalibrasi OK")
        f_ruang_suhu = st.selectbox("Suhu Ruangan Sesuai (25-30°C)", ["Ya", "Tidak"])
        f_suhu_terkini = st.text_input("Suhu Terkini (°C)", "27")
    with cr2:
        f_ruang_bersih = st.selectbox("Kebersihan Ruangan OK", ["Ya", "Tidak"])
        f_ruang_bersih_ket = st.text_input("Catatan Kebersihan", "Bersih, bebas debu")
        f_insect_killer = st.selectbox("Insect Killer Berfungsi", ["Ya", "Tidak"])
        f_insect_unit = st.number_input("Jumlah Insect Killer (Unit)", min_value=0, value=2)

    st.subheader("3. Penerimaan Bahan Baku")
    st.caption("Format: Jumlah | Kualitas | Jam Terima | Nama Penerima")
    
    def input_bb(label):
        col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 3])
        with col_a:
            jml = st.text_input(f"Jml {label}", "50 kg", key=f"jml_{label}")
        with col_b:
            kual = st.selectbox(f"Kual {label}", ["Baik/Sesuai SOP", "Kurang Baik"], key=f"kual_{label}")
        with col_c:
            jam = st.text_input(f"Jam {label}", "05:30", key=f"jam_{label}")
        with col_d:
            nama = st.text_input(f"Penerima {label}", "Asep", key=f"nama_{label}")
        return jml, kual, jam, nama

    bb_karbo = input_bb("Karbohidrat")
    bb_prohe = input_bb("Protein Hewani")
    bb_prona = input_bb("Protein Nabati")
    bb_buah = input_bb("Buah")
    bb_sayur = input_bb("Sayur")

    st.markdown("**Suhu Penyimpanan Beku & Cold Storage**")
    cs1, cs2 = st.columns(2)
    with cs1:
        f_beku1_nama = st.text_input("Bahan Beku 1", "Daging Ayam")
        f_beku1_suhu = st.text_input("Suhu Beku 1 (°C)", "-18")
        f_beku1_jam = st.text_input("Jam Cek Beku 1", "06:00")
        f_chiller_suhu = st.text_input("Suhu Chiller (°C)", "4")
        f_chiller_jam = st.text_input("Jam Cek Chiller", "06:00")
    with cs2:
        f_beku2_nama = st.text_input("Bahan Beku 2", "Daging Sapi")
        f_beku2_suhu = st.text_input("Suhu Beku 2 (°C)", "-15")
        f_beku2_jam = st.text_input("Jam Cek Beku 2", "06:00")
        f_freezer_suhu = st.text_input("Suhu Freezer (°C)", "-20")
        f_freezer_jam = st.text_input("Jam Cek Freezer", "06:00")

    st.markdown("**Aturan Khusus & Rotasi**")
    cx1, cx2, cx3 = st.columns(3)
    with cx1:
        f_cuci_air = st.selectbox("Pencucian Air Sesuai", ["Ya", "Tidak"])
        f_cuci_air_src = st.text_input("Sumber Air Cuci", "Air Terfilter")
    with cx2:
        f_tahu_chiller = st.selectbox("Tahu Masuk Chiller", ["Ya", "Tidak"])
        f_tahu_suhu = st.text_input("Suhu Chiller Tahu (°C)", "4")
    with cx3:
        f_fifo = st.selectbox("Rotasi FIFO/FEFO Diterapkan", ["Ya", "Tidak"])
        f_fifo_ket = st.text_input("Catatan FIFO", "Labeling Rapi")

    st.subheader("4. Persiapan, Pengolahan, & Pendinginan")
    st.markdown("**Higiene & Persiapan**")
    cp1, cp2 = st.columns(2)
    with cp1:
        f_p_sakit = st.selectbox("Tim Persiapan Sakit", ["Tidak Ada", "Ada (Diistirahatkan)"])
        f_p_apd = st.selectbox("Tim Persiapan Pakai APD Lengkap", ["Ya", "Tidak"])
        f_p_ctps = st.selectbox("Tim Persiapan CTPS", ["Ya", "Tidak"])
    with cp2:
        f_p_sop_prohe = st.selectbox("SOP Thawing Prohe Sesuai", ["Ya", "Tidak"])
        f_p_bahan_rusak = st.selectbox("Ada Bahan Berbau/Lendir", ["Tidak Ada", "Ada (Afkir)"])
        f_p_kendala = st.text_input("Kendala Persiapan", "Nihil")

    st.markdown("**Status Menu Rawan**")
    cmr1, cmr2 = st.columns(2)
    with cmr1:
        f_mr_ikan = st.selectbox("Ikan / Seafood", ["Aman", "Tidak Digunakan Hari Ini"])
        f_mr_ayam_santan = st.selectbox("Ayam Bersantan", ["Aman", "Tidak Digunakan Hari Ini"])
        f_mr_ayam_suwir = st.selectbox("Ayam Suwir / Olahan Ulang", ["Aman", "Tidak Digunakan Hari Ini"])
    with cmr2:
        f_mr_telur = st.selectbox("Telur Dadar", ["Aman", "Tidak Digunakan Hari Ini"])
        f_mr_susu = st.selectbox("Susu Kemasan/UHT", ["Aman", "Tidak Digunakan Hari Ini"])

    st.markdown("**Pengolahan & Pendinginan**")
    co1, co2 = st.columns(2)
    with co1:
        f_o_sakit = st.selectbox("Tim Pengolahan Sakit", ["Tidak Ada", "Ada"])
        f_o_apd = st.selectbox("Tim Pengolahan APD Lengkap", ["Ya", "Tidak"])
        f_o_ctps = st.selectbox("Tim Pengolahan CTPS", ["Ya", "Tidak"])
        f_o_matang = st.selectbox("Tingkat Kematangan Sempurna", ["Ya", "Tidak"])
        f_o_suhu_matang = st.text_input("Suhu Matang Makanan (°C)", "85")
        f_o_jam_matang = st.text_input("Jam Selesai Masak", "08:00")
    with co2:
        f_o_sop = st.selectbox("Memasak Sesuai SOP BGN", ["Ya", "Tidak"])
        f_o_kendala = st.text_input("Kendala Pengolahan", "Nihil")
        f_dingin_ruang = st.selectbox("Ruang Pendinginan Steril", ["Ya", "Tidak"])
        f_dingin_suhu = st.text_input("Suhu Ruang Pendinginan (°C)", "24")
        f_nasi_suhu_ruang = st.selectbox("Nasi >2 Jam di Suhu Terbuka", ["Tidak", "Ya"])

    st.subheader("5. Pemorsian & Distribusi")
    cd1, cd2 = st.columns(2)
    with cd1:
        f_pors_gizi = st.selectbox("Pemorsian Sesuai URT & Gizi", ["Ya", "Tidak"])
        f_pors_suhu = st.text_input("Suhu Makanan Saat Diporsi (°C)", "65")
        f_qc_oleh = st.text_input("QC / Organoleptik Oleh", "Pengawas Gizi (Plog)")
        f_qc_jam = st.text_input("Jam Organoleptik", "08:30")
        f_qc_hasil = st.selectbox("Hasil Organoleptik (Rasa/Aroma/Tekstur)", ["Baik/Layak", "Tidak Layak"])
        f_sampel_2menu = st.selectbox("Sampel 2 Porsi Disimpan Steril", ["Ya", "Tidak"])
        f_pors_kendala = st.text_input("Kendala Pemorsian", "Nihil")
    with cd2:
        f_sisa_nasi = st.text_input("Sisa Nasi (kg)", "0")
        f_sisa_prohe = st.text_input("Sisa Prohe (kg)", "0")
        f_sisa_prona = st.text_input("Sisa Prona (kg)", "0")
        f_sisa_sayur = st.text_input("Sisa Sayur (kg)", "0")
        f_sisa_buah = st.text_input("Sisa Buah (kg)", "0")
        f_alat_pisah = st.selectbox("Alat Mentah & Matang Dipisah", ["Ya", "Tidak"])
        f_meja_bersih = st.selectbox("Meja Pemorsian Steril", ["Ya", "Tidak"])
        f_sanitasi_fisik = st.selectbox("Bebas Bocor & Genangan Air", ["Ya", "Tidak"])

    st.markdown("**Distribusi**")
    ct1, ct2 = st.columns(2)
    with ct1:
        f_jam_selesai_masak = st.text_input("Jam Selesai Masak All", "08:00 WIB")
        f_jam_berangkat = st.text_input("Jam Berangkat Armada", "09:00 WIB")
        f_jam_sampai = st.text_input("Jam Sampai di Sekolah/PM", "09:30 WIB")
        f_jam_konsumsi = st.text_input("Jam Target Konsumsi", "10:00 WIB")
    with ct2:
        f_label_segel = st.selectbox("Ompreng Disegel & Diberi Label", ["Ya", "Tidak"])
        f_suhu_dist_panas = st.text_input("Suhu Makanan Panas Tiba (°C)", "60")
        f_suhu_dist_dingin = st.text_input("Suhu Makanan Dingin Tiba (°C)", "15")
        f_dist_kendala = st.text_input("Kendala Distribusi", "Lalu lintas lancar")

    st.subheader("6. Temuan Khusus & Keputusan Final")
    f_temuan_khusus = st.text_area("Temuan Operasional Harian", "Seluruh alur kerja berjalan sesuai SOP standar BGN.")
    f_keputusan_final = st.selectbox(
        "Keputusan Final Operasional Hari Ini",
        ["LULUS / LAYAK DISTRIBUSI", "LULUS DENGAN CATATAN", "DITOLAK / TIDAK LAYAK"]
    )

    btn_submit = st.form_submit_button("💾 Proses & Siapkan PDF Resmi")

    if btn_submit:
        data_lap = {
            "nama_sppg": st.session_state.dapur_aktif,
            "kepala_sppg": f_kepala,
            "plok": f_plok,
            "plog": f_plog,
            "asisten_lapangan": f_asisten,
            "chef": f_chef,
            "tanggal": str(f_tanggal),
            "jam_zoom": str(f_jam_zoom),
            "pm_didik_potensi": f_pm_d_pot,
            "pm_didik_dilayani": f_pm_d_dil,
            "pm_3b_potensi": f_pm_3b_pot,
            "pm_3b_dilayani": f_pm_3b_dil,
            "sertif_slhs": f_slhs,
            "sertif_halal": f_halal,
            "sertif_bnsp": f_bnsp,
            "air_minum_sumber": f_air_m_src,
            "air_minum_ph": f_air_m_ph,
            "air_minum_tgljam": f_air_m_tgl,
            "air_masak_sumber": f_air_k_src,
            "air_masak_ph": f_air_k_ph,
            "air_masak_tgljam": f_air_k_tgl,
            "ruang_termo": f_ruang_termo,
            "ruang_termo_ket": f_ruang_termo_ket,
            "ruang_suhu": f_ruang_suhu,
            "suhu_terkini": f_suhu_terkini,
            "ruang_bersih": f_ruang_bersih,
            "ruang_bersih_ket": f_ruang_bersih_ket,
            "insect_killer": f_insect_killer,
            "insect_killer_unit": f_insect_unit,
            "bb_karbohidrat_jml": bb_karbo[0],
            "bb_karbohidrat_kual": bb_karbo[1],
            "bb_karbohidrat_jam": bb_karbo[2],
            "bb_karbohidrat_nama": bb_karbo[3],
            "bb_protein_hewani_jml": bb_prohe[0],
            "bb_protein_hewani_kual": bb_prohe[1],
            "bb_protein_hewani_jam": bb_prohe[2],
            "bb_protein_hewani_nama": bb_prohe[3],
            "bb_protein_nabati_jml": bb_prona[0],
            "bb_protein_nabati_kual": bb_prona[1],
            "bb_protein_nabati_jam": bb_prona[2],
            "bb_protein_nabati_nama": bb_prona[3],
            "bb_buah_jml": bb_buah[0],
            "bb_buah_kual": bb_buah[1],
            "bb_buah_jam": bb_buah[2],
            "bb_buah_nama": bb_buah[3],
            "bb_sayur_jml": bb_sayur[0],
            "bb_sayur_kual": bb_sayur[1],
            "bb_sayur_jam": bb_sayur[2],
            "bb_sayur_nama": bb_sayur[3],
            "beku1_nama": f_beku1_nama,
            "beku1_suhu": f_beku1_suhu,
            "beku1_jam": f_beku1_jam,
            "beku2_nama": f_beku2_nama,
            "beku2_suhu": f_beku2_suhu,
            "beku2_jam": f_beku2_jam,
            "suhu_chiller": f_chiller_suhu,
            "jam_chiller": f_chiller_jam,
            "suhu_freezer": f_freezer_suhu,
            "jam_freezer": f_freezer_jam,
            "cuci_air_sesuai": f_cuci_air,
            "sumber_air_cuci": f_cuci_air_src,
            "tahu_chiller": f_tahu_chiller,
            "tahu_suhu_chiller": f_tahu_suhu,
            "fifo_fefo": f_fifo,
            "fifo_ket": f_fifo_ket,
            "p_sakit": f_p_sakit,
            "p_apd": f_p_apd,
            "p_ctps": f_p_ctps,
            "p_sop_prohe": f_p_sop_prohe,
            "p_bahan_rusak": f_p_bahan_rusak,
            "p_kendala": f_p_kendala,
            "mr_ikan": f_mr_ikan,
            "mr_ayam_santan": f_mr_ayam_santan,
            "mr_ayam_suwir": f_mr_ayam_suwir,
            "mr_telur": f_mr_telur,
            "mr_susu": f_mr_susu,
            "o_sakit": f_o_sakit,
            "o_apd": f_o_apd,
            "o_ctps": f_o_ctps,
            "o_matang": f_o_matang,
            "o_suhu_matang": f_o_suhu_matang,
            "o_jam_matang": f_o_jam_matang,
            "o_sop": f_o_sop,
            "o_kendala": f_o_kendala,
            "dingin_ruang": f_dingin_ruang,
            "dingin_suhu": f_dingin_suhu,
            "nasi_suhu_ruang": f_nasi_suhu_ruang,
            "pors_gizi": f_pors_gizi,
            "pors_suhu": f_pors_suhu,
            "qc_oleh": f_qc_oleh,
            "qc_jam": f_qc_jam,
            "qc_hasil": f_qc_hasil,
            "sampel_2menu": f_sampel_2menu,
            "pors_kendala": f_pors_kendala,
            "sisa_nasi": f_sisa_nasi,
            "sisa_prohe": f_sisa_prohe,
            "sisa_prona": f_sisa_prona,
            "sisa_sayur": f_sisa_sayur,
            "sisa_buah": f_sisa_buah,
            "alat_pisah": f_alat_pisah,
            "meja_bersih": f_meja_bersih,
            "sanitasi_fisik": f_sanitasi_fisik,
            "jam_selesai_masak": f_jam_selesai_masak,
            "jam_berangkat": f_jam_berangkat,
            "jam_sampai": f_jam_sampai,
            "jam_konsumsi": f_jam_konsumsi,
            "label_segel": f_label_segel,
            "suhu_dist_panas": f_suhu_dist_panas,
            "suhu_dist_dingin": f_suhu_dist_dingin,
            "dist_kendala": f_dist_kendala,
            "temuan_khusus": f_temuan_khusus,
            "keputusan_final": f_keputusan_final,
        }

        pdf_bytes = generate_pdf(data_lap)
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        filename = f"Checklist_SPPG_{st.session_state.dapur_aktif}_{date.today()}.pdf"

        st.session_state.html_download_button = f"""
            <a href="data:application/pdf;base64,{b64_pdf}" download="{filename}" style="
                display: inline-block;
                width: 100%;
                padding: 12px 20px;
                color: white;
                background-color: #ff4b4b;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                font-size: 16px;
                text-align: center;
                box-sizing: border-box;
                margin-top: 10px;
            " target="_blank">📄 KLIK DISINI UNTUK UNDUH PDF (RAMAH IDM & BROWSER HP)</a>
        """
        st.success("PDF berhasil disiapkan! Silakan unduh di bawah ini.")

# ==========================================
# 4. AREA TOMBOL UNDUH (DI LUAR FORM)
# ==========================================
if (
    "html_download_button" in st.session_state
    and st.session_state.html_download_button
):
    st.markdown("---")
    st.subheader("📥 Unduh Laporan Resmi PDF")
    # PERBAIKAN: Menggunakan unsafe_allow_html=True
    st.markdown(st.session_state.html_download_button, unsafe_allow_html=True)
