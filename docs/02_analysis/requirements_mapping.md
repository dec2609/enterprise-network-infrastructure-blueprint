# REQUIREMENTS TO ARCHITECTURE MAPPING SPECIFICATION

**Document ID:** MAP-DOC-001  
**Project:** Enterprise Network Infrastructure Blueprint  
**Status:** **APPROVED & FROZEN**

---

## 1. Overview & Traceability Logic
This document establishes the direct mapping bridge between the System Requirements (FR, SR, AR, MG) defined in [`system_requirements.md`](./system_requirements.md) and the architectural components (Trust Zones, VLANs, Devices, Policy Enforcement Points).

---

## 2. Requirements-to-Zone Traceability Matrix

| Requirement ID | Requirement Category | Target Trust Zone | Target Subnet / VLAN | Architecture Enforcement Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Dev Workstation Access | Zone 1 (DEV) | VLAN 10 (`10.10.10.0/24`) | L2 Access Port allocation on `ACC-F2-01`, Gateway on Core SVI 10. |
| **FR-02** | QA Testbed Access | Zone 2 (QA) | VLAN 20 (`10.10.20.0/24`) | L2 Access Port allocation on `ACC-F2-01`, Gateway on Core SVI 20. |
| **FR-03** | HR Management Access | Zone 3 (HR) | VLAN 30 (`10.10.30.0/24`) | L2 Access Port allocation on `ACC-F1-01`, Gateway on Core SVI 30. |
| **FR-04** | Finance Operations Access | Zone 4 (FIN) | VLAN 40 (`10.10.40.0/24`) | L2 Access Port allocation on `ACC-F1-01`, Gateway on Core SVI 40. |
| **FR-05** | Executive Suite Access | Zone 5 (EXEC) | VLAN 50 (`10.10.50.0/24`) | L2 Access Port allocation on `ACC-F3-01`, Gateway on Core SVI 50. |
| **FR-06** | Infrastructure Services | Zone 6 (SERVER) | VLAN 60 (`10.10.60.0/24`) | Centralized Server Zone connected to `ACC-F3-01` & Core SVI 60. |
| **FR-07** | Guest Isolation | Zone 9 (GUEST) | VLAN 90 (`10.10.90.0/24`) | Isolated Guest SVI Vlan90; Extended ACL `ACL_GUEST_IN` blocks internal LAN. |
| **SR-01** | Inter-Zone ACL Filtering | All Zones | VLANs 10–90 | Extended ACLs (`ACL_DEV_IN`, `ACL_FIN_IN`, `ACL_GUEST_IN`) applied on SVI. |
| **SR-02** | Layer 2 Edge Protection | Edge Ports | Access Switches | `spanning-tree bpduguard enable` + `portfast` on all user-facing ports. |
| **SR-03** | Rogue DHCP Mitigation | Access Layer | All Access Switches | `ip dhcp snooping` enabled; Trusted ports explicitly bound to Uplinks. |
| **AR-01** | Uplink Redundancy | Core-Access Trunks| All Switches | LACP Active EtherChannels (`Port-channel1`) using dual physical links. |
| **AR-02** | Spanning-Tree Convergence| L2 Loop Protection| Entire Topology | `spanning-tree mode rapid-pvst` with hardcoded Root Primary/Secondary. |

---

## 3. Policy Enforcement Point (PEP) Assignment

* **Primary L3 PEP:** `CORE-L3-01` (Centralized SVI Gateway + Extended ACL Policy Objects).
* **Primary L2 PEP:** Access Switches (`ACC-F1-01`, `ACC-F2-01`, `ACC-F3-01`) enforcing Port Security, BPDU Guard, and DHCP Snooping.
* **Egress Gateway PEP:** Edge Firewall (`FW-EDGE-01`) enforcing Internet Access Policies and NAT Overload.