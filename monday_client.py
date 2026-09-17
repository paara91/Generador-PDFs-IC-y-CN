"""Thin client over Monday.com's GraphQL API (https://api.monday.com/v2)."""
import json

import requests

API_URL = "https://api.monday.com/v2"


class MondayClient:
    def __init__(self, api_token: str):
        self.api_token = api_token

    def _graphql(self, query: str, variables: dict | None = None) -> dict:
        resp = requests.post(
            API_URL,
            json={"query": query, "variables": variables or {}},
            headers={"Authorization": self.api_token},
            timeout=30,
        )
        resp.raise_for_status()
        payload = resp.json()
        if "errors" in payload:
            raise RuntimeError(f"Monday.com API error: {payload['errors']}")
        return payload["data"]

    def fetch_recent_items(
        self, board_id: str, limit: int = 25, status_column_id: str | None = None
    ) -> list[dict]:
        column_ids = [status_column_id] if status_column_id else []
        query = """
        query ($board_id: [ID!], $limit: Int!, $column_ids: [String!]) {
          boards (ids: $board_id) {
            items_page (
              limit: $limit,
              query_params: { order_by: [{ column_id: "__creation_log__", direction: desc }] }
            ) {
              items {
                id
                name
                created_at
                column_values (ids: $column_ids) { id text }
              }
            }
          }
        }
        """
        data = self._graphql(
            query, {"board_id": [board_id], "limit": limit, "column_ids": column_ids}
        )
        raw_items = data["boards"][0]["items_page"]["items"]
        result = []
        for it in raw_items:
            status_col = (
                next((c for c in it["column_values"] if c["id"] == status_column_id), None)
                if status_column_id
                else None
            )
            result.append(
                {
                    "id": it["id"],
                    "name": it["name"],
                    "created_at": it["created_at"],
                    "state_label": status_col["text"] if status_col else None,
                }
            )
        return result

    def fetch_item(self, item_id: str) -> dict:
        query = """
        query ($item_id: [ID!]) {
          items (ids: $item_id) {
            id
            name
            column_values {
              id
              text
              value
              column { title type settings_str }
            }
          }
        }
        """
        data = self._graphql(query, {"item_id": [item_id]})
        return data["items"][0]

    def get_status_color(self, column_value: dict) -> str | None:
        column = column_value.get("column", {})
        if column.get("type") not in ("color", "status"):
            return None
        settings = json.loads(column.get("settings_str") or "{}")
        labels_colors = settings.get("labels_colors", {})
        raw_value = column_value.get("value")
        if not raw_value:
            return None
        try:
            index = json.loads(raw_value).get("index")
        except (json.JSONDecodeError, AttributeError):
            return None
        entry = labels_colors.get(str(index))
        return entry.get("color") if entry else None

    def fetch_item_image_bytes(self, item_id: str, column_id: str) -> bytes | None:
        query = """
        query ($item_id: [ID!], $column_id: [String!]) {
          items (ids: $item_id) {
            column_values (ids: $column_id) { id value }
          }
        }
        """
        data = self._graphql(query, {"item_id": [item_id], "column_id": [column_id]})
        column_values = data["items"][0]["column_values"]
        raw_value = column_values[0]["value"] if column_values else None
        if not raw_value:
            return None
        files = json.loads(raw_value).get("files", [])
        if not files:
            return None
        asset_id = files[0]["assetId"]

        assets_query = """
        query ($asset_id: [ID!]!) {
          assets (ids: $asset_id) { public_url }
        }
        """
        assets_data = self._graphql(assets_query, {"asset_id": [asset_id]})
        public_url = assets_data["assets"][0]["public_url"]

        resp = requests.get(public_url, timeout=30)
        resp.raise_for_status()
        return resp.content

    def upload_pdf_to_item(
        self, item_id: str, column_id: str, filename: str, pdf_bytes: bytes
    ) -> None:
        mutation = """
        mutation ($item_id: ID!, $column_id: String!, $file: File!) {
          add_file_to_column (item_id: $item_id, column_id: $column_id, file: $file) { id }
        }
        """
        resp = requests.post(
            "https://api.monday.com/v2/file",
            headers={"Authorization": self.api_token},
            data={
                "query": mutation,
                "variables": json.dumps(
                    {"item_id": item_id, "column_id": column_id, "file": None}
                ),
                "map": json.dumps({"file": ["variables.file"]}),
            },
            files={"file": (filename, pdf_bytes, "application/pdf")},
            timeout=60,
        )
        resp.raise_for_status()
        payload = resp.json()
        if "errors" in payload:
            raise RuntimeError(f"Monday.com upload error: {payload['errors']}")
