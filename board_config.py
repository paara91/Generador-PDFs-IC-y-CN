"""Real Monday.com board and column IDs, filled in from scripts/discover_schema.py output."""

BOARD_IDS = {
    "idea_chart": "7924872045",
    "caso_negocio": "8876482252",
}

# Status/state column per board, used to show a state label in the item picker.
# None means the board has no equivalent column (Caso de Negocio items are just
# collected, not routed through an approval status like Idea Chart is).
STATUS_COLUMN_IDS = {
    "idea_chart": "estado_mkmwvxbn",  # "Estado Envío"
    "caso_negocio": None,
}

# Internal field key -> Monday.com column id, for the Idea Chart board.
COLUMN_IDS_IDEA_CHART = {
    "responsable": "text__1",  # "Líder del proyecto"
    "uen": "selecci_n__nica__1",  # "UEN"
    "descripcion_idea": "texto_corto__1",  # "Descripción"
    "imagen_producto": "cargar_archivo_mkmky23b",  # "Imagen del producto"
    "presentaciones_pvsp": "texto_largo8__1",  # "Presentaciones y PVSP ($)"
    "lanzamiento_estimado": "fecha_mkmkmx59",  # "Mes estimado de lanzamiento"
    "ebitda_estimado": "text7__1",  # "%EBITDA estimado"
    "sabores": "texto_largo1__1",  # "Sabores"
    "volumen_estimado_cu": "texto_corto7__1",  # "Volumen estimado CU"
    "canales": "selecci_n_m_ltiple1__1",  # "Canales"
    "regiones": "selecci_n_m_ltiple__1",  # "Regiones"
    "centro_productor": "selecci_n_m_ltiple_mkn81124",  # "Centro de producción"
    "pre_factibilidad_tecnica": "texto_largo9__1",  # "Pre factibilidad técnica"
    "archivo_pdf": "file_mm786v23",  # "PDF IC" (created via API for this project)
}

# Internal field key -> Monday.com column id, for the Caso de Negocio board.
COLUMN_IDS_CASO_NEGOCIO = {
    "lider_proyecto": "short_text6qh4r5ld",  # "Responsable del proyecto"
    "descripcion_proyecto": "long_text_mkq08hdk",  # "Descripción del proyecto."
    "fecha_creacion": "date_mkq1yhyv",  # "Fecha de creación."
    "uen": "color_mkq0c9ec",  # "UEN."
    "tipo_proyecto_categoria": "color_mkq0j4th",  # "Tipo de proyecto."
    "fecha_estimada_lanzamiento": "date_mkq1yg57",  # "Fecha de lanzamiento."
    "concepto": "long_text_mkq05ed8",  # "Concepto."
    "marca": "text_mkq0gpys",  # "Marca."
    "sabores": "long_text_mkq0rfxs",  # "SABORES (% Mix):"
    "canales": "dropdown_mkq0fb2n",  # "Canales."
    "regiones": "dropdown_mkq0x4n5",  # "Regiones."
    "estado_registro_marca_clase": "long_text_mkq023qe",  # "Estado registro de marca y clases."
    "lanzamiento_in_out": "color_mkq0h3xj",  # "El Lanzamiento es In & Out."
    "inversiones_marketing": "long_text_mkq0kc6q",  # "Especifique las inversiones en marketing."
    "inversiones_capex": "long_text_mkq07ej7",  # "Especifique las inversiones en CAPEX."
    "caracteristicas_formula": "long_text_mkq0e3q3",  # "Características de la fórmula..."
    "caracteristicas_empaque": "long_text_mkq0kn78",  # "Características del empaque..."
    "vida_util": "text_mkq0xrh5",  # "Vida útil."
    "centro_produccion": "dropdown_mkq0se2d",  # "Centro de producción."
    "resultados_prueba_industrial_transporte": "long_text_mkq08kza",
    "posibles_riesgos": "dropdown_mkq0fynf",
    "planes_accion": "long_text_mkq0k12w",  # "Describa los planes de acción."
    "volumenes_iniciativa": "long_text_mkt31cey",  # "Volúmenes 3 primeros meses"
    "ebitda_iniciativa": "long_text_mkt381tk",  # "EBITDA"
    "observaciones_generales": "long_text_mkq0z4n9",
    "archivo_pdf": "file_mm79kv19",  # "PDF CN" (created via API for this project)
}
