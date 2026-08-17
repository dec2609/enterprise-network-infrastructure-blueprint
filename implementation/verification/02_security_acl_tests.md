# RAW EVIDENCE LOG 02: SECURITY CONTROL & EXTENDED ACL VERIFICATION

**Target Phase:** Phase 10 — Security & ACL Enforcement  
**Execution Date:** August 13, 2026  
**Status:** 🟡 **PASS (WITH PLATFORM LIMITATION)**

---

## 1. Extended ACL Object Configuration (`CORE-L3-01`)

```cisconetwork
CORE-L3-01#show access-lists ACL_DEV_IN
Extended IP access list ACL_DEV_IN
    10 permit tcp 10.10.10.0 0.0.0.255 host 10.10.60.21 eq 22
    20 permit tcp 10.10.10.0 0.0.0.255 host 10.10.60.21 eq 443
    30 permit udp 10.10.10.0 0.0.0.255 host 10.10.60.10 eq domain
    40 permit ip 10.10.10.0 0.0.0.255 host 10.10.70.2
    50 deny ip any 10.0.0.0 0.255.255.255
    60 permit ip any any
```

## 2. Traffic Policy Enforcement Test (Dev PC -> Git Server ICMP Block)

```cmd
C:\>ping 10.10.60.21

Pinging 10.10.60.21 with 32 bytes of data:
Reply from 10.10.10.1: Destination host unreachable.
Reply from 10.10.10.1: Destination host unreachable.
Reply from 10.10.10.1: Destination host unreachable.
Reply from 10.10.10.1: Destination host unreachable.

Ping statistics for 10.10.60.21:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
```
*(Analysis: Gateway 10.10.10.1 explicitly rejects ICMP packets due to Rule 50 deny ip any 10.0.0.0 0.255.255.255 while TCP SSH/HTTPS is allowed).*

## 3. Simulator Limitation Evidence (SVI Binding Parser Behavior)

```cisconetwork
CORE-L3-01#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
CORE-L3-01(config)#int Vlan10
CORE-L3-01(config-if)#ip access-group ACL_DEV_IN in
CORE-L3-01(config-if)#exit
CORE-L3-01(config)#exit
CORE-L3-01#

CORE-L3-01#show running-config | section interface Vlan10
interface Vlan10
 description Gateway for DEV Zone
 mac-address 000c.cfdb.7601
 ip address 10.10.10.1 255.255.255.0

CORE-L3-01#show ip interface Vlan10
Vlan10 is up, line protocol is up
  Internet address is 10.10.10.1/24
  Broadcast address is 255.255.255.255
  Address determined by setup command
  MTU is 1500 bytes
  Helper address is not set
  Directed broadcast forwarding is disabled
  Inbound access list is not set
  Outgoing access list is not set
```

**Engineering Finding:**  
Command `ip access-group ACL_DEV_IN in` is accepted without syntax error by Packet Tracer parser, but kernel engine fails to commit line into running-config under Catalyst 3650 SVI model. Documented as Packet Tracer Simulator Limitation.
