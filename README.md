# Network Automation Lab

Lab built on real hardware: UserGate NGFW + Cisco Catalyst 2960.

## Architecture

- **UserGate NGFW**: WAN `10.1.10.50/24`, LAN `10.100.20.1/24`, DHCP, NAT, firewall
- **Catalyst 2960**: L2 switch, VLAN 1, SSH `10.100.20.10`
- **Ansible**: control node on macOS

## Tech Stack

- Ansible 2.21.4
- `cisco.ios` collection
- Python 3.13 (venv)
- `paramiko 3.5.1` (for legacy SSH)

## Playbooks

| Playbook | Description |
|---|---|
| `gather_facts.yml` | Collect device info from Catalyst 2960 |
| `backup_config.yml` | Save running-config with timestamp |
| `configure_vlan.yml` | Create VLANs 100 and 200 |
| `configure_port_security.yml` | Configure port-security on access ports |

## Legacy SSH Support

For old Cisco IOS (12.2), we use `paramiko 3.5.1` with explicit KEX algorithms in `~/.ssh/config`. This is more reliable than `ansible_legacy_ssh=true`.

## Security Practices

- Passwords stored in encrypted Ansible Vault (`group_vars/switches/vault.yml`)
- Backups excluded from Git via `.gitignore` (industry best practice)
- No secrets in plaintext anywhere in the repository

## How to Run

```bash
source ~/ansible-venv/bin/activate
ansible-playbook -i inventory.ini playbooks/gather_facts.yml --ask-vault-pass
```