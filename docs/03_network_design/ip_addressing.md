# DESIGN REVIEW 3.3: ENTERPRISE IP ADDRESSING PLAN & GOVERNANCE POLICY
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** System Design & Implementation Phase (Chapter 3)  
**Document Focus:** Deterministic Addressing Strategy, Subnet Mapping, Static Registries & IP Governance Rules  
**Parent Reviews:** Design Review 3.1 (Logical Architecture) & Design Review 3.2 (Physical Topology)

---

## 3.3.1 Overview & Addressing Strategy

Design Review 3.3 defines the corporate-wide IP addressing plan for **ABC Software Solutions**. Rather than allocating arbitrary subnets, this strategy establishes a **Deterministic Addressing Scheme** derived directly from the business scale and asset counts established in Chapter 2 [cite: 1].

### **Core Supernet Selection: RFC 1918 Private Block `10.10.0.0/16`**
The enterprise adopts the `10.10.0.0/16` Private IPv4 block over traditional `192.168.0.0/16` address space [cite: 1].

```text
 ┌───────────────┬───────────────┬───────────────────┬───────────────────┐
 │ Octet 1 (10)  │ Octet 2 (10)  │  Octet 3 (VLAN)   │   Octet 4 (Host)  │
 ├───────────────┼───────────────┼───────────────────┼───────────────────┤
 │ Enterprise    │ Site / HQ     │ Logical Subnet ID │ Specific Host ID  │
 │ Private Net   │ Identifier    │ (e.g., 10 = Dev)  │ (e.g., .1 = GW)   │
 └───────────────┴───────────────┴───────────────────┴───────────────────┘
```

**Strategic Rationale:**
1. **Deterministic Readability:** An administrator can immediately deduce the functional VLAN and department of any host by inspecting its 3rd octet (e.g., `10.10.10.x` = VLAN 10 Development) [cite: 1].
2. **Growth Reservation:** Supports up to 255 discrete subnets with flexible VLSM masks while maintaining 65,534 host addresses for 5-10 year expansion [cite: 1].
3. **Summarization Efficiency:** All internal traffic can be summarized into a single route (`10.10.0.0/16`) at the Edge Firewall / Router boundary [cite: 1].

---

## 3.3.2 Enterprise Subnet & VLAN Mapping (VLSM Allocation)

Subnet masks are tailored to host counts derived from **Design Review 2.2 Asset Inventory** to prevent address waste while reserving growth headroom [cite: 1]:

| VLAN ID | Subnet Name | Functional Department | Mapped Assets (DR 2.2) | Subnet Mask | Default Gateway (Core SVI) | Usable IP Range | DHCP Dynamic Pool |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **10** | **Development** | Software Engineering | 80 Dev PCs (`AST-01`) | `/24` (`255.255.255.0`) | `10.10.10.1` | `10.10.10.1 - 254` | `10.10.10.100 - 254` |
| **20** | **Quality_Assurance** | QA Testing Lab | 20 QA PCs (`AST-02`) | `/24` (`255.255.255.0`) | `10.10.20.1` | `10.10.20.1 - 254` | `10.10.20.100 - 254` |
| **30** | **Human_Resources** | HR Department | 10 HR PCs (`AST-03`) | `/25` (`255.255.255.128`) | `10.10.30.1` | `10.10.30.1 - 126` | `10.10.30.51 - 126` |
| **40** | **Finance** | Finance & Payroll | 10 Finance PCs (`AST-04`) | `/25` (`255.255.255.128`) | `10.10.40.1` | `10.10.40.1 - 126` | `10.10.40.51 - 126` |
| **50** | **Executive_Mgmt** | Board & Executives | 10 Laptops (`AST-05`) | `/25` (`255.255.255.128`) | `10.10.50.1` | `10.10.50.1 - 126` | `10.10.50.51 - 126` |
| **60** | **Server_Zone** | MDF Server Room | Git, ERP (`AST-11/12`) | `/24` (`255.255.255.0`) | `10.10.60.1` | `10.10.60.1 - 254` | *None (All Static)* |
| **70** | **IT_Management** | Infrastructure Out-of-Band | Switches & Firewalls | `/24` (`255.255.255.0`) | `10.10.70.1` | `10.10.70.1 - 254` | *None (All Static)* |
| **80** | **VoIP_and_IoT** | Building Voice & CCTV | 20 Phones, 16 Cameras | `/24` (`255.255.255.0`) | `10.10.80.1` | `10.10.80.1 - 254` | `10.10.80.100 - 254` |
| **90** | **Guest_Zone** | Visitor Wi-Fi Lobby | 50 Visitors (`AST-13`) | `/24` (`255.255.255.0`) | `10.10.90.1` | `10.10.90.1 - 254` | `10.10.90.100 - 254` |

---

## 3.3.3 Intra-Subnet Address Allocation Policy

Inside every `/24` (or `/25`) department subnet, IP address assignment follows a mandatory standardized layout [cite: 1]:

```text
 Subnet IP Boundary (e.g., 10.10.10.0/24)
 ├── .1           ──► Default Gateway (Core Switch SVI Interface)
 ├── .2  - .20    ──► Network Infrastructure Static IPs (Switches, Firewalls)
 ├── .21 - .50    ──► Enterprise Servers & Domain Controllers (Static Only)
 ├── .51 - .99    ──► Network Printers, Static Workstations & Reserved Headroom
 └── .100 - .254  ──► Dynamic DHCP Pool (Auto-assigned to User Endpoints)
```

---

## 3.3.4 Static Address Reservation Registry

| Hostname | Device Category | VLAN ID | Static IP Address | Subnet Mask | Operational Purpose |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`CORE-L3-01-MGMT`** | Core L3 Switch Primary | 70 | `10.10.70.10` | `255.255.255.0` | Central SVI Management & SSH Interface [cite: 1] |
| **`CORE-L3-02-MGMT`** | Core L3 Switch Backup | 70 | `10.10.70.11` | `255.255.255.0` | Secondary Core SVI Management Interface [cite: 1] |
| **`ACC-F1-01-MGMT`** | Access Switch Floor 1 | 70 | `10.10.70.21` | `255.255.255.0` | Floor 1 Switch SSH Management Interface [cite: 1] |
| **`ACC-F2-01-MGMT`** | Access Switch Floor 2 | 70 | `10.10.70.22` | `255.255.255.0` | Floor 2 Switch SSH Management Interface [cite: 1] |
| **`ACC-F3-01-MGMT`** | Access Switch Floor 3 | 70 | `10.10.70.23` | `255.255.255.0` | Floor 3 Switch SSH Management Interface [cite: 1] |
| **`SRV-GIT-01`** | Application Server | 60 | `10.10.60.21` | `255.255.255.0` | Git Source Code & CI/CD Repository [cite: 1] |
| **`SRV-ERP-01`** | Application Server | 60 | `10.10.60.22` | `255.255.255.0` | ERP & Financial Accounting Database [cite: 1] |
| **`SRV-DC-01`** | Core Directory Server | 60 | `10.10.60.23` | `255.255.255.0` | Active Directory Domain Controller & DNS [cite: 1] |

---

## 3.3.5 IP Address Governance Policy (Standard Operating Procedure)

This policy governs the administrative lifecycle of all IP address assets within **ABC Software Solutions**:

1. **Rule 1 — Gateway Invariance:** The `.1` address of every subnet is strictly reserved for the Collapsed Core SVI Interface acting as the Layer 3 Default Gateway [cite: 1].
2. **Rule 2 — Mandatory DHCP Scope Isolation:** Static IP assignments on user endpoints are strictly prohibited within the dynamic DHCP scope (`.100` to `.254`) to prevent duplicate address conflicts [cite: 1].
3. **Rule 3 — Pre-Deployment Static Registry:** No server or network switch may be connected to the production network without prior registration in the `dr3_3_static_ip_reservations.csv` ledger [cite: 1].
4. **Rule 4 — In-Band Management Restriction:** Administrative management protocols (SSH/SNMP) are enabled exclusively on Management VLAN 70 SVI interfaces (`10.10.70.0/24`) [cite: 1].
5. **Rule 5 — Guest Domain Isolation:** Dynamic DHCP leases issued in Guest VLAN 90 (`10.10.90.0/24`) must only offer external public DNS resolvers (e.g., `8.8.8.8`) and must never expose internal domain suffixes [cite: 1].
6. **Rule 6 — Future Subnet Expansion:** Unassigned VLAN IDs 91 through 110 and subnets `10.10.91.0/24` to `10.10.110.0/24` are designated as the official growth buffer for future office expansion [cite: 1].

---

## 3.3.6 Transition Checklist to DR 3.4 (Layer-2 Design)

- [x] Supernet block `10.10.0.0/16` selected with explicit engineering rationale [cite: 1].
- [x] Subnets mapped to all 9 VLANs with non-overlapping IP boundaries [cite: 1].
- [x] Gateway convention (`.1`), Static Server ranges, and DHCP pools standardized [cite: 1].
- [x] Static IP reservation registry generated for all switches and core servers [cite: 1].
- [x] 1-page IP Address Governance Policy established [cite: 1].
- [x] IP Addressing Plan frozen and ready for Layer-2 VLAN & Trunking Design (DR 3.4) [cite: 1].
