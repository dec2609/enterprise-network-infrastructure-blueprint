# DESIGN REVIEW 2.5: ARCHITECTURE DECISION RECORDS (ADR)

**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** Engineering Architecture Analysis & Trade-Off Evaluation  
**Status:** **APPROVED & RECONCILED (v1.0 Baseline)**  
**Parent Specifications:** [`system_requirements.md`](./system_requirements.md) & [`business_context.md`](./business_context.md)  

---

## 2.5.1 Overview & Decision Context

This document captures the architectural evaluation, trade-off analysis, and formal Architecture Decision Records (ADRs) that define the foundational structure of the enterprise network for **ABC Software Solutions**.

The architectural selection is derived from the **21 System Requirements** (FR-01..05, SR-01..06, AR-01..03, SC-01..03, MG-01..04) and evaluated against Cisco Validated Design (CVD) principles for mid-sized campus environments.

---

## 2.5.2 Candidate Architecture Options

Three candidate topology models were evaluated against organizational scale (150 users across 3 physical office floors), operational complexity, and budgetary parameters:

* **Option A — Collapsed Core Architecture (2-Tier):** Combines Core and Distribution functions into a dual-switch Layer 3 platform with direct dual-homed LACP uplinks from Floor Access Switches.
* **Option B — Traditional 3-Tier Campus Architecture (Core / Distribution / Access):** Deploys dedicated Core switches, separate Distribution pairs, and Access switches on each floor.
* **Option C — Flat Layer-2 Network with Router-on-a-Stick (Legacy Model):** Operates an unsegmented or sub-interfaced Layer 2 switching fabric routing through a single perimeter router.

---

## 2.5.3 Weighted Decision Matrix

| Evaluation Criteria | Weight | Option A: Collapsed Core (2-Tier) | Option B: 3-Tier Campus | Option C: Router-on-a-Stick |
| :--- | :---: | :---: | :---: | :---: |
| **Cost & Hardware Footprint** | 25% | **4.5 / 5.0** (Optimal hardware count) | 2.0 / 5.0 (Excessive for 150 users) | 5.0 / 5.0 (Lowest initial Capex) |
| **L2/L3 Throughput & Latency** | 20% | **4.5 / 5.0** (Wirespeed SVI switching) | 5.0 / 5.0 (Maximum core capacity) | 1.5 / 5.0 (Severe trunk bottleneck) |
| **High Availability & Link Resiliency** | 20% | **4.0 / 5.0** (Dual LACP & STP redundancy) | 5.0 / 5.0 (Full multi-tier failover) | 1.0 / 5.0 (Multiple single points of failure) |
| **Security Segmentation & Policy Control** | 20% | **4.5 / 5.0** (Centralized SVI ACL filtering) | 4.5 / 5.0 (Granular distribution filtering) | 2.0 / 5.0 (Limited router CPU filtering) |
| **Operational & Maintenance Simplicity** | 15% | **4.8 / 5.0** (Streamlined SME management) | 2.5 / 5.0 (Complex routing protocols) | 3.0 / 5.0 (Difficult troubleshooting) |
| **Weighted Total Score** | **100%** | **4.45 / 5.00 (SELECTED)** | **3.70 / 5.00** | **2.55 / 5.00** |

---

## 2.5.4 Selected Architecture Statement

> **ARCHITECTURAL DECISION:** **Option A — Collapsed Core Architecture (2-Tier)** is formally selected as the enterprise network foundation for **ABC Software Solutions**.
> 
> **V1 IMPLEMENTATION BASELINE:** The selected architecture is implemented using a dual-core switching topology with **CORE-L3-01 operating as the active Layer 3 gateway** and **CORE-L3-02 providing Layer 2 redundancy**. Full Layer 3 gateway redundancy is intentionally deferred from Version 1.
> 
> **JUSTIFICATION:** The Collapsed Core model provides centralized Layer 3 routing, security policy enforcement, redundant access-layer uplinks, and a practical hardware footprint for a 150-user, three-floor SME environment. It avoids the additional hardware and operational complexity of a traditional three-tier campus architecture while preserving a clear migration path toward full Layer 3 gateway redundancy.
> 
> **V1 TRADE-OFF:** Version 1 prioritizes implementation simplicity and resource efficiency. As a result, failure of `CORE-L3-01` temporarily interrupts inter-VLAN routing because `CORE-L3-02` does not operate as an active Layer 3 gateway. This limitation is explicitly accepted within the V1 scope.
> 
> **FUTURE EVOLUTION:** Full Layer 3 gateway redundancy may be introduced in Version 2 through a first-hop redundancy mechanism such as HSRP or VRRP.

---

## 2.5.5 Formal Architecture Decision Records (ADRs)

| Decision ID | Domain | Architecture Decision Statement | Driven By (Requirements) | Engineering Rationale & Trade-Off Boundary |
| :---: | :--- | :--- | :---: | :--- |
| **DEC-01** | **Topology** | **Collapsed Core 2-Tier with Dual-Core Switching Infrastructure** | `SC-01`, `AR-01`, `AR-02` | Eliminates dedicated Distribution hardware and provides redundant core/access connectivity within the V1 resource scope. Full L3 gateway redundancy is deferred to V2. |
| **DEC-02** | **Segmentation** | **Hierarchical 802.1Q VLAN Subnetting (VLAN 10–90, 999)** | `FR-01`, `SR-01`, `SC-03` | Replaces flat L2 broadcast domains with 9 departmental VLANs and an isolated, unused Native VLAN 999 with zero SVI binding. |
| **DEC-03** | **Routing** | **Centralized Core SVI (Switched Virtual Interface) L3 Routing** | `FR-01`, `SR-01` | Provides centralized inter-VLAN routing and a consistent enforcement point for Layer 3 access-control policies without Router-on-a-Stick bottlenecks. |
| **DEC-04** | **L2 Hardening** | **Standardized Access Edge Defense (BPDU Guard, PortFast, Port-Security)** | `SR-04`, `SR-05`, `MG-01` | Mitigates STP manipulation, rogue DHCP servers, and unauthorized physical endpoint patching (Sticky MAC `maximum 1`, violation restrict). |
| **DEC-05** | **Link HA** | **LACP EtherChannel Dual-Uplinks (Access to Core)** | `AR-01`, `SC-01` | Bundles redundant physical uplinks into logical Port-Channels (`Po1..3`) and maintains connectivity when an individual member link fails. This provides link-level resilience but does not provide L3 gateway failover. |
| **DEC-06** | **Power Delivery** | **Access Layer Inline 802.3at PoE+ Provisioning** | `AR-03` | Delivers centralized inline power across designated ports for Wireless APs (`Fa0/21`), IP Phones (`Fa0/22`), and Surveillance CCTV (`Fa0/19-20`). |
| **DEC-07** | **Security Controls** | **Ingress SVI Extended Access Control Lists (ACLs)** | `FR-02`, `SR-02`, `SR-03` | Enforces granular traffic segregation (`ACL_DEV_IN`, `ACL_FIN_IN`, `ACL_HR_IN`) and complete lateral isolation for the untrusted Guest Zone (`ACL_GUEST_IN`). |

---

## 2.5.6 Requirement Coverage & Implementation Boundary

The selected architecture provides design coverage for all 21 System Requirements. However, **design coverage does not imply that every requirement is fully implemented and validated in Version 1**.

Implementation and validation status are tracked separately to preserve engineering traceability and explicitly document accepted limitations:

| Requirement Category | System Requirement ID | Architecture Decision Coverage | V1 Implementation Baseline | Validation Status (Phase 12) |
| :--- | :---: | :--- | :--- | :---: |
| **Functional (FR)** | `FR-01` | `DEC-02`, `DEC-03` | Centralized SVI Routing on `CORE-L3-01` | 🟢 **PASS** |
| | `FR-02` | `DEC-02`, `DEC-07` | Guest SVI 90 + Extended Ingress `ACL_GUEST_IN` | 🟢 **PASS** |
| | `FR-03` | `DEC-03` | DHCP Pools on `CORE-L3-01` (DNS `10.10.60.10`) | 🟢 **PASS** |
| | `FR-04` | `DEC-04`, `DEC-06` | AP Infrastructure Ports (`Fa0/21`) on Access Switches | 🟢 **PASS** |
| | `FR-05` | `DEC-02`, `DEC-04` | Management SVI Vlan70 (`10.10.70.10` / `.101–.103`) | 🟢 **PASS** |
| **Security (SR)** | `SR-01` | `DEC-02`, `DEC-03` | 802.1Q Subnet Logical Isolation across VLAN 10–90 | 🟢 **PASS** |
| | `SR-02` | `DEC-07` | Extended Ingress ACLs (`ACL_DEV_IN`, `ACL_FIN_IN`) | 🟢 **PASS** |
| | `SR-03` | `DEC-07` | RFC 1918 Lateral Isolation via `ACL_GUEST_IN` | 🟢 **PASS** |
| | `SR-04` | `DEC-04` | `ip dhcp snooping` with Trusted Uplinks (`Po1..3`) | 🟢 **PASS** |
| | `SR-05` | `DEC-04` | Rapid-PVST+ Loop Suppression & PortFast/BPDU Guard | 🟢 **PASS** |
| | `SR-06` | `DEC-02`, `DEC-04` | SSHv2 & VTY Access Control via Management VLAN 70 | 🟢 **PASS** |
| **Availability (AR)** | `AR-01` | `DEC-05` | Dual-Link LACP Active EtherChannels (`Po1`, `Po2`, `Po3`) | 🟢 **PASS** |
| | `AR-02` | `DEC-01` | **Partial:** Active-Passive L2 Core Pair (`CORE-L3-02` Standby). STP failover validated (<2s); L3 Gateway redundancy deferred to v2.0. | 🟡 **PARTIAL / Accepted Limitation** |
| | `AR-03` | `DEC-06` | 802.3at PoE+ Provisioning on Edge Interfaces | 🟢 **PASS** |
| **Scalability (SC)** | `SC-01` | `DEC-01`, `DEC-02` | Modular Collapsed Core Architecture | 🟢 **PASS** |
| | `SC-02` | `DEC-01`, `DEC-05` | Standardized Replicable 24-Port Access Node Templates | 🟢 **PASS** |
| | `SC-03` | `DEC-02` | Structured `/24` Addressing with Subnet Expansion Reserve | 🟢 **PASS** |
| **Manageability (MG)** | `MG-01` | `DEC-04` | Standardized, Version-Controlled Modular CLI Configs | 🟢 **PASS** |
| | `MG-02` | `DEC-02` | Deterministic Octet-to-VLAN IP Addressing Plan | 🟢 **PASS** |
| | `MG-03` | `DEC-01..07` | End-to-End Traceability verified through `CHANGE-001` | 🟢 **PASS** |
| | `MG-04` | `DEC-01` | Baseline Config Codebase Exported in `implementation/` | 🟢 **PASS** |

---

## 2.5.7 Architecture Transition & Chapter Scope Boundary

> **V1 SCOPE BOUNDARY:** The detailed design and validation artifacts in Chapter 3 and Chapter 4 represent the implemented Version 1 baseline. Full Layer 3 gateway redundancy is intentionally outside the V1 implementation scope and remains a documented V2 evolution path.
