"""Declarative mapping from Monday.com columns to template context values.

To add a field later: add one FieldSpec to the relevant list below — no
template or rendering code needs to change.
"""
import json
from dataclasses import dataclass
from typing import Callable

from board_config import COLUMN_IDS_IDEA_CHART, COLUMN_IDS_CASO_NEGOCIO
from field_formatters import format_text, format_date_es, format_percent, render_status_pill


@dataclass
class FieldSpec:
    key: str                    # name used in the template context
    column_id: str               # Monday.com column id (from board_config)
    formatter: Callable[[str | None], str]


def _find_column_value(item: dict, column_id: str) -> dict | None:
    return next((c for c in item["column_values"] if c["id"] == column_id), None)


def _raw_date(column_value: dict | None) -> str | None:
    """Monday.com date columns return their value as a JSON object: {"date": "YYYY-MM-DD", "icon": ...}."""
    if not column_value or not column_value.get("value"):
        return None
    return json.loads(column_value["value"]).get("date")


def _title_font_size_pt(nombre_proyecto: str | None) -> float:
    """Buckets the document title's font size down as the project name gets longer,
    so long names shrink to fit instead of overflowing the page (WeasyPrint clips
    text that runs past the margin instead of wrapping/shrinking it on its own).
    """
    length = len(nombre_proyecto or "")
    if length <= 25:
        return 16
    if length <= 40:
        return 14
    return 11.5


IDEA_CHART_FIELDS = [
    FieldSpec("responsable", COLUMN_IDS_IDEA_CHART["responsable"], format_text),
    FieldSpec("descripcion_idea", COLUMN_IDS_IDEA_CHART["descripcion_idea"], format_text),
    FieldSpec("presentaciones_pvsp", COLUMN_IDS_IDEA_CHART["presentaciones_pvsp"], format_text),
    FieldSpec("ebitda_estimado", COLUMN_IDS_IDEA_CHART["ebitda_estimado"], format_percent),
    FieldSpec("sabores", COLUMN_IDS_IDEA_CHART["sabores"], format_text),
    FieldSpec("volumen_estimado_cu", COLUMN_IDS_IDEA_CHART["volumen_estimado_cu"], format_text),
    FieldSpec("canales", COLUMN_IDS_IDEA_CHART["canales"], format_text),
    FieldSpec("regiones", COLUMN_IDS_IDEA_CHART["regiones"], format_text),
    FieldSpec("centro_productor", COLUMN_IDS_IDEA_CHART["centro_productor"], format_text),
    FieldSpec(
        "pre_factibilidad_tecnica", COLUMN_IDS_IDEA_CHART["pre_factibilidad_tecnica"], format_text
    ),
]


def build_idea_chart_context(item: dict, monday_client) -> dict:
    context = {
        "nombre_proyecto": item["name"],
        "title_font_size": _title_font_size_pt(item["name"]),
    }

    for spec in IDEA_CHART_FIELDS:
        column_value = _find_column_value(item, spec.column_id)
        text = column_value["text"] if column_value else None
        context[spec.key] = spec.formatter(text)

    # Date column needs the raw ISO value, not Monday's pre-rendered text.
    date_col = _find_column_value(item, COLUMN_IDS_IDEA_CHART["lanzamiento_estimado"])
    context["lanzamiento_estimado"] = format_date_es(_raw_date(date_col))

    # UEN is rendered as a pill using Monday's native color for that value.
    uen_col = _find_column_value(item, COLUMN_IDS_IDEA_CHART["uen"])
    uen_label = uen_col["text"] if uen_col else None
    uen_color = monday_client.get_status_color(uen_col) if uen_col else None
    context["uen_pill"] = render_status_pill(uen_label, uen_color)

    return context


CASO_NEGOCIO_FIELDS = [
    FieldSpec("lider_proyecto", COLUMN_IDS_CASO_NEGOCIO["lider_proyecto"], format_text),
    FieldSpec("descripcion_proyecto", COLUMN_IDS_CASO_NEGOCIO["descripcion_proyecto"], format_text),
    FieldSpec("tipo_proyecto_categoria", COLUMN_IDS_CASO_NEGOCIO["tipo_proyecto_categoria"], format_text),
    FieldSpec("concepto", COLUMN_IDS_CASO_NEGOCIO["concepto"], format_text),
    FieldSpec("marca", COLUMN_IDS_CASO_NEGOCIO["marca"], format_text),
    FieldSpec("sabores", COLUMN_IDS_CASO_NEGOCIO["sabores"], format_text),
    FieldSpec("canales", COLUMN_IDS_CASO_NEGOCIO["canales"], format_text),
    FieldSpec("regiones", COLUMN_IDS_CASO_NEGOCIO["regiones"], format_text),
    FieldSpec("estado_registro_marca_clase", COLUMN_IDS_CASO_NEGOCIO["estado_registro_marca_clase"], format_text),
    FieldSpec("lanzamiento_in_out", COLUMN_IDS_CASO_NEGOCIO["lanzamiento_in_out"], format_text),
    FieldSpec("inversiones_marketing", COLUMN_IDS_CASO_NEGOCIO["inversiones_marketing"], format_text),
    FieldSpec("inversiones_capex", COLUMN_IDS_CASO_NEGOCIO["inversiones_capex"], format_text),
    FieldSpec("caracteristicas_formula", COLUMN_IDS_CASO_NEGOCIO["caracteristicas_formula"], format_text),
    FieldSpec("caracteristicas_empaque", COLUMN_IDS_CASO_NEGOCIO["caracteristicas_empaque"], format_text),
    FieldSpec("vida_util", COLUMN_IDS_CASO_NEGOCIO["vida_util"], format_text),
    FieldSpec("centro_produccion", COLUMN_IDS_CASO_NEGOCIO["centro_produccion"], format_text),
    FieldSpec(
        "resultados_prueba_industrial_transporte",
        COLUMN_IDS_CASO_NEGOCIO["resultados_prueba_industrial_transporte"],
        format_text,
    ),
    FieldSpec("posibles_riesgos", COLUMN_IDS_CASO_NEGOCIO["posibles_riesgos"], format_text),
    FieldSpec("planes_accion", COLUMN_IDS_CASO_NEGOCIO["planes_accion"], format_text),
    FieldSpec("volumenes_iniciativa", COLUMN_IDS_CASO_NEGOCIO["volumenes_iniciativa"], format_text),
    FieldSpec("ebitda_iniciativa", COLUMN_IDS_CASO_NEGOCIO["ebitda_iniciativa"], format_text),
    FieldSpec("observaciones_generales", COLUMN_IDS_CASO_NEGOCIO["observaciones_generales"], format_text),
]


def build_caso_negocio_context(item: dict, monday_client) -> dict:
    context = {
        "nombre_proyecto": item["name"],
        "title_font_size": _title_font_size_pt(item["name"]),
    }

    for spec in CASO_NEGOCIO_FIELDS:
        column_value = _find_column_value(item, spec.column_id)
        text = column_value["text"] if column_value else None
        context[spec.key] = spec.formatter(text)

    fecha_creacion_col = _find_column_value(item, COLUMN_IDS_CASO_NEGOCIO["fecha_creacion"])
    context["fecha_creacion"] = format_date_es(_raw_date(fecha_creacion_col))

    fecha_lanzamiento_col = _find_column_value(
        item, COLUMN_IDS_CASO_NEGOCIO["fecha_estimada_lanzamiento"]
    )
    context["fecha_estimada_lanzamiento"] = format_date_es(_raw_date(fecha_lanzamiento_col))

    uen_col = _find_column_value(item, COLUMN_IDS_CASO_NEGOCIO["uen"])
    uen_label = uen_col["text"] if uen_col else None
    uen_color = monday_client.get_status_color(uen_col) if uen_col else None
    context["uen_pill"] = render_status_pill(uen_label, uen_color)

    return context
