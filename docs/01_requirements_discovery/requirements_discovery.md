# REQUIREMENTS DISCOVERY REPORT

**Document ID:** REQ-DISC-001  
**Project:** Enterprise Network Infrastructure Blueprint  
**Source Dataset:** `research/raw/raw_jobs.csv` (157 Market Job Descriptions)  
**Status:** **APPROVED & ARCHIVED**

---

## 1. Overview & Dataset Scope
This report documents the automated extraction and qualitative analysis of **157 Job Descriptions (JDs)** targeting Entry-level IT Support, Helpdesk, and Junior Network roles in the Vietnamese job market.

The objective is to establish an empirical, evidence-based baseline of industry requirements to drive the scope of the Enterprise Network Infrastructure Blueprint.

---

## 2. Explicit Keyword Frequency Analysis

Quantitative analysis reveals direct mentions of core networking and security technologies across the 157 JDs dataset:

### Network Services
* **DNS:** Mentioned explicitly in **7 JDs** (e.g., Axon, TechValley, CMC University, Reeracoen, HSC, Manpower).
* **DHCP:** Mentioned explicitly in **6 JDs** (e.g., Axon, TechValley, CMC University, Reeracoen, Manpower).

### Routing & Segmentation
* **Routing:** Mentioned explicitly in **7 JDs** (e.g., TechValley, CMC University, Reeracoen, FedEx, NAKIVO, Synopsys).
* **VLAN:** Mentioned explicitly in **2 JDs** (e.g., CyberLogitec Vietnam, TechValley).

### Security & Remote Access
* **VPN:** Mentioned explicitly in **5 JDs** (e.g., Axon, CyberLogitec, TechValley, Reeracoen, Manpower).
* **Firewall:** Mentioned explicitly in **3 JDs** (e.g., TechValley, Reeracoen, Manpower).

### Identity & Operational Support
* **Active Directory:** Mentioned explicitly in **9 JDs** (e.g., Chubb Insurance, CyberLogitec, Reeracoen, FWD, Prudential).
* **Troubleshooting:** Mentioned explicitly in **8 JDs** (e.g., The Sentry, DXC Technology, HSC, Intel, Synopsys).
* **Printer Support:** Mentioned explicitly in **2 JDs** (e.g., Reeracoen, Alchemy Asia).

---

## 3. Qualitative Validation & Implied Requirements

Manual sample review identifies a significant **False Negative** phenomenon inherent to recruitment texts:

* **Broad Responsibilities:** Many job listings do not explicitly list low-level terms like `VLAN` or `Subnetting`, but mandate broad duties such as *"Manage LAN/WAN infrastructure"* or *"Configure Cisco/Mikrotik Switches"* (e.g., Manpower, Bellsystem24, Vina Research).
* **Technical Implication:** In enterprise operations, Layer 2/3 switch administration implicitly requires VLAN segmentation and IP subnet planning. Thus, VLAN support is classified as a **Reasonable Implied Requirement**.

---

## 4. Dataset Limitations
* **Recruitment Purpose vs. Engineering Specs:** Job postings attract candidates and do not serve as technical architecture blueprints. Keyword frequency indicates term popularity rather than exact deployment ratios.
* **Scope Boundary:** The 157 JDs dataset provides a practical snapshot reliable enough to justify project scope boundaries without claiming universal statistical conclusions.
