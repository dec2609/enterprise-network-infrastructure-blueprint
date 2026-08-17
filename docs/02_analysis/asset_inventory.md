# DESIGN REVIEW 2.2: ASSET INVENTORY & TRUST ZONES
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** Engineering Design Phase (Top-Down Asset Analysis)  
**Parent Review:** Design Review 2.1 (Business Context & System Requirements)

---

## 2.2.1 Asset Classification

Business assets for **ABC Software Solutions** are categorized into 6 core technical domains:

1. **People & Roles:** Internal Employees (150) and External Visitors/Contractors (50).
2. **Endpoints:** Developer PCs, QA PCs, HR Workstations, Finance Workstations, Executive Laptops, IP Phones.
3. **Infrastructure:** Collapsed Core L3 Switches, Floor Access Switches, Enterprise Wireless Access Points.
4. **Servers & Applications:** Git Repository & CI/CD Build Servers, ERP & Accounting Servers, Core Domain Services.
5. **IoT & Security:** CCTV Surveillance Cameras, Door Access Controllers.
6. **External & Guest:** Visitor Personal Laptops, Mobile Devices.

---

## 2.2.2 Asset Inventory Table

| Asset ID | Asset Name | Category | Qty | Owner | Location | Criticality | Network Dependency |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **AST-01** | Software Developer PCs | Endpoints | 80 | Dev Team | Floor 2 | High | High Bandwidth, Subnet Isolation |
| **AST-02** | Quality Assurance PCs | Endpoints | 20 | QA Team | Floor 2 | Medium | Staging Access, Subnet Isolation |
| **AST-03** | HR Workstations | Endpoints | 10 | HR Dept | Floor 1 | High | Secure Access, Restricted Subnet |
| **AST-04** | Finance Workstations | Endpoints | 10 | Finance Dept | Floor 1 | Critical | Strict ACLs, Encrypted Gateway |
| **AST-05** | Executive Laptops | Endpoints | 10 | Management | Floor 3 | High | Privileged Access, Secure Wi-Fi |
| **AST-06** | Floor Access Switches | Infrastructure | 3 | IT Infra | Floors 1-3 | Critical | PoE+ Support, Trunking, Port Security |
| **AST-07** | Collapsed Core L3 Switches | Infrastructure | 2 | IT Infra | Floor 3 Server Room | Critical | High-Density Routing, Redundancy |
| **AST-08** | Enterprise Wireless APs | Infrastructure | 6 | IT Infra | Floors 1-3 | High | Continuous PoE, Multi-SSID VLAN Mapping |
| **AST-09** | CCTV Security Cameras | IoT & Security | 16 | Physical Security | Floors 1-3 | Medium | Continuous PoE, Isolated Video Subnet |
| **AST-10** | Corporate IP Phones | Endpoints | 20 | All Depts | Floors 1-3 | Medium | PoE Power, Voice QoS, Dedicated VLAN |
| **AST-11** | Git Repo & CI/CD Server | Servers | 2 | DevOps | Floor 3 Server Room | Critical | High Bandwidth, Dev Access Only |
| **AST-12** | ERP & Accounting Server | Servers | 1 | Finance / IT | Floor 3 Server Room | Critical | Strict ACL Control, Finance Access Only |
| **AST-13** | Guest Devices | External | 50 | Visitors | Floor 1 Reception | Low | Internet-only Access, Complete Isolation |

---

## 2.2.3 Criticality & Business Impact Assessment

* **Critical (RTO = 0, High Business Loss):** AST-04 (Finance), AST-06/07 (Network Backbone), AST-11 (Git Repo), AST-12 (ERP Server). A failure in these assets directly halts business operations or exposes financial records.
* **High (RTO < 2h, Moderate Loss):** AST-01 (Dev PCs), AST-03 (HR PCs), AST-05 (Exec Laptops), AST-08 (Wireless APs).
* **Medium (RTO < 8h, Low Loss):** AST-02 (QA PCs), AST-09 (CCTV), AST-10 (IP Phones).
* **Low (Best Effort):** AST-13 (Guest Devices).

---

## 2.2.4 Network Dependency Analysis

```text
Business Asset ──► Technical Need ──► Required Network Capability
-----------------------------------------------------------------------
Camera / APs   ──► Inline Power   ──► PoE / PoE+ 802.3at Support (REQ-03)
Finance / HR   ──► Data Isolation ──► Dedicated VLANs + Inter-VLAN ACLs (REQ-02)
Core Backbone  ──► Zero SPOF      ──► Dual Link Trunking & Redundancy (REQ-01)
Guest Wi-Fi    ──► Threat Boundary──► L2 Isolation & Port Security (REQ-04)
```

---

## 2.2.5 Design Implications (Top-Down Engineering Inferences)

1. **Observation 1:** High concentration of PoE endpoints (16 Cameras + 6 APs + 20 IP Phones = 42 PoE devices).  
   * **Design Implication:** Access Switches must be 802.3at PoE+ capable with at least 370W power budget per switch.
2. **Observation 2:** Finance (AST-04) and HR (AST-03) handle highly confidential PII and accounting data.  
   * **Design Implication:** Require strict logical boundary enforcement via Layer 3 Access Control Lists (ACLs) on the Collapsed Core.
3. **Observation 3:** 80 Developers (AST-01) continuously pull/push large codebase artifacts to Git Repos (AST-11).  
   * **Design Implication:** Gigabit Ethernet (1000BASE-T) links required at Access layer, with 10Gbps/LACP uplinks to Core.

---

## 2.2.6 Asset-to-Requirement Traceability Matrix

| Asset Group | Primary Risk / Threat | Mapped System Requirement | Enforced Design Control |
| :--- | :--- | :--- | :--- |
| **Workstations (AST-01 to 05)** | Lateral malware spread & data sniffing | **REQ-02 (Logical Segmentation)** | Department VLANs (VLAN 10, 20, 30, 40, 50) |
| **Switches (AST-06, 07)** | Network outage & bottlenecking | **REQ-01 (Hierarchical Topology)** | Collapsed Core 2-Tier with Dual Trunks |
| **PoE Devices (AST-08 to 10)** | Power disruption & voice quality degradation | **REQ-03 (Resiliency & PoE)** | 802.3at PoE+ Switches & Voice QoS |
| **Guest Access (AST-13)** | Rogue DHCP, LAN intrusion, sniffing | **REQ-02, REQ-04 (Edge Security)** | Guest Isolation VLAN 90 & DHCP Snooping |
