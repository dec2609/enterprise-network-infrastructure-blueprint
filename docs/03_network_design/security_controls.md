# DESIGN REVIEW 3.6: SECURITY CONTROL DESIGN
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** System Design & Implementation Phase (Chapter 3)  
**Document Focus:** SME Threat Modeling, Defense-in-Depth Layer 2/3 Controls, ACL Policies & Traceability  
**Parent Reviews:** DR 3.1 (Logical Arch), 3.3 (IP Plan), 3.4 (Layer 2 Design), & 3.5 (Layer 3 Routing)

---

## 3.6.1 Overview & Security Design Principles

Design Review 3.6 establishes the security controls framework for **ABC Software Solutions**. Rather than configuring isolated commands, this review designs a multi-layered defense model that operationalizes the **Trust Zones** from DR 2.3 and **System Security Requirements** (`SR-01..06`) from DR 2.4 [cite: 1, 3, 4].

**Core Architectural Principles:**
* **Principle 1 — Least Privilege Access:** Default deny all inter-VLAN communications. Cross-subnet traffic is permitted exclusively for business-required protocols [cite: 1, 3].
* **Principle 2 — Role-Based Segmentation:** Each department resides in a dedicated Security Zone corresponding to an isolated Layer 2/3 broadcast domain [cite: 1, 3, 7].
* **Principle 3 — Centralized Policy Enforcement:** Inter-VLAN Access Control Lists (ACLs) are centralized 100% on the Collapsed Core Layer 3 Switch SVI interfaces, executed via hardware TCAM [cite: 1, 4].
* **Principle 4 — Defense-in-Depth:** Security does not rely on a single mechanism. Layer 2 edge controls (DHCP Snooping, Port Security, BPDU Guard) complement Layer 3 boundary controls (Extended ACLs, Egress Default Route) [cite: 1, 3, 4, 6].

---

## 3.6.2 SME Threat Model & Security Control Mapping

The security architecture targets six realistic operational threats identified for a 150-user software engineering SME [cite: 1, 3, 4]:

| Threat ID | Identified Threat / Attack Scenario | Enforced Security Control | Layer | Enforcement Point |
| :---: | :--- | :--- | :---: | :--- |
| **THR-01** | Unauthorized Inter-VLAN Lateral Access [cite: 3] | Inter-VLAN Extended Access Control Lists [cite: 1, 4] | Layer 3 | Core SVI Interfaces (`Vlan10..90`) [cite: 1, 4, 8] |
| **THR-02** | Rogue DHCP Server Insertion [cite: 3] | DHCP Snooping with Untrusted Edge Ports [cite: 1, 3] | Layer 2 | Access Switches (`ACC-F1/F2/F3`) [cite: 1] |
| **THR-03** | MAC Spoofing & Unauthorized Rogue Devices [cite: 3] | Port Security (Sticky MAC, Max 2, Restrict) [cite: 1, 3] | Layer 2 | Access Switch User Ports [cite: 1] |
| **THR-04** | STP Rogue Switch BPDU Injection [cite: 1, 3] | RSTP BPDU Guard & PortFast Enablement [cite: 1, 3] | Layer 2 | Access Switch User Ports [cite: 1] |
| **THR-05** | Untrusted Guest Lateral Intrusion [cite: 3] | Guest Isolation ACL (Block RFC 1918) [cite: 1, 3] | Layer 3 | Core SVI `Vlan90` Inbound [cite: 1, 4, 8] |
| **THR-06** | Unauthorized Control Plane Probing [cite: 3, 4] | Dedicated Management VLAN 70 Restriction [cite: 1, 3, 7] | Layer 3 | Core SVI `Vlan70` Inbound [cite: 1, 4, 8] |

---

## 3.6.3 Layer 3 Security Policy Specifications (ACL Specifications)

Policy enforcement occurs via **Inbound Extended ACLs** applied to Core SVI interfaces [cite: 1, 4]:

```text
 ┌───────────────────────────────────────────────────────────────────────────┐
 │                      COLLAPSED CORE L3 SWITCHING FABRIC                   │
 │                                                                           │
 │  [ SVI Vlan10 (DEV) ]  ──► Inbound ACL ──► Permit Git/DNS/Web Only       │
 │  [ SVI Vlan30 (HR) ]   ──► Inbound ACL ──► Permit ERP/DNS/Web Only       │
 │  [ SVI Vlan40 (FIN) ]  ──► Inbound ACL ──► Permit ERP Database/DNS Only  │
 │  [ SVI Vlan90 (GUEST) ]──► Inbound ACL ──► Deny RFC1918 (Internet Only)   │
 └───────────────────────────────────────────────────────────────────────────┘
```

1. **Development Policy (`ACL_DEV_IN` on SVI `Vlan10`):**  
   * **Permit:** TCP Port 22 (SSH/Git) and Port 443 (HTTPS) to `SRV-GIT-01` (`10.10.60.21`) [cite: 1, 3, 7].  
   * **Permit:** UDP Port 53 (DNS) to `SRV-DC-01` (`10.10.60.23`) and Outbound Internet Egress [cite: 1, 3, 7].  
   * **Deny:** All access to Finance Subnet (`10.10.40.0/25`), HR Subnet (`10.10.30.0/25`), and Mgmt Subnet (`10.10.70.0/24`) [cite: 1, 3, 7].
2. **Finance Policy (`ACL_FIN_IN` on SVI `Vlan40`):**  
   * **Permit:** TCP Port 1433 (MS SQL) and Port 443 (HTTPS) to `SRV-ERP-01` (`10.10.60.22`) [cite: 1, 3, 7].  
   * **Permit:** UDP Port 53 (DNS) to `SRV-DC-01` (`10.10.60.23`) and Outbound Internet Egress [cite: 1, 3, 7].  
   * **Deny:** All access to Dev Subnet (`10.10.10.0/24`), QA Subnet (`10.10.20.0/24`), and Guest Subnet (`10.10.90.0/24`) [cite: 1, 3, 7].
3. **Guest Isolation Policy (`ACL_GUEST_IN` on SVI `Vlan90`):**  
   * **Deny:** All traffic destined to RFC 1918 private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) [cite: 1, 3].  
   * **Permit:** Any remaining outbound traffic to external public Internet destinations [cite: 1, 3].

---

## 3.6.4 Layer 2 Edge Defense Controls

* **DHCP Snooping Strategy:** Switches `ACC-F1/F2/F3` enable DHCP Snooping on VLANs 10-90 [cite: 1, 3, 7]. Uplinks `Gi0/1-2` to Core Switches are designated as **Trusted Ports** [cite: 1]. All user ports default to **Untrusted Ports**, dropping unauthorized DHCP Offers [cite: 1, 3].
* **Port Security Strategy:** User ports enforce `switchport port-security` with sticky MAC learning and a maximum limit of **2 MACs** (to accommodate 1 VoIP Phone + 1 PC pass-through) [cite: 1, 3]. Violations trigger the `restrict` or `shutdown` action [cite: 1, 3].
* **BPDU Guard & PortFast:** User edge ports configure `spanning-tree portfast` and `spanning-tree bpduguard enable` [cite: 1, 3]. Detection of an unauthorized switch BPDU frame immediately disables the port (`err-disable`) to prevent Layer 2 loops [cite: 1, 3].

---

## 3.6.5 Management Plane Protection (MPP)

* In-band administrative access (SSH v2, SNMP v3) is restricted exclusively to **Management VLAN 70 (`10.10.70.0/24`)** [cite: 1, 3, 7].
* Access attempts to switch management interfaces originating from Dev (`VLAN 10`), Finance (`VLAN 40`), or Guest (`VLAN 90`) subnets are dropped at the Core SVI boundary [cite: 1, 3, 7, 8].

---

## 3.6.6 Security Requirements Traceability Matrix

| Requirement ID | Security Objective | Planned Security Control | Enforcement Point | Validation Method (Chapter 4) |
| :---: | :--- | :--- | :--- | :--- |
| **SR-01** | Subnet Logical Isolation [cite: 4] | Inter-VLAN Extended ACLs [cite: 1, 4] | Core SVI Interfaces [cite: 1, 4, 8] | ICMP ping blocked between Dev & Finance [cite: 1, 3] |
| **SR-02** | Confidential Asset Boundary [cite: 4] | Explicit Server Port Filtering [cite: 1, 3] | Core SVI `Vlan60` Inbound [cite: 1, 4, 8] | Unpermitted port connection to ERP dropped [cite: 1, 3] |
| **SR-03** | Guest Isolation Boundary [cite: 4] | Guest Isolation ACL (Block RFC1918) [cite: 1, 3] | Core SVI `Vlan90` Inbound [cite: 1, 4, 8] | Guest pinging 10.10.10.1 rejected [cite: 1, 3, 7] |
| **SR-04** | Rogue DHCP Mitigation [cite: 4] | L2 DHCP Snooping & Untrusted Ports [cite: 1, 3] | Access Switches (`ACC-F1..F3`) [cite: 1] | Rogue DHCP Offer dropped at access port [cite: 1, 3] |
| **SR-05** | L2 Loop Suppression [cite: 4] | RSTP BPDU Guard & PortFast [cite: 1, 3] | Access Switch Edge Ports [cite: 1, 3] | Port transitions to err-disable on BPDU [cite: 1, 3] |
| **SR-06** | Control Plane Protection [cite: 4] | Dedicated Mgmt VLAN 70 Restriction [cite: 1, 3, 7] | Core SVI `Vlan70` Inbound [cite: 1, 4, 8] | Non-IT SSH attempt dropped at core SVI [cite: 1, 3, 7] |

---

## 3.6.7 Transition Checklist to DR 3.7 (High Availability)

- [x] SME Threat Model established for 6 primary risk scenarios [cite: 1, 3, 4].
- [x] Inter-VLAN Extended ACL policies defined without hardcoded CLI commands [cite: 1, 4].
- [x] Layer 2 DHCP Snooping, Port Security, and BPDU Guard controls specified [cite: 1, 3].
- [x] Management Plane Protection restricted to Management VLAN 70 [cite: 1, 3, 7].
- [x] 100% Traceability maintained to SR-01..06 requirements [cite: 1, 4].
- [x] Security Controls Design frozen and ready for High Availability Design (DR 3.7) [cite: 1, 4].
