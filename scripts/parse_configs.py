"""
parse_configs.py

Парсинг данных, собранных netmiko_collect.py.
Извлекает структурированную информацию из вывода Cisco IOS.
"""

import json
import re
import os


def parse_vlans(vlan_output):
    """Парсит вывод 'show vlan brief' в список VLAN."""
    vlans = []
    # Ищем строки вида: "100  LAB-USERS    active    Fa0/3"
    pattern = r"^(\d+)\s+(\S+)\s+(\S+)\s*(.*)$"
    for line in vlan_output.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            vlan_id, name, status, ports = match.groups()
            # Пропускаем заголовки и разделители
            if vlan_id.isdigit():
                vlans.append({
                    "id": int(vlan_id),
                    "name": name,
                    "status": status,
                    "ports": [p.strip() for p in ports.split(",") if p.strip()],
                })
    return vlans


def parse_interfaces(interface_output):
    """Парсит вывод 'show ip interface brief' в список интерфейсов."""
    interfaces = []
    # Ищем строки вида: "Vlan1    10.100.20.10    YES manual up    up"
    pattern = r"^(\S+)\s+(\S+)\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s*$"
    for line in interface_output.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            name, ip, status, protocol = match.groups()
            # Пропускаем заголовок
            if name.lower() == "interface":
                continue
            interfaces.append({
                "name": name,
                "ip": ip,
                "status": status,
                "protocol": protocol,
            })
    return interfaces


def parse_interface_status(status_output):
    """Парсит вывод 'show interfaces status' в список портов."""
    ports = []
    # Разбиваем по пробелам (2+ пробела = разделитель колонок)
    for line in status_output.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("port"):
            continue
        # Разбиваем по 2+ пробелам
        parts = re.split(r"\s{2,}", line)
        if len(parts) >= 5:
            port = parts[0].strip()
            # Если Name пустой — parts[1] это Status
            # Если Name есть — parts[1] это Name, parts[2] это Status
            if len(parts) == 6:
                # Есть Name
                _, name, status, vlan, duplex, speed_type = parts
            else:
                # Нет Name
                name = ""
                status = parts[1]
                vlan = parts[2]
                duplex = parts[3]
                speed_type = parts[4]

            ports.append({
                "port": port,
                "name": name,
                "status": status,
                "vlan": vlan,
                "duplex": duplex,
                "speed": speed_type.split()[0] if speed_type else "",
            })
    return ports


def load_facts(filename="output/facts.json"):
    """Загружает данные из JSON."""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_parsed(data, filename="output/parsed.json"):
    """Сохраняет распарсенные данные в JSON."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Сохранено в {filename}")


if __name__ == "__main__":
    print("🔍 Парсинг данных с Catalyst 2960...")

    # Загружаем собранные данные
    facts = load_facts()
    commands = facts["commands"]

    # Парсим каждый вывод
    parsed = {
        "hostname": facts["hostname"],
        "collected_at": facts["collected_at"],
        "vlans": parse_vlans(commands["show vlan brief"]),
        "interfaces": parse_interfaces(commands["show ip interface brief"]),
        "ports": parse_interface_status(commands["show interfaces status"]),
    }

    # Выводим результат
    print(f"\n📋 VLANs: {len(parsed['vlans'])}")
    for vlan in parsed["vlans"]:
        print(f"   VLAN {vlan['id']}: {vlan['name']} — {vlan['status']}")

    print(f"\n🔌 Interfaces: {len(parsed['interfaces'])}")
    for iface in parsed["interfaces"]:
        print(f"   {iface['name']}: {iface['ip']} — {iface['status']}/{iface['protocol']}")

    print(f"\n🔗 Ports: {len(parsed['ports'])}")
    for port in parsed["ports"]:
        print(f"   {port['port']}: {port['status']} (VLAN {port['vlan']})")

    # Сохраняем
    save_parsed(parsed)
    print("\n✅ Готово")