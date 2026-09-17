"""Pure functions that turn raw Monday.com column values into display strings/HTML."""

_MESES_ES = {
    1: "ene", 2: "feb", 3: "mar", 4: "abr", 5: "may", 6: "jun",
    7: "jul", 8: "ago", 9: "sep", 10: "oct", 11: "nov", 12: "dic",
}


def format_text(value: str | None) -> str:
    if value is None or value == "":
        return "N/A"
    return value


def format_date_es(iso_date: str | None) -> str:
    if not iso_date:
        return "N/A"
    year, month, day = iso_date.split("-")[:3]
    day = day.split("T")[0]
    mes = _MESES_ES[int(month)]
    return f"{mes} {int(day)}, {year}"


def format_percent(value: str | None) -> str:
    if not value:
        return "N/A"
    value = value.strip()
    return value if value.endswith("%") else f"{value}%"


def render_status_pill(label: str | None, color: str | None) -> str:
    display_label = label if label else "N/A"
    bg = color if color else "#9aa5b5"
    return (
        f'<span style="display:inline-block; padding:0.8mm 3mm; border-radius:2.2mm; '
        f'font-size:9pt; font-weight:700; color:#fff; background:{bg};">{display_label}</span>'
    )
