import os

import streamlit as st

from board_config import BOARD_IDS, STATUS_COLUMN_IDS, COLUMN_IDS_IDEA_CHART, COLUMN_IDS_CASO_NEGOCIO
from field_config import build_idea_chart_context, build_caso_negocio_context
from image_utils import to_data_uri
from monday_client import MondayClient
from pdf_render import render_html_to_pdf
from template_render import render_idea_chart_html, render_caso_negocio_html

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
    st.set_page_config(page_title="Generador de PDF — IC / CN", page_icon="📄")
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_postobon.png")
    st.image(logo_path, width=160)
    st.title("Generador de PDF — Idea Charts y Casos de Negocio")

    doc_type = st.radio(
        "Tipo de documento",
        options=list(DOC_TYPES.keys()),
        format_func=lambda key: DOC_TYPES[key]["label"],
        horizontal=True,
    )

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
