import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class TemplateManager:
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(__file__).parent / template_dir
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir), trim_blocks=True, lstrip_blocks=True
        )

        # Add custom JSON filter
        self.env.filters["tojson"] = lambda value, indent=None: json.dumps(
            value, indent=indent, ensure_ascii=False
        )

    def render_python(
        self, name: str, readme: str | None = None, experiments: list | None = None, cv: dict | None = None
    ) -> str:
        """Render Python code for experiment set creation"""
        if cv:
            template = self.env.get_template("experiment_set_cv.py.j2")
            return template.render(name=name, readme=readme, cv=cv)
        else:
            template = self.env.get_template("experiment_set.py.j2")
            return template.render(name=name, readme=readme, experiments=experiments)

    def render_curl(
        self, name: str, readme: str | None = None, experiments: list | None = None, cv: dict | None = None
    ) -> str:
        """Render cURL command for experiment set creation"""
        if cv:
            template = self.env.get_template("experiment_set_cv.sh.j2")
            return template.render(name=name, readme=readme, cv=cv)
        else:
            template = self.env.get_template("experiment_set.sh.j2")
            return template.render(name=name, readme=readme, experiments=experiments)
