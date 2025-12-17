from typing import Dict, Any
from tools.google_forms_client import client
from mcp_instance import mcp


@mcp.tool()
def get_form(form_id: str) -> Dict[str, Any]:
    """
    Получить всю форму по её ID — metadata + элементы (questions/items).

    Args:
        form_id (str): Идентификатор формы в Google Forms.

    Returns:
        dict: Объект формы, содержащий её информацию, настройки, список вопросов (items) и пр.
    """
    return client.get_form(form_id)
