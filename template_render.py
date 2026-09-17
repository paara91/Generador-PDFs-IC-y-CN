import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
_env = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    autoescape=select_autoescape(enabled_extensions=("jinja",)),
)


def render_idea_chart_html(context: dict) -> str:
    template = _env.get_template("idea_chart.html.jinja")
    return template.render(**context)


def render_caso_negocio_html(context: dict) -> str:
    template = _env.get_template("caso_negocio.html.jinja")
    return template.render(**context)
