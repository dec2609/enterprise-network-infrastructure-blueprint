# ACCEPTANCE TEST CASES SPECIFICATION

This document details the 15 formal Test Cases (TC) executed during the Phase 1–12 validation cycle.

---

## 1. Layer 2 & Physical Topology (TC-L2)

### TC-L2-01: VLAN Trunking & Dot1Q Encapsulation
* **Target:** Core-to-Access Interconnections (`CORE-L3-01` to `ACC-F1/F2/F3`).
* **Pre-conditions:** All interfaces configured as Trunk.
* **Test Steps:** Run `show interfaces trunk` on Core and Access switches.
* **Expected Result:** Allowed VLANs `10-90,999` active; encapsulation `dot1q`; Native VLAN `999`.

### TC-L2-02: LACP EtherChannel Link Aggregation
* **Target:** `ACC-F1-01` Port-Channel 1 (`Fa0/23`, `Fa0/24`).
* **Test Steps:** Run `show etherchannel summary`.
* **Expected Result:** Group 1 protocol `LACP`, status `Po1(SU)` (In Use / Layer 2), member ports marked `(P)`.

### TC-L2-03: Rapid PVST+ Root Bridge Election
* **Target:** Entire Switch Topology.
* **Test Steps:** Run `show spanning-tree vlan 10` on `CORE-L3-01` and `CORE-L3-02`.
* **Expected Result:** `CORE-L3-01` holds Root Primary for all VLANs (Priority 4096). Cổng `Gi1/0/24` trên Core 2 ở trạng thái `Altn BLK`.

### TC-L2-04: L2 Edge Defense (BPDU Guard & PortFast)
* **Target:** Access Switches Port Range (`Fa0/1`–`18`).
* **Test Steps:** Connect unauthorized switch or send BPDU into edge port.
* **Expected Result:** Edge port immediately transitions to `err-disable` upon receiving BPDU.

---

## 2. Layer 3 Routing & Connectivity (TC-L3)

### TC-L3-01: SVI Gateway Reachability
* **Target:** Core L3 SVI Gateways (`10.10.10.1` through `10.10.90.1`).
* **Test Steps:** Ping local SVI IP from respective VLAN host.
* **Expected Result:** 100% ICMP ping success rate (`4/4 Reply`).

### TC-L3-02: Inter-VLAN Routing Execution
* **Target:** Inter-Zone Communication (Dev PC `10.10.10.10` -> Git Server `10.10.60.21`).
* **Test Steps:** Initiate ICMP ping from Dev PC to Git Server.
* **Expected Result:** Successful ping responses (`Reply from 10.10.60.21`).

### TC-L3-03: Default Egress Routing
* **Target:** Edge Firewall Gateway (`10.10.70.2`).
* **Test Steps:** Ping `10.10.70.2` from internal host in VLAN 10.
* **Expected Result:** Packet routed via Core SVI 70 (`10.10.70.10`) to Firewall.

---

## 3. Security & Access Control (TC-SEC)

### TC-SEC-01: Extended ACL Traffic Filtering
* **Target:** Dev Zone (`ACL_DEV_IN`) on SVI Vlan10.
* **Test Steps:** Ping Git Server (`10.10.60.21`) from Dev PC (`10.10.10.10`).
* **Expected Result:** ICMP blocked by policy (`Destination host unreachable` returned by Gateway).

### TC-SEC-02: Guest Zone Isolation
* **Target:** Guest VLAN 90.
* **Test Steps:** Attempt ping from Guest PC (`10.10.90.10`) to Internal Server (`10.10.60.21`).
* **Expected Result:** Traffic dropped; lateral access to internal subnets prohibited.

---

## 4. High Availability & Chaos Testing (TC-HA)

### TC-HA-01: Core-to-Core Trunk Link Down Failover
* **Target:** Primary Trunk Link (`Gi1/0/23` on `CORE-L3-01`).
* **Test Steps:** Issue `shutdown` on `Gi1/0/23`. Monitor STP state on `CORE-L3-02`.
* **Expected Result:** Alternate port `Gi1/0/24` on Core 2 transitions from `Altn BLK` to `Root FWD` (RSTP Convergence).

### TC-HA-02: LACP Member Link Failure Resilience
* **Target:** `ACC-F1-01` Port-Channel 1 (`Fa0/23`).
* **Test Steps:** Shut down `Fa0/23`. Monitor continuous ping from host.
* **Expected Result:** `Po1` remains `(SU)` up; remaining port `Fa0/24(P)` carries traffic with zero packet loss.

### TC-HA-03: Active Core L3 Gateway Outage
* **Target:** Active Core Switch (`CORE-L3-01`).
* **Test Steps:** Isolate all interfaces on Core 1.
* **Expected Result:** Documented Single-Gateway limitation; traffic drops as Core 2 operates as L2 Secondary Bridge.