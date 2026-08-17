# DESIGN REVIEW 3.7: HIGH AVAILABILITY DESIGN
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** System Design & Implementation Phase (Chapter 3)  
**Document Focus:** High Availability Scope, LACP EtherChannel Bundling, Rapid STP & Failure Domain Isolation  
**Parent Reviews:** DR 3.1 (Logical Arch), 3.2 (Physical), 3.4 (Layer 2 Design), & 3.6 (Security Controls)

---

## 3.7.1 Overview & Availability Design Objectives

Design Review 3.7 establishes the High Availability (HA) framework for **ABC Software Solutions**. This review bridges availability requirements (`AR-01..03`) into a practical, resilient network backbone designed specifically for a 150-user, 3-floor SME environment [cite: 1, 3, 4].

**Core Architectural Objectives:**
* **AO-1. Zero-Downtime Uplink Failover:** Ensure that single physical cable cuts between Access Switches and Core L3 Switches trigger sub-second failover without dropping user sessions [cite: 1, 3, 4].
* **AO-2. Active Bandwidth Aggregation:** Bundle dual physical uplinks into a single logical pipe (`Port-Channel 1`) to double effective uplink bandwidth (2Gbps / 20Gbps) [cite: 1, 3, 4].
* **AO-3. Bounded Failure Domains:** Isolate hardware and cable failure impacts to individual floor access nodes without collapsing the core switching fabric [cite: 1, 4, 8].
* **AO-4. Operational Simplicity:** Deploy standardized IEEE 802.3ad LACP and Rapid PVST+ protocols to maintain manageable operating procedures for IT personnel [cite: 1, 3, 4].

---

## 3.7.2 High Availability Scope & Boundary Definition

Rather than over-engineering DC-grade redundancy, the HA architecture establishes a realistic boundary tailored to SME scale [cite: 1, 3, 4]:

| Included in HA Scope (SME Scale) | Excluded from HA Scope (Out-of-Scope) | Architectural Justification |
| :--- | :--- | :--- |
| **IEEE 802.3ad LACP EtherChannel** [cite: 1, 3] | Dual ISP BGP Multi-Homing [cite: 1] | Single ISP WAN circuit is sufficient for SME operational budget [cite: 1, 3]. |
| **Rapid Spanning Tree (RSTP 802.1w)** [cite: 1, 3] | First Hop Redundancy (HSRP/VRRP) [cite: 1] | Collapsed Core SVI acts as single logical gateway fabric [cite: 1, 4, 7, 8]. |
| **Dual-Homed Physical Uplinks** [cite: 1, 3] | Dynamic Routing Protocols (OSPF/BGP) [cite: 1] | Deterministic static default route (`0.0.0.0/0`) is optimal [cite: 1, 6, 7]. |
| **Core Hardware Redundancy (`CORE-L3-01/02`)** [cite: 1, 6] | Multi-Chassis VSS / Stacking Fabrics [cite: 1] | Prevents hardware licensing over-spending [cite: 1, 3]. |

---

## 3.7.3 HA Trade-off Analysis Matrix

The architecture evaluates three uplink strategies before selecting **Dual Uplink + LACP EtherChannel** [cite: 1, 3, 4]:

| Uplink Redundancy Strategy | Effective Bandwidth | Fault Tolerance Level | Operational Risk | Architectural Decision |
| :--- | :---: | :--- | :--- | :--- |
| **Single Uplink (No Redundancy)** | 1 Gbps / 10 Gbps | Single Point of Failure (SPOF) [cite: 1, 6, 8] | Cable cut isolates an entire floor [cite: 1, 6, 8]. | **REJECTED** [cite: 1] |
| **Dual Uplink without EtherChannel** | 1 Gbps (50% wasted) | STP-based recovery (30-50s) [cite: 1] | Unused link blocked by STP; slow failover [cite: 1]. | **REJECTED** [cite: 1] |
| **Dual Uplink + IEEE 802.3ad LACP** | **2 Gbps / 20 Gbps (100%)** | **Sub-second LACP failover** [cite: 1, 3, 4] | Active-Active bandwidth with zero link waste [cite: 1, 3, 4]. | **SELECTED ARCHITECTURE** [cite: 1, 3, 4] |

---

## 3.7.4 EtherChannel & Rapid STP Design Specifications

```text
 ┌───────────────────────────────────────────────────────────────────────────┐
 │                      COLLAPSED CORE L3 SWITCH FABRIC                      │
 │                                                                           │
 │         [ CORE-L3-01 (Primary) ] ◄─── Stack Link ───► [ CORE-L3-02 ]      │
 └─────────────────▲─────────────────────────────────────────▲───────────────┘
                   ║                                         ║
     Port-Channel 1║ (LACP Active Active)        Port-Channel 1║ (LACP Active Active)
                   ║                                         ║
 ┌─────────────────▼────────────────┐       ┌────────────────▼───────────────┐
 │ ACC-F1-01 (Floor 1 Access)       │       │ ACC-F2-01 (Floor 2 Access)     │
 └──────────────────────────────────┘       └────────────────────────────────┘
```

1. **LACP Dynamic Port Channel Strategy:** Dual Gigabit uplink ports (`Gi0/1` and `Gi0/2`) on each Access Switch (`ACC-F1/F2/F3`) bundle into a logical interface **`Port-Channel 1` (Po1)** connecting back to the Core Switch pair [cite: 1, 3, 4]. LACP mode is set to **Active** on both ends to force dynamic negotiation and continuous link health monitoring [cite: 1, 3, 4].
2. **Rapid PVST+ Integration:** Rapid PVST+ runs transparently over `Port-Channel 1` [cite: 1, 3, 4]. In the event of a total logical link failure or misconfiguration loop, RSTP enforces topology re-convergence under 2 seconds [cite: 1, 3, 4].

---

## 3.7.5 Failure Scenarios & Impact Analysis

* **Scenario 1 — Single Physical Fiber Cut on Uplink:** LACP detects link loss on `Gi0/1` within milliseconds and shifts 100% of frame traffic to `Gi0/2` inside `Port-Channel 1` [cite: 1, 3, 4]. Active user TCP sessions experience zero packet drop [cite: 1, 3, 4].
* **Scenario 2 — Physical Cable Loop at Access Edge:** BPDU Guard immediately detects incoming BPDU frames on user Access ports (`Fa0/1-20`) and transitions the offending port to `err-disable`, protecting the L2 switching fabric from broadcast storms [cite: 1, 3].
* **Scenario 3 — Complete Access Switch Outage (`ACC-F1-01`):** Failure impact is isolated strictly to Floor 1 endpoints [cite: 1, 6, 8]. Floor 2, Floor 3, and MDF Server Zone services remain 100% operational [cite: 1, 6, 8].

---

## 3.7.6 Availability Requirements Traceability Matrix

| Requirement ID | High Availability Focus | Planned HA Technology | Planned Configuration | Validation Method (Chapter 4) |
| :---: | :--- | :--- | :--- | :--- |
| **AR-01** | Link Redundancy & Fault Tolerance [cite: 4] | Dual-Homed LACP EtherChannel [cite: 1, 3] | `interface Port-Channel 1`, `channel-group 1 mode active` [cite: 1, 3] | Pull physical cable during continuous ping test [cite: 1, 3, 4] |
| **AR-02** | Core Switching HA & Loop Suppression [cite: 4] | Rapid PVST+ Root Priorities [cite: 1, 3] | `spanning-tree mode rapid-pvst`, Primary Root `4096` [cite: 1, 3] | Verify RSTP convergence upon link state change [cite: 1, 3, 4] |
| **AR-03** | Inline Power Resiliency [cite: 4] | 802.3at PoE+ with Central UPS [cite: 1, 3] | Active 48V PoE delivery backed by 3KVA UPS [cite: 1, 3] | Cut AC power mains; verify APs & IP Phones stay up [cite: 1, 3, 4] |

---

## 3.7.7 Transition Checklist to DR 3.8 (Device Configurations)

- [x] HA Scope defined with explicit SME-tailored inclusions and exclusions [cite: 1, 3, 4].
- [x] HA Trade-off Analysis matrix established favoring 802.3ad LACP [cite: 1, 3, 4].
- [x] LACP Active-Active Port-Channel bundling specified for all access switches [cite: 1, 3, 4].
- [x] Failure scenarios analyzed for link cut, loop injection, and node failure [cite: 1, 3, 4, 6, 8].
- [x] 100% Traceability maintained to AR-01..03 availability requirements [cite: 1, 4].
- [x] High Availability Design frozen and ready for Device CLI Codebase (DR 3.8) [cite: 1, 4].
