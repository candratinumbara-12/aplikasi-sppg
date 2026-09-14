import streamlit as st
import sqlite3
from fpdf import FPDF
from datetime import date, time

st.set_page_config(page_title="Checklist Harian SPPG Nasional", layout="wide")

# ==========================================
# INISIALISASI DATABASE SQLITE
# ==========================================
def init_db():
    conn = sqlite3.connect('sppg_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sppg_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_sppg TEXT UNIQUE,
            kepala_sppg TEXT,
            pengawas_gizi TEXT,
            pengawas_keu TEXT,
            asisten_lapangan TEXT,
            chef TEXT,
            pm_didik INTEGER,
            pm_3b INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Fungsi helper untuk mengambil data SPPG berdasarkan namanya
def get_sppg_data(nama_sppg):
    conn = sqlite3.connect('sppg_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sppg_accounts WHERE nama_sppg = ?', (nama_sppg,))
    data = cursor.fetchone()
    conn.close()
    return data

# Fungsi helper untuk mengambil semua daftar nama SPPG
def get_all_sppg_names():
    conn = sqlite3.connect('sppg_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nama_sppg FROM sppg_accounts')
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    return data

# ==========================================
# SIDEBAR: NAVIGASI AKUN & PENGATURAN
# ==========================================
st.sidebar.title("Menu Utama SPPG")
menu_navigasi = st.sidebar.radio("Pilih Mode:", ["📝 Form Checklist Harian", "➕ Tambah Akun SPPG Baru"])

# ==========================================
# HALAMAN 1: TAMBAH AKUN SPPG BARU
# ==========================================
if menu_navigasi == "➕ Tambah Akun SPPG Baru":
    st.markdown("<h2 style='text-align: center; background-color: #002B5B; color: white; padding: 10px;'>PENDAFTARAN AKUN / DAPUR SPPG BARU</h2>", unsafe_allow_html=True)
    st.write("Daftarkan dapur atau wilayah SPPG baru Anda agar tersimpan secara permanen di database.")

    with st.form("form_tambah_akun"):
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            new_nama_sppg = st.text_input("Nama SPPG / Dapur:", placeholder="Contoh: SPPG Padalarang Mandiri")
            new_kepala_sppg = st.text_input("Nama Kepala SPPG:")
            new_pengawas_gizi = st.text_input("Nama Pengawas Gizi:")
        with col_t2:
            new_pengawas_keu = st.text_input("Nama Pengawas Keuangan:")
            new_asisten_lapangan = st.text_input("Asisten Lapangan:", value="-")
            new_chef = st.text_input("Chef / Penanggung Jawab Masak:")

        st.markdown("---")
        st.subheader("Jumlah Penerima Manfaat (PM) Tetap")
        col_tp1, col_tp2 = st.columns(2)
        with col_tp1:
            new_pm_didik = st.number_input("Jumlah PM Sekolah (Peserta Didik):", min_value=0, value=3000)
        with col_tp2:
            new_pm_3b = st.number_input("Jumlah PM 3B (Ibu Hamil/Menyusui/Balita):", min_value=0, value=150)

        submitted_new_acc = st.form_submit_button("Simpan Akun ke Database", type="primary")

        if submitted_new_acc:
            if not new_nama_sppg.strip():
                st.error("Nama SPPG tidak boleh kosong!")
            else:
                try:
                    conn = sqlite3.connect('sppg_database.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO sppg_accounts (nama_sppg, kepala_sppg, pengawas_gizi, pengawas_keu, asisten_lapangan, chef, pm_didik, pm_3b)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (new_nama_sppg, new_kepala_sppg, new_pengawas_gizi, new_pengawas_keu, new_asisten_lapangan, new_chef, new_pm_didik, new_pm_3b))
                    conn.commit()
                    conn.close()
                    st.success(f"Akun SPPG '{new_nama_sppg}' berhasil disimpan! Silakan pindah ke menu 'Form Checklist Harian' untuk mulai menggunakannya.")
                except sqlite3.IntegrityError:
                    st.error(f"Nama SPPG '{new_nama_sppg}' sudah terdaftar di database. Gunakan nama lain.")

# ==========================================
# HALAMAN 2: FORM CHECKLIST HARIAN
# ==========================================
else:
    daftar_sppg = get_all_sppg_names()

    if not daftar_sppg:
        st.warning("Belum ada akun SPPG yang terdaftar di database. Silakan pilih menu **'➕ Tambah Akun SPPG Baru'** di sidebar terlebih dahulu.")
    else:
        # Pilih akun SPPG yang aktif di sidebar atau bagian atas
        st.sidebar.markdown("---")
        st.sidebar.subheader("Pilih SPPG Aktif")
        pilih_sppg_aktif = st.sidebar.selectbox("Daftar Dapur SPPG:", daftar_sppg)

        # Ambil data dari database berdasarkan SPPG yang dipilih
        data_db = get_sppg_data(pilih_sppg_aktif)
        
        if data_db:
            db_id, db_nama, db_kepala, db_gizi, db_keu, db_asisten, db_chef, db_pm_didik, db_pm_3b = data_db

            st.markdown(f"<h2 style='text-align: center; background-color: #002B5B; color: white; padding: 10px;'>CHECKLIST HARIAN - {db_nama.upper()}</h2>", unsafe_allow_html=True)
            st.write(f"Menampilkan form checklist harian untuk **{db_nama}**. Data profil di bawah otomatis dimuat dari database.")

            with st.form("form_sppg_db"):
                # HEADER INFORMASI DARI DATABASE
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Nama SPPG:** {db_nama}\n\n**Kepala SPPG:** {db_kepala}\n\n**Pengawas Gizi:** {db_gizi}")
                    tanggal = st.date_input("Tanggal Checklist:", date.today())
                with col2:
                    st.info(f"**Pengawas Keuangan:** {db_keu}\n\n**Asisten Lapangan:** {db_asisten}\n\n**Chef:** {db_chef}")
                    jam_zoom = st.time_input("Jam Mulai Zoom:", value=time(14, 0))

                st.markdown("---")

                # I. DATA UMUM
                st.subheader("I. DATA UMUM")
                st.markdown("**1. Jumlah Penerima Manfaat (PM) & Sertifikasi**")
                c1, c2 = st.columns(2)
                with c1:
                    pm_didik_hari_ini = st.number_input("PM Peserta Didik (Dilayani Hari Ini)", min_value=0, value=db_pm_didik)
                    pm_3b_hari_ini = st.number_input("PM Ibu Hamil/Menyusui/Balita (3B) (Dilayani Hari Ini)", min_value=0, value=db_pm_3b)
                with c2:
                    sertif_slhs = st.radio("Sertifikat SLHS:", ["Ya", "Tidak"], index=0, horizontal=True)
                    sertif_halal = st.radio("Sertifikat Halal:", ["Ya", "Tidak"], index=0, horizontal=True)
                    sertif_bnsp = st.radio("Sertifikat BNSP Chef:", ["Ya", "Tidak"], index=0, horizontal=True)

                st.markdown("**2. Air Bersih**")
                c4, c5 = st.columns(2)
                with c4:
                    sumber_air_minum = st.selectbox("Sumber Air Minum:", ["PDAM", "RO", "Galon", "Sumur", "Lainnya"], index=0)
                    sumber_air_masak = st.selectbox("Sumber Air Masak:", ["PDAM", "RO", "Galon", "Sumur", "Lainnya"], index=0)
                with c5:
                    ph_minum = st.text_input("pH Air Minum:", value="7.0 (Sesuai Standar)")
                    ph_masak = st.text_input("pH Air Masak:", value="7.0 (Sesuai Standar)")

                st.markdown("**3. Kondisi Ruangan**")
                ruang_termo = st.radio("Semua ruangan memiliki termometer?", ["Ya", "Tidak"], index=0, horizontal=True)
                ruang_suhu = st.radio("Suhu ruang sesuai standar (25-30 derajat)?", ["Ya", "Tidak"], index=0, horizontal=True)
                suhu_ruang_terkini = st.text_input("Suhu ruangan terkini (derajat C):", value="26")
                ruang_bersih = st.radio("Ruangan dalam keadaan bersih?", ["Ya", "Tidak"], index=0, horizontal=True)
                insect_killer = st.radio("Terdapat insect killer berfungsi baik?", ["Ya", "Tidak"], index=0, horizontal=True)

                st.markdown("---")

                # II. PENERIMAAN DAN PENYIMPANAN BAHAN BAKU
                st.subheader("II. PENERIMAAN DAN PENYIMPANAN BAHAN BAKU")
                st.markdown("**1. Waktu Kedatangan Bahan Baku**")
                w1, w2, w3 = st.columns(3)
                with w1:
                    jam_terima_karbo = st.time_input("Jam Datang Karbohidrat:", value=time(5, 30))
                    jam_terima_prohe = st.time_input("Jam Datang Protein Hewani:", value=time(5, 30))
                with w2:
                    jam_terima_prona = st.time_input("Jam Datang Protein Nabati:", value=time(5, 30))
                    jam_terima_sayur = st.time_input("Jam Datang Sayuran:", value=time(5, 30))
                with w3:
                    jam_terima_buah = st.time_input("Jam Datang Buah:", value=time(5, 30))
                
                st.markdown("**2. Spesifikasi Bahan Baku (Cek Kesesuaian)**")
                c6, c7, c8 = st.columns(3)
                with c6:
                    karbo = st.selectbox("Karbohidrat", ["Sesuai", "Kurang", "Lebih"], index=0)
                    prohe = st.selectbox("Protein Hewani", ["Sesuai", "Kurang", "Lebih"], index=0)
                with c7:
                    prona = st.selectbox("Protein Nabati", ["Sesuai", "Kurang", "Lebih"], index=0)
                    buah = st.selectbox("Buah", ["Sesuai", "Kurang", "Lebih"], index=0)
                with c8:
                    sayur = st.selectbox("Sayur", ["Sesuai", "Kurang", "Lebih"], index=0)
                    
                st.markdown("**3. Suhu Bahan Baku & Ruang Penyimpanan**")
                suhu_beku_1 = st.text_input("Suhu bahan baku beku (1) (C & Nama Bahan):", value="-18 C (Ayam/Daging)")
                suhu_beku_2 = st.text_input("Suhu bahan baku beku (2) (C & Nama Bahan):", value="-18 C (Ikan)")
                suhu_chiller = st.text_input("Suhu chiller / kulkas bahan baku (C):", value="4 C")
                suhu_freezer = st.text_input("Suhu freezer bahan baku (C):", value="-18 C")

                st.markdown("**4. Bahan Makanan**")
                bahan_dicuci = st.radio("Semua bahan dicuci air mengalir?", ["Ya", "Tidak"], index=0, horizontal=True)
                tahu_chiller = st.radio("Tahu disimpan di chiller?", ["Ya", "Tidak"], index=0, horizontal=True)
                rotasi_fifo = st.radio("Pemakaian rotasi FIFO / FEFO?", ["Ya", "Tidak"], index=0, horizontal=True)

                st.markdown("---")

                # III. PERSIAPAN, PENGOLAHAN DAN PENDINGINAN
                st.subheader("III. PERSIAPAN, PENGOLAHAN DAN PENDINGINAN")
                st.markdown("**1. Personal Higiene & Persiapan**")
                hig_sakit = st.radio("Ada tim yang demam, batuk, diare, luka?", ["Ya", "Tidak"], index=1, horizontal=True)
                opsi_apd = ["Apron / Celemek", "Hairnet / Penutup Kepala", "Masker", "Sarung Tangan / Gloves", "Sepatu Tertutup / Boot"]
                apd_dipakai = st.multiselect("Pilih APD yang digunakan tim:", options=opsi_apd, default=opsi_apd)
                hig_ctps = st.radio("Semua cuci tangan pakai sabun (CTPS)?", ["Ya", "Tidak"], index=0, horizontal=True)
                persiapan_sop = st.radio("Protein hewani ditatalaksana sesuai SOP?", ["Ya", "Tidak"], index=0, horizontal=True)
                persiapan_bau = st.radio("Ada bahan baku berbau tidak sedap/berubah warna?", ["Ya", "Tidak"], index=1, horizontal=True)

                st.markdown("**2. Menu Rawan Hari Ini**")
                rawan_ikan = st.checkbox("Ikan")
                rawan_ayam_santan = st.checkbox("Ayam bersantan")
                rawan_ayam_suwir = st.checkbox("Ayam olahan (suwir tambahan bumbu)")
                rawan_telur = st.checkbox("Telur dadar")
                rawan_susu = st.checkbox("Susu")

                st.markdown("**3. Proses Pengolahan & Pendinginan**")
                olah_matang = st.radio("Daging/Ayam/Ikan/Telur dicek matang sempurna?", ["Ya", "Tidak"], index=0, horizontal=True)
                suhu_matang = st.text_input("Suhu makanan matang tertentu (C & Jam):", value="75 C")
                olah_sop = st.radio("Tata laksana pengolahan sesuai SOP?", ["Ya", "Tidak"], index=0, horizontal=True)
                dingin_area = st.radio("Ada area/ruang khusus untuk pendinginan?", ["Ya", "Tidak"], index=0, horizontal=True)
                nasi_suhu_ruang = st.radio("Nasi berada di suhu ruang selama 2 jam?", ["Ya", "Tidak"], index=0, horizontal=True)
                dingin_suhu = st.radio("Suhu makanan sudah diukur (Panas 60C, Dingin -5C)?", ["Ya", "Tidak"], index=0, horizontal=True)

                st.markdown("---")

                # IV. PEMORSIAN DAN DISTRIBUSI
                st.subheader("IV. PEMORSIAN DAN DISTRIBUSI")
                st.markdown("**1. Rincian Sisa Makanan (Gramasi)**")
                sisa_makanan = st.text_area(
                    "Tuliskan nama makanan sisa dan beratnya (Gram):", 
                    value="1. Nasi: ... gram\n2. Lauk Hewani (...): ... gram\n3. Lauk Nabati (...): ... gram\n4. Sayur (...): ... gram\n5. Buah (...): ... gram",
                    height=140
                )
                
                st.markdown("**2. Alat, Tempat & Proses Distribusi**")
                meja_bersih = st.radio("Apakah meja pengolahan bersih?", ["Ya", "Tidak"], index=0, horizontal=True)
                saluran_bocor = st.radio("Apakah saluran air lantai tidak ada yang bocor?", ["Ya", "Tidak"], index=0, horizontal=True)
                sample_makanan = st.radio("Apakah sudah menyimpan sample makanan?", ["Ya", "Tidak"], index=0, horizontal=True)
                
                porsi_standar = st.radio("Memenuhi standar gizi & URT?", ["Ya", "Tidak"], index=0, horizontal=True)
                porsi_qc = st.radio("Quality control organoleptik dilakukan?", ["Ya", "Tidak"], index=0, horizontal=True)
                alat_pisah = st.radio("Peralatan pengolahan dipisah (talenan/pisau)?", ["Ya", "Tidak"], index=0, horizontal=True)
                
                col_jam1, col_jam2 = st.columns(2)
                with col_jam1:
                    jam_selesai_masak = st.time_input("Jam selesai masak:", value=time(10, 0))
                    jam_distribusi = st.time_input("Jam pendistribusian:", value=time(10, 30))
                with col_jam2:
                    jam_sampai = st.time_input("Jam sampai lokasi:", value=time(11, 30))
                    suhu_dibagikan = st.text_input("Suhu makanan saat mulai dibagikan (C):", value="60 C")
                    
                segel_terpasang = st.radio("Label ompreng/segel terpasang?", ["Ya", "Tidak"], index=0, horizontal=True)

                st.markdown("---")

                # V. TEMUAN & KEPUTUSAN
                st.subheader("V. TEMUAN & KEPUTUSAN")
                temuan = st.text_area("Temuan (Apabila ada):", value="-")
                keputusan = st.radio(
                    "Keputusan Final:",
                    [
                        "GO - produksi dapat dimulai / dilanjutkan",
                        "GO dengan catatan - lanjut, perbaikan segera",
                        "NO-GO - eskalasi ke Dinkes / Badan Gizi Nasional sebelum masak dilanjutkan"
                    ],
                    index=0
                )

                submitted_checklist = st.form_submit_button("Simpan Checklist & Unduh PDF", type="primary")

            # GENERATE PDF
            def bersihkan_teks(teks):
                if isinstance(teks, str):
                    return teks.replace('—', '-').replace('–', '-').replace('“', '"').replace('”', '"').replace("’", "'").replace('°', ' derajat ')
                return str(teks)

            if submitted_checklist:
                pdf = FPDF()
                pdf.add_page()
                
                pdf.set_font("Arial", 'B', 14)
                pdf.set_fill_color(0, 43, 91)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(0, 10, f"CHECKLIST HARIAN - {db_nama.upper()}", ln=True, align='C', fill=True)
                pdf.ln(5)
                
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", '', 9)
                pdf.cell(95, 7, bersihkan_teks(f"Nama SPPG: {db_nama}"), border=1)
                pdf.cell(95, 7, bersihkan_teks(f"Pengawas Keu: {db_keu}"), border=1, ln=True)
                pdf.cell(95, 7, bersihkan_teks(f"Kepala SPPG: {db_kepala}"), border=1)
                pdf.cell(95, 7, bersihkan_teks(f"Pengawas Gizi: {db_gizi}"), border=1, ln=True)
                pdf.cell(95, 7, bersihkan_teks(f"Tanggal: {tanggal}"), border=1)
                pdf.cell(95, 7, bersihkan_teks(f"Asisten Lapangan: {db_asisten}"), border=1, ln=True)
                pdf.cell(95, 7, bersihkan_teks(f"Jam Mulai Zoom: {jam_zoom.strftime('%H:%M')}"), border=1)
                pdf.cell(95, 7, bersihkan_teks(f"Chef: {db_chef}"), border=1, ln=True)
                pdf.ln(3)
                
                def print_section(title, data_list):
                    pdf.set_font("Arial", 'B', 10)
                    pdf.set_fill_color(220, 230, 241)
                    pdf.cell(0, 7, bersihkan_teks(title), ln=True, fill=True)
                    pdf.set_font("Arial", '', 9)
                    for item in data_list:
                        pdf.multi_cell(0, 6, bersihkan_teks(item), border='B')
                    pdf.ln(2)

                print_section("I. DATA UMUM", [
                    f"Jumlah Penerima Manfaat (PM):\n  - Peserta Didik: {pm_didik_hari_ini} dilayani (Database Setup: {db_pm_didik})\n  - Ibu Hamil/Menyusui/Balita (3B): {pm_3b_hari_ini} dilayani (Database Setup: {db_pm_3b})",
                    f"Sertifikasi:\n  - SLHS: {sertif_slhs}\n  - Halal: {sertif_halal}\n  - BNSP Chef: {sertif_bnsp}",
                    f"Sumber Air Bersih:\n  - Air Minum: {sumber_air_minum} (pH: {ph_minum})\n  - Air Masak: {sumber_air_masak} (pH: {ph_masak})",
                    f"Kondisi Ruangan:\n  - Termometer tersedia: {ruang_termo}\n  - Suhu sesuai standar: {ruang_suhu} ({suhu_ruang_terkini})\n  - Ruangan bersih: {ruang_bersih}\n  - Insect killer berfungsi: {insect_killer}"
                ])

                print_section("II. PENERIMAAN BAHAN BAKU", [
                    f"Waktu Penerimaan Bahan Baku:\n  - Karbohidrat: {jam_terima_karbo.strftime('%H:%M')}\n  - Protein Hewani: {jam_terima_prohe.strftime('%H:%M')}\n  - Protein Nabati: {jam_terima_prona.strftime('%H:%M')}\n  - Sayuran: {jam_terima_sayur.strftime('%H:%M')}\n  - Buah: {jam_terima_buah.strftime('%H:%M')}",
                    f"Kesesuaian Stok:\n  - Karbohidrat: {karbo}\n  - Protein Hewani: {prohe}\n  - Protein Nabati: {prona}\n  - Sayur: {sayur}\n  - Buah: {buah}",
                    f"Suhu Ruang & Diterima:\n  - Beku 1: {suhu_beku_1}\n  - Beku 2: {suhu_beku_2}\n  - Chiller: {suhu_chiller}\n  - Freezer: {suhu_freezer}",
                    f"Higiene Bahan:\n  - Dicuci air mengalir: {bahan_dicuci}\n  - Tahu di Chiller: {tahu_chiller}\n  - Rotasi FIFO/FEFO: {rotasi_fifo}"
                ])

                menu_rawan_list = []
                if rawan_ikan: menu_rawan_list.append("Ikan")
                if rawan_ayam_santan: menu_rawan_list.append("Ayam bersantan")
                if rawan_ayam_suwir: menu_rawan_list.append("Ayam olahan (suwir tambahan bumbu)")
                if rawan_telur: menu_rawan_list.append("Telur dadar")
                if rawan_susu: menu_rawan_list.append("Susu")
                teks_rawan = ", ".join(menu_rawan_list) if menu_rawan_list else "Tidak ada"

                teks_apd = ", ".join(apd_dipakai) if apd_dipakai else "Tidak menggunakan APD"
                
                print_section("III. PERSIAPAN, PENGOLAHAN & PENDINGINAN", [
                    f"Higiene Tim:\n  - Sakit/Luka: {hig_sakit}\n  - APD Digunakan: {teks_apd}\n  - Cuci Tangan (CTPS): {hig_ctps}",
                    f"Cek Persiapan:\n  - SOP Protein: {persiapan_sop}\n  - Bahan Berbau/Berubah Warna: {persiapan_bau}",
                    f"Menu Rawan Hari Ini:\n  - {teks_rawan}",
                    f"Pengolahan:\n  - Daging/ayam matang sempurna: {olah_matang}\n  - Suhu Matang: {suhu_matang}\n  - Sesuai SOP: {olah_sop}",
                    f"Pendinginan:\n  - Nasi di suhu ruang 2 jam: {nasi_suhu_ruang}\n  - Area khusus: {dingin_area}\n  - Suhu Terukur: {dingin_suhu}"
                ])

                sisa_makanan_rapi = sisa_makanan.replace('\n', '\n    ')
                
                print_section("IV. PEMORSIAN & DISTRIBUSI", [
                    f"Data Sisa Makanan (Gramasi):\n    {sisa_makanan_rapi}",
                    f"Pemorsian, QC & Sample:\n  - Simpan Sample Makanan: {sample_makanan}\n  - Standar gizi & URT: {porsi_standar}\n  - QC Organoleptik: {porsi_qc}",
                    f"Alat, Tempat & Distribusi:\n  - Meja pengolahan bersih: {meja_bersih}\n  - Saluran air lantai tidak bocor: {saluran_bocor}\n  - Alat Pisah (Talenan/Pisau): {alat_pisah}\n  - Jam Selesai Masak: {jam_selesai_masak.strftime('%H:%M')}\n  - Jam Distribusi: {jam_distribusi.strftime('%H:%M')}\n  - Jam Sampai Lokasi: {jam_sampai.strftime('%H:%M')}\n  - Label/Segel Terpasang: {segel_terpasang}\n  - Suhu Saat Dibagikan: {suhu_dibagikan}"
                ])

                print_section("V. TEMUAN & KEPUTUSAN", [
                    f"Catatan Temuan:\n  - {temuan}",
                    f"Keputusan Final:\n  - {keputusan}"
                ])

                nama_file = f"{tanggal} - {db_nama}.pdf"
                pdf.output(nama_file)
                
                with open(nama_file, "rb") as file:
                    st.download_button(
                        label="⬇️ Unduh File PDF",
                        data=file,
                        file_name=nama_file,
                        mime="application/pdf"
                    )
                st.success("Form checklist berhasil diproses! Klik tombol unduh di atas.")