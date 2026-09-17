from unittest.mock import MagicMock

from app import generate_pdf_for_item


def test_generate_pdf_for_item_idea_chart_produces_pdf_bytes(monkeypatch):
    fake_item = {
        "name": "ATENEA NARANJA PET 300ML",
        "column_values": [],
    }
    fake_client = MagicMock()
    fake_client.fetch_item.return_value = fake_item
    fake_client.get_status_color.return_value = None
    fake_client.fetch_item_image_bytes.return_value = None

    pdf_bytes = generate_pdf_for_item("idea_chart", "1001", fake_client)

    assert pdf_bytes[:5] == b"%PDF-"
    fake_client.fetch_item.assert_called_once_with("1001")


def test_generate_pdf_for_item_caso_negocio_produces_pdf_bytes(monkeypatch):
    fake_item = {"name": "BABY YODA", "column_values": []}
    fake_client = MagicMock()
    fake_client.fetch_item.return_value = fake_item
    fake_client.get_status_color.return_value = None

    pdf_bytes = generate_pdf_for_item("caso_negocio", "2002", fake_client)

    assert pdf_bytes[:5] == b"%PDF-"


def test_generate_pdf_for_item_rejects_unknown_doc_type():
    fake_client = MagicMock()

    try:
        generate_pdf_for_item("algo_raro", "1001", fake_client)
        assert False, "expected ValueError"
    except ValueError:
        pass
