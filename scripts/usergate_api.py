"""
usergate_api.py

Работа с UserGate NGFW через XML-RPC API.
Получает список правил firewall.
"""

import xmlrpc.client
import json
import os
from datetime import datetime

USERGATE_HOST = "10.100.20.1"
USERGATE_PORT = 4040
API_USER = "api_admin"
API_PASSWORD = os.getenv("USERGATE_API_PASSWORD")


def login(server, username, password):
    """Авторизация, возвращает токен."""
    result = server.v2.core.login(username, password, {})
    return result["auth_token"]


def get_firewall_rules(server, token):
    """Получает список правил firewall."""
    try:
        result = server.v1.firewall.rules.list(token, 0, 100, {})
        return result
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return []


def logout(server, token):
    """Завершает сессию."""
    try:
        server.v2.core.logout(token)
    except Exception as e:
        print(f"⚠️ Logout: {e}")


def main():
    print("🔍 Подключение к UserGate API...")

    server = xmlrpc.client.ServerProxy(
        f"http://{USERGATE_HOST}:{USERGATE_PORT}/rpc",
        verbose=False,
    )

    # Авторизация
    try:
        token = login(server, API_USER, API_PASSWORD)
        print(f"✅ Авторизация OK (токен: {token[:8]}...)")
    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
        return

    # Получение правил firewall
    print("   → Получение правил firewall...")
    rules = get_firewall_rules(server, token)

    if isinstance(rules, dict) and "items" in rules:
        rule_count = len(rules["items"])
        print(f"      Правил: {rule_count}")
        for rule in rules["items"]:
            name = rule.get("name", "N/A")
            action = rule.get("action", "N/A")
            print(f"        - {name} ({action})")
    else:
        print(f"      Правил: N/A")

    logout(server, token)
    print("✅ Сессия завершена")

    # Сохранение
    os.makedirs("output", exist_ok=True)
    filename = "output/usergate_data.json"
    data = {
        "collected_at": datetime.now().isoformat(),
        "host": USERGATE_HOST,
        "firewall_rules": rules,
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Сохранено в {filename}")


if __name__ == "__main__":
    main()