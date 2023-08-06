from typing import Any, Dict, Optional


def make_app_info(app_name: str,
                  app_version: Optional[str]) -> Dict[str, Any]:
    payload = dict(
        name=app_name,
        version=app_version,
    )
    return payload
