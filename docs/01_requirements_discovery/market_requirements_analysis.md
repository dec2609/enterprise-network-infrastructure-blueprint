# MARKET REQUIREMENTS ANALYSIS & SCOPE DERIVATION

**Document ID:** MKT-ANALYSIS-001  
**Project:** Enterprise Network Infrastructure Blueprint  
**Status:** **APPROVED & ARCHIVED**

---

## 1. Executive Summary
This document analyzes the technical insights derived from [`requirements_discovery.md`](./requirements_discovery.md) and translates market demand keywords into concrete **System Requirements** and **Architectural Scope** for Version 1.0 of the enterprise lab.

---

## 2. Translation of Market Demand to Technical Architecture

| Market Demand Keyword | Frequency / Context | Implicit Engineering Need | Lab Blueprint Feature Mapping |
| :--- | :--- | :--- | :--- |
| **VLAN & Routing** | Explicit in 2 JDs; Implied in LAN/WAN JDs | Multi-zone broadcast containment & inter-subnet routing | 9 Production VLANs (10–90) & Centralized Core L3 SVI Routing |
| **Active Directory & Identity** | Explicit in 9 JDs | Identity-aware network segmentation & trust zones | 5 Trust Level Security Matrix (DEV, QA, HR, FIN, EXEC, GUEST) |
| **Firewall & Security** | Explicit in 3 JDs | Perimeter security & traffic filtering | Edge ASA Firewall / Router NAT Overload & Extended SVI ACLs |
| **VPN & Remote Access** | Explicit in 5 JDs | Secure egress & remote user connectivity | Transit VLAN 70 to Edge Router/Firewall Gateway |
| **DHCP & DNS Services** | Explicit in 13 JDs combined | Core IP Infrastructure Services | Centralized Infrastructure Server Zone (VLAN 60 / Git `10.10.60.21`) |

---

## 3. Scope Boundary Justification (Version 1.0)

### In-Scope Items
1. **Layer 2 Infrastructure:** Dot1Q Trunking, LACP EtherChannel, Rapid PVST+, BPDU Guard, PortFast, DHCP Snooping.
2. **Layer 3 Infrastructure:** Centralized SVI Routing on Catalyst 3650 Core Switch, Egress Default Static Route.
3. **Security Controls:** Extended Access Control Lists (ACLs) for zone isolation, Guest Zone quarantine.

### Out-of-Scope Items (Deferred to Future Work)
1. **Dynamic Routing Protocols (BGP / OSPF):** Exceeded SME scope requirements for Version 1.0.
2. **L3 Zero-Downtime HA (HSRP / VRRP):** Documented as Active-Passive L2-only limitation for Version 1.0 baseline.
