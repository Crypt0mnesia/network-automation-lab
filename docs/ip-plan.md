# IP Plan

## Home Network

| Device | IP | Notes |
|---|---|---|
| Router | 10.1.10.2 | Home gateway |
| UserGate WAN | 10.1.10.50/24 | port0, Untrusted |

## Lab Network

| Device | IP | Notes |
|---|---|---|
| UserGate LAN | 10.100.20.1/24 | port1, Trusted |
| Catalyst 2960 | 10.100.20.10/24 | VLAN 1, SSH |
| DHCP pool | 10.100.20.100-200 | For clients |
| MacBook | 10.100.20.x | Ansible control node |

## VLANs

| VLAN | Name | Purpose |
|---|---|---|
| 1 | default | Management |
| 100 | LAB-USERS | User access |
| 200 | LAB-SERVERS | Server access |