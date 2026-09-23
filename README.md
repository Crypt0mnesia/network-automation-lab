# Network Automation Lab

Lab built on real hardware: UserGate NGFW + Cisco Catalyst 2960.

## Architecture

- **UserGate NGFW**: WAN `10.1.10.50/24`, LAN `10.100.20.1/24`, DHCP, NAT, firewall
- **Catalyst 2960**: L2 switch, VLAN 1, SSH `10.100.20.10`
- **Ansible**: control node on macOS
## Topology

```mermaid
graph TB
    Internet([🌐 Internet])
    
    Router[Router<br/>10.1.10.2]
    CG[Catalyst 3560-CG<br/>Home switch]
    
    subgraph UG["UserGate D200/500 (NGFW)"]
        WAN[port0 WAN<br/>10.1.10.50/24<br/>Zone: Untrusted]
        LAN[port1 LAN<br/>10.100.20.1/24<br/>Zone: Trusted]
        UG_SVC[DHCP: 10.100.20.100-200<br/>NAT: Trusted → Untrusted<br/>Firewall: Allow Trusted → Untrusted]
    end
    
    SW[Cisco Catalyst 2960<br/>VLAN 1<br/>IP: 10.100.20.10<br/>SSH: ansible]
    
    Mac[💻 MacBook<br/>10.100.20.x<br/>Ansible Control Node<br/>- 4 playbooks<br/>- Ansible Vault]
    
    Internet --> Router
    Router --> CG
    CG --> WAN
    WAN --- UG_SVC
    UG_SVC --- LAN
    LAN --> SW
    SW --> Mac
```
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