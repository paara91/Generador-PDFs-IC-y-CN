"""
Run manually, once, to find real Monday.com board/column IDs:
    export MONDAY_API_TOKEN=xxx   (or set it in the shell before running)
    python scripts/discover_schema.py <board_id>

Prints every column's id, title and type so you can fill in board_config.py.
"""
import os
import sys
import requests

API_URL = "https://api.monday.com/v2"


def main():
    if len(sys.argv) != 2:
        print("Usage: python discover_schema.py <board_id>")
        sys.exit(1)
    board_id = sys.argv[1]
    token = os.environ["MONDAY_API_TOKEN"]

    query = """
    query ($board_id: [ID!]) {
      boards (ids: $board_id) {
        name
        columns { id title type settings_str }
      }
    }
    """
    resp = requests.post(
        API_URL,
        json={"query": query, "variables": {"board_id": [board_id]}},
        headers={"Authorization": token},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()["data"]["boards"][0]
    print(f"Board: {data['name']}\n")
    for col in data["columns"]:
        print(f"  id={col['id']!r:30} type={col['type']:15} title={col['title']}")


if __name__ == "__main__":
    main()
