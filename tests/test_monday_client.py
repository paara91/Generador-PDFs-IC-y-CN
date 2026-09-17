import json
import os
import responses

from monday_client import MondayClient

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def load_fixture(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return json.load(f)


@responses.activate
def test_fetch_recent_items_returns_name_and_state():
    responses.add(
        responses.POST,
        "https://api.monday.com/v2",
        json=load_fixture("monday_boards_response.json"),
        status=200,
    )
    client = MondayClient(api_token="fake-token")

    items = client.fetch_recent_items(board_id="123", limit=5, status_column_id="status")

    assert items[0]["id"] == "1001"
    assert items[0]["name"] == "ATENEA NARANJA PET 300ML"
    assert items[0]["state_label"] == "Aprobado"


@responses.activate
def test_fetch_recent_items_without_status_column_id_leaves_state_label_none():
    responses.add(
        responses.POST,
        "https://api.monday.com/v2",
        json=load_fixture("monday_boards_response.json"),
        status=200,
    )
    client = MondayClient(api_token="fake-token")

    items = client.fetch_recent_items(board_id="123", limit=5)

    assert items[0]["name"] == "ATENEA NARANJA PET 300ML"
    assert items[0]["state_label"] is None


@responses.activate
def test_fetch_item_returns_column_values():
    responses.add(
        responses.POST,
        "https://api.monday.com/v2",
        json=load_fixture("monday_item_response.json"),
        status=200,
    )
    client = MondayClient(api_token="fake-token")

    item = client.fetch_item(item_id="1001")

    assert item["name"] == "ATENEA NARANJA PET 300ML"
    uen_col = next(c for c in item["column_values"] if c["id"] == "uen")
    assert uen_col["text"] == "Frutas"


def test_get_status_color_reads_native_monday_color():
    column_value = {
        "id": "uen",
        "text": "Frutas",
        "value": '{"index": 2}',
        "column": {
            "title": "UEN",
            "type": "color",
            "settings_str": json.dumps(
                {
                    "labels": {"2": "Frutas"},
                    "labels_colors": {"2": {"color": "#FCB820", "border": "#e0a300"}},
                }
            ),
        },
    }
    client = MondayClient(api_token="fake-token")

    assert client.get_status_color(column_value) == "#FCB820"


def test_get_status_color_returns_none_for_non_status_column():
    column_value = {
        "id": "sabores",
        "text": "Naranja",
        "value": '"Naranja"',
        "column": {"title": "Sabores", "type": "text", "settings_str": "{}"},
    }
    client = MondayClient(api_token="fake-token")

    assert client.get_status_color(column_value) is None


@responses.activate
def test_fetch_item_image_bytes_downloads_asset():
    responses.add(
        responses.POST,
        "https://api.monday.com/v2",
        json={
            "data": {
                "items": [
                    {
                        "column_values": [
                            {
                                "id": "imagen_producto",
                                "value": '{"files":[{"assetId": 555}]}',
                            }
                        ]
                    }
                ]
            }
        },
        status=200,
    )
    responses.add(
        responses.POST,
        "https://api.monday.com/v2",
        json={"data": {"assets": [{"public_url": "https://files.monday.com/fake.png"}]}},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://files.monday.com/fake.png",
        body=b"fake-image-bytes",
        status=200,
    )
    client = MondayClient(api_token="fake-token")

    image_bytes = client.fetch_item_image_bytes(item_id="1001", column_id="imagen_producto")

    assert image_bytes == b"fake-image-bytes"


@responses.activate
def test_fetch_item_image_bytes_returns_none_when_no_file():
    responses.add(
        responses.POST,
        "https://api.monday.com/v2",
        json={"data": {"items": [{"column_values": [{"id": "imagen_producto", "value": None}]}]}},
        status=200,
    )
    client = MondayClient(api_token="fake-token")

    assert client.fetch_item_image_bytes(item_id="1001", column_id="imagen_producto") is None


@responses.activate
def test_upload_pdf_to_item_posts_multipart_file():
    responses.add(
        responses.POST,
        "https://api.monday.com/v2/file",
        json={"data": {"add_file_to_column": {"id": "999"}}},
        status=200,
    )
    client = MondayClient(api_token="fake-token")

    client.upload_pdf_to_item(
        item_id="1001", column_id="archivo_pdf", filename="idea_chart.pdf", pdf_bytes=b"%PDF-fake"
    )

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.monday.com/v2/file"

    # Verify multipart body structure
    request_body = responses.calls[0].request.body

    # Check that filename is present in Content-Disposition header
    assert b'filename="idea_chart.pdf"' in request_body

    # Check that content-type is correct for the file part
    assert b'Content-Type: application/pdf' in request_body

    # Check that the PDF bytes are in the body
    assert b"%PDF-fake" in request_body

    # Check that variables JSON contains the correct item_id and column_id
    assert b'"item_id": "1001"' in request_body
    assert b'"column_id": "archivo_pdf"' in request_body


@responses.activate
def test_upload_pdf_to_item_raises_on_monday_error():
    responses.add(
        responses.POST,
        "https://api.monday.com/v2/file",
        json={"errors": ["Failed to upload file"]},
        status=200,
    )
    client = MondayClient(api_token="fake-token")

    try:
        client.upload_pdf_to_item(
            item_id="1001", column_id="archivo_pdf", filename="idea_chart.pdf", pdf_bytes=b"%PDF-fake"
        )
        assert False, "Expected RuntimeError to be raised"
    except RuntimeError as e:
        assert "Monday.com upload error" in str(e)
        assert "Failed to upload file" in str(e)
