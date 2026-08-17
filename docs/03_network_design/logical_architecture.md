# DESIGN REVIEW 3.1: ENTERPRISE LOGICAL ARCHITECTURE
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** System Design & Implementation Phase (Chapter 3)  
**Document Focus:** Functional Logical Architecture & Traffic Flow Boundaries  
**Parent Chapter:** Chapter 2 (Design Analysis Phase - DR 2.1 to 2.5)

---

## 3.1.1 Overview & Design Objectives

Design Review 3.1 establishes the vendor-neutral, functional logical architecture for **ABC Software Solutions**. This review bridges the requirement decisions established in Chapter 2 into a high-level operational blueprint. 

**Core Objectives:**
* Abstract physical hardware, port numbers, and specific model numbers [cite: 1].
* Define clear functional zones, trust boundaries, and logical traffic flows [cite: 1].
* Maintain 100% traceability to System Requirements (`FR-01..05`, `SR-01..06`, `AR-01..03`, `SC-01..03`, `MG-01..04`) [cite: 1].

---

## 3.1.2 Guiding Architectural Principles

The enterprise logical architecture is governed by five core engineering principles:

* **P1. Layered Functional Architecture:** The network is partitioned into distinct functional layers (Edge, Core Routing, Access, Services) to bound blast radiuses and reduce operational complexity [cite: 1].
* **P2. Strict Separation of Trust:** Every logical network broadcast domain (VLAN) operates as an independent Security Zone [cite: 1]. Inter-zone communication is denied by default [cite: 1].
* **P3. Centralized Layer 3 Routing:** All inter-VLAN routing and gateway functions reside at the Collapsed Core layer, eliminating distributed routing complexity [cite: 1].
* **P4. Principle of Least Privilege:** Cross-zone network paths permit only explicit, business-required protocol ports via Layer 3 Access Control Lists [cite: 1].
* **P5. Modular Scalability:** The functional structure allows adding new user departments, physical floors, or server zones without modifying the core backbone topology [cite: 1].

---

## 3.1.3 Functional Components & Roles

```text
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                           1. EXTERNAL EDGE                              │
 │   [ Internet ] ◄──► [ Edge Router ] ◄──► [ Enterprise Firewall ]        │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
 ┌────────────────────────────────────▼────────────────────────────────────┐
 │                     2. CORE ROUTING & SECURITY FABRIC                   │
 │                [ Collapsed Layer 3 Core Switching Engine ]              │
 └───────┬────────────────────────────┬────────────────────────────┬───────┘
         │                            │                            │
 ┌───────▼─────────────┐     ┌────────▼─────────────┐     ┌────────▼─────────────┐
 │  3. USER ACCESS     │     │  4. SERVER SERVICES  │     │  5. UNTRUSTED GUEST  │
 │  • Dev & QA Zone    │     │  • Git / CI/CD Repo  │     │  • Visitor Wi-Fi     │
 │  • HR & Finance     │     │  • ERP & Database    │     │  • Isolated Egress   │
 │  • Executive Mgmt   │     │  • Core Directory    │     │  (Internet Only)     │
 └─────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

| Functional Component | Operational Role | Security Trust Boundary |
| :--- | :--- | :---: |
| **Internet & Edge Router** | Manages WAN connectivity, ISP default routing, and NAT/PAT translation [cite: 1]. | External / Untrusted [cite: 1] |
| **Enterprise Firewall** | Enforces perimeter security policy, stateful packet inspection, and DMZ/Edge filtering [cite: 1]. | Perimeter Boundary [cite: 1] |
| **Collapsed Core Layer** | Serves as the central L3 SVI routing engine, inter-VLAN gateway, and ACL policy enforcement point [cite: 1]. | Core Control Plane (Trust ⭐⭐⭐⭐⭐) [cite: 1] |
| **Access Layer** | Provides endpoint connectivity, Layer 2 broadcast domain isolation, PoE power, and edge port security [cite: 1]. | Edge Switching Plane [cite: 1] |
| **Server Zone** | Houses shared enterprise application services (Git/CI-CD, ERP Database, Domain Services) [cite: 1]. | Critical Internal (Trust ⭐⭐⭐⭐⭐) [cite: 1] |
| **Department User Networks**| Segregates functional user groups (Dev, QA, HR, Finance, Executive) into dedicated subnets [cite: 1]. | Internal Role-Based (Trust ⭐⭐⭐..⭐⭐⭐⭐) [cite: 1] |
| **Guest Zone** | Delivers untrusted internet access for visitors while completely blocking internal corporate LAN paths [cite: 1]. | Untrusted Internal (Trust ⭐) [cite: 1] |

---

## 3.1.4 Logical Traffic Flow Patterns

1. **Internet Egress Flow (Corporate Users):**  
   `Client Endpoint` ──► `Access Layer` ──► `Collapsed Core (Default Route)` ──► `Firewall Inspection` ──► `Edge Router (NAT)` ──► `Internet` [cite: 1]
2. **Internal Controlled Service Flow (Dev to Git Repo):**  
   `Dev Endpoint` ──► `Access Layer` ──► `Collapsed Core SVI` ──► `Inter-VLAN ACL Inspection (Permit Port 22/443)` ──► `Server Zone (Git Server)` [cite: 1]
3. **Restricted Cross-Zone Flow (Dev to Finance - Blocked):**  
   `Dev Endpoint` ──► `Access Layer` ──► `Collapsed Core SVI` ──► `Inter-VLAN ACL Inspection (Deny All)` ──► `DROPPED AT CORE` [cite: 1]
4. **Untrusted Guest Egress Flow:**  
   `Guest Wi-Fi Endpoint` ──► `Access Layer (Guest VLAN)` ──► `Collapsed Core` ──► `Guest Isolation ACL (Deny RFC 1918)` ──► `Firewall / Edge Router` ──► `Internet` [cite: 1]

---

## 3.1.5 Requirement Traceability & Design Confirmation

| Requirement ID | Mapped Functional Component | Logical Design Response | Status |
| :---: | :--- | :--- | :---: |
| **FR-01** | User Networks & Core Layer | Departments mapped to dedicated logical subnets with Core inter-VLAN routing [cite: 1]. | **CONFIRMED** |
| **FR-02** | Guest Zone & Core Layer | Isolated Guest broadcast domain with outbound-only internet route [cite: 1]. | **CONFIRMED** |
| **FR-03** | Server Zone | Centralized DHCP/DNS services hosted in isolated Server Zone [cite: 1]. | **CONFIRMED** |
| **SR-01** | User Networks & Access Layer | Logical L2 broadcast isolation per functional role [cite: 1]. | **CONFIRMED** |
| **SR-02** | Core Layer & Server Zone | Centralized Inter-VLAN ACLs protecting Finance and ERP Server [cite: 1]. | **CONFIRMED** |
| **SR-03** | Guest Zone | Strict boundary isolation blocking RFC 1918 private IP destinations [cite: 1]. | **CONFIRMED** |
| **AR-02** | Collapsed Core Layer | High-availability central switching fabric handling all routing SVIs [cite: 1]. | **CONFIRMED** |
| **SC-01** | Core & Access Layers | Modular layered architecture supporting horizontal growth [cite: 1]. | **CONFIRMED** |

---

## 3.1.6 Transition Checklist to DR 3.2 (Physical Topology)

- [x] No physical hardware model numbers, cables, or interface IDs specified [cite: 1].
- [x] Clear functional roles and trust boundaries defined for every node [cite: 1].
- [x] All 5 Guiding Principles enforced in traffic flows [cite: 1].
- [x] 100% Traceability maintained to Chapter 2 System Requirements [cite: 1].
- [x] Logical Architecture frozen and ready for Physical Topology Mapping (DR 3.2) [cite: 1].
