import importlib
from unittest.mock import patch

import board_config
import field_config
from field_config import (
    build_idea_chart_context,
    build_caso_negocio_context,
    _title_font_size_pt,
)
from monday_client import MondayClient

# Test-local column IDs that replace "REPLACE" placeholders during tests.
# These distinct fake IDs let us verify the code correctly looks up columns.
TEST_COLUMN_IDS_IDEA_CHART = {
    "responsable": "responsable",
    "uen": "uen",
    "descripcion_idea": "descripcion_idea",
    "imagen_producto": "imagen_producto",
    "presentaciones_pvsp": "presentaciones_pvsp",
    "lanzamiento_estimado": "lanzamiento_estimado",
    "ebitda_estimado": "ebitda_estimado",
    "sabores": "sabores",
    "volumen_estimado_cu": "volumen_estimado_cu",
    "canales": "canales",
    "regiones": "regiones",
    "centro_productor": "centro_productor",
    "pre_factibilidad_tecnica": "pre_factibilidad_tecnica",
    "archivo_pdf": "archivo_pdf",
}

TEST_COLUMN_IDS_CASO_NEGOCIO = {
    "lider_proyecto": "lider_proyecto",
    "descripcion_proyecto": "descripcion_proyecto",
    "fecha_creacion": "fecha_creacion",
    "uen": "uen",
    "tipo_proyecto_categoria": "tipo_proyecto_categoria",
    "fecha_estimada_lanzamiento": "fecha_estimada_lanzamiento",
    "concepto": "concepto",
    "marca": "marca",
    "sabores": "sabores",
    "canales": "canales",
    "regiones": "regiones",
    "estado_registro_marca_clase": "estado_registro_marca_clase",
    "lanzamiento_in_out": "lanzamiento_in_out",
    "inversiones_marketing": "inversiones_marketing",
    "inversiones_capex": "inversiones_capex",
    "caracteristicas_formula": "caracteristicas_formula",
    "caracteristicas_empaque": "caracteristicas_empaque",
    "vida_util": "vida_util",
    "centro_produccion": "centro_produccion",
    "resultados_prueba_industrial_transporte": "resultados_prueba_industrial_transporte",
    "posibles_riesgos": "posibles_riesgos",
    "planes_accion": "planes_accion",
    "volumenes_iniciativa": "volumenes_iniciativa",
    "ebitda_iniciativa": "ebitda_iniciativa",
    "observaciones_generales": "observaciones_generales",
    "archivo_pdf": "archivo_pdf",
}


class FakeMondayClient:
    """Stands in for MondayClient in tests — no network calls."""

    def get_status_color(self, column_value):
        if column_value["id"] == "uen":
            return "#FCB820"
        return None


def _column(id_, text, value=None):
    return {"id": id_, "text": text, "value": value, "column": {"type": "color" if id_ == "uen" else "text", "settings_str": "{}"}}


def test_build_idea_chart_context_maps_all_fields():
    # Patch board_config.COLUMN_IDS_IDEA_CHART with test-local distinct IDs,
    # reload field_config so IDEA_CHART_FIELDS rebuilds with the test IDs,
    # then run the test. This ensures the test uses fake but realistic column IDs
    # without requiring production config to change from "REPLACE" placeholders.
    with patch.dict(board_config.COLUMN_IDS_IDEA_CHART, TEST_COLUMN_IDS_IDEA_CHART, clear=True):
        importlib.reload(field_config)

        item = {
            "name": "ATENEA NARANJA PET 300ML",
            "column_values": [
                _column("responsable", "Maria Camila Barco L"),
                _column("uen", "Frutas"),
                _column("descripcion_idea", "Hit Naranja Pet 300ml x 12"),
                _column("presentaciones_pvsp", "Pet 300ml $2.000"),
                _column("lanzamiento_estimado", None, value='{"date": "2027-01-20"}'),
                _column("ebitda_estimado", "16"),
                _column("sabores", "Naranja"),
                _column("volumen_estimado_cu", "13.000 CU"),
                _column("canales", "Tradicional, Moderno, Canales Alternos"),
                _column("regiones", "Antioquia, Centro Norte, Centro Sur, Santander, Occidente"),
                _column("centro_productor", "Postobón Yumbo"),
                _column("pre_factibilidad_tecnica", "No se requiere"),
            ],
        }

        context = field_config.build_idea_chart_context(item, FakeMondayClient())

        assert context["nombre_proyecto"] == "ATENEA NARANJA PET 300ML"
        assert context["responsable"] == "Maria Camila Barco L"
        assert "Frutas" in context["uen_pill"]
        assert "#FCB820" in context["uen_pill"]
        assert context["descripcion_idea"] == "Hit Naranja Pet 300ml x 12"
        assert context["lanzamiento_estimado"] == "ene 20, 2027"
        assert context["ebitda_estimado"] == "16%"
        assert context["sabores"] == "Naranja"
        assert context["regiones"] == "Antioquia, Centro Norte, Centro Sur, Santander, Occidente"
        assert context["title_font_size"] == 16
    importlib.reload(field_config)


def test_build_idea_chart_context_missing_field_is_na():
    with patch.dict(board_config.COLUMN_IDS_IDEA_CHART, TEST_COLUMN_IDS_IDEA_CHART, clear=True):
        importlib.reload(field_config)

        item = {"name": "PROYECTO X", "column_values": []}

        context = field_config.build_idea_chart_context(item, FakeMondayClient())

        assert context["responsable"] == "N/A"
        assert context["sabores"] == "N/A"
        assert "N/A" in context["uen_pill"]
    importlib.reload(field_config)


def test_build_caso_negocio_context_maps_all_fields():
    with patch.dict(board_config.COLUMN_IDS_CASO_NEGOCIO, TEST_COLUMN_IDS_CASO_NEGOCIO, clear=True):
        importlib.reload(field_config)

        item = {
            "name": "BABY YODA",
            "column_values": [
                _column("lider_proyecto", "Johanna Bermúdez"),
                _column("descripcion_proyecto", "Gatorade Frutos Tropicales 350ml a $2.500."),
                _column("fecha_creacion", None, value='{"date": "2026-08-04"}'),
                _column("uen", "BNG"),
                _column("tipo_proyecto_categoria", "Nueva presentación - (Táctico)"),
                _column("fecha_estimada_lanzamiento", None, value='{"date": "2026-10-05"}'),
                _column("concepto", "Consumidores de bebidas isotónicas..."),
                _column("marca", "GATORADE"),
                _column("sabores", "Frutos Tropicales - 80%"),
                _column("canales", "Tradicional, Autoservicios"),
                _column("regiones", "Costa, Centro Sur"),
                _column("estado_registro_marca_clase", "RSA-003939-2017"),
                _column("lanzamiento_in_out", "No"),
                _column("inversiones_marketing", "Dentro del plan. $600.000.000"),
                _column("inversiones_capex", "NO SE REALIZARON INVERSIONES"),
                _column("caracteristicas_formula", "Agua, azúcar, maltodextrina..."),
                _column("caracteristicas_empaque", None),
                _column("vida_util", "9 meses"),
                _column("centro_produccion", "Lux Bogotá"),
                _column("resultados_prueba_industrial_transporte", "NO APLICA"),
                _column("posibles_riesgos", "Ninguno"),
                _column("planes_accion", "-"),
                _column("volumenes_iniciativa", "CF: Presentación 350ml --> Mes 1: 60.000"),
                _column("ebitda_iniciativa", None),
                _column("observaciones_generales", "N/A"),
            ],
        }

        context = build_caso_negocio_context(item, FakeMondayClient())

        assert context["nombre_proyecto"] == "BABY YODA"
        assert context["lider_proyecto"] == "Johanna Bermúdez"
        assert context["fecha_creacion"] == "ago 4, 2026"
        assert "BNG" in context["uen_pill"]
        assert context["fecha_estimada_lanzamiento"] == "oct 5, 2026"
        assert context["marca"] == "GATORADE"
        assert context["caracteristicas_empaque"] == "N/A"
        assert context["ebitda_iniciativa"] == "N/A"
        assert context["title_font_size"] == 16
    importlib.reload(field_config)


def test_title_font_size_pt_buckets_by_name_length():
    assert _title_font_size_pt("ATENEA NARANJA") == 16  # 14 chars, <=25
    assert _title_font_size_pt("A" * 25) == 16
    assert _title_font_size_pt("A" * 26) == 14
    assert _title_font_size_pt("A" * 40) == 14
    assert _title_font_size_pt("A" * 41) == 11.5
    assert _title_font_size_pt(None) == 16
    assert _title_font_size_pt("") == 16


def test_build_idea_chart_context_shrinks_title_font_for_long_name():
    with patch.dict(board_config.COLUMN_IDS_IDEA_CHART, TEST_COLUMN_IDS_IDEA_CHART, clear=True):
        importlib.reload(field_config)

        long_name = "PROYECTO CON UN NOMBRE MUY LARGO QUE DEBE REDUCIR EL TAMANO DE FUENTE DEL TITULO"
        item = {"name": long_name, "column_values": []}

        context = field_config.build_idea_chart_context(item, FakeMondayClient())

        assert context["title_font_size"] == 11.5
    importlib.reload(field_config)


def test_build_caso_negocio_context_shrinks_title_font_for_long_name():
    with patch.dict(board_config.COLUMN_IDS_CASO_NEGOCIO, TEST_COLUMN_IDS_CASO_NEGOCIO, clear=True):
        importlib.reload(field_config)

        long_name = "CASO DE NEGOCIO CON UN NOMBRE DE PROYECTO EXTREMADAMENTE LARGO PARA VALIDAR EL AJUSTE"
        item = {"name": long_name, "column_values": []}

        context = field_config.build_caso_negocio_context(item, FakeMondayClient())

        assert context["title_font_size"] == 11.5
    importlib.reload(field_config)
