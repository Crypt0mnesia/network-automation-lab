"""
netmiko_collect.py

Сбор данных с Catalyst 2960 через Netmiko.
Сохраняет результат в JSON.
"""
from netmiko import ConnectHandler
from datetime import datetime
import json
import os

# Параметры устройства
DEVICE = {
    "device_type": "cisco_ios",
    "host": "10.100.20.10",
    "username": "ansible",
    "password": os.getenv("CISCO_PASSWORD"),
}

# Команды для сбора
COMMANDS = [
    "show version",
    "show ip interface brief",
    "show vlan brief",
    "show interfaces status",
]

def collect_facts(device, commands):
    """Подключается к устройству и собирает вывод команд."""
    with ConnectHandler(**device) as conn:
        hostname = conn.find_prompt().strip("#>")
        print(f"✅ Подключено к {hostname}")

        results = {
            "hostname": hostname,
            "collected_at": datetime.now().isoformat(),
            "commands": {},
        }

        for cmd in commands:
            print(f"   → Выполняю: {cmd}")
            output = conn.send_command(cmd)
            results["commands"][cmd] = output

        return results

def save_to_json(data, filename="output/facts.json"):
    """Сохраняет данные в JSON."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Сохранено в {filename}")

if __name__ == "__main__":
    print("🔍 Сбор данных с Catalyst 2960...")
    facts = collect_facts(DEVICE, COMMANDS)
    save_to_json(facts)
    print("✅ Готово")