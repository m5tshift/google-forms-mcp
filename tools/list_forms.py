from typing import List, Dict, Any
from tools.google_forms_client import client
from mcp_instance import mcp


@mcp.tool()
def list_forms() -> List[Dict[str, Any]]:
    """
    Получить список всех форм пользователя через Google Drive.

    Возвращает базовую информацию — id, name — для каждой формы, доступной учётной записи.
    После этого по ID можно вызвать get_form, чтобы получить детали.

    Returns:
        list of dict: Список форм — каждый dict содержит минимум 'id' и 'name'.
    """
    return client.list_forms()
