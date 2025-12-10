from fastmcp import FastMCP
from google_forms_client import GoogleFormsClient
from typing import Optional, List, Dict, Any

client = GoogleFormsClient()
mcp = FastMCP(name="google-forms-mcp")


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


@mcp.tool()
def apply_questions_patch(
    form_id: str, requests: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Применить набор операций (patch) к вопросам/элементам формы через batchUpdate.

    Позволяет:
      - add / create вопрос / элемент (createItem),
      - удалять элемент (deleteItem),
      - перемещать (moveItem),
      - изменять существующие элементы (updateItem),
      - любые комбинации одновременно — все операции будут применены в одной транзакции.

    Args:
        form_id (str): ID формы.
        requests (List[dict]): Список операций в формате Google Forms API (каждый dict — одна sub-request).

    Returns:
        dict: Ответ API — может содержать обновлённую форму + детали по каждому запросу (itemId, ошибки, etc).
    """
    return client.batch_update(form_id, requests)


if __name__ == "__main__":
    mcp.run(transport="stdio")  # или transport="http" + host/port, если нужен HTTP
