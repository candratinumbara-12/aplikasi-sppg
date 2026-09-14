import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF
from datetime import date, time

st.set_page_config(page_title="Checklist Harian SPPG Nasional", layout="wide")

# ==========================================
# KONFIGURASI KONEKSI SUPABASE
# ==========================================
SUPABASE_URL = "https://mbrsqeldonrydxqyjyiq.supabase.co"
SUPABASE_KEY = "sb_publishable_0RCCm7dOR11Ep7nbLDQfhw_NkK9SlXv"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

# ==========================================
# INISIALISASI SESSION STATE LOGIN
# ==========================================
if "user" not in st.session_state:
    st.session_state.user = None

# ==========================================
# FUNGSI HELPER SUPABASE
# ==========================================
def get_all_sppg_names():
    try:
        response = supabase.table("sppg_accounts").select("nama_sppg").execute()
        if response.data:
            return [row["nama_sppg"] for row in response.data]
    except Exception as e:
        st.error(f"Gagal memuat data dari Supabase: {e}")
    return []

def get_sppg_data(nama_sppg):
    try:
        response = supabase.table("sppg_accounts").select("*").eq("nama_sppg", nama_sppg).execute()
        if response.data:
            row = response.data[0]
            # Mengembalikan tuple dengan format yang sama seperti kode lamamu
            return (
                row.get("id"),
                row.get("nama_sppg"),
                row.get("kepala_sppg"),
                row.get("pengawas_gizi"),
                row.get("pengawas_keu"),
                row.get("asisten_lapangan"),
                row.get("chef"),
                row.get("pm_didik"),
                row.get("pm_3b")
            )
    except Exception as e:
        st.error(f"Gagal mengambil detail SPPG: {e}")
    return None

# ==========================================
# HALAMAN LOGIN / OTENTIKASI
# ==========================================
if not st.session_state.user:
    st.markdown("<h2 style='text-align: center; background-color: #002B5B; color: white; padding: 10px;'>LOGIN AKUN / DAPUR SPPG</h2>", unsafe_allow_html=True)
    st.write("Silakan masukkan nama atau akun dapur SPPG Anda untuk masuk ke sistem.")
    
    with st.form("form_login"):
        input_user = st.text_input("Nama Akun / Dapur SPPG:")
        btn_login = st.form_submit_button("Masuk Aplikasi", type="primary")
        
        if btn_login:
            if input_user.strip():
                st.session_state.user = input_user.strip()
                st.success(f"Berhasil masuk sebagai {st.session_state.user}!")
                st.rerun()
            else:
                st.warning("Nama akun tidak boleh kosong!")
else:
    # ==========================================
    # SIDEBAR: NAVIGASI & AKUN AKTIF
    # ==========================================
    st.sidebar.title("Menu Utama SPPG")
    st.sidebar.markdown(f"👤 Login: **{st.session_state.user}**")
    if st.sidebar.button("Keluar (Logout)"):
        st.session_state.user = None
        st.rerun()

    st.sidebar.markdown("---")
    menu_navigasi = st.sidebar.radio("Pilih Mode:", ["📝 Form Checklist Harian", "➕ Tambah Akun SPPG Baru"])

    # ==========================================
    # HALAMAN 1: TAMBAH AKUN SPPG BARU
    # ==========================================
    if menu_navigasi == "➕ Tambah Akun SPPG Baru":
        st.markdown("<h2 style='text-align: center; background-color: #002B5B; color: white; padding: 10px;'>PENDAFTARAN AKUN / DAPUR SPPG BARU</h2>", unsafe_allow_html=True)
        st.write("Daftarkan dapur atau wilayah SPPG baru Anda agar tersimpan secara permanen di database Cloud Supabase.")

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

            submitted_new_acc = st.form_submit_button("Simpan Akun ke Supabase", type="primary")

            if submitted_new_acc:
                if not new_nama_sppg.strip():
                    st.error("Nama SPPG tidak boleh kosong!")
                else:
                    try:
                        data_insert = {
                            "nama_sppg": new_nama_sppg.strip(),
                            "kepala_sppg": new_kepala_sppg,
                            "pengawas_gizi": new_pengawas_gizi,
                            "pengawas_keu": new_pengawas_keu,
                            "asisten_lapangan": new_asisten_lapangan,
                            "chef": new_chef,
                            "pm_didik": new_pm_didik,
                            "pm_3b": new_pm_3b
                        }
                        supabase.table("sppg_accounts").insert(data_insert).execute()
                        st.success(f"Akun SPPG '{new_nama_sppg}' berhasil disimpan ke Cloud! Silakan pindah ke menu 'Form Checklist Harian'.")
                    except Exception as e:
                        st.error(f"Gagal menyimpan akun (Kemungkinan nama SPPG sudah terdaftar): {e}")

    # ==========================================
    # HALAMAN 2: FORM CHECKLIST HARIAN
    # ==========================================
    else:
        daftar_sppg = get_all_sppg_names()

        if not daftar_sppg:
            st.warning("Belum ada akun SPPG yang terdaftar di database cloud. Silakan pilih menu **'➕ Tambah Akun SPPG Baru'** di sidebar terlebih dahulu.")
        else:
            st.sidebar.markdown("---")
            st.sidebar.subheader("Pilih SPPG Aktif")
            pilih_sppg_aktif = st.sidebar.selectbox("Daftar Dapur SPPG:", daftar_sppg)

            data_db = get_sppg_data(pilih_sppg_aktif)
            
            if data_db:
                db_id, db_nama, db_kepala, db_gizi, db_keu, db_asisten, db_chef, db_pm_didik, db_pm_3b = data_db

                st.markdown(f"<h2 style='text-align: center; background-color: #002B5B; color: white; padding: 10px;'>CHECKLIST HARIAN - {db_nama.upper()}</h2>", unsafe_allow_html=True)
                st.write(f"Menampilkan form checklist harian untuk **{db_nama}**. Data profil di bawah otomatis dimuat dari Cloud Supabase.")

                with st.form("form_sppg_db"):
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

                    submitted_checklist = st.form_submit_button("Proses & Generate Laporan", type="primary")
                    if submitted_checklist:
                        st.success("Formulir berhasil diproses!")
