from typing import List, Dict, Any
from tools.google_forms_client import client
from mcp_instance import mcp


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
