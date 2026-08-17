# Physical Topology & Endpoint Allocation

## 1. Physical Layout Overview
The physical infrastructure is distributed across floors with structured cabling terminating at floor access switches.

## 2. Endpoint Allocation Matrix (As-Built)

| Endpoint Hostname | Physical Location | Connected Switch | Switch Port | Access VLAN | IP Address |
| :--- | :--- | :--- | :--- | :--- | :--- |
| DEV-PC-01 | Floor 2 (Dev Team Area) | ACC-F2-01 | FastEthernet0/1 | VLAN 10 | 10.10.10.10/24 |
| HR-PC-01 | Floor 1 (HR Office) | ACC-F1-01 | FastEthernet0/2 | VLAN 30 | 10.10.30.10/24 |
| FIN-PC-01 | Floor 1 (Finance Office) | ACC-F1-01 | FastEthernet0/9 | VLAN 40 | 10.10.40.10/24 |
| QA-PC-01 | Floor 2 (QA Lab) | ACC-F2-01 | FastEthernet0/17 | VLAN 20 | 10.10.20.10/24 |
| GUEST-PC-01 | Floor 1 (Visitor Area) | ACC-F1-01 | FastEthernet0/21 | VLAN 90 | 10.10.90.100/24 |
| CCTV-CAM-01 | Floor 1 (Entrance) | ACC-F1-01 | FastEthernet0/19 | VLAN 80 | 10.10.80.11/24 |
| CCTV-CAM-02 | Floor 1 (Corridor) | ACC-F1-01 | FastEthernet0/20 | VLAN 80 | 10.10.80.12/24 |
| IP-PHONE-01 | Floor 1 (Admin Desk) | ACC-F1-01 | FastEthernet0/22 | VLAN 80 | 10.10.80.21/24 |

## 3. Switch Physical Placement
- **ACC-F1-01**: Floor 1 IDF Rack
- **ACC-F2-01**: Floor 2 IDF Rack
- **CORE-L3-01**: Floor 3 Server Room MDF Rack
