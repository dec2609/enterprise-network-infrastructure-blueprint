# REQUIREMENTS TO ARCHITECTURE MAPPING SPECIFICATION

**Document ID:** MAP-DOC-001  
**Project:** Enterprise Network Infrastructure Blueprint  
**Status:** **APPROVED & RECONCILED (v1.0)**  
**Parent Specifications:** [`system_requirements.md`](./system_requirements.md) & [`business_context.md`](./business_context.md)  

---

## 1. Overview & Traceability Logic

This document establishes the bidirectional mapping bridge between the formal System Requirements (FR, SR, AR, SC, MG) specified in [`system_requirements.md`](./system_requirements.md) and the architectural implementation components (Trust Zones, VLAN Subnets, Switching Nodes, and Policy Enforcement Points).

```text
[ System Requirements (FR / SR / AR / SC / MG) ]
                       │
                       ▼ (Mapped to)
[ Trust Zones, VLAN Subnets, L2/L3 Nodes & PEPs ]
                       │
                       ▼ (Implemented in)
[ Cisco Catalyst 3650/2960, ASA 5506-X, ISR 4331 ]
```

---

## 2. System Requirements to Architecture Mapping Matrix

### 2.1 Functional Requirements Mapping (FR)

| REQ ID | Canonical Requirement Title | Target Zone / Domain | Target Subnet / Segment | Architecture Implementation & Enforcement Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Inter-Departmental Communication | Zones 1–5 (DEV, QA, HR, FIN, EXEC) | VLANs 10–50 (10.10.10.0/24 to 10.10.50.0/24) | Centralized SVI routing on CORE-L3-01; Inter-VLAN forwarding controlled via SVI Extended Ingress ACLs. |
| **FR-02** | Guest Internet Egress | Zone 8 (Untrusted Guest) | VLAN 90 (10.10.90.0/24) | Isolated SVI Vlan90; Filtered by ACL_GUEST_IN to allow DNS/DHCP and Internet egress while blocking 10.10.0.0/16. |
| **FR-03** | Automated IP Allocation (DHCP) | All Production User & Service Zones | VLANs 10–60, 80, 90 | Centralized DHCP Server pools hosted on CORE-L3-01 (10.10.60.10 / SVI helper addresses). |
| **FR-04** | Wireless Mobility Support | Zone 7 (WLAN Infrastructure) | VLAN 90 (Guest AP) & Corporate SSIDs | Dedicated Access Switch ports (Fa0/21) provisioned for 802.11ac Access Points across all 3 floors. |
| **FR-05** | Secure Remote Administration | Zone 2 (Management & Transit) | VLAN 70 (10.10.70.0/24) | SVI Vlan70 (10.10.70.10 Core, 10.10.70.101–103 Access); SSHv2 and SNMPv3 access restricted to authorized hosts. |

---

### 2.2 Security Requirements Mapping (SR)

| REQ ID | Canonical Requirement Title | Target Zone / Boundary | Architecture Enforcement Mechanism | Policy Enforcement Point (PEP) |
| :--- | :--- | :--- | :--- | :--- |
| **SR-01** | Subnet Logical Isolation | Access Layer Boundaries | 802.1Q VLAN separation across access switches (ACC-F1-01, ACC-F2-01, ACC-F3-01). | Access Switch ASIC / VLAN Database |
| **SR-02** | Confidential Asset Protection | High-Value Server Farm (Zone 1) | Ingress SVI Extended ACLs (ACL_DEV_IN, ACL_FIN_IN) restricting server access to authorized ports (22, 443, 1433). | CORE-L3-01 (SVI 10, SVI 40) |
| **SR-03** | Guest Untrusted Isolation | Perimeter / Lateral Boundary | ACL_GUEST_IN denying all RFC 1918 corporate IP blocks (10.10.0.0/16). | CORE-L3-01 (SVI 90 Ingress) |
| **SR-04** | Rogue DHCP Mitigation | Access Layer Host Ports | Globally enabled `ip dhcp snooping`; Trunk uplinks set to trusted, all host access ports untrusted. | ACC-F1-01, ACC-F2-01, ACC-F3-01 |
| **SR-05** | Layer 2 Loop Suppression | Entire Campus Switching Fabric | `spanning-tree mode rapid-pvst`; Root Bridge hardcoded (CORE-L3-01 Primary, CORE-L3-02 Secondary); BPDU Guard on edge. | All Core & Access Switches |
| **SR-06** | Control Plane Hardening | Infrastructure Management Plane | Management SVI restricted to VLAN 70; VTY lines configured with `transport input ssh` and execution timeouts. | CORE-L3-01, CORE-L3-02, Access Switches |

---

### 2.3 Availability Requirements Mapping (AR)

| REQ ID | Canonical Requirement Title | Target Layer / Link | Architecture Implementation & Resiliency Mechanism |
| :--- | :--- | :--- | :--- |
| **AR-01** | Uplink Redundancy & Load Sharing | Core-to-Access Uplinks | Dual-link IEEE 802.3ad LACP EtherChannels (Port-channel1..3) bundled via Core Gi1/0/1-6 to Access Fa0/23-24. |
| **AR-02** | Spanning-Tree & Path Redundancy | Inter-Core Backbone & Access Uplinks | Dual redundant Dot1Q trunks (Gi1/0/23-24) running Rapid-PVST+ with sub-2-second failover (Altn BLK &rarr; Root FWD).<br><br>*(Accepted v1.0 Limitation: Active-Passive L2 core model; L3 SVI gateway redundancy deferred to v2.0).* |
| **AR-03** | Inline Power Delivery (PoE/PoE+) | Edge Endpoint Attachments | Standardized 802.3at PoE capability on designated switch ports for Surveillance Cameras (Fa0/19-20), APs (Fa0/21), and IP Phones (Fa0/22). |

---

### 2.4 Scalability & Manageability Requirements Mapping (SC & MG)

| REQ ID | Canonical Requirement Title | Target Scope | Architecture Implementation Mechanism |
| :--- | :--- | :--- | :--- |
| **SC-01** | Modular Subnet Expansion | Core Routing Backbone | Hierarchical /24 addressing architecture allowing new VLAN SVIs without redesigning core routing logic. |
| **SC-02** | Floor Density Replication | Physical Access Layer | Standardized 24-port switch template (ACC-F*-01) enabling plug-and-play addition of future office floors. |
| **SC-03** | IP Capacity Reservation | Enterprise Address Block | 10.10.0.0/16 master allocation reserving blocks 10.10.100.0/24 through 10.10.254.0/24 for organizational growth. |
| **MG-01** | Standardized Config Codebases | All 7 Network Nodes | Modular, version-controlled CLI configurations with explicit port labeling and interface descriptions. |
| **MG-02** | Deterministic Addressing Scheme | Enterprise Infrastructure | Structured IP mapping where the 3rd octet matches the VLAN ID (e.g., VLAN 30 &rarr; 10.10.30.0/24). |
| **MG-03** | Logical-to-Physical Traceability | As-Built Records & Diagrams | Maintained across 5 formal vector architecture views (.drawio.svg) and verified against CHANGE-001. |
| **MG-04** | Disaster Recovery & Config Backups | Repository Archive | Baseline running configurations exported and archived in `implementation/configs/` for rapid bare-metal recovery. |

---

## 3. Policy Enforcement Point (PEP) Summary

```text
                                 [ WAN / INTERNET ]
                                         │
                                         ▼
                            [ RTR-EDGE-01 (ISR 4331) ]
                                         │
                                         ▼ (Outside Transit 192.168.100.0/30)
                            [ FW-EDGE-01 (ASA 5506-X) ]
                            • Perimeter Stateful Inspection
                            • Dynamic NAT Overload (PAT)
                                         │
                                         ▼ (VLAN 70 Transit 10.10.70.0/24)
                            [ CORE-L3-01 (Catalyst 3650) ]
                            • Centralized L3 SVI Routing Engine
                            • Extended Ingress ACL PEP (ACL_DEV_IN, ACL_FIN_IN, ACL_GUEST_IN)
                            • Rapid-PVST+ Primary Root Bridge (Priority 4096)
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 ▼ (Po1 - LACP)          ▼ (Po2 - LACP)          ▼ (Po3 - LACP)
         [ ACC-F1-01 (Floor 1) ] [ ACC-F2-01 (Floor 2) ] [ ACC-F3-01 (Floor 3) ]
         • BPDU Guard / PortFast • BPDU Guard / PortFast • BPDU Guard / PortFast
         • DHCP Snooping         • DHCP Snooping         • DHCP Snooping
         • Sticky Port Security  • CHANGE-001 Anchor     • Sticky Port Security
         • Endpoints: HR, FIN    • Endpoints: DEV, QA    • Endpoints: EXEC, SRV
```

* **Perimeter & NAT PEP:** FW-EDGE-01 (Cisco ASA 5506-X) enforcing stateful egress security policies.
* **Centralized L3 Routing & Traffic Filtering PEP:** CORE-L3-01 (Catalyst 3650) enforcing SVI Extended ACL policy boundaries and default routing.
* **Layer 2 Edge Hardening PEPs:** Access Switches (ACC-F1-01, ACC-F2-01, ACC-F3-01) enforcing PortFast, BPDU Guard, DHCP Snooping, and Sticky Port-Security.
