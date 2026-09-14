import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF
from datetime import date, time
import base64

# Konfigurasi Halaman
st.set_page_config(page_title="Sistem Operasional SPPG", page_icon="🍲", layout="wide")

# ==========================================
# 1. KELAS GENERATOR PDF LAPORAN KUSTOM RAPI
# ==========================================
class PDFReport(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Halaman {self.page_no()} | Dicetak otomatis via Sistem Cloud SPPG", 0, 0, "C")

def generate_pdf(d):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", "", 9)

    # Judul Utama (Kotak Biru Tua)
    pdf.set_fill_color(0, 43, 91)      
    pdf.set_text_color(255, 255, 255)  
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "CHECKLIST HARIAN - KOORDINASI ZOOM", 1, 1, "C", fill=True)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 9)

    # Tabel Identitas 2 Kolom Atas
    col_w = 95
    row_h = 6
    
    identitas_rows = [
        ("Nama SPPG: " + str(d.get("nama_sppg")), "Pengawas Keu: " + str(d.get("pengawas_keu", "-"))),
        ("Kepala SPPG: " + str(d.get("kepala_sppg")), "Pengawas Gizi: " + str(d.get("pengawas_gizi"))),
        ("Tanggal: " + str(d.get("tanggal")), "Asisten Lapangan: " + str(d.get("asisten_lapangan", "-"))),
        ("Jam Mulai Zoom: " + str(d.get("jam_zoom")), "Chef: " + str(d.get("chef", "-")))
    ]

    for col1_text, col2_text in identitas_rows:
        pdf.cell(col_w, row_h, col1_text, 1, 0, "L")
        pdf.cell(col_w, row_h, col2_text, 1, 1, "L")

    pdf.ln(3)

    def add_section_header(title):
        pdf.set_fill_color(218, 230, 242)  
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, title, 1, 1, "L", fill=True)
        pdf.set_font("Arial", "", 9)

    # I. DATA UMUM
    add_section_header("I. DATA UMUM")
    pdf.cell(0, 5, "  Jumlah Penerima Manfaat (PM):", 0, 1, "L")
    pdf.cell(0, 5, f"    - Peserta Didik: {d.get('pm_didik')} dilayani", 0, 1, "L")
    pdf.cell(0, 5, f"    - Ibu Hamil/Menyusui/Balita: {d.get('pm_3b')} dilayani", 0, 1, "L")
    
    pdf.cell(0, 5, "  Sertifikasi:", 0, 1, "L")
    pdf.cell(0, 5, f"    - SLHS: {d.get('sertif_slhs')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Halal: {d.get('sertif_halal')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - BNSP Chef: {d.get('sertif_bnsp')}", 0, 1, "L")

    pdf.cell(0, 5, "  Sumber Air Bersih:", 0, 1, "L")
    pdf.cell(0, 5, f"    - Air Minum: {d.get('sumber_air_minum')} (pH: {d.get('ph_minum')})", 0, 1, "L")
    pdf.cell(0, 5, f"    - Air Masak: {d.get('sumber_air_masak')} (pH: {d.get('ph_masak')})", 0, 1, "L")

    pdf.cell(0, 5, "  Kondisi Ruangan:", 0, 1, "L")
    pdf.cell(0, 5, f"    - Termometer tersedia: {d.get('ruang_termo')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Suhu sesuai standar: {d.get('ruang_suhu')} ({d.get('suhu_ruang')})", 0, 1, "L")
    pdf.cell(0, 5, f"    - Ruangan bersih: {d.get('ruang_bersih')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Insect killer berfungsi: {d.get('insect_killer')}", 0, 1, "L")
    pdf.ln(2)

    # II. PENERIMAAN BAHAN BAKU
    add_section_header("II. PENERIMAAN BAHAN BAKU")
    pdf.cell(0, 5, "  Waktu Penerimaan Bahan Baku:", 0, 1, "L")
    pdf.cell(0, 5, f"    - Karbohidrat: {d.get('t_karbo')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Protein Hewani: {d.get('t_prohe')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Protein Nabati: {d.get('t_prona')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sayuran: {d.get('t_sayur')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Buah: {d.get('t_buah')}", 0, 1, "L")

    pdf.cell(0, 5, "  Kesesuaian Stok:", 0, 1, "L")
    pdf.cell(0, 5, f"    - Karbohidrat: {d.get('k_karbo')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Protein Hewani: {d.get('k_prohe')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Protein Nabati: {d.get('k_prona')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sayur: {d.get('k_sayur')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Buah: {d.get('k_buah')}", 0, 1, "L")
    pdf.ln(2)

    # III. PERSIAPAN & PENGOLAHAN
    add_section_header("III. PERSIAPAN, PENGOLAHAN DAN PENDINGINAN")
    pdf.cell(0, 5, f"  Tim sakit / demam / batuk: {d.get('hig_sakit')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Penggunaan APD lengkap: {d.get('apd_pakai')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Cuci Tangan Pakai Sabun (CTPS): {d.get('hig_ctps')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Menu Rawan Hari Ini: {d.get('menu_rawan')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Pengecekan Suhu Matang Sempurna: {d.get('suhu_matang')}", 0, 1, "L")
    pdf.ln(2)

    # IV. PENGEMASAN & DISTRIBUSI
    add_section_header("IV. PENGEMASAN DAN DISTRIBUSI")
    pdf.cell(0, 5, f"  Jam Pengemasan: {d.get('jam_kemas')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Suhu Makanan Saat Dikemas: {d.get('suhu_kemas')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Wadah Pangan Food Grade: {d.get('wadah_pangan')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Distribusi Tepat Waktu: {d.get('distrib_tepat')}", 0, 1, "L")
    pdf.ln(2)

    # V. PENGAWASAN MUTU & SAMPEL
    add_section_header("V. PENGAWASAN MUTU & SAMPEL")
    pdf.cell(0, 5, f"  Uji Organoleptik (Rasa/Aroma/Warna): {d.get('uji_organoleptik')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Penyimpanan Food Sample (2x24 Jam): {d.get('sampel_simpan')} (Suhu: {d.get('suhu_sampel')})", 0, 1, "L")
    pdf.ln(2)

    # VI. KEBERSIHAN & LIMBAH
    add_section_header("VI. KEBERSIHAN AREA & PENGELOLAAN LIMBAH")
    pdf.cell(0, 5, f"  Pembersihan & Sanitasi Dapur Total: {d.get('dapur_bersih')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Pengelolaan Limbah & Sampah: {d.get('limbah_kelola')}", 0, 1, "L")
    pdf.ln(2)

    # VII. EVALUASI SISA MAKANAN & CATATAN
    add_section_header("VII. EVALUASI SISA MAKANAN (PLATE WASTE) & CATATAN KHUSUS")
    pdf.cell(0, 5, "  Estimasi Sisa Makanan (Gram):", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Nasi / Karbohidrat: {d.get('sisa_nasi')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Protein Hewani: {d.get('sisa_prohe')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Protein Nabati: {d.get('sisa_prona')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Sayuran: {d.get('sisa_sayur')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Buah: {d.get('sisa_buah')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Catatan / Kendala Operasional: {d.get('catatan')}", 0, 1, "L")

    return pdf.output(dest="S").encode("latin1")


# ==========================================
# 2. INISIALISASI SESSION STATE LOGIN & DAPUR
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "data_laporan" not in st.session_state:
    st.session_state.data_laporan = None
if "daftar_dapur" not in st.session_state:
    st.session_state.daftar_dapur = [
        "SPPG Bandung Paseh Cigentur", 
        "SPPG Rancaekek Kencana", 
        "SPPG Majalaya"
    ]


# ==========================================
# 3. HALAMAN LOGIN
# ==========================================
if not st.session_state.logged_in:
    st.title("🔐 Login - Sistem Cloud SPPG")
    st.markdown("Badan Gizi Nasional - Program Pemenuhan Gizi Nasional")
    
    with st.form("form_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Masuk")
        
        if submit_login:
            # Contoh validasi sederhana (bisa disesuaikan dengan database Supabase Anda)
            if username == "admin" and password == "sppg2026":
                st.session_state.logged_in = True
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Username atau Password salah!")
                
else:
    # ==========================================
    # 4. HALAMAN UTAMA APLIKASI SETELAH LOGIN
    # ==========================================
    st.sidebar.title("⚙️ Menu Navigasi")
    
    # Fitur Tambah Dapur Baru di Sidebar
    st.sidebar.markdown("### Tambah Dapur Baru")
    dapur_baru = st.sidebar.text_input("Nama Dapur/SPPG Baru")
    if st.sidebar.button("Tambah Dapur"):
        if dapur_baru and dapur_baru not in st.session_state.daftar_dapur:
            st.session_state.daftar_dapur.append(dapur_baru)
            st.sidebar.success(f"Dapur {dapur_baru} berhasil ditambahkan!")
        else:
            st.sidebar.warning("Nama dapur kosong atau sudah ada.")

    if st.sidebar.button("Keluar (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🍲 Sistem Cloud Pengawasan Operasional SPPG")
    st.markdown("Badan Gizi Nasional - Program Pemenuhan Gizi Nasional")

    # Pilih Dapur yang aktif
    pilih_dapur = st.selectbox("Pilih Dapur / SPPG Aktif", st.session_state.daftar_dapur)

    with st.form("form_checklist_sppg"):
        st.subheader(f"Formulir Checklist Harian - {pilih_dapur}")
        
        col1, col2 = st.columns(2)
        with col1:
            db_nama = st.text_input("Nama SPPG", pilih_dapur)
            db_kepala = st.text_input("Kepala SPPG", "Candra Tinumbara")
            tanggal = st.date_input("Tanggal Checklist", date.today())
            jam_zoom = st.time_input("Jam Mulai Zoom", time(14, 0))
            pengawas_gizi = st.text_input("Pengawas Gizi", "Priska Grace")
            chef = st.text_input("Chef", "Davi Agus Nugraha")
        
        with col2:
            pengawas_keu = st.text_input("Pengawas Keuangan", "Cintia Rinawati")
            asisten_lapangan = st.text_input("Asisten Lapangan", "-")
            pm_didik_hari_ini = st.number_input("Jumlah Peserta Didik Dilayani", value=3000)
            pm_3b_hari_ini = st.number_input("Jumlah PM 3B (Ibu Hamil/Balita) Dilayani", value=150)

        st.markdown("---")
        st.markdown("### I. Data Umum & Sertifikasi")
        c1, c2, c3 = st.columns(3)
        with c1:
            sertif_slhs = st.selectbox("Sertifikat SLHS", ["Ya", "Tidak"], index=0)
            sumber_air_minum = st.text_input("Sumber Air Minum", "PDAM")
            ph_minum = st.text_input("pH Air Minum", "7.0 (Sesuai Standar)")
        with c2:
            sertif_halal = st.selectbox("Sertifikat Halal", ["Ya", "Tidak"], index=0)
            sumber_air_masak = st.text_input("Sumber Air Masak", "PDAM")
            ph_masak = st.text_input("pH Air Masak", "7.0 (Sesuai Standar)")
        with c3:
            sertif_bnsp = st.selectbox("Sertifikat BNSP Chef", ["Ya", "Tidak"], index=0)
            ruang_termo = st.selectbox("Termometer tersedia", ["Ya", "Tidak"], index=0)
            ruang_suhu = st.selectbox("Suhu sesuai standar", ["Ya", "Tidak"], index=0)
            suhu_ruang = st.text_input("Suhu Ruangan (°C)", "26")
            ruang_bersih = st.selectbox("Ruangan bersih", ["Ya", "Tidak"], index=0)
            insect_killer = st.selectbox("Insect killer berfungsi", ["Ya", "Tidak"], index=0)

        st.markdown("---")
        st.markdown("### II. Penerimaan Bahan Baku")
        p1, p2, p3, p4, p5 = st.columns(5)
        with p1:
            jam_terima_karbo = st.text_input("Jam Karbo", "05:30")
            karbo = st.selectbox("Stok Karbo", ["Sesuai", "Tidak"], index=0)
        with p2:
            jam_terima_prohe = st.text_input("Jam Prohe", "05:30")
            prohe = st.selectbox("Stok Prohe", ["Sesuai", "Tidak"], index=0)
        with p3:
            jam_terima_prona = st.text_input("Jam Prona", "05:30")
            prona = st.selectbox("Stok Prona", ["Sesuai", "Tidak"], index=0)
        with p4:
            jam_terima_sayur = st.text_input("Jam Sayur", "05:30")
            sayur = st.selectbox("Stok Sayur", ["Sesuai", "Tidak"], index=0)
        with p5:
            jam_terima_buah = st.text_input("Jam Buah", "05:30")
            buah = st.selectbox("Stok Buah", ["Sesuai", "Tidak"], index=0)

        st.markdown("---")
        st.markdown("### III. Persiapan, Pengolahan & Pendinginan")
        o1, o2, o3 = st.columns(3)
        with o1:
            hig_sakit = st.selectbox("Tim sakit / demam / batuk", ["Tidak Ada", "Ada"], index=0)
            apd_pakai = st.selectbox("Penggunaan APD lengkap", ["Ya", "Tidak"], index=0)
        with o2:
            hig_ctps = st.selectbox("Cuci Tangan Pakai Sabun (CTPS)", ["Ya", "Tidak"], index=0)
            menu_rawan = st.text_input("Menu Rawan Hari Ini", "Ikan / Santan")
        with o3:
            suhu_matang = st.text_input("Pengecekan Suhu Matang Sempurna", "Ya (>85°C)")

        st.markdown("---")
        st.markdown("### IV. Pengemasan & Distribusi")
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            jam_kemas = st.text_input("Jam Pengemasan", "09:00 - 10:00")
        with d2:
            suhu_kemas = st.text_input("Suhu Makanan Saat Dikemas", "65°C")
        with d3:
            wadah_pangan = st.selectbox("Wadah Pangan Food Grade", ["Ya", "Tidak"], index=0)
        with d4:
            distrib_tepat = st.selectbox("Distribusi Tepat Waktu", ["Ya", "Tidak"], index=0)

        st.markdown("---")
        st.markdown("### V. Pengawasan Mutu & Sampel")
        m1, m2 = st.columns(2)
        with m1:
            uji_organoleptik = st.selectbox("Uji Organoleptik (Rasa/Aroma/Warna)", ["Sesuai / Layak", "Tidak Layak"], index=0)
        with m2:
            sampel_simpan = st.selectbox("Penyimpanan Food Sample (2x24 Jam)", ["Ya", "Tidak"], index=0)
            suhu_sampel = st.text_input("Suhu Penyimpanan Sampel", "4°C (Chiller)")

        st.markdown("---")
        st.markdown("### VI. Kebersihan Area & Pengelolaan Limbah")
        k_l1, k_l2 = st.columns(2)
        with k_l1:
            dapur_bersih = st.selectbox("Pembersihan & Sanitasi Dapur Total", ["Ya", "Tidak"], index=0)
        with k_l2:
            limbah_kelola = st.selectbox("Pengelolaan Limbah & Sampah", ["Terkelola Baik", "Kurang Baik"], index=0)

        st.markdown("---")
        st.markdown("### VII. Evaluasi Sisa Makanan (Plate Waste) & Catatan")
        s_m1, s_m2, s_m3, s_m4, s_m5 = st.columns(5)
        with s_m1:
            sisa_nasi_gram = st.text_input("Sisa Nasi", "50 gram")
        with s_m2:
            sisa_prohe_gram = st.text_input("Sisa Prohe", "20 gram")
        with s_m3:
            sisa_prona_gram = st.text_input("Sisa Prona", "10 gram")
        with s_m4:
            sisa_sayur_gram = st.text_input("Sisa Sayur", "30 gram")
        with s_m5:
            sisa_buah_gram = st.text_input("Sisa Buah", "15 gram")

        catatan_khusus = st.text_area("Catatan / Kendala Operasional", "Semua proses operasional berjalan lancar sesuai standar protokol kesehatan Badan Gizi Nasional.")

        submitted_checklist = st.form_submit_button("💾 Proses & Siapkan Laporan PDF")

        if submitted_checklist:
            st.session_state.data_laporan = {
                "nama_sppg": db_nama,
                "kepala_sppg": db_kepala,
                "pengawas_gizi": pengawas_gizi,
                "pengawas_keu": pengawas_keu,
                "asisten_lapangan": asisten_lapangan,
                "chef": chef,
                "tanggal": str(tanggal),
                "jam_zoom": str(jam_zoom),
                "pm_didik": pm_didik_hari_ini,
                "pm_3b": pm_3b_hari_ini,
                "sertif_slhs": sertif_slhs,
                "sertif_halal": sertif_halal,
                "sertif_bnsp": sertif_bnsp,
                "sumber_air_minum": sumber_air_minum,
                "ph_minum": ph_minum,
                "sumber_air_masak": sumber_air_masak,
                "ph_masak": ph_masak,
                "ruang_termo": ruang_termo,
                "ruang_suhu": ruang_suhu,
                "suhu_ruang": suhu_ruang,
                "ruang_bersih": ruang_bersih,
                "insect_killer": insect_killer,
                "t_karbo": jam_terima_karbo,
                "t_prohe": jam_terima_prohe,
                "t_prona": jam_terima_prona,
                "t_sayur": jam_terima_sayur,
                "t_buah": jam_terima_buah,
                "k_karbo": karbo,
                "k_prohe": prohe,
                "k_prona": prona,
                "k_sayur": sayur,
                "k_buah": buah,
                "hig_sakit": hig_sakit,
                "apd_pakai": apd_pakai,
                "hig_ctps": hig_ctps,
                "menu_rawan": menu_rawan,
                "suhu_matang": suhu_matang,
                "jam_kemas": jam_kemas,
                "suhu_kemas": suhu_kemas,
                "wadah_pangan": wadah_pangan,
                "distrib_tepat": distrib_tepat,
                "uji_organoleptik": uji_organoleptik,
                "sampel_simpan": sampel_simpan,
                "suhu_sampel": suhu_sampel,
                "dapur_bersih": dapur_bersih,
                "limbah_kelola": limbah_kelola,
                "sisa_nasi": sisa_nasi_gram,
                "sisa_prohe": sisa_prohe_gram,
                "sisa_prona": sisa_prona_gram,
                "sisa_sayur": sisa_sayur_gram,
                "sisa_buah": sisa_buah_gram,
                "catatan": catatan_khusus
            }
            st.success("Formulir berhasil diproses! Silakan unduh PDF di bawah.")

    # Tombol Download PDF jika data di session state sudah ada
    if st.session_state.data_laporan is not None:
        st.markdown("---")
        st.subheader("📥 Unduh Laporan Resmi")
        pdf_bytes = generate_pdf(st.session_state.data_laporan)
        
        st.download_button(
            label="Download PDF Checklist Harian SPPG",
            data=pdf_bytes,
            file_name=f"Laporan_SPPG_{st.session_state.data_laporan['nama_sppg']}_{date.today()}.pdf",
            mime="application/pdf"
        )
