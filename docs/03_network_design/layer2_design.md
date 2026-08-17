# DESIGN REVIEW 3.4: LAYER-2 NETWORK DESIGN (VLAN, TRUNKING & STP)
**Project:** Enterprise Network Infrastructure Blueprint  
**Phase:** System Design & Implementation Phase (Chapter 3)  
**Document Focus:** Broadcast Domain Isolation, Trunking Security, Spanning-Tree Topology & Port Allocation  
**Parent Reviews:** Design Review 3.1 (Logical Arch), 3.2 (Physical Topology), & 3.3 (IP Addressing Plan)

---

## 3.4.1 Overview & Design Objectives

Design Review 3.4 establishes the Layer 2 switching architecture for **ABC Software Solutions**. This review bridges physical topology decisions into a structured broadcast isolation design prior to Layer 3 routing configuration in DR 3.5 [cite: 1].

**Core Objectives:**
* **O1. Broadcast Isolation:** Partition Layer 2 broadcast domains by business department to eliminate unneeded broadcast traffic [cite: 1].
* **O2. Security Segmentation:** Enforce hard Layer 2 isolation preventing direct communication between untrusted, development, and sensitive subnets [cite: 1].
* **O3. Scalability:** Support seamless addition of future VLANs without altering core switching links [cite: 1].
* **O4. Deterministic Organization:** Align VLAN IDs directly with IP subnets established in DR 3.3 [cite: 1].
* **O5. Loop Prevention:** Guarantee a loop-free Layer 2 topology via Rapid Spanning Tree Protocol (RSTP IEEE 802.1w) [cite: 1].

---

## 3.4.2 Enterprise VLAN Plan & Trust Mapping Table

VLAN IDs align 1-to-1 with the IP addressing scheme from **Design Review 3.3** and security zones from **Design Review 2.3** [cite: 1, 3, 7]:

| VLAN ID | VLAN Name | Department / Purpose | Associated Subnet (DR 3.3) | Mapped Trust Zone (DR 2.3) | Operational Mode |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **10** | **DEV** | Software Development | `10.10.10.0/24` [cite: 7] | Dev & QA Zone (Trust ⭐⭐⭐) [cite: 3] | Active / Access |
| **20** | **QA** | Quality Assurance Testing | `10.10.20.0/24` [cite: 7] | Dev & QA Zone (Trust ⭐⭐⭐) [cite: 3] | Active / Access |
| **30** | **HR** | Human Resources | `10.10.30.0/25` [cite: 7] | HR Zone (Trust ⭐⭐⭐⭐) [cite: 3] | Active / Access |
| **40** | **FIN** | Finance & Payroll | `10.10.40.0/25` [cite: 7] | Finance Zone (Trust ⭐⭐⭐⭐⭐) [cite: 3] | Active / Access |
| **50** | **EXEC** | Executive Board | `10.10.50.0/25` [cite: 7] | Management Zone (Trust ⭐⭐⭐⭐) [cite: 3] | Active / Access |
| **60** | **SERVER** | Application Servers | `10.10.60.0/24` [cite: 7] | Server Zone (Trust ⭐⭐⭐⭐⭐) [cite: 3] | Active / Access |
| **70** | **MGMT** | Infrastructure Mgmt | `10.10.70.0/24` [cite: 7] | Infrastructure Zone (Trust ⭐⭐⭐⭐⭐) [cite: 3] | Active / Access |
| **80** | **VOICE** | IP Phones & CCTV | `10.10.80.0/24` [cite: 7] | IoT & Security Zone (Trust ⭐⭐) [cite: 3] | Active / Access |
| **90** | **GUEST** | Visitor Wi-Fi | `10.10.90.0/24` [cite: 7] | Guest Zone (Trust ⭐) [cite: 3] | Active / Access |
| **999** | **NATIVE** | Unused Native Identifier | *No IP Assigned* [cite: 1] | Infrastructure Base [cite: 1] | Trunk Native Only [cite: 1] |

---

## 3.4.3 Switch Role Definition & Port Allocation Plan

### **Switch Role Definition**
* **Core Switching Fabric (`CORE-L3-01/02`):** Dedicated exclusively to SVI routing, Layer 3 gateway termination, and trunk aggregation [cite: 1]. No user endpoints connect directly to Core Switches [cite: 1].
* **Access Layer Switches (`ACC-F1/F2/F3`):** Dedicated to endpoint connection, VLAN membership tagging, PortFast, BPDU Guard, and edge security controls [cite: 1].

### **Switch Port Allocation Matrix**

| Switch Hostname | Port Range | Target Endpoint Category | VLAN Membership | Port Mode | Edge Security Controls |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **`ACC-F1-01`** | `Fa0/1 - Fa0/8` | HR Workstations | VLAN 30 | Access | PortFast, BPDU Guard, Port Security [cite: 1] |
| **`ACC-F1-01`** | `Fa0/9 - Fa0/16` | Finance Workstations | VLAN 40 | Access | PortFast, BPDU Guard, Port Security [cite: 1] |
| **`ACC-F1-01`** | `Fa0/17 - Fa0/20` | Wireless APs & IP Phones | VLAN 80 / 90 | Multi-VLAN | 802.3at PoE+, BPDU Guard [cite: 1] |
| **`ACC-F1-01`** | `Gi0/1 - Gi0/2` | Dual Uplinks to Core | 10,20,30,40,50,60,70,80,90 | Trunk (802.1Q) | Native VLAN 999, Nonegotiate [cite: 1] |
| **`ACC-F2-01`** | `Fa0/1 - Fa0/16` | Developer PCs | VLAN 10 | Access | PortFast, BPDU Guard, Port Security [cite: 1] |
| **`ACC-F2-01`** | `Fa0/17 - Fa0/20` | QA Testing PCs | VLAN 20 | Access | PortFast, BPDU Guard, Port Security [cite: 1] |
| **`ACC-F2-01`** | `Gi0/1 - Gi0/2` | Dual Uplinks to Core | 10,20,30,40,50,60,70,80,90 | Trunk (802.1Q) | Native VLAN 999, Nonegotiate [cite: 1] |
| **`ACC-F3-01`** | `Fa0/1 - Fa0/8` | Executive Laptops | VLAN 50 | Access | PortFast, BPDU Guard, Port Security [cite: 1] |
| **`ACC-F3-01`** | `Fa0/9 - Fa0/16` | IT Department PCs | VLAN 70 | Access | PortFast, BPDU Guard, Port Security [cite: 1] |
| **`ACC-F3-01`** | `Fa0/17 - Fa0/24` | MDF Servers | VLAN 60 | Access | PortFast, Port Security [cite: 1] |
| **`ACC-F3-01`** | `Gi0/1 - Gi0/2` | Dual Uplinks to Core | 10,20,30,40,50,60,70,80,90 | Trunk (802.1Q) | Native VLAN 999, Nonegotiate [cite: 1] |

---

## 3.4.4 Trunking Strategy & Native VLAN 999 Security

1. **IEEE 802.1Q Encapsulation Standard:** All trunk links connecting Access Switches to the Core Switch pair enforce 802.1Q tagging [cite: 1].
2. **Explicit Allowed VLAN List:** Trunk ports strictly restrict permitted VLANs to `10,20,30,40,50,60,70,80,90` [cite: 1]. The command `switchport trunk allowed vlan all` is prohibited [cite: 1].
3. **Dedicated Native VLAN 999:** Default VLAN 1 is stripped from trunk negotiation [cite: 1]. **`VLAN 999`** is created as an unrouted, unused Native VLAN to mitigate **VLAN Hopping & Double Tagging attacks** [cite: 1].
4. **Dynamic Trunking Protocol (DTP) Prohibition:** Auto-negotiation is disabled on all switch ports (`switchport nonegotiate` on trunks, `switchport mode access` on edge ports) to prevent rogue trunk formation [cite: 1].

---

## 3.4.5 Spanning-Tree Architecture (Rapid PVST+ 802.1w)

To ensure fault recovery under 2 seconds during link outages, the network deploys **Rapid Per-VLAN Spanning Tree Plus (Rapid PVST+)** [cite: 1]:

* **Primary Root Bridge:** `CORE-L3-01` configured with priority `4096` across all VLANs [cite: 1].
* **Secondary Root Bridge:** `CORE-L3-02` configured with priority `8192` as an automatic failover peer [cite: 1].
* **Access Layer Switches:** `ACC-F1/F2/F3` remain at default priority `32768` [cite: 1].

---

## 3.4.6 Layer 2 Security Controls & Edge Protection

* **PortFast Enablement:** `spanning-tree portfast` enabled on all end-user Access ports to bypass Listening/Learning states, granting immediate DHCP IP acquisition [cite: 1].
* **BPDU Guard Protection:** `spanning-tree bpduguard enable` enforced on all PortFast access ports [cite: 1]. If an unauthorized switch or bridge protocol data unit (BPDU) is detected, the port immediately transitions to `err-disable` status [cite: 1].
* **Unused Port Parking:** All unassigned switch ports are explicitly shut down (`shutdown`) and assigned to isolated `VLAN 999` [cite: 1].

---

## 3.4.7 Transition Checklist to DR 3.5 (Layer-3 Routing)

- [x] Enterprise VLAN Plan mapped to Trust Zones and IP subnets [cite: 1, 3, 7].
- [x] Switch Port Allocation Matrix defined for all 3 building floors [cite: 1].
- [x] 802.1Q Trunking with explicit allowed list and Native VLAN 999 configured [cite: 1].
- [x] Rapid PVST+ Root Bridge priorities established [cite: 1].
- [x] PortFast, BPDU Guard, and DTP prohibition specified [cite: 1].
- [x] Layer 2 Architecture frozen and ready for Layer 3 SVI & Inter-VLAN Routing (DR 3.5) [cite: 1].
