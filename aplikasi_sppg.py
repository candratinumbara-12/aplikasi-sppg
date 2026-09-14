import streamlit as st
from fpdf import FPDF
from datetime import date, time

# Konfigurasi Halaman
st.set_page_config(page_title="Checklist Harian SPPG - BGN", page_icon="🍲", layout="wide")

# ==========================================
# 1. GENERATOR PDF (PRESISI FORMULIR RESMI)
# ==========================================
class PDFChecklistResmi(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 6, "CHECKLIST HARIAN - KOORDINASI ZOOM", 0, 1, "C")
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 7)
        self.cell(0, 10, f"Halaman {self.page_no()} | Dokumen Resmi SPPG Badan Gizi Nasional", 0, 0, "C")

def generate_pdf(d):
    pdf = PDFChecklistResmi()
    pdf.add_page()
    pdf.set_font("Arial", "", 8)
    
    col_w = 95
    row_h = 5

    # Header Identitas Dapur & Tim
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w, row_h, f"Nama SPPG: {d.get('nama_sppg')}", 1, 0, "L")
    pdf.cell(col_w, row_h, f"Pengawas Keuangan (PLOK): {d.get('plok')}", 1, 1, "L")
    
    pdf.cell(col_w, row_h, f"Kepala SPPG: {d.get('kepala_sppg')}", 1, 0, "L")
    pdf.cell(col_w, row_h, f"Pengawas Gizi (Plog): {d.get('plog')}", 1, 1, "L")
    
    pdf.cell(col_w, row_h, f"Tanggal: {d.get('tanggal')}", 1, 0, "L")
    pdf.cell(col_w, row_h, f"Asisten Lapangan: {d.get('asisten_lapangan')}", 1, 1, "L")
    
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
    pdf.cell(0, 5, f"1. JUMLAH PENERIMA MANFAAT & SERTIFIKASI", 0, 1, "L")
    pdf.cell(0, 4, f"   - PM Peserta Didik: Terdata ({d.get('pm_didik_potensi')}) | Dilayani Hari Ini ({d.get('pm_didik_dilayani')})", 0, 1, "L")
    pdf.cell(0, 4, f"   - PM 3B (Bumil/Balita): Terdata ({d.get('pm_3b_potensi')}) | Dilayani Hari Ini ({d.get('pm_3b_dilayani')})", 0, 1, "L")
    pdf.cell(0, 4, f"   - Total PM Dilayani: {int(d.get('pm_didik_dilayani', 0)) + int(d.get('pm_3b_dilayani', 0))}", 0, 1, "L")
    pdf.cell(0, 4, f"   - Sertifikat SLHS: {d.get('sertif_slhs')} | Sertifikat Halal: {d.get('sertif_halal')} | Sertifikat BNSP Chef: {d.get('sertif_bnsp')}", 0, 1, "L")
    
    pdf.cell(0, 5, f"2. AIR BERSIH", 0, 1, "L")
    pdf.cell(0, 4, f"   - Air Minum: {d.get('air_minum_sumber')} | pH: {d.get('air_minum_ph')} | Tgl/Jam Ambil: {d.get('air_minum_tgljam')}", 0, 1, "L")
    pdf.cell(0, 4, f"   - Air Masak: {d.get('air_masak_sumber')} | pH: {d.get('air_masak_ph')} | Tgl/Jam Ambil: {d.get('air_masak_tgljam')}", 0, 1, "L")
    
    pdf.cell(0, 5, f"3. KONDISI RUANGAN", 0, 1, "L")
    pdf.cell(0, 4, f"   - Termometer Berfungsi: {d.get('ruang_termo')} (Ket: {d.get('ruang_termo_ket')})", 0, 1, "L")
    pdf.cell(0, 4, f"   - Suhu Ruangan Sesuai (25-30°C): {d.get('ruang_suhu')} (Suhu Terkini: {d.get('suhu_terkini')} °C)", 0, 1, "L")
    pdf.cell(0, 4, f"   - Kebersihan Ruangan: {d.get('ruang_bersih')} (Catatan: {d.get('ruang_bersih_ket')})", 0, 1, "L")
    pdf.cell(0, 4, f"   - Insect Killer Berfungsi: {d.get('insect_killer')} (Jumlah Berfungsi: {d.get('insect_killer_unit')} unit)", 0, 1, "L")
    pdf.ln(2)

    # II. PENERIMAAN & PENYIMPANAN BAHAN BAKU
    print_section("II. PENERIMAAN DAN PENYIMPANAN BAHAN BAKU")
    pdf.cell(0, 4, "1. Spesifikasi Bahan Baku (Penerimaan):", 0, 1, "L")
    for kat in ["Karbohidrat", "Protein Hewani", "Protein Nabati", "Buah", "Sayur"]:
        k = kat.lower().replace(" ", "_")
        pdf.cell(0, 4, f"   - {kat}: Jml ({d.get(f'bb_{k}_jml')}) | Kualitas ({d.get(f'bb_{k}_kual')}) | Jam ({d.get(f'bb_{k}_jam')}) | Penerima ({d.get(f'bb_{k}_nama')})", 0, 1, "L")
    
    pdf.cell(0, 4, f"2. Suhu Bahan Baku Beku & Ruang Penyimpanan:", 0, 1, "L")
    pdf.cell(0, 4, f"   - Beku 1: {d.get('beku1_nama')} ({d.get('beku1_suhu')} °C, Jam {d.get('beku1_jam')})", 0, 1, "L")
    pdf.cell(0, 4, f"   - Beku 2: {d.get('beku2_nama')} ({d.get('beku2_suhu')} °C, Jam {d.get('beku2_jam')})", 0, 1, "L")
    pdf.cell(0, 4, f"   - Suhu Chiller: {d.get('suhu_chiller')} °C (Jam {d.get('jam_chiller')}) | Suhu Freezer: {d.get('suhu_freezer')} °C (Jam {d.get('jam_freezer')})", 0, 1, "L")
    
    pdf.cell(0, 4, f"3. Bahan Makanan & Rotasi:", 0, 1, "L")
    pdf.cell(0, 4, f"   - Pencucian Pakai Sumber Air di Atas: {d.get('cuci_air_sesuai')} (Sumber: {d.get('sumber_air_cuci')})", 0, 1, "L")
    pdf.cell(0, 4, f"   - Tahu Disimpan di Chiller: {d.get('tahu_chiller')} (Suhu Chiller: {d.get('tahu_suhu_chiller')} °C)", 0, 1, "L")
    pdf.cell(0, 4, f"   - Rotasi FIFO/FEFO: {d.get('fifo_fefo')} (Ket: {d.get('fifo_ket')})", 0, 1, "L")
    pdf.ln(2)

    # III. PERSIAPAN, PENGOLAHAN DAN PENDINGINAN
    print_section("III. PERSIAPAN, PENGOLAHAN DAN PENDINGINAN")
    pdf.cell(0, 4, f"1. Higiene Tim Persiapan: Sakit ({d.get('p_sakit')}) | APD ({d.get('p_apd')}) | CTPS ({d.get('p_ctps')})", 0, 1, "L")
    pdf.cell(0, 4, f"2. Persiapan: SOP Prohe ({d.get('p_sop_prohe')}) | Bahan Berbau/Lendir ({d.get('p_bahan_rusak')}) | Kendala ({d.get('p_kendala')})", 0, 1, "L")
    
    pdf.cell(0, 4, f"3. Status Menu Rawan Hari Ini:", 0, 1, "L")
    pdf.cell(0, 4, f"   - Ikan/Seafood: {d.get('mr_ikan')} | Ayam Bersantan: {d.get('mr_ayam_santan')}", 0, 1, "L")
    pdf.cell(0, 4, f"   - Ayam Suwir/Olahan Ulang: {d.get('mr_ayam_suwir')} | Telur Dadar: {d.get('mr_telur')} | Susu: {d.get('mr_susu')}", 0, 1, "L")
    
    pdf.cell(0, 4, f"4. Higiene Tim Pengolahan: Sakit ({d.get('o_sakit')}) | APD ({d.get('o_apd')}) | CTPS ({d.get('o_ctps')})", 0, 1, "L")
    pdf.cell(0, 4, f"5. Pengolahan: Matang Sempurna ({d.get('o_matang')}) | Suhu Matang ({d.get('o_suhu_matang')} °C, Jam {d.get('o_jam_matang')}) | SOP ({d.get('o_sop')}) | Kendala ({d.get('o_kendala')})", 0, 1, "L")
    pdf.cell(0, 4, f"6. Pendinginan: Ruang Steril ({d.get('dingin_ruang')}) | Suhu Diukur ({d.get('dingin_suhu')} °C) | Nasi >2 jam Ruang ({d.get('nasi_suhu_ruang')})", 0, 1, "L")
    pdf.ln(2)

    # IV. PEMORSIAN DAN DISTRIBUSI
    print_section("IV. PEMORSIAN DAN DISTRIBUSI")
    pdf.cell(0, 4, f"1. Pemorsian: Gizi & URT Sesuai ({d.get('pors_gizi')}) | Suhu Pemorsian ({d.get('pors_suhu')} °C)", 0, 1, "L")
    pdf.cell(0, 4, f"   - Quality Control / Organoleptik: Oleh ({d.get('qc_oleh')}), Jam ({d.get('qc_jam')}), Hasil ({d.get('qc_hasil')})", 0, 1, "L")
    pdf.cell(0, 4, f"   - Sample Menu Simpan (2 Sampel): {d.get('sampel_2menu')} | Kendala: {d.get('pors_kendala')}", 0, 1, "L")
    pdf.cell(0, 4, f"   - Sisa Makanan Pemorsian: Nasi ({d.get('sisa_nasi')} kg), Prohe ({d.get('sisa_prohe')} kg), Prona ({d.get('sisa_prona')} kg), Sayur ({d.get('sisa_sayur')} kg), Buah ({d.get('sisa_buah')} kg)", 0, 1, "L")
    
    pdf.cell(0, 4, f"2. Alat & Tempat: Alat Terpisah ({d.get('alat_pisah')}) | Meja/Alat Bersih ({d.get('meja_bersih')}) | Bebas Bocor/Genangan ({d.get('sanitasi_fisik')})", 0, 1, "L")
    
    pdf.cell(0, 4, f"3. Rantai Distribusi:", 0, 1, "L")
    pdf.cell(0, 4, f"   - Jam Selesai Masak: {d.get('jam_selesai_masak')} | Jam Berangkat: {d.get('jam_berangkat')} | Jam Sampai: {d.get('jam_sampai')} | Jam Konsumsi: {d.get('jam_konsumsi')}", 0, 1, "L")
    pdf.cell(0, 4, f"   - Label/Segel Ompreng: {d.get('label_segel')} | Suhu Bagikan (Panas: {d.get('suhu_dist_panas')} °C / Dingin: {d.get('suhu_dist_dingin')} °C)", 0, 1, "L")
    pdf.cell(0, 4, f"   - Kendala Distribusi: {d.get('dist_kendala')}", 0, 1, "L")
    pdf.ln(2)

    # V. TEMUAN & KEPUTUSAN
    print_section("V. TEMUAN & KEPUTUSAN FINAL")
    pdf.cell(0, 4, f"Temuan Operasional: {d.get('temuan_khusus')}", 0, 1, "L")
    pdf.set_font("Arial", "B", 9)
    pdf.cell(0, 5, f"KEPUTUSAN FINAL: {d.get('keputusan_final')}", 0, 1, "L")
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 4, "Kontak Darurat: PSC 119 WA +62 8777 7591097 | pheoc.indonesia@kemkes.go.id", 0, 1, "L")

    return pdf.output(dest="S").encode("latin1")


# ==========================================
# 2. INISIALISASI SESSION STATE
# ==========================================
if "db_akun" not in st.session_state:
    st.session_state.db_akun = {
        "sppg01": {"password": "123", "nama_sppg": "SPPG Paseh Cigentur"}
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_id_dapur" not in st.session_state:
    st.session_state.current_id_dapur = ""
if "dapur_aktif" not in st.session_state:
    st.session_state.dapur_aktif = ""

if "setup_selesai" not in st.session_state:
    st.session_state.setup_selesai = False
if "profile_tim" not in st.session_state:
    st.session_state.profile_tim = {
        "kepala_sppg": "Candra Tinumbara",
        "plok": "Cintia Rinawati",
        "plog": "Priska Grace",
        "chef": "Davi Agus Nugraha",
        "asisten_lapangan": "-",
        "pm_didik_potensi": 3000,
        "pm_didik_dilayani": 3000,
        "pm_3b_potensi": 150,
        "pm_3b_dilayani": 150
    }

if "data_laporan" not in st.session_state:
    st.session_state.data_laporan = None


# ==========================================
# 3. LOGIN & REGISTRASI
# ==========================================
if not st.session_state.logged_in:
    st.title("🍲 Portal Sistem Operasional SPPG")
    st.markdown("Badan Gizi Nasional - Checklist Harian Monitoring Zoom (RAPIM 18 Agustus 2026)")
    
    tab_login, tab_reg = st.tabs(["🔑 Login ID Dapur", "📝 Registrasi Dapur Baru"])
    
    with tab_login:
        with st.form("form_login"):
            input_id = st.text_input("ID Dapur (contoh: sppg01)")
            input_pass = st.text_input("Password", type="password")
            if st.form_submit_button("Masuk Sistem"):
                clean_id = input_id.strip().lower()
                if clean_id in st.session_state.db_akun and st.session_state.db_akun[clean_id]["password"] == input_pass:
                    st.session_state.logged_in = True
                    st.session_state.current_id_dapur = clean_id
                    st.session_state.dapur_aktif = st.session_state.db_akun[clean_id]["nama_sppg"]
                    st.success("Login Berhasil!")
                    st.rerun()
                else:
                    st.error("ID Dapur atau Password salah!")

    with tab_reg:
        with st.form("form_registrasi"):
            reg_nama = st.text_input("Nama SPPG (contoh: SPPG Paseh Cigentur)")
            reg_id = st.text_input("ID Dapur Baru (contoh: paseh01)")
            reg_p1 = st.text_input("Password", type="password")
            reg_p2 = st.text_input("Konfirmasi Password", type="password")
            if st.form_submit_button("Daftarkan Dapur"):
                clean_reg_id = reg_id.strip().lower()
                if not reg_nama or not clean_reg_id or not reg_p1:
                    st.error("Semua kolom wajib diisi!")
                elif reg_p1 != reg_p2:
                    st.error("Konfirmasi password tidak cocok!")
                elif clean_reg_id in st.session_state.db_akun:
                    st.error("ID Dapur sudah terdaftar!")
                else:
                    st.session_state.db_akun[clean_reg_id] = {"password": reg_p1, "nama_sppg": reg_nama}
                    st.success("Registrasi berhasil! Silakan Login.")

else:
    # ==========================================
    # 4. SETUP DATA AWAL (WIZARD)
    # ==========================================
    if not st.session_state.setup_selesai:
        st.title(f"🛠️ Setup Data Awal Dapur: {st.session_state.dapur_aktif}")
        with st.form("form_setup_awal"):
            c1, c2 = st.columns(2)
            with c1:
                s_kepala = st.text_input("Kepala SPPG", value=st.session_state.profile_tim["kepala_sppg"])
                s_plok = st.text_input("Pengawas Keuangan (PLOK)", value=st.session_state.profile_tim["plok"])
                s_plog = st.text_input("Pengawas Gizi (Plog)", value=st.session_state.profile_tim["plog"])
                s_chef = st.text_input("Chef", value=st.session_state.profile_tim["chef"])
                s_asisten = st.text_input("Asisten Lapangan", value=st.session_state.profile_tim["asisten_lapangan"])
            with c2:
                s_pm_d_pot = st.number_input("PM Peserta Didik (Potensi / Terdata)", value=st.session_state.profile_tim["pm_didik_potensi"])
                s_pm_d_dil = st.number_input("PM Peserta Didik (Dilayani Hari Ini)", value=st.session_state.profile_tim["pm_didik_dilayani"])
                s_pm_3b_pot = st.number_input("PM 3B (Potensi / Terdata)", value=st.session_state.profile_tim["pm_3b_potensi"])
                s_pm_3b_dil = st.number_input("PM 3B (Dilayani Hari Ini)", value=st.session_state.profile_tim["pm_3b_dilayani"])
            
            if st.form_submit_button("Simpan & Lanjutkan"):
                st.session_state.profile_tim = {
                    "kepala_sppg": s_kepala, "plok": s_plok, "plog": s_plog, "chef": s_chef,
                    "asisten_lapangan": s_asisten, "pm_didik_potensi": s_pm_d_pot,
                    "pm_didik_dilayani": s_pm_d_dil, "pm_3b_potensi": s_pm_3b_pot, "pm_3b_dilayani": s_pm_3b_dil
                }
                st.session_state.setup_selesai = True
                st.rerun()

    else:
        # ==========================================
        # 5. FORMULIR HARIAN PRESISI BGN PDF
        # ==========================================
        st.sidebar.title("⚙️ Panel Kontrol Dapur")
        st.sidebar.info(f"Dapur: **{st.session_state.dapur_aktif}**\nID: `{st.session_state.current_id_dapur}`")
        
        if st.sidebar.button("✏️ Ubah Data Tim / Sasaran PM"):
            st.session_state.setup_selesai = False
            st.rerun()

        with st.sidebar.expander("🔑 Ubah Password"):
            with st.form("form_ubah_pass"):
                p_lama = st.text_input("Password Lama", type="password")
                p_baru = st.text_input("Password Baru", type="password")
                p_konf = st.text_input("Konfirmasi Password", type="password")
                if st.form_submit_button("Perbarui Password"):
                    cid = st.session_state.current_id_dapur
                    if st.session_state.db_akun[cid]["password"] == p_lama and p_baru == p_konf and p_baru != "":
                        st.session_state.db_akun[cid]["password"] = p_baru
                        st.success("Password Berhasil Diubah!")
                    else:
                        st.error("Gagal mengubah password!")

        if st.sidebar.button("Keluar (Logout)"):
            st.session_state.logged_in = False
            st.session_state.setup_selesai = False
            st.rerun()

        st.title(f"CHECKLIST HARIAN KOORDINASI ZOOM - {st.session_state.dapur_aktif}")

        with st.form("form_presisi_pdf"):
            # Header Informasi Tim
            col1, col2 = st.columns(2)
            with col1:
                f_nama_sppg = st.text_input("Nama SPPG", st.session_state.dapur_aktif, disabled=True)
                f_kepala = st.text_input("Kepala SPPG", st.session_state.profile_tim["kepala_sppg"])
                f_tanggal = st.date_input("Tanggal Checklist", date.today())
                f_jam_zoom = st.time_input("Jam Mulai Zoom", time(14, 0))
            with col2:
                f_plok = st.text_input("Pengawas Keuangan (PLOK)", st.session_state.profile_tim["plok"])
                f_plog = st.text_input("Pengawas Gizi (Plog)", st.session_state.profile_tim["plog"])
                f_asisten = st.text_input("Asisten Lapangan", st.session_state.profile_tim["asisten_lapangan"])
                f_chef = st.text_input("Chef", st.session_state.profile_tim["chef"])

            st.markdown("---")
            st.subheader("I. DATA UMUM")
            
            st.markdown("**1. Jumlah Penerima Manfaat & Sertifikasi**")
            pm1, pm2, pm3, pm4 = st.columns(4)
            with pm1: f_pm_d_pot = st.number_input("PM Didik (Terdata)", value=st.session_state.profile_tim["pm_didik_potensi"])
            with pm2: f_pm_d_dil = st.number_input("PM Didik (Dilayani)", value=st.session_state.profile_tim["pm_didik_dilayani"])
            with pm3: f_pm_3b_pot = st.number_input("PM 3B (Terdata)", value=st.session_state.profile_tim["pm_3b_potensi"])
            with pm4: f_pm_3b_dil = st.number_input("PM 3B (Dilayani)", value=st.session_state.profile_tim["pm_3b_dilayani"])
            
            sert1, sert2, sert3 = st.columns(3)
            with sert1: f_slhs = st.selectbox("Sertifikat SLHS", ["Ya", "Tidak"])
            with sert2: f_halal = st.selectbox("Sertifikat Halal", ["Ya", "Tidak"])
            with sert3: f_bnsp = st.selectbox("Sertifikat BNSP Chef", ["Ya", "Tidak"])

            st.markdown("**2. Air Bersih**")
            ab1, ab2 = st.columns(2)
            with ab1:
                f_air_m_src = st.selectbox("Sumber Air Minum", ["RO", "Galon", "PDAM", "Sumur", "Lainnya"])
                f_air_m_ph = st.text_input("pH Air Minum (isi NA bila tidak ada alat)", "7.0")
                f_air_m_tgl = st.text_input("Tgl & Jam Ambil Air Minum", "18/08/2026 05:00")
            with ab2:
                f_air_k_src = st.selectbox("Sumber Air Masak", ["RO", "Galon", "PDAM", "Sumur", "Lainnya"])
                f_air_k_ph = st.text_input("pH Air Masak (isi NA bila tidak ada alat)", "7.0")
                f_air_k_tgl = st.text_input("Tgl & Jam Ambil Air Masak", "18/08/2026 05:00")

            st.markdown("**3. Kondisi Ruangan**")
            r1, r2, r3, r4 = st.columns(4)
            with r1:
                f_ruang_termo = st.selectbox("Termometer Berfungsi", ["Ya", "Tidak"])
                f_ruang_termo_ket = st.text_input("Jika tidak, sebutkan ruangan", "-")
            with r2:
                f_ruang_suhu = st.selectbox("Suhu Sesuai Standar (25-30°C)", ["Ya", "Tidak"])
                f_suhu_terkini = st.text_input("Suhu Ruangan Terkini (°C)", "26")
            with r3:
                f_ruang_bersih = st.selectbox("Ruangan Bersih Sesuai Standar", ["Ya", "Tidak"])
                f_ruang_bersih_ket = st.text_input("Catatan Kebersihan", "Bersih & Sanitasi Lengkap")
            with r4:
                f_insect_killer = st.selectbox("Insect Killer Berfungsi Baik", ["Ya", "Tidak"])
                f_insect_unit = st.number_input("Jumlah Unit Berfungsi", value=2)

            st.markdown("---")
            st.subheader("II. PENERIMAAN DAN PENYIMPANAN BAHAN BAKU")
            st.markdown("**1. Spesifikasi Bahan Baku**")
            
            def row_bb(label_name):
                c1, c2, c3, c4, c5 = st.columns([2,2,2,2,3])
                with c1: st.write(f"**{label_name}**")
                with c2: jml = st.selectbox(f"Jumlah ({label_name})", ["Sesuai", "Kurang", "Lebih"], key=f"j_{label_name}")
                with c3: kual = st.selectbox(f"Kualitas ({label_name})", ["Sesuai", "Baik", "Kurang Baik"], key=f"k_{label_name}")
                with c4: jam = st.text_input(f"Jam Terima ({label_name})", "05:30", key=f"t_{label_name}")
                with c5: nama = st.text_input(f"Nama & TTD Penerima ({label_name})", "Petunjuk Logistik", key=f"n_{label_name}")
                return jml, kual, jam, nama

            bb_karbo = row_bb("Karbohidrat")
            bb_prohe = row_bb("Protein Hewani")
            bb_prona = row_bb("Protein Nabati")
            bb_buah = row_bb("Buah")
            bb_sayur = row_bb("Sayur")

            st.markdown("**2. Suhu Bahan Baku & Ruang Penyimpanan**")
            sb1, sb2 = st.columns(2)
            with sb1:
                f_beku1_nama = st.text_input("Nama Bahan Baku Beku (1)", "Daging Ayam")
                f_beku1_suhu = st.text_input("Suhu Beku 1 (°C)", "-20")
                f_beku1_jam = st.text_input("Jam Ambil Suhu Beku 1", "05:35")
                f_chiller_suhu = st.text_input("Suhu Chiller / Kulkas (°C)", "3")
                f_chiller_jam = st.text_input("Jam Ambil Suhu Chiller", "05:40")
            with sb2:
                f_beku2_nama = st.text_input("Nama Bahan Baku Beku (2)", "Ikan Fillet")
                f_beku2_suhu = st.text_input("Suhu Beku 2 (°C)", "-19")
                f_beku2_jam = st.text_input("Jam Ambil Suhu Beku 2", "05:35")
                f_freezer_suhu = st.text_input("Suhu Freezer Bahan Baku (°C)", "-20")
                f_freezer_jam = st.text_input("Jam Ambil Suhu Freezer", "05:40")

            st.markdown("**3. Bahan Makanan & Rotasi**")
            bm1, bm2, bm3 = st.columns(3)
            with bm1:
                f_cuci_air = st.selectbox("Semua bahan dicuci air sumber di atas?", ["Ya", "Tidak"])
                f_cuci_air_src = st.text_input("Sumber Air Pencucian", "PDAM Terfilter")
            with bm2:
                f_tahu_chiller = st.selectbox("Tahu disimpan dalam chiller?", ["Ya", "Tidak"])
                f_tahu_suhu = st.text_input("Suhu Chiller Tahu (°C)", "4")
            with bm3:
                f_fifo = st.selectbox("Rotasi FIFO/FEFO Diterapkan?", ["Ya", "Tidak"])
                f_fifo_ket = st.text_input("Keterangan Rotasi", "Sesuai Label Tanggal Masuk")

            st.markdown("---")
            st.subheader("III. PERSIAPAN, PENGOLAHAN DAN PENDINGINAN")
            
            p1, p2 = st.columns(2)
            with p1:
                st.markdown("**1. Personal Higiene Tim Persiapan**")
                f_p_sakit = st.selectbox("Ada tim sakit/luka di persiapan?", ["Tidak", "Ya"])
                f_p_apd = st.selectbox("Memakai APD Lengkap (Masker, Hairnet, Gloves, Apron)?", ["Ya", "Tidak"])
                f_p_ctps = st.selectbox("Cuci Tangan Pakai Sabun (CTPS)?", ["Ya", "Tidak"])
            with p2:
                st.markdown("**2. Persiapan**")
                f_p_sop_prohe = st.selectbox("Prohe ditata laksana sesuai SOP?", ["Ya", "Tidak"])
                f_p_bahan_rusak = st.selectbox("Ada bahan berbau / berubah warna / berlendir?", ["Tidak", "Ya"])
                f_p_kendala = st.text_input("Kendala Tahap Persiapan", "Nihil")

            st.markdown("**3. Menu Rawan Hari Ini**")
            mr1, mr2, mr3, mr4, mr5 = st.columns(5)
            with mr1: f_mr_ikan = st.selectbox("Ikan / Seafood", ["Ya", "Tidak"])
            with mr2: f_mr_ayam_santan = st.selectbox("Ayam Bersantan / Kuah Kental", ["Ya", "Tidak"])
            with mr3: f_mr_ayam_suwir = st.selectbox("Ayam Diolah Ulang / Suwir", ["Ya", "Tidak"])
            with mr4: f_mr_telur = st.selectbox("Telur / Telur Dadar", ["Ya", "Tidak"])
            with mr5: f_mr_susu = st.selectbox("Susu / Olahan Susu", ["Ya", "Tidak"])

            o1, o2, o3 = st.columns(3)
            with o1:
                st.markdown("**4. Personal Higiene Tim Pengolahan**")
                f_o_sakit = st.selectbox("Ada tim sakit/luka di pengolahan?", ["Tidak", "Ya"])
                f_o_apd = st.selectbox("Penggunaan APD Lengkap Saat Masak?", ["Ya", "Tidak"])
                f_o_ctps = st.selectbox("CTPS Sebelum Masak & Keluar Masuk?", ["Ya", "Tidak"])
            with o2:
                st.markdown("**5. Proses Pengolahan Makanan**")
                f_o_matang = st.selectbox("Prohe Matang Sempurna (Tidak Merah Muda)?", ["Ya", "Tidak"])
                f_o_suhu_matang = st.text_input("Suhu Matang (°C)", "88")
                f_o_jam_matang = st.text_input("Jam Pengukuran Suhu Matang", "08:30")
                f_o_sop = st.selectbox("Pengolahan Sesuai SOP?", ["Ya", "Tidak"])
                f_o_kendala = st.text_input("Kendala Pengolahan", "Nihil")
            with o3:
                st.markdown("**6. Proses Pendinginan Makanan**")
                f_dingin_ruang = st.selectbox("Ruang Khusus (Steril) Pendinginan?", ["Ya", "Tidak"])
                f_dingin_suhu = st.text_input("Suhu Makanan Diukur (°C)", "65")
                f_nasi_suhu_ruang = st.selectbox("Nasi Berada Suhu Ruang > 2 Jam?", ["Tidak", "Ya"])

            st.markdown("---")
            st.subheader("IV. PEMORSIAN DAN DISTRIBUSI")
            
            por1, por2 = st.columns(2)
            with por1:
                st.markdown("**1. Proses Pemorsian**")
                f_pors_gizi = st.selectbox("Memenuhi Standar Gizi & URT?", ["Ya", "Tidak"])
                f_pors_suhu = st.text_input("Suhu Saat Pemorsian (°C)", "62")
                f_qc_oleh = st.text_input("Uji Organoleptik Oleh", "Plog / Pengawas Gizi")
                f_qc_jam = st.text_input("Jam Uji Organoleptik", "09:15")
                f_qc_hasil = st.text_input("Hasil Organoleptik", "Rasa & Aroma Layak / Sesuai")
                f_sampel_2menu = st.selectbox("Penyimpanan 2 Sampel Menu (Chiller & Freezer)?", ["Ya", "Tidak"])
                f_pors_kendala = st.text_input("Kendala Pemorsian", "Nihil")
            with por2:
                st.markdown("**Detail Sisa Makanan Pemorsian (Plate Waste):**")
                f_sisa_nasi = st.text_input("Sisa Karbohidrat (kg)", "0.5")
                f_sisa_prohe = st.text_input("Sisa Protein Hewani (kg)", "0.2")
                f_sisa_prona = st.text_input("Sisa Protein Nabati (kg)", "0.1")
                f_sisa_sayur = st.text_input("Sisa Sayur (kg)", "0.3")
                f_sisa_buah = st.text_input("Sisa Buah (kg)", "0.0")

                st.markdown("**2. Alat & Tempat**")
                f_alat_pisah = st.selectbox("Alat Terpisah Sesuai Jenis Bahan?", ["Ya", "Tidak"])
                f_meja_bersih = st.selectbox("Meja & Alat Bersih/Kering Sebelum Pakai?", ["Ya", "Tidak"])
                f_sanitasi_fisik = st.selectbox("Lantai/Saluran Air Bebas Bocor & Genangan?", ["Ya", "Tidak"])

            st.markdown("**3. Proses Distribusi**")
            d1, d2, d3, d4 = st.columns(4)
            with d1: f_jam_selesai_masak = st.text_input("Jam Selesai Masak", "09:00")
            with d2: f_jam_berangkat = st.text_input("Jam Berangkat SPPG", "09:30")
            with d3: f_jam_sampai = st.text_input("Jam Sampai Sekolah/Posyandu", "09:50")
            with d4: f_jam_konsumsi = st.text_input("Jam Konsumsi (Maks 4 Jam)", "10:15")

            d5, d6, d7 = st.columns(3)
            with d5: f_label_segel = st.selectbox("Label Ompreng Terpasang Sebagai Segel?", ["Ya", "Tidak"])
            with d6:
                f_suhu_dist_panas = st.text_input("Suhu Makanan Panas Saat Dibagikan (>60°C)", "62")
                f_suhu_dist_dingin = st.text_input("Suhu Makanan Dingin Saat Dibagikan (<5°C)", "NA")
            with d7: f_dist_kendala = st.text_input("Kendala Distribusi", "Lancar, Cuaca Cerah")

            st.markdown("---")
            st.subheader("V. TEMUAN & KEPUTUSAN FINAL")
            f_temuan_khusus = st.text_area("Temuan Operasional (Apabila ada)", "Proses produksi & distribusi berjalan lancar sesuai standar protokol kesehatan Badan Gizi Nasional.")
            f_keputusan_final = st.selectbox("Keputusan Final Rapid Test / Monitoring", [
                "GO - produksi dapat dimulai / dilanjutkan",
                "GO dengan catatan lanjut, perbaikan segera (isi Temuan Khusus)",
                "NO-GO - eskalasi ke Dinkes / BGN sebelum masak / distribusi dilanjutkan"
            ])

            btn_submit = st.form_submit_button("💾 Proses & Siapkan PDF Resmi")

            if btn_submit:
                st.session_state.data_laporan = {
                    "nama_sppg": st.session_state.dapur_aktif, "kepala_sppg": f_kepala, "plok": f_plok, "plog": f_plog,
                    "asisten_lapangan": f_asisten, "chef": f_chef, "tanggal": str(f_tanggal), "jam_zoom": str(f_jam_zoom),
                    "pm_didik_potensi": f_pm_d_pot, "pm_didik_dilayani": f_pm_d_dil, "pm_3b_potensi": f_pm_3b_pot, "pm_3b_dilayani": f_pm_3b_dil,
                    "sertif_slhs": f_slhs, "sertif_halal": f_halal, "sertif_bnsp": f_bnsp,
                    "air_minum_sumber": f_air_m_src, "air_minum_ph": f_air_m_ph, "air_minum_tgljam": f_air_m_tgl,
                    "air_masak_sumber": f_air_k_src, "air_masak_ph": f_air_k_ph, "air_masak_tgljam": f_air_k_tgl,
                    "ruang_termo": f_ruang_termo, "ruang_termo_ket": f_ruang_termo_ket, "ruang_suhu": f_ruang_suhu,
                    "suhu_terkini": f_suhu_terkini, "ruang_bersih": f_ruang_bersih, "ruang_bersih_ket": f_ruang_bersih_ket,
                    "insect_killer": f_insect_killer, "insect_killer_unit": f_insect_unit,
                    "bb_karbohidrat_jml": bb_karbo[0], "bb_karbohidrat_kual": bb_karbo[1], "bb_karbohidrat_jam": bb_karbo[2], "bb_karbohidrat_nama": bb_karbo[3],
                    "bb_protein_hewani_jml": bb_prohe[0], "bb_protein_hewani_kual": bb_prohe[1], "bb_protein_hewani_jam": bb_prohe[2], "bb_protein_hewani_nama": bb_prohe[3],
                    "bb_protein_nabati_jml": bb_prona[0], "bb_protein_nabati_kual": bb_prona[1], "bb_protein_nabati_jam": bb_prona[2], "bb_protein_nabati_nama": bb_prona[3],
                    "bb_buah_jml": bb_buah[0], "bb_buah_kual": bb_buah[1], "bb_buah_jam": bb_buah[2], "bb_buah_nama": bb_buah[3],
                    "bb_sayur_jml": bb_sayur[0], "bb_sayur_kual": bb_sayur[1], "bb_sayur_jam": bb_sayur[2], "bb_sayur_nama": bb_sayur[3],
                    "beku1_nama": f_beku1_nama, "beku1_suhu": f_beku1_suhu, "beku1_jam": f_beku1_jam,
                    "beku2_nama": f_beku2_nama, "beku2_suhu": f_beku2_suhu, "beku2_jam": f_beku2_jam,
                    "suhu_chiller": f_chiller_suhu, "jam_chiller": f_chiller_jam, "suhu_freezer": f_freezer_suhu, "jam_freezer": f_freezer_jam,
                    "cuci_air_sesuai": f_cuci_air, "sumber_air_cuci": f_cuci_air_src, "tahu_chiller": f_tahu_chiller, "tahu_suhu_chiller": f_tahu_suhu,
                    "fifo_fefo": f_fifo, "fifo_ket": f_fifo_ket, "p_sakit": f_p_sakit, "p_apd": f_p_apd, "p_ctps": f_p_ctps,
                    "p_sop_prohe": f_p_sop_prohe, "p_bahan_rusak": f_p_bahan_rusak, "p_kendala": f_p_kendala,
                    "mr_ikan": f_mr_ikan, "mr_ayam_santan": f_mr_ayam_santan, "mr_ayam_suwir": f_mr_ayam_suwir, "mr_telur": f_mr_telur, "mr_susu": f_mr_susu,
                    "o_sakit": f_o_sakit, "o_apd": f_o_apd, "o_ctps": f_o_ctps, "o_matang": f_o_matang, "o_suhu_matang": f_o_suhu_matang,
                    "o_jam_matang": f_o_jam_matang, "o_sop": f_o_sop, "o_kendala": f_o_kendala, "dingin_ruang": f_dingin_ruang,
                    "dingin_suhu": f_dingin_suhu, "nasi_suhu_ruang": f_nasi_suhu_ruang, "pors_gizi": f_pors_gizi, "pors_suhu": f_pors_suhu,
                    "qc_oleh": f_qc_oleh, "qc_jam": f_qc_jam, "qc_hasil": f_qc_hasil, "sampel_2menu": f_sampel_2menu, "pors_kendala": f_pors_kendala,
                    "sisa_nasi": f_sisa_nasi, "sisa_prohe": f_sisa_prohe, "sisa_prona": f_sisa_prona, "sisa_sayur": f_sisa_sayur, "sisa_buah": f_sisa_buah,
                    "alat_pisah": f_alat_pisah, "meja_bersih": f_meja_bersih, "sanitasi_fisik": f_sanitasi_fisik,
                    "jam_selesai_masak": f_jam_selesai_masak, "jam_berangkat": f_jam_berangkat, "jam_sampai": f_jam_sampai, "jam_konsumsi": f_jam_konsumsi,
                    "label_segel": f_label_segel, "suhu_dist_panas": f_suhu_dist_panas, "suhu_dist_dingin": f_suhu_dist_dingin, "dist_kendala": f_dist_kendala,
                    "temuan_khusus": f_temuan_khusus, "keputusan_final": f_keputusan_final
                }
                st.success("Formulir berhasil diproses secara lengkap! Silakan unduh PDF di bawah.")

        if st.session_state.data_laporan is not None:
            st.markdown("---")
            st.subheader("📥 Unduh Laporan Resmi PDF")
            pdf_bytes = generate_pdf(st.session_state.data_laporan)
            st.download_button(
                label="Unduh PDF Checklist SPPG Resmi",
                data=pdf_bytes,
                file_name=f"Checklist_SPPG_{st.session_state.dapur_aktif}_{date.today()}.pdf",
                mime="application/pdf"
            )
