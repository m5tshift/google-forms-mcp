from tools.google_forms_client import client
from mcp_instance import mcp


@mcp.tool()
def close_form(form_id: str) -> dict:
    """
    Закрыть форму для новых ответов — остановить приём новых submissions.

    После вызова форма останется, её структура сохранится, но новые ответы не будут приниматься.

    Args:
        form_id (str): Идентификатор формы, которую нужно “закрыть”.

    Returns:
        dict: Результат API — обновлённые настройки формы (или ошибка, если форма не поддерживает закрытие).
    """
    return client.close_form_for_responses(form_id)
