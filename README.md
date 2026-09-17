# Generador de PDF — Idea Charts y Casos de Negocio

App de Streamlit que trae datos de un ítem de Monday.com y genera un PDF con el
diseño de marca de Postobón, listo para descargar o adjuntar de vuelta al
ítem en Monday.

## Correr localmente

1. `pip install -r requirements.txt -r requirements-dev.txt`
2. Copia `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml` y pega
   tu token de Monday.com ahí (ese archivo está en `.gitignore` — nunca lo
   subas a git ni lo compartas).
3. `streamlit run app.py`

**Windows:** WeasyPrint (la librería que genera el PDF) necesita el runtime de
GTK3 (Pango/Cairo/GObject) instalado aparte — no viene con `pip install`. Si
al correr la app ves un error tipo `cannot load library 'gobject-2.0-0'`,
instala el runtime de GTK3 para Windows (busca "GTK3 runtime Windows") y
asegúrate de que sus DLLs queden en el PATH.

## Correr las pruebas

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

## Publicar en Streamlit Community Cloud

1. Sube esta carpeta completa a un repositorio de GitHub (puede ser privado).
2. Entra a [share.streamlit.io](https://share.streamlit.io) e inicia sesión
   con tu cuenta de GitHub.
3. "New app" → selecciona el repositorio → "Main file path": `app.py` →
   Deploy.
4. En Settings → Secrets, pega el contenido de tu `secrets.toml` real (nunca
   el `.example`):
   ```toml
   MONDAY_API_TOKEN = "tu-token-real"
   ```
5. En un par de minutos obtienes una URL pública tipo
   `https://<algo>.streamlit.app` — ese es el link que compartes con tu
   equipo. No lo compartas fuera del equipo: los documentos que genera son
   confidenciales y cualquiera con el link puede generarlos.

## Configuración de boards

`board_config.py` tiene los IDs reales de los boards y columnas de Monday.com
ya configurados para los boards de Idea Chart y Caso de Negocio de Postobón.
Si alguna vez cambian los nombres/tipos de columna en Monday, o quieres
apuntar a otro board, corre `scripts/discover_schema.py <board_id>` (con tu
token como variable de entorno `MONDAY_API_TOKEN`) para ver los IDs
actuales de cada columna y actualízalos ahí.
