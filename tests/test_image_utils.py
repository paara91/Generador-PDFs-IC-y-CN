import base64

from image_utils import to_data_uri


def test_to_data_uri_encodes_bytes_as_base64_png():
    result = to_data_uri(b"fake-bytes", "image/png")

    expected_b64 = base64.b64encode(b"fake-bytes").decode("ascii")
    assert result == f"data:image/png;base64,{expected_b64}"


def test_to_data_uri_defaults_to_png_mime_type():
    result = to_data_uri(b"fake-bytes")

    assert result.startswith("data:image/png;base64,")
