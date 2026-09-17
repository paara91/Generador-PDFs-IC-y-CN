from template_render import render_idea_chart_html, render_caso_negocio_html

SAMPLE_CONTEXT = {
    "nombre_proyecto": "ATENEA NARANJA PET 300ML",
    "title_font_size": 16,
    "responsable": "Maria Camila Barco L",
    "uen_pill": '<span style="background:#FCB820;">Frutas</span>',
    "descripcion_idea": "Hit Naranja Pet 300ml x 12",
    "presentaciones_pvsp": "Pet 300ml $2.000",
    "lanzamiento_estimado": "ene 20, 2027",
    "ebitda_estimado": "16%",
    "sabores": "Naranja",
    "volumen_estimado_cu": "13.000 CU",
    "canales": "Tradicional, Moderno, Canales Alternos",
    "regiones": "Antioquia, Centro Norte, Centro Sur, Santander, Occidente",
    "centro_productor": "Postobón Yumbo",
    "pre_factibilidad_tecnica": "No se requiere",
    "imagen_producto_src": None,
}


def test_render_idea_chart_html_includes_title_and_fields():
    html = render_idea_chart_html(SAMPLE_CONTEXT)

    assert "IDEA CHART PROYECTO ATENEA NARANJA PET 300ML" in html
    assert "Maria Camila Barco L" in html
    assert "Frutas" in html
    assert "#FCB820" in html
    assert "ene 20, 2027" in html
    assert "16%" in html
    assert "Idea Chart · Proyecto ATENEA NARANJA PET 300ML · Confidencial" in html


def test_render_idea_chart_html_omits_image_cell_when_no_image():
    html = render_idea_chart_html(SAMPLE_CONTEXT)

    assert "<img" not in html


def test_render_idea_chart_html_includes_image_when_present():
    context = {**SAMPLE_CONTEXT, "imagen_producto_src": "data:image/png;base64,AAAA"}

    html = render_idea_chart_html(context)

    assert '<img class="product-photo" src="data:image/png;base64,AAAA">' in html


def test_render_idea_chart_html_shrinks_title_font_for_long_project_name():
    long_name = "PROYECTO CON UN NOMBRE MUY LARGO QUE NO DEBERIA DESBORDAR LA PAGINA DEL PDF"
    context = {**SAMPLE_CONTEXT, "nombre_proyecto": long_name, "title_font_size": 11.5}

    html = render_idea_chart_html(context)

    assert "font-size: 11.5pt;" in html
    assert "font-size: 16pt;" not in html


CN_SAMPLE_CONTEXT = {
    "nombre_proyecto": "BABY YODA",
    "title_font_size": 16,
    "lider_proyecto": "Johanna Bermúdez",
    "uen_pill": '<span style="background:#7AD35B;">BNG</span>',
    "descripcion_proyecto": "Gatorade Frutos Tropicales 350ml a $2.500.",
    "fecha_creacion": "ago 4, 2026",
    "tipo_proyecto_categoria": "Nueva presentación - (Táctico)",
    "fecha_estimada_lanzamiento": "oct 5, 2026",
    "concepto": "Consumidores de bebidas isotónicas...",
    "marca": "GATORADE",
    "sabores": "Frutos Tropicales - 80%",
    "canales": "Tradicional, Autoservicios",
    "regiones": "Costa, Centro Sur",
    "estado_registro_marca_clase": "RSA-003939-2017",
    "lanzamiento_in_out": "No",
    "inversiones_marketing": "Dentro del plan. $600.000.000",
    "inversiones_capex": "NO SE REALIZARON INVERSIONES",
    "caracteristicas_formula": "Agua, azúcar, maltodextrina...",
    "caracteristicas_empaque": "N/A",
    "vida_util": "9 meses",
    "centro_produccion": "Lux Bogotá",
    "resultados_prueba_industrial_transporte": "NO APLICA",
    "posibles_riesgos": "Ninguno",
    "planes_accion": "-",
    "volumenes_iniciativa": "CF: Presentación 350ml --> Mes 1: 60.000",
    "ebitda_iniciativa": "N/A",
    "observaciones_generales": "N/A",
}


def test_render_caso_negocio_html_includes_title_and_sections():
    html = render_caso_negocio_html(CN_SAMPLE_CONTEXT)

    assert "CASO DE NEGOCIO BABY YODA" in html
    assert "Johanna Bermúdez" in html
    assert "BNG" in html
    assert "#7AD35B" in html
    assert "ago 4, 2026" in html
    assert "INVERSIONES" in html
    assert "Caso de Negocio · Proyecto BABY YODA · Confidencial" in html


def test_render_caso_negocio_html_shrinks_title_font_for_long_project_name():
    long_name = "CASO DE NEGOCIO CON UN NOMBRE DE PROYECTO EXTREMADAMENTE LARGO PARA VALIDAR EL AJUSTE"
    context = {**CN_SAMPLE_CONTEXT, "nombre_proyecto": long_name, "title_font_size": 11.5}

    html = render_caso_negocio_html(context)

    assert "font-size: 11.5pt;" in html
    assert "font-size: 16pt;" not in html
