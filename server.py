from mcp_instance import mcp
import sys


def main():
    print("🔧 Загружаем инструменты...", file=sys.stderr)
    try:
        from tools.list_forms import list_forms

        print("✅ list_forms загружен", file=sys.stderr)
    except Exception as e:
        print(f"❌ Ошибка импорта list_forms: {e}", file=sys.stderr)

    try:
        from tools.apply_questions_patch import apply_questions_patch

        print("✅ apply_questions_patch загружен", file=sys.stderr)
    except Exception as e:
        print(f"❌ Ошибка импорта apply_questions_patch: {e}", file=sys.stderr)

    try:
        from tools.close_form import close_form

        print("✅ close_form загружен", file=sys.stderr)
    except Exception as e:
        print(f"❌ Ошибка импорта close_form: {e}", file=sys.stderr)

    try:
        from tools.get_form import get_form

        print("✅ get_form загружен", file=sys.stderr)
    except Exception as e:
        print(f"❌ Ошибка импорта get_form: {e}", file=sys.stderr)

    try:
        from tools.upsert_form import upsert_form

        print("✅ upsert_form загружен", file=sys.stderr)
    except Exception as e:
        print(f"❌ Ошибка импорта upsert_form: {e}", file=sys.stderr)

    """Запуск MCP сервера с HTTP транспортом."""
    print("=" * 60, file=sys.stderr)
    print("🌐 ЗАПУСК MCP СЕРВЕРА", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    # print(f"🚀 MCP Server: http://{SERVER_HOST}:{SERVER_PORT}/mcp", file=sys.stderr)
    # print("=" * 60, file=sys.stderr)
    # mcp.run(
    #     transport="streamable-http",
    #     host=SERVER_HOST,
    #     port=SERVER_PORT,
    #     stateless_http=True,
    # )
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
