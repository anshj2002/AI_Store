from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

PROMPTS_DIR = Path(__file__).parent / "prompts"

_env = Environment(
    loader=FileSystemLoader(str(PROMPTS_DIR)),
    autoescape=select_autoescape(disabled_extensions=("md", "j2"))
)

def render_template(name: str, **kwargs) -> str:
    tmpl = _env.get_template(name)
    return tmpl.render(**kwargs)
