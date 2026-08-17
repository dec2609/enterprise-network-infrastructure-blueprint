# Design Decisions & Technical Scope Definition

## 1. Context & Case Study Assumptions

The infrastructure design is engineered around a realistic deployment scenario for a mid-sized Vietnamese enterprise (**ABC Digital Solutions**):
* **Scale & Organization:** 150 employees distributed across a 3-floor office facility operating under a hybrid working model.
* **Architectural Baseline:** ABC Digital Solutions previously operated on an unsegmented Flat Layer-2 Network where all endpoints and departments shared a single broadcast domain, introducing severe broadcast congestion and substantial security risks.

The primary project objective is to redesign, implement, validate, and document a multi-tier, secure, high-performance, and auditable enterprise campus infrastructure with structured change governance.

---

## 2. Evidence-Based Requirements & Engineering Interpretation

The technical boundaries of the architecture were established through a structured Systems Engineering lifecycle: **Evidence Collection $\rightarrow$ Requirement Synthesis $\rightarrow$ Architectural Decision**.
* **Explicit Market Evidence:** Quantitative analysis of 157 Vietnamese IT job postings (IT Support, Helpdesk, Junior Network Engineer; raw dataset archived at `research/raw/raw_jobs.csv`) revealed core demand for Active Directory (9 JDs), Routing (7 JDs), DNS (7 JDs), DHCP (6 JDs), VPN (5 JDs), Firewalls (3 JDs), and VLAN Segmentation (2 JDs) across enterprises such as Axon, CyberLogitec, TechValley, Reeracoen, and Manpower (reference report: `docs/01_requirements_discovery/requirements_discovery.md`).
* **Implicit Review & Qualitative Synthesis:** Qualitative review revealed that many technical job specifications omit explicit keywords like "VLAN" and instead rely on higher-level operational competencies such as "LAN/WAN Administration" or "Cisco Switch Configuration". This demonstrates that Layer-2 managed switching competencies and VLAN segmentation are core underlying industry expectations.
* **Cisco Validated Design (CVD) Reconciliation:** Market requirements were cross-referenced against official Cisco Validated Designs (`research/raw/cisco_cvd_raw_text.csv`) to translate basic JD requirements into enterprise-grade architectural standards (e.g., Collapsed Core L3 switching, Rapid-PVST+, and dual-link LACP active aggregation).

---

## 3. Scope Definition for Version 1.0 (In-Scope)

Version 1.0 focuses on building a resilient, fully verified **Enterprise Core Network & Edge Security Baseline**:
* **Hierarchical Switching & Centralized L3 Routing:** Deployment of dual Cisco Catalyst 3650 Core Switches (`CORE-L3-01` active gateway, `CORE-L3-02` standby L2) utilizing centralized Switched Virtual Interfaces (SVIs) for 9 production subnets (VLAN 10–90) and floating default routing (`0.0.0.0/0 via 10.10.70.2`) to eliminate Router-on-a-Stick bandwidth bottlenecks.
* **Layer-2 High Availability & Redundancy:** Implementation of dual-link IEEE 802.3ad LACP EtherChannels (`Port-channel1..3`) between Core and Access switches, Spanning-Tree tuning via Rapid-PVST+ with deterministic root bridge priority, and an isolated Native VLAN 999 with zero SVI binding.
* **Edge Hardening & Port Security:** Mandatory enforcement of `spanning-tree portfast`, `bpduguard enable`, DHCP Snooping, and Sticky Port-Security (`maximum 1`, violation restrict) across host-facing access ports.
* **Granular Security Controls & Lateral Isolation:** Deployment of ingress SVI Extended ACLs (`ACL_DEV_IN`, `ACL_FIN_IN`, `ACL_GUEST_IN`) to isolate guest wireless traffic and enforce strict role-based access to shared server infrastructure (Git Server `10.10.60.21` and Database `10.10.60.22`).
* **Perimeter Security & WAN Egress:** Integration of a Cisco ASA 5506-X Firewall (`FW-EDGE-01`) terminating Transit VLAN 70, performing stateful inspection and NAT Overload via WAN Router (`RTR-EDGE-01`) to the ISP gateway.
* **Change Governance (CHANGE-001):** Full documentation and execution of change control procedures to resolve physical endpoint cabling discrepancies with immutable before/after audit logs.

---

## 4. Explicit Out-of-Scope (Planned for Future Releases)

To ensure maximum engineering focus and verification depth on core network plumbing and security baselines, the following capabilities are explicitly deferred:
* **Active Directory / Windows Server Domain Integration (Version 2.0):** While frequently requested in market JDs, identity management belongs to System Administration and will be integrated after Layer 2/Layer 3 stability is established.
* **Remote Access & Site-to-Site IPsec VPN (Version 1.5):** Scheduled for perimeter expansion in subsequent iterations.
* **Centralized SIEM & NetFlow Analytics (Version 3.0):** Advanced Security Operations and telemetry analysis are deferred to enterprise scale-up phases.
* **First Hop Redundancy Protocols (HSRP / VRRP):** Version 1.0 operates on an Active-Passive L2 Core redundancy model; active-active FHRP is slated for multi-core scaling.

---

## 5. Requirement Traceability Matrix

| Architectural Feature (v1.0) | Market Evidence (Source: `docs/01_requirements_discovery/`) | Engineering Interpretation & CVD Reference | Business / Technical Risk Mitigated |
| :--- | :--- | :--- | :--- |
| **VLAN Segmentation (10–90, 999)** | CyberLogitec, TechValley (Explicit) + Manpower (Implied) | Enterprise Layer-2 isolation required per department | Eliminates broadcast storms and unauthorized cross-department data exposure. |
| **Centralized L3 SVI Routing** | 7 JDs (TechValley, Reeracoen, FedEx...) | Collapsed core architecture eliminating single-router bottleneck | Prevents throughput degradation caused by legacy Router-on-a-Stick models. |
| **LACP EtherChannel (Po1..3)** | Cisco CVD + DXC, Intel Troubleshooting JDs | Link aggregation across uplinks for bandwidth and failover | Eliminates single-cable failure downtime between Core and Access switches. |
| **Rapid-PVST+ Tuning** | Troubleshooting 8 JDs (Cisco Campus Design) | Sub-2-second deterministic convergence on link failure | Prevents Layer-2 loops and prolonged Spanning-Tree recalculation outages. |
| **Guest Network Isolation (ACL)** | Firewall 3 JDs + Security Baseline Specs | Lateral isolation of untrusted endpoints at Layer 3 | Mitigates malware/ransomware propagation into internal subnets. |
| **Port Security & BPDU Guard** | Troubleshooting 8 JDs + Cisco SAFE Guidelines | Physical edge hardening against rogue access points/switches | Prevents MAC flooding attacks, rogue DHCP injection, and STP hijacking. |
| **Evidence Change Control (CHANGE-001)** | Production Governance & Audit Assurance | Formal change ticketing, blast radius control & audit trailing | Prevents configuration drift and undocumented infrastructure state divergence. |

---

## 6. Dataset Limitations & Research Validity

* **Recruitment vs. Architecture:** Job postings (`research/raw/raw_jobs.csv`) reflect hiring intent rather than technical architectural blueprints. Certain standard protocols (e.g., LACP, Rapid-PVST+, Dot1Q trunking) are operationally implied rather than explicitly detailed in entry-level postings.
* **Sampling Context:** The 157 JD dataset provides an empirical snapshot of the Vietnamese IT employment market, serving as an evidence-based foundation to justify technical design priorities for this enterprise implementation.
