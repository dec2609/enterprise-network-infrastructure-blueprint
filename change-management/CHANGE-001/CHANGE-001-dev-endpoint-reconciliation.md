# CHANGE RECORD: CHANGE-001

**Title:** Physical Endpoint & Port-Security Reconciliation for DEV-PC-01  
**Category:** Implementation Correction & Baseline Reconciliation  
**Target Devices:** `ACC-F1-01`, `ACC-F2-01`  
**Author:** Network & Security Engineering Team  
**Status:** `Closed / Implemented & Revalidated`  

---

## 1. Problem Statement & Deviation Discovery
During the post-implementation audit and baseline validation phase of the multi-tier enterprise network, a discrepancy between the documented physical design and the actual Packet Tracer implementation was identified:
* **Documented Baseline:** `DEV-PC-01` (Software Development workstation, VLAN 10) was designated to attach to the Floor 2 Access Switch (`ACC-F2-01 / FastEthernet0/1`).
* **Actual State Discovered:** `DEV-PC-01` was physically cabled to Floor 1 Access Switch (`ACC-F1-01 / FastEthernet0/1`), where it learned a sticky MAC address on a port allocated for HR Department (VLAN 30).
* **Root Cause:** Manual cabling misallocation during Phase 4 access layer deployment in Cisco Packet Tracer.

---

## 2. Blast Radius & Scope Control
To maintain zero impact on unaffected production zones, strict change boundaries were established:
* **In-Scope (Impacted):**  
  * `ACC-F1-01`: Port `FastEthernet0/1` (De-register stale MAC, restore baseline for HR).  
  * `ACC-F2-01`: Port `FastEthernet0/1` (Re-cable endpoint, configure Port Security & Sticky MAC for DEV).
* **Frozen / Out-of-Scope (Zero Modification):**  
  * Core Switches (`CORE-L3-01`, `CORE-L3-02`), Floor 3 Switch (`ACC-F3-01`).  
  * Edge Router (`RTR-EDGE-01`) and Firewall (`FW-EDGE-01`).  
  * VLAN Subnets, SVI IP assignments, Inter-VLAN Routing, DHCP Pools, and ACL Policies.

---

## 3. Implementation Steps (Execution Log)

### Step 1: Reconstruct Pre-Change Artifacts & Clear Stale State on Switch F1
* Captured pre-change state into immutable audit logs.
* Removed stale sticky MAC binding and restored intended HR baseline on `ACC-F1-01`:

```cisco
ACC-F1-01# configure terminal
ACC-F1-01(config)# interface FastEthernet0/1
ACC-F1-01(config-if)# no switchport port-security mac-address sticky
ACC-F1-01(config-if)# description HR-PC-01 Connection
ACC-F1-01(config-if)# switchport access vlan 30
ACC-F1-01(config-if)# switchport port-security mac-address sticky
ACC-F1-01(config-if)# exit
ACC-F1-01(config)# exit
```

### Step 2: Physical Cable Relocation & Port Provisioning on Switch F2
* Physically relocated the patch cable of `DEV-PC-01` from `ACC-F1-01:Fa0/1` to `ACC-F2-01:Fa0/1`.
* Configured access mode, VLAN 10, PortFast, BPDU Guard, and Port-Security on `ACC-F2-01`:

```cisco
ACC-F2-01# configure terminal
ACC-F2-01(config)# interface FastEthernet0/1
ACC-F2-01(config-if)# description Software Developer PC - Primary
ACC-F2-01(config-if)# switchport mode access
ACC-F2-01(config-if)# switchport access vlan 10
ACC-F2-01(config-if)# spanning-tree portfast
ACC-F2-01(config-if)# spanning-tree bpduguard enable
ACC-F2-01(config-if)# switchport port-security
ACC-F2-01(config-if)# switchport port-security maximum 1
ACC-F2-01(config-if)# switchport port-security violation restrict
ACC-F2-01(config-if)# switchport port-security mac-address sticky
ACC-F2-01(config-if)# exit
ACC-F2-01(config)# exit
```

---

## 4. Post-Change Verification & Audit Evidence

| Test Scenario | Target / Destination | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **L2 Port Security Binding** | ACC-F2-01 Fa0/1 | Learn MAC 0001.4335.147D | Secure-up, MAC bound | **PASS** |
| **DHCP / IP Lease** | DEV-PC-01 | Receive IP in 10.10.10.0/24 | 10.10.10.11 /24 | **PASS** |
| **Default Gateway Ping** | CORE-L3-01 (10.10.10.1) | 0% packet loss | 5/5 packets received | **PASS** |
| **Dev Server Connectivity** | Git Server (10.10.60.21) | Reachable via Core Routing | 5/5 packets received | **PASS** |
| **ACL Policy Validation** | Outside Edge / Management | Follow ACL_DEV_IN rules | Enforced as specified | **PASS** |

---

## 5. Artifacts Reconciled
The following project artifacts have been synchronized with the post-change state:
1. `implementation/configs/03_ACC-F1-01_implemented.cfg` (Fa0/1 assigned to VLAN 30 HR)
2. `implementation/configs/04_ACC-F2-01_implemented.cfg` (Fa0/1 assigned to VLAN 10 DEV)
3. `datasets/network/switch_port_plan.csv` (Mapped DEV-PC-01 to ACC-F2-01:Fa0/1)
4. `docs/03_network_design/physical_topology.md` (Updated Floor 2 deployment map)
5. `docs/03_network_design/configuration_traceability.md` (Updated requirement mapping)
6. `implementation/verification/01_connectivity_matrix.md` (Recorded test execution evidence)
