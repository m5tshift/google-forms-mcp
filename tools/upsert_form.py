from typing import Optional, Dict, Any
from tools.google_forms_client import client
from mcp_instance import mcp


@mcp.tool()
def upsert_form(
    form_id: Optional[str], title: str, description: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Создать новую форму или обновить существующую (по form_id).

    Если form_id не указан (None) — создаётся новая форма с указанным title (и, при необходимости, description).
    Если form_id указан — выполняется update: изменяются title и/или description.

    Args:
        form_id (str | None): ID формы для обновления, либо None для создания новой.
        title (str): Заголовок (title) формы.
        description (str, optional): Описание формы. По умолчанию "".

    Returns:
        dict: Результат API — информация о форме (или обновлённая metadata).
    """
    if form_id:
        body = {
            "requests": [
                {
                    "updateFormInfo": {
                        "info": {"title": title, "description": description},
                        "updateMask": "title,description",
                    }
                }
            ]
        }
        return client.batch_update(form_id, [body["requests"][0]])
    else:
        return client.create_form(title=title, description=description)
