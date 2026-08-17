# DESIGN REVIEW 2.5: ARCHITECTURE DECISION RECORD (ADR)
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** Engineering Design Phase (Architecture Decision & Solution Selection)  
**Parent Review:** Design Review 2.4 (System Requirements Specification)  
**Output Milestone:** Completion of Chapter 2 (Design Analysis Phase)

---

## 2.5.1 Candidate Architectures

To address the 21 System Requirements established in **Design Review 2.4**, three candidate topologies were formally evaluated:

1. **Option A — Collapsed Core Architecture (2-Tier):** Merges the Core and Distribution functions into a redundant pair of Layer 3 switches. Access switches connect directly to this core pair via dual-homed trunks.
2. **Option B — Traditional 3-Tier Campus Architecture:** Implements distinct Access, Distribution, and Core layers with dedicated switch hardware pairs at each tier.
3. **Option C — Routed Access Layer Architecture:** Pushes Layer 3 routing boundaries down to the Access Switches, replacing Layer 2 trunks with routed IP links.

---

## 2.5.2 Evaluation Criteria & Weight Allocation

Candidates were scored against 5 weighted engineering criteria derived from business scale and requirements:

* **Security Boundary Enforcement (25% Weight - Critical):** Ability to centralize ACLs, isolate subnets, and enforce Guest boundaries (`SR-01` to `SR-06`).
* **High Availability & Resiliency (20% Weight - Critical):** Elimination of single points of failure and rapid fault recovery (`AR-01`, `AR-02`).
* **Hardware & Licensing Cost (20% Weight - High):** Capital expenditure suitability for a 150-user SME environment.
* **Scalability & Modularity (20% Weight - High):** Capacity to absorb floor expansion and new subnets (`SC-01` to `SC-03`).
* **Operational Simplicity (15% Weight - Medium):** Low management overhead and ease of troubleshooting (`MG-01` to `MG-04`).

---

## 2.5.3 Trade-off Analysis Matrix

| Evaluation Criteria (Weight) | Option A: Collapsed Core (2-Tier) | Option B: Traditional 3-Tier | Option C: Routed Access |
| :--- | :---: | :---: | :---: |
| **Security Enforcement (25%)** | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐⭐⭐ (4/5) |
| **High Availability (20%)** | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐⭐⭐⭐ (5/5) |
| **Hardware Cost (20%)** | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐ (2/5) | ⭐⭐⭐ (3/5) |
| **Scalability (20%)** | ⭐⭐⭐⭐ (4/5) | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐⭐⭐ (4/5) |
| **Operational Simplicity (15%)** | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐ (2/5) | ⭐⭐⭐ (3/5) |
| **Weighted Total Score** | **4.80 / 5.00 (SELECTED)** | **3.80 / 5.00** | **3.85 / 5.00** |

---

## 2.5.4 Selected Architecture Statement

> **ARCHITECTURAL DECISION:** **Option A — Collapsed Core Architecture (2-Tier)** is formally selected as the enterprise network foundation for **ABC Software Solutions**.
> 
> **JUSTIFICATION:** Collapsed Core delivers wire-speed Layer 3 routing, centralized Security ACL enforcement, and full core hardware redundancy (`AR-02`) at optimal capital expense. A Traditional 3-Tier model introduces excessive hardware cost and unnecessary Spanning-Tree complexity for a single 3-floor building with 150 users, while Routed Access increases access switch licensing costs without providing tangible operational benefits at this scale.

---

## 2.5.5 Design Decision Log

| Decision ID | Domain | Chosen Design Specification | Driven By System REQs | Engineering Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **DEC-01** | Topology | Collapsed Core 2-Tier with Redundant L3 Core Pair | `SC-01`, `AR-01`, `AR-02` | Eliminates Distribution hardware; provides zero-SPOF routing for 3 floors. |
| **DEC-02** | Segmentation | 8 Dedicated VLANs (VLAN 10 Dev to 90 Guest) | `SR-01`, `SR-02`, `SR-03` | Strictly separates broadcast domains and isolates untrusted guest devices. |
| **DEC-03** | Routing | Core SVI (Switched Virtual Interface) L3 Routing | `FR-01`, `SR-01`, `AR-02` | Wire-speed Inter-VLAN routing with centralized ACL enforcement. |
| **DEC-04** | Access Security | DHCP Snooping, PortFast, BPDU Guard, Port Security | `SR-04`, `SR-05`, `SR-06` | Suppresses L2 loops, blocks rogue DHCP servers, shuts unauthorized MAC ports. |
| **DEC-05** | Link Redundancy | LACP EtherChannel Dual-Uplinks (Access to Core) | `AR-01`, `AR-02`, `SC-01` | Bundles uplinks into 2Gbps logical pipes; enables sub-second link failover. |
| **DEC-06** | Inline Power | 802.3at PoE+ Managed Access Switches | `AR-03`, `FR-04` | Powers 42 endpoints (APs, IP Phones, CCTV Cameras) directly via Ethernet. |
| **DEC-07** | Boundary Filter | Extended Inbound Inter-VLAN ACLs on Core SVIs | `SR-02`, `SR-03`, `FR-02` | Blocks Guest access to RFC 1918 IPs; enforces port-level access to Git/ERP. |

---

## 2.5.6 Requirement Coverage Matrix

All 21 System Requirements established in **Design Review 2.4** are 100% satisfied by the chosen Design Decisions:

```text
Requirement Category ──► Specific Requirement ID ──► Satisfying Design Decision
----------------------------------------------------------------------------------
Functional (FR)      ──► FR-01, FR-03, FR-05     ──► DEC-02 (VLANs), DEC-03 (SVI Routing)
                     ──► FR-02, FR-04            ──► DEC-06 (PoE+ APs), DEC-07 (Guest ACLs)
Security (SR)        ──► SR-01, SR-02, SR-03     ──► DEC-02 (Subnets), DEC-07 (Inter-VLAN ACLs)
                     ──► SR-04, SR-05, SR-06     ──► DEC-04 (DHCP Snooping / BPDU Guard)
Availability (AR)    ──► AR-01, AR-02            ──► DEC-01 (Collapsed Core), DEC-05 (EtherChannel)
                     ──► AR-03                   ──► DEC-06 (802.3at PoE+ Switches)
Scalability (SC)     ──► SC-01, SC-02, SC-03     ──► DEC-01 (Modular Core), DEC-02 (IP Subnetting)
Manageability (MG)   ──► MG-01, MG-02, MG-03, 04 ──► 100% Traceable NDD Documentation
```

---

## 2.5.7 Transition to Chapter 3 (Detailed Network Architecture)

With **Chapter 2 (Design Analysis Phase)** complete, the project transitions from requirements specification to **Chapter 3 (Network Architecture & Detailed Design)**:

```text
[ CHAPTER 2: DESIGN ANALYSIS COMPLETE ]
Business Context (2.1) ──► Asset Inventory (2.2) ──► Security Zones (2.3) ──► System REQs (2.4) ──► ADR (2.5)
                                                                                                    │
                                                                                                    ▼
                                                                                [ CHAPTER 3: DETAILED DESIGN ]
                                                                                3.1 High-Level Architecture
                                                                                3.2 Physical Topology
                                                                                3.3 Logical Topology & IP Plan
                                                                                3.4 VLAN & Inter-VLAN Routing
                                                                                3.5 Security Control Placement
                                                                                3.6 High Availability Design
```
