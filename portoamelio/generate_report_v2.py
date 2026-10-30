import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that enables two-pass page numbering 'Halaman X dari Y'"""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            # Skip header and footer on cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header
        self.drawString(4 * cm, 28.2 * cm, "Laporan Penugasan Web Portofolio Ameliorer 2026")
        self.drawRightString(18 * cm, 28.2 * cm, "Teknik Informatika UNESA")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(4 * cm, 28.0 * cm, 18 * cm, 28.0 * cm)

        # Footer
        self.line(4 * cm, 2.3 * cm, 18 * cm, 2.3 * cm)
        self.drawString(4 * cm, 1.8 * cm, "Muhammad Guntur Cahyadi Putra - 26051204087")
        page_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(18 * cm, 1.8 * cm, page_text)
        self.restoreState()

def generate_pdf(output_filename):
    # Setup document with standard Indonesian academic margins (4-4-3-3 cm)
    # A4 width = 21.0 cm, height = 29.7 cm
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=4.0 * cm,
        rightMargin=3.0 * cm,
        topMargin=2.8 * cm,
        bottomMargin=2.6 * cm
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#334155'),
        spaceAfter=18
    )

    style_cover_identity = ParagraphStyle(
        'CoverIdentity',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e293b')
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=8,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b'),
        firstLineIndent=0.6 * cm,
        spaceAfter=4
    )

    style_body_no_indent = ParagraphStyle(
        'Body_NoIndent',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=3
    )

    style_list = ParagraphStyle(
        'List_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=0.5 * cm,
        spaceAfter=2.5
    )

    style_code_box = ParagraphStyle(
        'CodeBox',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0f172a')
    )

    story = []

    # ==========================================
    # HALAMAN 1: COVER
    # ==========================================
    story.append(Spacer(1, 1.0 * cm))
    story.append(Paragraph("LAPORAN PENUGASAN INDIVIDU AMELIORER 2026", style_cover_title))
    story.append(Paragraph("PERANCANGAN DAN PENGEMBANGAN WEBSITE PORTOFOLIO PRIBADI SEBAGAI REKAYASA DIGITAL MAHASISWA TEKNIK INFORMATIKA", style_cover_sub))
    story.append(Spacer(1, 1.0 * cm))

    # Decorative Academic Box
    cover_box_data = [[
        Paragraph(
            "<font size=9.5 color='#15803d'><b>PROGRAM STUDI S1 TEKNIK INFORMATIKA</b></font><br/>"
            "<font size=8 color='#475569'>JURUSAN TEKNIK INFORMATIKA - FAKULTAS TEKNIK<br/>UNIVERSITAS NEGERI SURABAYA</font>",
            ParagraphStyle('BoxText', alignment=TA_CENTER, leading=12)
        )
    ]]
    cover_box = Table(cover_box_data, colWidths=[14 * cm])
    cover_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#86efac')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cover_box)
    story.append(Spacer(1, 2.0 * cm))

    # Identitas Penyusun
    story.append(Paragraph("<b>Disusun Oleh:</b>", style_cover_identity))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("<font size=10.5><b>MUHAMMAD GUNTUR CAHYADI PUTRA</b></font>", style_cover_identity))
    story.append(Paragraph("<b>NIM. 26051204087</b>", style_cover_identity))
    story.append(Paragraph("Kelas: F (Pemrograman Dasar)", style_cover_identity))
    
    story.append(Spacer(1, 2.8 * cm))

    # Bagian Bawah Cover
    story.append(Paragraph("<b>UNIVERSITAS NEGERI SURABAYA</b>", style_cover_identity))
    story.append(Paragraph("<b>SURABAYA</b>", style_cover_identity))
    story.append(Paragraph("<b>2026</b>", style_cover_identity))
    story.append(PageBreak())

    # ==========================================
    # HALAMAN 2: BAB I PENDAHULUAN
    # ==========================================
    story.append(Paragraph("BAB I<br/>PENDAHULUAN", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    story.append(Paragraph("A. Latar Belakang", style_h2))
    story.append(Paragraph(
        "Di era transformasi digital dan pesatnya perkembangan industri teknologi informasi, eksistensi digital seorang calon insinyur informatika memegang peranan krusial. Portofolio bukan sekadar daftar riwayat hidup digital, melainkan sebuah artefak rekayasa perangkat lunak yang merefleksikan kompetensi teknis, pemahaman arsitektur sistem, serta kepekaan estetika dan ergonomi antarmuka pengguna (UI/UX).",
        style_body
    ))
    story.append(Paragraph(
        "Sebagai mahasiswa baru Program Studi S1 Teknik Informatika, Fakultas Teknik, Universitas Negeri Surabaya (UNESA), penugasan Web Portofolio pada rangkaian kegiatan Ameliorer Day 5 menjadi momentum strategis untuk mengintegrasikan pemahaman dasar pemrograman, penguasaan antarmuka modern, dan tata kelola repositori berbasis Git. Proyek ini dirancang secara mandiri dengan menerapkan standar rekayasa perangkat lunak modern, prinsip anti-slop frontend, aksesibilitas web (WCAG AA), dan adaptabilitas lintas perangkat (mobile-first design).",
        style_body
    ))

    story.append(Paragraph("B. Rumusan Masalah", style_h2))
    story.append(Paragraph("Berdasarkan latar belakang tersebut, rumusan masalah dalam perancangan ini adalah:", style_body_no_indent))
    story.append(Paragraph("1. Bagaimana merancang antarmuka web portofolio yang bersih, informatif, dan responsif tanpa redundansi visual?", style_list))
    story.append(Paragraph("2. Bagaimana mengimplementasikan fitur penyaringan proyek interaktif dan dual-theme (dark/light mode) menggunakan JavaScript modern?", style_list))
    story.append(Paragraph("3. Bagaimana menyajikan rekam jejak akademik, keahlian teknis, dan proyek unggulan secara terstruktur dan terukur?", style_list))

    story.append(Paragraph("C. Tujuan Penugasan", style_h2))
    story.append(Paragraph("Tujuan utama dari pembuatan Web Portofolio ini adalah:", style_body_no_indent))
    story.append(Paragraph("1. Memenuhi kewajiban penugasan resmi Ameliorer Day 5 Jurusan Teknik Informatika UNESA.", style_list))
    story.append(Paragraph("2. Membangun representasi digital profesional yang memuat profil, keterampilan pemrograman (C/C++, JavaScript, PHP, Next.js), dan karya proyek nyata.", style_list))
    story.append(Paragraph("3. Menerapkan disiplin version control berbasis Git dan mempublikasikan kode sumber secara terbuka pada GitHub.", style_list))

    story.append(Paragraph("D. Manfaat", style_h2))
    story.append(Paragraph(
        "Manfaat yang diharapkan dari pengembangan ini adalah tersedianya wadah representasi digital yang dapat terus dikembangkan sepanjang masa studi di UNESA, memudahkan verifikasi rekam jejak akademik oleh dosen dan rekan mahasiswa, serta menjadi fondasi portofolio profesional untuk peluang magang maupun kompetisi teknologi.",
        style_body
    ))

    story.append(PageBreak())

    # ==========================================
    # HALAMAN 3: BAB II PERANCANGAN SISTEM
    # ==========================================
    story.append(Paragraph("BAB II<br/>PERANCANGAN DAN ARSITEKTUR SISTEM", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    story.append(Paragraph("A. Analisis Kebutuhan Sistem", style_h2))
    story.append(Paragraph(
        "Perancangan web portofolio mengacu pada dua aspek kebutuhan sistem, yaitu fungsional dan non-fungsional:",
        style_body
    ))
    story.append(Paragraph("<b>1. Kebutuhan Fungsional (Functional Requirements):</b>", style_list))
    story.append(Paragraph("• Sistem mampu menyajikan profil personal, riwayat pendidikan, dan fokus bidang akademik.", style_list))
    story.append(Paragraph("• Sistem menyediakan katalog proyek yang dapat difilter secara dinamis berdasarkan kategori (Web App, Sistem & DevOps, Algoritma C++).", style_list))
    story.append(Paragraph("• Sistem mendukung mekanisme peralihan tema (Dark Mode dan Light Mode) dengan retensi status pada penyimpanan lokal browser (localStorage).", style_list))
    story.append(Paragraph("• Sistem menyediakan formulir kontak interaktif dengan validasi input dan visual feedback berupa notifikasi toast.", style_list))

    story.append(Paragraph("<b>2. Kebutuhan Non-Fungsional (Non-Functional Requirements):</b>", style_list))
    story.append(Paragraph("• <i>Responsiveness:</i> Tampilan stabil pada berbagai dimensi layar (Mobile 320px-480px, Tablet 768px, Desktop 1024px+).", style_list))
    story.append(Paragraph("• <i>Performance:</i> Waktu muat cepat dengan memanfaatkan distribusi CSS utilitas dan skrip ringan tanpa dependensi pustaka berat.", style_list))
    story.append(Paragraph("• <i>Accessibility (a11y):</i> Rasio kontras teks memenuhi standar WCAG AA (minimal 4.5:1) untuk menjamin kenyamanan keterbacaan.", style_list))

    story.append(Paragraph("B. Pemilihan Teknologi (Tech Stack)", style_h2))
    story.append(Paragraph(
        "Untuk menghasilkan website yang cepat, mudah dipelihara, dan handal, dipilih susunan teknologi berikut:",
        style_body
    ))

    tech_table_data = [
        [Paragraph("<b>Komponen</b>", style_cover_identity), Paragraph("<b>Teknologi</b>", style_cover_identity), Paragraph("<b>Alasan Pemilihan</b>", style_cover_identity)],
        [Paragraph("Struktur", style_body_no_indent), Paragraph("HTML5 Semantik", style_body_no_indent), Paragraph("Menjamin keterbacaan mesin pencari (SEO) dan struktur hirarki dokumen.", style_body_no_indent)],
        [Paragraph("Styling", style_body_no_indent), Paragraph("Tailwind CSS", style_body_no_indent), Paragraph("Framework utility-first modern yang memungkinkan penyesuaian desain presisi.", style_body_no_indent)],
        [Paragraph("Logika", style_body_no_indent), Paragraph("Vanilla JS (ES6+)", style_body_no_indent), Paragraph("Eksekusi native yang sangat cepat tanpa overhead runtime framework besar.", style_body_no_indent)],
        [Paragraph("Ikonografi", style_body_no_indent), Paragraph("Lucide Icons", style_body_no_indent), Paragraph("Set ikon open-source modern, bersih, dengan konsistensi ketebalan garis.", style_body_no_indent)],
        [Paragraph("Tipografi", style_body_no_indent), Paragraph("Plus Jakarta Sans & JetBrains Mono", style_body_no_indent), Paragraph("Kombinasi font sans-serif humanis dan monospace teknis yang ergonomis.", style_body_no_indent)]
    ]
    tech_table = Table(tech_table_data, colWidths=[2.6 * cm, 3.6 * cm, 7.8 * cm])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tech_table)

    story.append(Paragraph("C. Struktur Halaman dan Navigasi", style_h2))
    story.append(Paragraph(
        "Website portofolio ini disusun secara modular dalam 6 bagian terintegrasi: <b>(1) Header & Sticky Navigation</b>, <b>(2) Hero Section & Quick Status</b>, <b>(3) About & Academic Profile</b>, <b>(4) Skills & Tech Stack Matrix</b>, <b>(5) Featured Projects & Filter</b>, <b>(6) Academic Timeline & Experience</b>, serta <b>(7) Contact & Footer</b>.",
        style_body
    ))

    story.append(PageBreak())

    # ==========================================
    # HALAMAN 4: BAB III IMPLEMENTASI & DOKUMENTASI
    # ==========================================
    story.append(Paragraph("BAB III<br/>IMPLEMENTASI DAN DOKUMENTASI SISTEM", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    story.append(Paragraph("A. Implementasi Antarmuka dan Struktur Semantik", style_h2))
    story.append(Paragraph(
        "Implementasi antarmuka berpedoman pada struktur HTML5 semantik (<header>, <main>, <section>, <footer>) untuk memaksimalkan aksesibilitas. Pada bagian Hero, disajikan identitas singkat, status akademik sebagai Mahasiswa S1 Teknik Informatika FT UNESA angkatan 2026, serta tombol aksi cepat (Call to Action) menuju proyek dan repositori GitHub.",
        style_body
    ))

    story.append(Paragraph("B. Implementasi Fitur Utama", style_h2))
    story.append(Paragraph("<b>1. Sistem Dual-Theme (Dark/Light Mode Persistence):</b>", style_list))
    story.append(Paragraph(
        "Logika tema memanfaatkan manipulasi class 'dark' pada elemen root dokumen dengan sinkronisasi ke preferensi sistem operasi dan penyimpanan permanen pada browser client:",
        style_body_no_indent
    ))

    code_snippet_theme = (
        "// Inisialisasi dan Pergantian Tema (LocalStorage)\n"
        "function applyTheme(theme) {\n"
        "  if (theme === 'dark') {\n"
        "    document.documentElement.classList.add('dark');\n"
        "    localStorage.setItem('theme', 'dark');\n"
        "  } else {\n"
        "    document.documentElement.classList.remove('dark');\n"
        "    localStorage.setItem('theme', 'light');\n"
        "  }\n"
        "  lucide.createIcons();\n"
        "}"
    )
    code_table_1 = Table([[Paragraph(f"<pre>{code_snippet_theme}</pre>", style_code_box)]], colWidths=[14 * cm])
    code_table_1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(code_table_1)

    story.append(Paragraph("<b>2. Filtering Proyek Interaktif:</b>", style_list))
    story.append(Paragraph(
        "Setiap kartu proyek dilengkapi atribut data-category yang memungkinkan pengguna menyaring proyek secara instan (Web App, Sistem & DevOps, Algoritma C++) tanpa memuat ulang halaman.",
        style_body_no_indent
    ))

    story.append(Paragraph("C. Proyek yang Ditampilkan dalam Portofolio", style_h2))
    story.append(Paragraph("Terdapat 4 proyek unggulan yang didokumentasikan dalam portofolio:", style_body_no_indent))
    story.append(Paragraph("1. <b>Arunika Academic Portal (baturs.my.id):</b> Portal terpadu presensi dan materi kelas F Teknik Informatika UNESA dengan integrasi Cloudflare Named Tunnel.", style_list))
    story.append(Paragraph("2. <b>RuangTemu UNESA:</b> Platform web kolaborasi dan reservasi ruang belajar mahasiswa FT UNESA.", style_list))
    story.append(Paragraph("3. <b>Wameow Academic Gateway:</b> Layanan otomatisasi asinkron komunikasi WhatsApp untuk pengingat tugas kuliah dan notifikasi akademik.", style_list))
    story.append(Paragraph("4. <b>C++ Computational Suite:</b> Pustaka implementasi struktur data dan algoritma efisien berbasis C++17.", style_list))

    story.append(Paragraph("D. Pengujian Kualitas dan Aksesibilitas", style_h2))
    story.append(Paragraph(
        "Pengujian fungsional dilakukan pada lingkungan Google Chrome dan perangkat seluler. Hasil pengujian membuktikan bahwa seluruh elemen navigasi responsif, kontras warna memenuhi standar kenyamanan visual, dan interaktivitas JavaScript berjalan mulus tanpa error pada console.",
        style_body
    ))

    story.append(PageBreak())

    # ==========================================
    # HALAMAN 5: BAB IV PENUTUP, DAFTAR PUSTAKA, LAMPIRAN
    # ==========================================
    story.append(Paragraph("BAB IV<br/>PENUTUP", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    story.append(Paragraph("A. Kesimpulan", style_h2))
    story.append(Paragraph(
        "Penyusunan website portofolio pribadi ini telah berhasil diselesaikan secara utuh sesuai dengan petunjuk teknis penugasan Ameliorer Day 5 Jurusan Teknik Informatika UNESA. Melalui implementasi arsitektur frontend modern (HTML5, Tailwind CSS, JavaScript ES6+), website ini mampu menyajikan identitas akademik, keahlian teknis, dan portofolio proyek Muhammad Guntur Cahyadi Putra secara profesional, estetis, dan responsif.",
        style_body
    ))

    story.append(Paragraph("B. Rencana Pengembangan Lanjutan (Future Work)", style_h2))
    story.append(Paragraph(
        "Ke depan, website portofolio ini akan terus dikembangkan dengan menambahkan fitur blog teknis untuk mempublikasikan analisis algoritma, integrasi otomatis ke GitHub API untuk memperbarui status repositori secara real-time, serta penambahan showcase proyek tugas akhir perkuliahan.",
        style_body
    ))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("DAFTAR PUSTAKA", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=6))

    story.append(Paragraph(
        "Flanagan, D. (2020). <i>JavaScript: The Definitive Guide: Master the World's Most-Used Programming Language</i> (7th ed.). O'Reilly Media.",
        style_body_no_indent
    ))
    story.append(Paragraph(
        "Marcotte, E. (2011). <i>Responsive Web Design</i>. A Book Apart.",
        style_body_no_indent
    ))
    story.append(Paragraph(
        "Tailwind Labs. (2026). <i>Tailwind CSS Documentation: Utility-First Fundamentals</i>. Retrieved from https://tailwindcss.com/docs",
        style_body_no_indent
    ))
    story.append(Paragraph(
        "Universitas Negeri Surabaya. (2024). <i>Buku Pedoman Penulisan Karya Ilmiah dan Tugas Akhir Universitas Negeri Surabaya</i>. Unesa University Press.",
        style_body_no_indent
    ))
    story.append(Paragraph(
        "W3C Web Accessibility Initiative. (2023). <i>Web Content Accessibility Guidelines (WCAG) 2.2</i>. World Wide Web Consortium.",
        style_body_no_indent
    ))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("LAMPIRAN", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=6))

    attachment_data = [
        [Paragraph("<b>Informasi Tautan</b>", style_cover_identity), Paragraph("<b>URL / Keterangan</b>", style_cover_identity)],
        [Paragraph("<b>Domain & Live Portofolio</b>", style_body_no_indent), Paragraph("https://portoamelio.baturs.my.id", style_body_no_indent)],
        [Paragraph("<b>Cloudflare Pages Mirror</b>", style_body_no_indent), Paragraph("https://portoamelio.pages.dev", style_body_no_indent)],
        [Paragraph("<b>Link Repositori GitHub</b>", style_body_no_indent), Paragraph("https://github.com/muhammadgunturcahyadiputra-boop", style_body_no_indent)],
        [Paragraph("<b>Link Form Pengumpulan</b>", style_body_no_indent), Paragraph("https://unesa.me/PengumpulanWebPortofolioAmeliorer2026Day5", style_body_no_indent)],
        [Paragraph("<b>Status Deployment</b>", style_body_no_indent), Paragraph("Active & Production Live (Cloudflare Edge SSL)", style_body_no_indent)]
    ]
    att_table = Table(attachment_data, colWidths=[4.8 * cm, 9.2 * cm])
    att_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(att_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Laporan PDF berhasil dibuat di: {output_filename}")

if __name__ == '__main__':
    out_pdf = r"C:\Users\ASUS\portfolio-guntur\Laporan_Penugasan_Web_Portofolio_Ameliorer_Day5_Guntur_Cahyadi.pdf"
    generate_pdf(out_pdf)
