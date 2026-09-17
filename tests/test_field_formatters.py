from field_formatters import format_text, format_date_es, format_percent, render_status_pill


def test_format_text_passes_through_value():
    assert format_text("Naranja") == "Naranja"


def test_format_text_falls_back_to_na():
    assert format_text(None) == "N/A"
    assert format_text("") == "N/A"


def test_format_date_es_formats_spanish_short_month():
    assert format_date_es("2027-01-20") == "ene 20, 2027"
    assert format_date_es("2026-08-04") == "ago 4, 2026"
    assert format_date_es("2026-11-03") == "nov 3, 2026"


def test_format_date_es_falls_back_to_na():
    assert format_date_es(None) == "N/A"
    assert format_date_es("") == "N/A"


def test_format_percent_appends_sign():
    assert format_percent("16") == "16%"
    assert format_percent("16%") == "16%"


def test_format_percent_falls_back_to_na():
    assert format_percent(None) == "N/A"


def test_render_status_pill_with_color():
    html = render_status_pill("Frutas", "#FCB820")
    assert 'background:#FCB820' in html
    assert '>Frutas<' in html
    assert 'color:#fff' in html


def test_render_status_pill_without_color_falls_back_to_neutral_gray():
    html = render_status_pill("Frutas", None)
    assert 'background:#9aa5b5' in html


def test_render_status_pill_with_no_label_is_na_pill():
    html = render_status_pill(None, None)
    assert '>N/A<' in html
