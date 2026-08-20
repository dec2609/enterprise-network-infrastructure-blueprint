# Enterprise Network Infrastructure Blueprint

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Infrastructure: Cisco Catalyst](https://img.shields.io/badge/Infrastructure-Cisco%20Catalyst-orange.svg)
![Validation: 94.4% Pass](https://img.shields.io/badge/Validation-94.4%25%20Pass-green.svg)
![Status: In Review](https://img.shields.io/badge/Status-Final%20Review-yellow.svg)

> **Status:** Final cross-document review in progress. Core design, implementation, and test evidence are complete; a few documents are still being reconciled before the v1.0 baseline is frozen.

A vendor-neutral enterprise network design for **ABC Digital Solutions**, a fictional 150-user, three-floor SME. The project walks through the full engineering lifecycle — requirements gathering, architecture decisions, Cisco-based configuration, security controls, failure testing, change management, and as-built documentation — with each stage traceable to the one before it.

The main goal was not simply to assemble a standard topology, but to practice the technical discipline required in infrastructure design: justifying decisions with requirements, verifying failure scenarios instead of assuming reliability, and documenting change events cleanly.

---

## 🏛️ Architecture Overview

* **Layer 2 Foundations:** 9 production VLANs (VLAN 10–90) plus a dedicated native/dead VLAN (999); Rapid PVST+ (`rapid-pvst`) with deterministic root bridges; dual-link LACP active EtherChannels (`Port-channel1–3`); and access edge hardening (BPDU Guard, PortFast, DHCP Snooping, Sticky Port Security).
* **Layer 3 Forwarding:** Centralized Switched Virtual Interface (SVI) routing on Catalyst 3650 (`CORE-L3-01`) rather than Router-on-a-Stick, paired with a floating default route (`0.0.0.0/0 via 10.10.70.2`) toward the edge firewall transit segment.
* **Security Controls:** Extended ACLs (`ACL_DEV_IN`, `ACL_FIN_IN`, `ACL_HR_IN`, `ACL_GUEST_IN`) enforcing inter-zone isolation, with the Guest VLAN fully restricted from accessing internal enterprise segments.
* **High Availability & Link Resiliency:** Sub-2-second STP re-convergence upon core link failure, and zero-packet-loss failover across LACP bundle member links.

### What Version 1 Does Not Do
`CORE-L3-01` serves as the sole active Layer 3 default gateway. Because first-hop redundancy protocols (HSRP/VRRP) are deferred to Version 2, an outage on `CORE-L3-01` temporarily interrupts inter-VLAN routing until the device recovers. `CORE-L3-02` operates purely as an L2 secondary bridge in this baseline. This constraint is documented as an accepted V1 scope boundary.

---

## 🛡️ Change Management: CHANGE-001

During post-implementation verification, an endpoint allocation error was identified: `DEV-PC-01` (VLAN 10) was physically connected to Switch Floor 1 (`ACC-F1-01 / Fa0/1`) instead of Switch Floor 2 (`ACC-F2-01 / Fa0/1`), with a Sticky MAC violation triggered on Floor 1.

```text
Detected: Incorrect VLAN and switch port binding on Floor 1
   │
   ├── Scoped impact: Confined strictly to Floor 1 and Floor 2 access interfaces
   ├── Executed change: Re-patched physical cable to Floor 2, cleared stale Sticky MAC
   └── Verified: 100% ICMP reachability to gateway and server infrastructure; updated Port Plan
```

* **Full Ticket & Audit Trail:** [`change-management/CHANGE-001/CHANGE-001-dev-endpoint-reconciliation.md`](./change-management/CHANGE-001/CHANGE-001-dev-endpoint-reconciliation.md)
* **Pre/Post-Change Evidence Logs:** [`change-management/CHANGE-001/`](./change-management/CHANGE-001/)

---

## 🏗️ Architecture Diagrams

Visualizations are maintained in native vector format (`.svg` / `.drawio`) for direct inspection and editability:

### 1. Logical Topology *(Primary Overview)*
The 4-tier hierarchical topology illustrating core routing, distribution, perimeter firewalling, and access-layer segmentation.

![Logical Architecture](./architecture/logical/logical_topology.svg)

---

### 2. Supporting Views
<details>
<summary><b>🔍 Click to expand: Physical, Routing, Security & HA Views</b></summary>
<br>

* **2.1 Physical Rack Layout:** Equipment mounting, cable labeling, and power redundancy across the 42U Server Room rack.  
  ![Physical Architecture](./architecture/physical/physical_rack_layout.svg)

---

* **2.2 L3 Routing & Traffic Flow:** Inter-VLAN packet paths between endpoints, core infrastructure services (DNS/DHCP at `10.10.60.10`, Git at `10.10.60.21`), and NAT egress.  
  ![L3 Routing Flow](./architecture/routing/l3_routing_flow.svg)

---

* **2.3 Security Boundaries:** Trust-Zone classification (Levels 1–5) and ACL policy enforcement points.  
  ![Security Boundary](./architecture/security/acl_security_boundary.svg)

---

* **2.4 HA & Failover Behavior:** LACP single-link degradation and STP Alternate-to-Forwarding transitions.  
  ![High Availability](./architecture/high_availability/lacp_etherchannel_topology.svg)

</details>

---

## 🔬 Traceability Pipeline

```text
Market Analysis (157 IT job postings + Cisco CVD recommendations)
        │
System Requirements (Functional, Security, Availability specifications)
        │
Asset & Trust-Zone Classification (13 assets, 5 security zones)
        │
Architecture Decisions (ADR-001 through ADR-005)
        │
Network Design (VLAN allocation, subnetting, L2/L3 plans)
        │
Implementation (7 Cisco device configuration baselines)
        │
Change Governance (CHANGE-001 endpoint remediation)
        │
Chaos Testing (12-phase failure injection)
        │
Verification (CLI logs, as-built documentation)
```

---

## 🧪 Testing & Validation Summary

Acceptance testing was conducted in Cisco Packet Tracer across 12 structured phases, achieving a **94.4% overall validation pass rate**.

| Test Area | Phase | Result | Key Engineering Observation |
| :--- | :---: | :---: | :--- |
| **Topology, IP Plan & Trunking** | 1–4 | 🟢 Pass | 9 VLANs operational; 802.1Q trunks active on all Core-Access links. |
| **EtherChannel & STP Convergence** | 5–8 | 🟢 Pass | LACP bundles up `Po1..3(SU)`; Rapid PVST+ converged with deterministic root bridge. |
| **L3 Inter-VLAN & Egress Routing** | 9 | 🟢 Pass | Centralized SVI routing verified; 100% ICMP reachability to internal servers and gateway. |
| **ACL Policy Enforcement** | 10 | 🟡 Limitation | Policy syntax and logic verified; SVI ACL binding encounters a known Packet Tracer parser constraint. |
| **STP Link-Down Convergence** | 11.1 | 🟢 Pass | `CORE-L3-02` alternate port `Gi1/0/24` moved from `Altn BLK` to `Root FWD` in <2s. |
| **LACP Single-Link Degradation** | 11.2 | 🟢 Pass | Port-channel remained up `Po1(SU)` upon link shutdown; zero traffic loss on remaining link. |
| **Active Gateway Failure** | 11.3 | 🟡 Partial | Expected Single-Gateway behavior (inter-VLAN routing paused; L3 failover deferred to V2). |
| **System Auto-Recovery** | 11.4 | 🟢 Pass | Core 1 recovered; Spanning-Tree topology and SVI routing returned to baseline automatically. |

> Full test specifications and raw output captures are available in the [Validation Report](./docs/04_validation/validation_report.md) and [Raw Verification Logs](./implementation/verification/).

---

## ⚠️ Known Limitations

Being transparent about what Version 1 does and does not cover:

* **No First-Hop Gateway Redundancy:** `CORE-L3-01` represents a single point of failure for Layer 3 inter-VLAN routing. First-hop redundancy (HSRP/VRRP) is scoped for Version 2.
* **Packet Tracer SVI ACL Parser Behavior:** Extended ACL syntax and filtering logic are verified correct, but the Catalyst 3650 parser in Packet Tracer exhibits a known limitation preventing running-config commitment on SVI ingress.
* **Simulation Modeling Boundary:** Testing was performed within Cisco Packet Tracer; validation confirms architectural logic rather than physical hardware performance.

---

## 📂 Documentation Index

* 📚 **Ch. 1 — Requirements Discovery:** [`docs/01_requirements_discovery/`](./docs/01_requirements_discovery/)  
  *(Market analysis, keyword distributions, and project scope boundaries)*
* 🏛️ **Ch. 2 — System Architecture & Analysis:** [`docs/02_analysis/`](./docs/02_analysis/)  
  *(Business context, asset valuations AST-01..13, trust zones, system requirements, and ADRs)*
* 📐 **Ch. 3 — Detailed Network Design:** [`docs/03_network_design/`](./docs/03_network_design/)  
  *(Subnetting plan, L2/L3 design specs, extended ACL matrices, and switch CLI SOPs)*
* 🧪 **Ch. 4 — Test & Validation Strategy:** [`docs/04_validation/`](./docs/04_validation/)  
  *(15 test cases, 12-phase acceptance report, and failure scenario logs)*
* 💡 **Ch. 5 — Engineering Reflection & Roadmap:** [`docs/05_reflection/`](./docs/05_reflection/)  
  *(Lessons learned, architectural trade-offs, and V2 roadmap including HSRP/VRRP, NGFW, and EVE-NG)*
* 🛡️ **Change Management Records:** [`change-management/`](./change-management/)  
  *(CHANGE-001 incident handling, blast radius assessment, and As-Built updates)*

---

## 🛠️ Repository Artifacts

* **Cisco Configuration Baselines:** [`implementation/configs/`](./implementation/configs/) *(7 reconciled device configs)*
* **Packet Tracer Network File:** [`packettracer/enterprise_network_v1.0.pkt`](./packettracer/enterprise_network_v1.0.pkt)
* **Raw CLI Verification Logs:** [`implementation/verification/`](./implementation/verification/)
* **Audit & Traceability Scripts:** [`validation/`](./validation/)
* **Final Engineering Report:** [`deliverables/As_Built_Engineering_Report_v1.0.md`](./deliverables/As_Built_Engineering_Report_v1.0.md)

---

## 📜 License

This project is licensed under the MIT License. See the [`LICENSE`](./LICENSE) file for details.
