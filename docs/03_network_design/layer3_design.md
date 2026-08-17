# DESIGN REVIEW 3.5: LAYER-3 NETWORK DESIGN (INTER-VLAN ROUTING)
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** System Design & Implementation Phase (Chapter 3)  
**Document Focus:** Inter-VLAN Routing Fabric, Core SVI Gateway Plan, Traffic Flows & Default Route Egress  
**Parent Reviews:** Design Review 3.1 (Logical Arch), 3.2 (Physical), 3.3 (IP Plan), & 3.4 (Layer 2 Design)

---

## 3.5.1 Overview & Design Objectives

Design Review 3.5 establishes the Layer 3 routing fabric for **ABC Software Solutions**. This review transitions isolated Layer 2 broadcast domains (DR 3.4) into an interconnected enterprise network while establishing the Collapsed Core as the **Centralized Policy Enforcement Point** for security controls in DR 3.6 [cite: 1, 4, 8].

**Core Objectives:**
* **O1. Wire-Speed Inter-VLAN Connectivity:** Enable hardware-accelerated routing across all internal subnets via Switched Virtual Interfaces (SVIs) [cite: 1, 4].
* **O2. Centralized Gateway Architecture:** Terminate 100% of Layer 3 Default Gateways on the `CORE-L3-01/02` Collapsed Core pair [cite: 1, 4, 6].
* **O3. Centralized Policy Enforcement Point:** Designate Core SVI interfaces as the exclusive boundary for Inter-VLAN Access Control Lists (ACLs) [cite: 1, 4].
* **O4. Simplified Egress Routing:** Maintain a single deterministic default route (`0.0.0.0/0`) pointing towards the perimeter Firewall/Router [cite: 1, 6, 7].
* **O5. Bounded Failure Domains:** Ensure Layer 3 routing failure domain boundaries remain isolated to individual floor switches without affecting core backbone routing stability [cite: 1, 4, 6].

---

## 3.5.2 Routing Architecture Decision Matrix

Rather than selecting a routing mechanism by default, the architecture evaluates **Router-on-a-Stick (RoAS)** against **Layer 3 SVI Switching** based on the SME context from Chapter 2 [cite: 1, 4]:

| Evaluation Criteria | Router-on-a-Stick (RoAS) | Layer 3 SVI Switching (Collapsed Core) | Selected Architecture Choice |
| :--- | :--- | :--- | :--- |
| **Routing Throughput** | Bottlenecked by single sub-interface trunk link; CPU routed [cite: 1, 4]. | **Wire-speed ASIC switching backplane** [cite: 1, 4]. | **Layer 3 SVI Selected** [cite: 1, 4] |
| **ACL Policy Enforcement** | Software CPU-bound filtering; induces packet latency [cite: 1, 4]. | **Hardware TCAM-based ACL enforcement at wire-speed** [cite: 1, 4]. | **Layer 3 SVI Selected** [cite: 1, 4] |
| **Scalability** | Severe trunk link congestion as VLAN host counts increase [cite: 1, 4]. | **High-density SVI scalability across core switching fabric** [cite: 1, 4]. | **Layer 3 SVI Selected** [cite: 1, 4] |
| **SME Context Fit** | Suitable only for small lab environments [cite: 1, 4]. | **Optimal fit for 150-user 3-floor enterprise network** [cite: 1, 4]. | **Layer 3 SVI Selected** [cite: 1, 4] |

---

## 3.5.3 Default Gateway & Core SVI Specification Table

All 9 Switched Virtual Interfaces (SVIs) are hosted centrally on `CORE-L3-01/02` using the `.1` IP convention established in **Design Review 3.3** [cite: 1, 4, 7]:

| Interface ID | Associated VLAN | Network Subnet (DR 3.3) | Core SVI Gateway IP | Subnet Mask | Operational Function |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **`Vlan10`** | VLAN 10 (DEV) | `10.10.10.0/24` [cite: 7, 8] | **`10.10.10.1`** [cite: 7, 8] | `255.255.255.0` | Default Gateway for Software Engineering [cite: 1, 7, 8] |
| **`Vlan20`** | VLAN 20 (QA) | `10.10.20.0/24` [cite: 7, 8] | **`10.10.20.1`** [cite: 7, 8] | `255.255.255.0` | Default Gateway for QA Testing Lab [cite: 1, 7, 8] |
| **`Vlan30`** | VLAN 30 (HR) | `10.10.30.0/25` [cite: 7, 8] | **`10.10.30.1`** [cite: 7, 8] | `255.255.255.128` | Default Gateway for HR Department [cite: 1, 7, 8] |
| **`Vlan40`** | VLAN 40 (FIN) | `10.10.40.0/25` [cite: 7, 8] | **`10.10.40.1`** [cite: 7, 8] | `255.255.255.128` | Default Gateway for Finance & Payroll [cite: 1, 7, 8] |
| **`Vlan50`** | VLAN 50 (EXEC) | `10.10.50.0/25` [cite: 7, 8] | **`10.10.50.1`** [cite: 7, 8] | `255.255.255.128` | Default Gateway for Executive Management [cite: 1, 7, 8] |
| **`Vlan60`** | VLAN 60 (SERVER) | `10.10.60.0/24` [cite: 7, 8] | **`10.10.60.1`** [cite: 7, 8] | `255.255.255.0` | Default Gateway for Git, ERP, DC Servers [cite: 1, 7, 8] |
| **`Vlan70`** | VLAN 70 (MGMT) | `10.10.70.0/24` [cite: 7, 8] | **`10.10.70.1`** [cite: 7, 8] | `255.255.255.0` | Gateway for In-band Switch Management [cite: 1, 7, 8] |
| **`Vlan80`** | VLAN 80 (VOICE) | `10.10.80.0/24` [cite: 7, 8] | **`10.10.80.1`** [cite: 7, 8] | `255.255.255.0` | Default Gateway for VoIP Phones & CCTV [cite: 1, 7, 8] |
| **`Vlan90`** | VLAN 90 (GUEST) | `10.10.90.0/24` [cite: 7, 8] | **`10.10.90.1`** [cite: 7, 8] | `255.255.255.0` | Default Gateway for Untrusted Visitor Wi-Fi [cite: 1, 7, 8] |

---

## 3.5.4 Layer 3 Traffic Flow Patterns

```text
 1. INTRA-VLAN (Layer 2 Local Switching):
    Dev PC 1 ──► Access Switch ACC-F2-01 ──► Dev PC 2 (No L3 Routing Touch) [cite: 1, 8]

 2. INTER-VLAN (Layer 3 Core SVI Routing):
    Dev PC (10.10.10.100) ──► Access Switch ──► Core SVI Vlan10 (10.10.10.1)
                                                       │
                                            [ L3 Routing Engine ]
                                                       │
    Server SRV-GIT (10.10.60.21) ◄── Access Switch ◄── Core SVI Vlan60 (10.10.60.1) [cite: 1, 7, 8]

 3. INTERNET EGRESS (Default Static Route):
    Internal Host ──► Core SVI Gateway ──► Default Static Route (0.0.0.0/0)
                                                 │
    Internet Egress ◄── Edge Router (10.10.70.1) ◄── Firewall Internal IP (10.10.70.2) [cite: 1, 6, 7]
```

---

## 3.5.5 Separation of Concerns: Routing vs. Authorization

A foundational engineering principle governs Layer 3 design:

* **Layer 3 Routing (Connectivity):** SVI interfaces provide the physical/logical routing paths between subnets. Inter-VLAN routing enablement (`ip routing`) provides **reachability only** [cite: 1, 4].
* **Access Control Lists (Authorization):** Reachability does **NOT** imply permission [cite: 1, 4]. Authorization is enforced exclusively via **Inbound Extended ACLs** applied directly to Core SVI interfaces in DR 3.6 to permit or drop packets [cite: 1, 4].

---

## 3.5.6 Egress Default Route Strategy & Failure Domain Analysis

* **Perimeter Default Route Policy:** A single static default route is configured on the Core L3 Switch pointing to the internal interface of the Next-Gen Firewall [cite: 1, 6, 7]:  
  `ip route 0.0.0.0 0.0.0.0 10.10.70.2` [cite: 1, 6, 7]
* **Failure Domain Analysis:**  
  * *Access Switch Cable Cut:* Affects only local floor endpoints [cite: 1, 6, 8]. Routing across remaining floors and core server access remains operational [cite: 1, 6, 8].
  * *Core Switch Failure:* Single point of failure for all Inter-VLAN routing $ightarrow$ **Mitigated by Redundant Core Pair (`CORE-L3-01` & `CORE-L3-02`)** [cite: 1, 6].

---

## 3.5.7 Transition Checklist to DR 3.6 (Security Controls)

- [x] L3 SVI Switching selected over RoAS with explicit trade-off rationale [cite: 1, 4].
- [x] All 9 SVI Gateway IP addresses defined on Collapsed Core [cite: 1, 4, 7, 8].
- [x] Layer 3 traffic flow patterns documented for local, inter-VLAN, and internet paths [cite: 1, 7, 8].
- [x] Separation of Routing (Connectivity) and ACLs (Authorization) established [cite: 1, 4].
- [x] Static Default Route egress defined towards Firewall interface [cite: 1, 6, 7].
- [x] Layer 3 Routing Design frozen and ready for Security Control & ACL Placement (DR 3.6) [cite: 1, 4].
