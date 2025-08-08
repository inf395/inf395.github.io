import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import gray  # Import gray color


# Register the Ubuntu font (ensure the TTF file is present at the specified path)
pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu/Ubuntu-Regular.ttf'))

def create_overlay(page_num, total_pages, footnote_text, page_size):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=page_size)
    width, height = page_size

    # Draw footnote (bottom left)
    can.setFont("Ubuntu", 18)
    can.setFillColorRGB(0, 0, 0)  # Black for footnote
    can.drawString(40, 30, footnote_text)

    # Draw slide number (bottom right) in gray
    can.setFont("Ubuntu", 18)
    can.setFillColor(gray)  # Set fill color to gray
    slide_text = f"{page_num + 1} / {total_pages}"
    can.drawRightString(width+10, 30, slide_text)  # 40pt margin from right edge, 30pt from bottom

    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def add_footer_to_pdf(input_pdf, output_pdf, footnote_text):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    page_size = letter  # Adjust if your PDF uses a different size

    for i, page in enumerate(reader.pages):
        overlay = create_overlay(i, total_pages, footnote_text, page_size)
        page.merge_page(overlay)
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

# Usage
add_footer_to_pdf(
    input_pdf="recursos/01-intro-ml-dl.pdf",
    output_pdf="recursos/01-intro-ml-dl2.pdf",
    footnote_text="1 This is a sample footnote."
)

