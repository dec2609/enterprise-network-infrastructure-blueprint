# DESIGN REVIEW 2.1: BUSINESS CONTEXT & SYSTEM REQUIREMENTS
**Project:** Enterprise Network Infrastructure Blueprint
**Methodology:** Evidence-Driven Systems Engineering (10-Stage Systematic Review)
**Reference Document:** Cisco Campus LAN and Wireless LAN Solution Design Guide

---

## 1. Traceable Pipeline Lineage (10-Stage Traceability)

All design decisions in this document strictly adhere to a 10-stage traceable pipeline:
`PDF Raw Text` -> `Rule-based Screening (Stage B)` -> `Open Coding (Stage C)` -> `Emergent Themes (Stage D)` -> `Vendor-Neutral REQs (Stage E)` -> `Use Cases (Stage F)` -> `SME Scenario (Stage G)` -> `Trade-off Analysis (Stage H)` -> `Architecture Mapping (Stage I)` -> `DR 2.1 Output (Stage J)`.

---

## 2. Vendor-Neutral System Requirements (Stage E)

* **REQ-01 (Hierarchical Topology):** The infrastructure SHALL adopt a modular, hierarchical topology to enforce physical/logical abstraction, constrain fault domains, and support horizontal scaling (Traced to *Stage D Theme 1 / 23 Evidences*).
* **REQ-02 (Logical Segmentation):** The network SHALL enforce strict logical segmentation and access boundaries between staff subnets, administrative environments, and untrusted guest/IoT access points (Traced to *Stage D Theme 3 / 30 Evidences*).
* **REQ-03 (Resiliency & PoE):** The local network SHALL maintain continuous availability through link/node redundancy and provide standardized Power over Ethernet (PoE) delivery to connected endpoints (Traced to *Stage D Theme 2 / 17 Evidences*).
* **REQ-04 (Access Port Security):** Edge access ports SHALL implement baseline Layer 2 security controls to suppress Spanning-Tree topology loops and mitigate rogue dynamic addressing services (Traced to *Stage D Theme 4 / 6 Evidences*).

---

## 3. Instantiated Representative SME Scenario (Stage G)

To validate and test REQ-01 through REQ-04, an instantiated SME environment (**ABC Software Solutions**) is established:
* **Industry & Business Focus:** SaaS & Software Engineering firm.
* **Headcount & Device Scale:** 150 permanent employees + 50 guest/IoT devices.
* **Physical Layout:** 3-floor office building (Floor 1: Reception/HR/Finance; Floor 2: Software Dev/QA; Floor 3: Executive/DevOps/Server Room).
* **Functional Segmentation:** 6 logical zones (Dev, QA, HR, Finance, Executive Management, Guest Wi-Fi).

---

## 4. Business Context & Architectural Responses (5 Core Questions)

### Question 1: What is the company type and primary operational model?
* **Traceability Chain:** REQ-01 -> UC-01 -> Stage G Scenario Instantiation.
* **Architectural Response:** **ABC Software Solutions** operates as a growing SaaS software firm requiring high internal bandwidth for development and clear isolation for administrative/production services.

### Question 2: What are the required functional network zones/departments?
* **Traceability Chain:** REQ-02 -> UC-02 -> Stage I Mapping (VLAN Allocation).
* **Architectural Response:** 6 Dedicated VLANs: Software Dev (VLAN 10), QA (VLAN 20), HR (VLAN 30), Finance (VLAN 40), Executive Management (VLAN 50), Guest Wi-Fi (VLAN 90).

### Question 3: What is the physical user density and floor distribution?
* **Traceability Chain:** REQ-01, REQ-03 -> UC-01, UC-03 -> Stage G Physical Topology.
* **Architectural Response:** 150 Users across 3 Floors:
  * **Floor 1 (20 Staff + Guests):** HR, Finance, Reception Desk, Guest Wi-Fi APs.
  * **Floor 2 (85 Staff):** Software Engineering (Dev) & Quality Assurance (QA).
  * **Floor 3 (45 Staff + Infrastructure):** Executive Management, DevOps, Server Room core racks.
  * *Deployment:* 1 Dedicated Access Switch per floor with dual-homed uplinks to the Core L3 Switch pair.

### Question 4: Which functional zones require the highest security trust levels?
* **Traceability Chain:** REQ-02, REQ-04 -> UC-02, UC-04 -> Stage I Access Control Mapping.
* **Architectural Response:** **Server Room (DevOps/Internal Repos)** and **Finance/HR Subnets** (Trust Level ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐). Inter-departmental traffic is blocked by default and permitted via explicit ACL rules.

### Question 5: What is the baseline traffic flow matrix (Traffic Policy)?
* **Traceability Chain:** REQ-02, REQ-04 -> UC-02, UC-04 -> Stage I Security Mapping.
* **Architectural Response:**
  * **Dev/QA:** Allowed access to Code Repos & Staging Servers; blocked from HR/Finance subnets.
  * **Finance/HR:** Allowed access to ERP & Accounting servers; blocked from staging servers.
  * **Guest Wi-Fi:** Strictly isolated (Internet-only access via ACL blocking RFC 1918 private IP subnets).
  * **IT/DevOps:** Full administrative access across all management subnets.

---

## 5. Architectural Trade-off Summary (Stage H)

* **Chosen Topology:** **Collapsed Core Architecture (2-Tier)**.
* **Justification:** Evaluated against 3-Tier and Routed Access topologies. Collapsed Core provides the optimal balance of redundancy, performance, low operational complexity, and cost efficiency for a 150-user, 3-floor single-building SME environment.
