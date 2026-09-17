from pypdf import PdfReader
import io

from pdf_render import render_html_to_pdf

SIMPLE_HTML = """
<!DOCTYPE html>
<html><body><h1>IDEA CHART PROYECTO PRUEBA</h1></body></html>
"""


def test_render_html_to_pdf_produces_valid_pdf_bytes():
    pdf_bytes = render_html_to_pdf(SIMPLE_HTML)

    assert pdf_bytes[:5] == b"%PDF-"


def test_render_html_to_pdf_text_is_extractable():
    pdf_bytes = render_html_to_pdf(SIMPLE_HTML)

    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = reader.pages[0].extract_text()

    assert "IDEA CHART PROYECTO PRUEBA" in text
