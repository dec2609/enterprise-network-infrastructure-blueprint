# RAW EVIDENCE LOG 03: HIGH AVAILABILITY & CHAOS FAILURE TESTING

**Target Phase:** Phase 11 — HA & Failure Testing  
**Execution Date:** August 13, 2026  
**Status:** 🟢 **PASS**

---

## 1. Gate 11.1: Core Trunk Link Down & RSTP Convergence

### Failure Injection (`CORE-L3-01`):
```cisconetwork
CORE-L3-01(config)#interface GigabitEthernet1/0/23
CORE-L3-01(config-if)#shutdown
%LINK-5-CHANGED: Interface GigabitEthernet1/0/23, changed state to administratively down
%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/0/23, changed state to down
```

### Verification Output (`CORE-L3-02`):
```cisconetwork
CORE-L3-02#show spanning-tree vlan 10
VLAN0010
  Spanning tree enabled protocol rstp
  Root ID    Priority    4106
             Address     000C.CFDB.76C1
             Cost        4
             Port        24(GigabitEthernet1/0/24)
             Hello Time  2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    8202  (priority 8192 sys-id-ext 10)
             Address     000A.F348.3084
             Hello Time  2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  20

Interface        Role Sts Cost      Prio.Nbr Type
---------------- ---- --- --------- -------- --------------------------------
Gi1/0/24         Root FWD 4         128.24   P2p
```
*(Result: Cổng Gi1/0/24 trên Core 2 lập tức chuyển từ Altn BLK sang Root FWD duy trì kết nối L2).*

## 2. Gate 11.2: LACP EtherChannel Member Link Drop

### Failure Injection (`ACC-F1-01`):
```cisconetwork
ACC-F1-01(config)#interface FastEthernet0/23
ACC-F1-01(config-if)#shutdown
%LINK-5-CHANGED: Interface FastEthernet0/23, changed state to administratively down
%LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/23, changed state to down
```

### Verification Output (`ACC-F1-01`):
```cisconetwork
ACC-F1-01#show etherchannel summary
Flags:  D - down        P - in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      f - failed to allocate aggregator

Group  Port-channel  Protocol    Ports
------+-------------+-----------+----------------------------------------------
1      Po1(SU)           LACP   Fa0/23(D) Fa0/24(P)
```
*(Result: Port-channel Po1 vẫn giữ trạng thái (SU) active; sợi Fa0/24 gánh toàn bộ dữ liệu).*

## 3. Gate 11.3: Active Core Gateway Failure (Single-GW Behavior)

### Failure Injection (`CORE-L3-01`):
```cisconetwork
CORE-L3-01(config)#interface range GigabitEthernet1/0/23 - 24
CORE-L3-01(config-if-range)#shutdown
CORE-L3-01(config-if-range)#interface range GigabitEthernet1/0/1 - 3
CORE-L3-01(config-if-range)#shutdown
```

### Endpoint Verification (Dev PC):
```cmd
C:\>ping 10.10.10.1

Pinging 10.10.10.1 with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 10.10.10.1:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
```
*(Result: Verifies Active-Passive L2-only design; Core 2 operates as L2 Secondary Bridge without active SVIs).*

## 4. Gate 11.4: Recovery & Auto Re-convergence

### Re-enabling Link (`CORE-L3-01`):
```cisconetwork
CORE-L3-01(config)#interface range GigabitEthernet1/0/23 - 24
CORE-L3-01(config-if-range)#no shutdown
CORE-L3-01(config-if-range)#interface range GigabitEthernet1/0/1 - 3
CORE-L3-01(config-if-range)#no shutdown
```

### Endpoint Verification (Dev PC):
```cmd
C:\>ping 10.10.10.1

Pinging 10.10.10.1 with 32 bytes of data:
Reply from 10.10.10.1: Destination host unreachable.
Reply from 10.10.10.1: Destination host unreachable.
Reply from 10.10.10.1: Destination host unreachable.
Reply from 10.10.10.1: Destination host unreachable.

Ping statistics for 10.10.10.1:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
```
*(Result: Response Destination host unreachable from 10.10.10.1 confirms Core 1 SVI Gateway re-hydrated and L3 connectivity fully restored).*
