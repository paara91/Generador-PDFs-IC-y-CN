import os

import streamlit as st

from board_config import BOARD_IDS, STATUS_COLUMN_IDS, COLUMN_IDS_IDEA_CHART, COLUMN_IDS_CASO_NEGOCIO
from field_config import build_idea_chart_context, build_caso_negocio_context
from image_utils import to_data_uri
from monday_client import MondayClient
from pdf_render import render_html_to_pdf
from template_render import render_idea_chart_html, render_caso_negocio_html

# Marca Postobón — mismos tonos que la app de Shark Tank (Comité de Innovación)
NAVY_900 = "#000D27"
NAVY_CARD = "#142038"
CYAN = "#00b2f0"
HOVER_BLUE = "#046AB0"
TEXT_SECONDARY = "#9fc3d6"

DOC_TYPES = {
    "idea_chart": {
        "label": "Idea Chart",
        "board_key": "idea_chart",
        "image_column_key": "imagen_producto",
        "column_ids": COLUMN_IDS_IDEA_CHART,
        "build_context": build_idea_chart_context,
        "render_html": render_idea_chart_html,
    },
    "caso_negocio": {
        "label": "Caso de Negocio",
        "board_key": "caso_negocio",
        "image_column_key": None,
        "column_ids": COLUMN_IDS_CASO_NEGOCIO,
        "build_context": build_caso_negocio_context,
        "render_html": render_caso_negocio_html,
    },
}


def generate_pdf_for_item(doc_type: str, item_id: str, monday_client: MondayClient) -> bytes:
    if doc_type not in DOC_TYPES:
        raise ValueError(f"Unknown document type: {doc_type!r}")

    config = DOC_TYPES[doc_type]
    item = monday_client.fetch_item(item_id)
    context = config["build_context"](item, monday_client)

    if config["image_column_key"]:
        image_column_id = config["column_ids"][config["image_column_key"]]
        image_bytes = monday_client.fetch_item_image_bytes(item_id, image_column_id)
        context["imagen_producto_src"] = to_data_uri(image_bytes) if image_bytes else None

    html = config["render_html"](context)
    return render_html_to_pdf(html)


def _format_short_date(iso_datetime: str | None) -> str:
    """Shortens Monday.com's ISO created_at timestamp to just its date part, for the picker label."""
    if not iso_datetime:
        return "sin fecha"
    return iso_datetime[:10]


def _inject_brand_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap');
        html, body, .stApp, .stApp *:not([data-testid="stIconMaterial"]) {{
            font-family: 'Montserrat', sans-serif !important;
        }}
        .stApp {{ background-color: {NAVY_900}; color: #f7fcff; }}
        h1, h2, h3, h4, h5 {{ color: #f7fcff !important; }}

        /* Tarjeta central: el mismo look de "card" que en Shark Tank */
        div[data-testid="stAppViewContainer"] .block-container {{
            background-color: {NAVY_CARD};
            border-radius: 28px;
            padding: 2.4rem 2.6rem 2.8rem;
            margin-top: 3rem;
            max-width: 620px;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 30px 60px rgba(0,0,0,.35);
            position: relative; z-index: 1;
        }}

        [data-testid="stImage"] img {{ filter: brightness(0) invert(1); opacity: .92; }}

        div[data-testid="stButton"] > button, div[data-testid="stDownloadButton"] > button {{
            background-color: {CYAN}; color: {NAVY_900}; font-weight: 800;
            border-radius: 12px; border: none; width: 100%;
        }}
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stButton"] > button:focus,
        div[data-testid="stButton"] > button:focus:not(:active),
        div[data-testid="stButton"] > button:active,
        div[data-testid="stDownloadButton"] > button:hover,
        div[data-testid="stDownloadButton"] > button:focus,
        div[data-testid="stDownloadButton"] > button:focus:not(:active),
        div[data-testid="stDownloadButton"] > button:active {{
            background-color: {HOVER_BLUE} !important; color: #f7fcff !important;
            border-color: {HOVER_BLUE} !important;
        }}
        div[data-testid="stButton"] > button[kind="secondary"],
        div[data-testid="stDownloadButton"] > button[kind="secondary"] {{
            background-color: rgba(255,255,255,0.04) !important; color: #f7fcff; font-weight: 700;
            border: 1.5px solid rgba(255,255,255,0.22) !important; border-radius: 12px;
        }}
        div[data-testid="stButton"] > button[kind="secondary"]:hover,
        div[data-testid="stButton"] > button[kind="secondary"]:focus,
        div[data-testid="stButton"] > button[kind="secondary"]:focus:not(:active),
        div[data-testid="stButton"] > button[kind="secondary"]:active,
        div[data-testid="stDownloadButton"] > button[kind="secondary"]:hover,
        div[data-testid="stDownloadButton"] > button[kind="secondary"]:focus,
        div[data-testid="stDownloadButton"] > button[kind="secondary"]:focus:not(:active),
        div[data-testid="stDownloadButton"] > button[kind="secondary"]:active {{
            background-color: rgba(4,106,176,0.12) !important; color: #f7fcff !important;
            border-color: {HOVER_BLUE} !important;
        }}

        [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {{
            color: {TEXT_SECONDARY} !important; font-weight: 700 !important;
            text-transform: uppercase; letter-spacing: .06em; font-size: 12px !important;
        }}

        div[data-baseweb="select"] > div, div[data-testid="stSelectbox"] > div > div {{
            background-color: rgba(255,255,255,0.06) !important;
            border: 1.5px solid rgba(255,255,255,0.24) !important;
            border-radius: 12px !important;
        }}
        div[data-baseweb="select"] div, div[data-testid="stSelectbox"] * {{ color: #f7fcff !important; }}
        ul[data-testid="stSelectboxVirtualDropdown"], div[role="listbox"] {{ background-color: {NAVY_CARD} !important; }}
        ul[data-testid="stSelectboxVirtualDropdown"] li, div[role="listbox"] * {{ color: #f7fcff !important; }}

        div[data-testid="stAlertContainer"] {{
            background-color: rgba(0,178,240,0.12) !important; border: 1px solid rgba(0,178,240,0.35) !important;
        }}
        div[data-testid="stAlertContainer"] p {{ color: #f7fcff !important; }}

        /* Burbujas de fondo sutiles, sin animación (herramienta de trabajo, no un juego) */
        .brand-bubble {{
            position: fixed; border-radius: 50%; pointer-events: none; z-index: 0;
            background: radial-gradient(circle at 40% 35%, rgba(255,255,255,.28), rgba(0,178,240,.16) 45%, transparent 72%);
        }}
        .brand-bubble.b1 {{ width: 320px; height: 320px; top: -110px; left: -90px; }}
        .brand-bubble.b2 {{ width: 240px; height: 240px; bottom: -90px; right: -70px; }}
        </style>
        <div class="brand-bubble b1"></div>
        <div class="brand-bubble b2"></div>
        """,
        unsafe_allow_html=True,
    )


def _get_monday_client() -> MondayClient:
    try:
        api_token = st.secrets["MONDAY_API_TOKEN"]
    except Exception:
        # Covers both a missing key (KeyError) and a missing secrets.toml
        # file entirely (Streamlit raises its own FileNotFoundError
        # subclass for that case, not KeyError).
        st.error("Falta configurar MONDAY_API_TOKEN en los secretos de la app.")
        st.stop()
    return MondayClient(api_token=api_token)


def main():
    st.set_page_config(
        page_title="Generador de PDF — IC / CN", page_icon="📄", layout="centered"
    )
    _inject_brand_css()

    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_postobon.png")
    st.image(logo_path, width=160)
    st.title("Generador de PDF — Idea Charts y Casos de Negocio")

    if "doc_type" not in st.session_state:
        st.session_state["doc_type"] = "idea_chart"

    st.caption("TIPO DE DOCUMENTO")
    col_ic, col_cn = st.columns(2)
    with col_ic:
        if st.button(
            "Idea Chart",
            type="primary" if st.session_state["doc_type"] == "idea_chart" else "secondary",
            use_container_width=True,
        ):
            st.session_state["doc_type"] = "idea_chart"
    with col_cn:
        if st.button(
            "Caso de Negocio",
            type="primary" if st.session_state["doc_type"] == "caso_negocio" else "secondary",
            use_container_width=True,
        ):
            st.session_state["doc_type"] = "caso_negocio"
    doc_type = st.session_state["doc_type"]

    client = _get_monday_client()
    board_id = BOARD_IDS[DOC_TYPES[doc_type]["board_key"]]

    status_column_id = STATUS_COLUMN_IDS[DOC_TYPES[doc_type]["board_key"]]
    try:
        with st.spinner("Cargando ítems recientes de Monday.com..."):
            items = client.fetch_recent_items(
                board_id=board_id, limit=25, status_column_id=status_column_id
            )
    except Exception as exc:
        st.error(f"No se pudo conectar con Monday.com: {exc}")
        st.stop()

    if not items:
        st.info("No se encontraron ítems recientes en este board.")
        return

    labels = [
        f"{it['name']} — {_format_short_date(it['created_at'])} — {it['state_label'] or 'sin estado'}"
        for it in items
    ]
    selected_index = st.selectbox(
        "Elige el ítem", options=range(len(items)), format_func=lambda i: labels[i]
    )
    selected_item = items[selected_index]

    if st.button("Generar PDF", type="primary"):
        try:
            with st.spinner("Generando PDF..."):
                pdf_bytes = generate_pdf_for_item(doc_type, selected_item["id"], client)
        except Exception as exc:
            st.error(f"No se pudo generar el PDF: {exc}")
        else:
            st.session_state["last_pdf"] = {
                "bytes": pdf_bytes,
                "name": f"{DOC_TYPES[doc_type]['label']} - {selected_item['name']}.pdf",
                "item_id": selected_item["id"],
                "doc_type": doc_type,
            }
            st.success("¡Listo!")

    last_pdf = st.session_state.get("last_pdf")
    is_current_selection = (
        last_pdf is not None
        and last_pdf["item_id"] == selected_item["id"]
        and last_pdf["doc_type"] == doc_type
    )
    if is_current_selection:
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Descargar",
                data=last_pdf["bytes"],
                file_name=last_pdf["name"],
                mime="application/pdf",
            )
        with col2:
            if st.button("📎 Adjuntar en Monday"):
                try:
                    column_ids = DOC_TYPES[last_pdf["doc_type"]]["column_ids"]
                    client.upload_pdf_to_item(
                        item_id=last_pdf["item_id"],
                        column_id=column_ids["archivo_pdf"],
                        filename=last_pdf["name"],
                        pdf_bytes=last_pdf["bytes"],
                    )
                except Exception as exc:
                    st.error(f"No se pudo adjuntar el PDF en Monday.com: {exc}")
                else:
                    st.success("Adjuntado al ítem de Monday.com")


if __name__ == "__main__":
    main()
