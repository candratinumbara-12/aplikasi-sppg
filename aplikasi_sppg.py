# ==========================================
# KELAS GENERATOR PDF LAPORAN KUSTOM RAPI
# ==========================================
class PDFReport(FPDF):
    def header(self):
        # Header kosong agar halaman berikutnya tidak otomatis menimpa
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Halaman {self.page_no()} | Dicetak otomatis via Sistem Cloud SPPG", 0, 0, "C")

def generate_pdf(d):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", "", 9)

    # 1. Judul Utama (Kotak Biru Tua)
    pdf.set_fill_color(0, 43, 91)      # Warna Biru Tua (#002B5B)
    pdf.set_text_color(255, 255, 255)  # Teks Putih
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "CHECKLIST HARIAN - KOORDINASI ZOOM", 1, 1, "C", fill=True)
    
    # Reset warna teks ke hitam
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 9)

    # 2. Tabel Identitas 2 Kolom Atas
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

    # Helper untuk Section Header (Kotak Biru Muda)
    def add_section_header(title):
        pdf.set_fill_color(218, 230, 242)  # Biru Muda lembut
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, title, 1, 1, "L", fill=True)
        pdf.set_font("Arial", "", 9)

    def add_item(kunci, nilai):
        pdf.cell(0, 5, f"  - {kunci}: {nilai}", 0, 1, "L")

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

    # VII. EVALUASI SISA MAKANAN (PLATE WASTE) & CATATAN
    add_section_header("VII. EVALUASI SISA MAKANAN (PLATE WASTE) & CATATAN KHUSUS")
    pdf.cell(0, 5, "  Estimasi Sisa Makanan (Gram):", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Nasi / Karbohidrat: {d.get('sisa_nasi')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Protein Hewani: {d.get('sisa_prohe')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Protein Nabati: {d.get('sisa_prona')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Sayuran: {d.get('sisa_sayur')}", 0, 1, "L")
    pdf.cell(0, 5, f"    - Sisa Buah: {d.get('sisa_buah')}", 0, 1, "L")
    pdf.cell(0, 5, f"  Catatan / Kendala Operasional: {d.get('catatan')}", 0, 1, "L")

    return pdf.output(dest="S").encode("latin1")
