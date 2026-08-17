# DESIGN REVIEW 2.3: SECURITY ZONES & TRUST BOUNDARIES
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** Engineering Design Phase (Trust Boundary & Policy Derivation)  
**Parent Reviews:** Design Review 2.1 (Business Context) & Design Review 2.2 (Asset Inventory)

---

## 2.3.1 Trust Level Definition

To establish systematic access control without hardcoding network addresses, **ABC Software Solutions** defines a 5-tier Trust Spectrum:

* **Level 5 — Critical Trust (⭐⭐⭐⭐⭐):** Core servers, core switching fabric, and financial databases. Maximum security enforcement required.
* **Level 4 — High Trust (⭐⭐⭐⭐):** Corporate executive management and HR systems handling private personnel records.
* **Level 3 — Medium Trust (⭐⭐⭐):** Primary engineering and production environments (Software Developers & QA).
* **Level 2 — Low Trust (⭐⭐):** Auxiliary connected devices (CCTV Cameras, VoIP IP Phones).
* **Level 1 — Untrusted (⭐):** External visitor endpoints, contractor devices, and unauthenticated wireless connections.

---

## 2.3.2 Security Zones Taxonomy

Assets identified in **Design Review 2.2** are mapped to 8 distinct Security Zones:

| Zone ID | Security Zone Name | Trust Rating | Mapped Assets | Inbound Policy | Outbound Policy |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **ZON-01** | **Server Zone** | ⭐⭐⭐⭐⭐ | Git Repos, CI/CD, ERP Server (`AST-11`, `AST-12`) | Restricted (Explicit ACLs) | Restricted (No Direct Internet) |
| **ZON-02** | **Infrastructure Zone** | ⭐⭐⭐⭐⭐ | Core L3 Switches, Access Switches (`AST-06`, `AST-07`) | Restricted (SSH/SNMP Mgmt Only) | Deny By Default |
| **ZON-03** | **Finance Zone** | ⭐⭐⭐⭐⭐ | Finance Workstations (`AST-04`) | Deny By Default | Permit (ERP Server, HTTPS) |
| **ZON-04** | **HR Zone** | ⭐⭐⭐⭐ | HR Workstations (`AST-03`) | Deny By Default | Permit (ERP Server, HTTPS) |
| **ZON-05** | **Management Zone** | ⭐⭐⭐⭐ | Executive Laptops (`AST-05`) | Restricted (Admin Access) | Permit (All Subnets, Internet) |
| **ZON-06** | **Dev & QA Zone** | ⭐⭐⭐ | Dev & QA PCs (`AST-01`, `AST-02`) | Peer Access Permitted | Permit (Git Repos, Internet) |
| **ZON-07** | **IoT & Security Zone** | ⭐⭐ | CCTV Cameras, IP Phones (`AST-09`, `AST-10`) | Deny By Default | Restricted (Video NVR / Voice QoS) |
| **ZON-08** | **Guest Zone** | ⭐ | Visitor & Contractor Devices (`AST-13`) | Deny All | Internet Only (Block Private IPs) |

---

## 2.3.3 Trust Boundary Analysis

Cross-zone traffic traversing different Trust Levels triggers an explicit **Trust Boundary Enforcement**:

```text
               [ Internet (External) ]
                          │
                  (Boundary: Firewall)
                          │
                [ Guest Zone (Trust 1) ]
                          │
         (Trust Boundary 1: Guest Isolation ACL)
                          │
  ────────────────────────────────────────────────────────
   [ Dev/QA Zone (Trust 3) ]   [ HR Zone (Trust 4) ]
  ────────────────────────────────────────────────────────
                          │
      (Trust Boundary 2: Core Inter-VLAN Filter ACLs)
                          │
  ────────────────────────────────────────────────────────
   [ Finance Zone (Trust 5) ]  [ Server Zone (Trust 5) ]
  ────────────────────────────────────────────────────────
                          │
   [ Infrastructure Control Plane (Trust 5 - Management) ]
```

---

## 2.3.4 Communication Matrix (Precursor to ACL Policy)

| Source \ Destination | Internet | Server Zone | Finance Zone | HR Zone | Dev Zone | Guest Zone |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dev Zone (Trust 3)** | ✅ PERMIT | ⚠️ RESTRICTED (Git Only) | ❌ DENY | ❌ DENY | ✅ PERMIT | ❌ DENY |
| **Finance Zone (Trust 5)** | ✅ PERMIT | ⚠️ RESTRICTED (ERP Only) | ✅ PERMIT | ❌ DENY | ❌ DENY | ❌ DENY |
| **HR Zone (Trust 4)** | ✅ PERMIT | ⚠️ RESTRICTED (ERP Only) | ❌ DENY | ✅ PERMIT | ❌ DENY | ❌ DENY |
| **Management Zone (Trust 4)**| ✅ PERMIT | ✅ PERMIT (Full Admin) | ⚠️ RESTRICTED | ⚠️ RESTRICTED | ✅ PERMIT | ❌ DENY |
| **Guest Zone (Trust 1)** | ✅ PERMIT | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY |
| **Server Zone (Trust 5)** | ❌ DENY | ✅ PERMIT | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY |

---

## 2.3.5 Security Design Implications (Pre-VLAN & Pre-ACL Justification)

1. **Top-Down Inference 1 (Guest Containment):**  
   Guest Zone (`ZON-08`) operates at Trust Level 1.  
   * **Design Choice:** Must be mapped to an isolated Layer 2 Broadcast Domain (VLAN) with an outbound ACL explicitly denying access to RFC 1918 private address ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).
2. **Top-Down Inference 2 (Critical Server Protection):**  
   Server Zone (`ZON-01`) operates at Trust Level 5 and houses source code and ERP databases.  
   * **Design Choice:** Direct inbound traffic from any subnet is blocked by default; only explicit port-level traffic (e.g., SSH/Git port 22, HTTPS port 443, MS SQL port 1433) is permitted via Layer 3 Access Control Lists.
3. **Top-Down Inference 3 (Cross-Departmental Lateral Isolation):**  
   Finance (`ZON-03`) and HR (`ZON-04`) must not be accessible by Developers (`ZON-06`).  
   * **Design Choice:** Enforce inter-VLAN routing controls on the Collapsed Core L3 Switch to drop lateral packets between department subnets.
