from typing import Optional, Union

from flasgger import Swagger
from flask import Flask


def create_swagger(app: Flask,
                   title: str,
                   description: str,
                   version: Optional[Union[str, int]] = None,
                   host: Optional[str] = None,
                   show_ui: bool = True,
                   ui_route: str = '/api',
                   spec_route: str = '/api.json') -> Swagger:

    if version and not isinstance(version, str):
        version = str(version)

    template = _make_template(title=title, description=description, version=version, host=host)

    swagger_config: dict = Swagger.DEFAULT_CONFIG.copy()

    swagger_config['swagger_ui'] = show_ui
    swagger_config['specs_route'] = ui_route
    swagger_config['specs'][0]['route'] = spec_route

    swagger = Swagger(app, config=swagger_config, template=template)

    return swagger


def _make_template(title: str,
                   description: str,
                   version: Optional[str] = None,
                   host: Optional[str] = None,
                   **kwargs) -> dict:
    template = {
        "swagger": "2.0",
        "info": {
            "title": title,
            "description": description,
            "version": version
        },
        "schemes": [
            "http",
            "https"
        ]
    }
    if host:
        template.update({'host': host})

    template.update(kwargs)

    return template
