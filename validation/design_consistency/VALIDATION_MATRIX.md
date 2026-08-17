# VALIDATION MATRIX
## Enterprise Network Infrastructure Blueprint — Design Consistency & Implementation Validation

**Validation scope:** Batch 1–10  
**Purpose:** Cross-check extracted design evidence, configuration evidence, implementation dependencies, and unresolved design conditions before Packet Tracer implementation.

---

## 1. DOCUMENTATION CONFLICT REGISTER

| ID | Category | Source A | Source B | Conflict / Finding | Impact | Status | Implementation Decision |
|---|---|---|---|---|---|---|---|
| **CON-001** | Architecture / HA | `dr3_2_physical_device_inventory.csv` — `CORE-L3-02` described as linked via **StackWise/LACP** with `CORE-L3-01` | `docs_Design_Review_3_7_High_Availability.md` — **Multi-Chassis VSS / Stacking Fabrics excluded** | Core redundancy model is contradictory: stacking appears assumed in inventory but excluded from HA design | If stacking is not active, the two cores are independent. No HSRP/VRRP or dynamic routing is defined to provide redundant gateway operation | **UNRESOLVED** | **Do not silently enable stacking/VSS.** Implementation must explicitly document the chosen simulation model. |
| **CON-002** | Capacity / Physical topology | `research_datasets_asset_inventory.csv` — **80 DEV + 20 QA + 10 HR + 10 FIN** endpoints | `research_datasets_dr3_4_switch_port_plan.csv` — only **16 DEV + 4 QA** ports on F2 and **8 HR + 8 FIN** ports on F1 | Allocated access ports are insufficient for the declared endpoint inventory | Physical design cannot connect the declared endpoint population | **UNRESOLVED** | Treat current switch-port assignment as a **representative simulation model**, not a physically complete 150-user deployment. Do not fabricate additional switches/ports in Validation. |
| **CON-003** | Port allocation | `research_datasets_dr3_2_port_allocation_strategy.csv` — `Fa0/13–20` reserved for Voice/AP; `Fa0/21–24` for CCTV/Printers | `research_datasets_dr3_4_switch_port_plan.csv` — F2 `Fa0/1–16` used for DEV; F3 `Fa0/17–24` used for MDF servers | Actual port assignments overlap the global service-port allocation strategy | AP/Voice/CCTV/Server physical placement cannot simultaneously satisfy both documents | **UNRESOLVED** | Preserve both sources. Resolve during **Implementation Decision Register** before cabling those endpoints. |
| **CON-004** | Security policy | `research_datasets_acl_policy_matrix.csv` — `ACL_HR_IN` denies HR → Finance and HR → Dev | Same policy does **not explicitly deny HR → QA (`10.10.20.0/24`)** | HR-to-QA boundary is not explicitly enforced | Depending on routing/ACL behavior, HR may reach QA resources contrary to the intended segmentation model | **UNRESOLVED** | Treat as a **security design gap**. Do not silently add the deny rule to the original design evidence. |
| **CON-005** | Security policy coverage | ACL matrix defines inbound ACLs for DEV, FIN, HR, GUEST | QA VLAN 20 and Executive VLAN 50 have no corresponding inbound SVI ACL | QA and Executive segments lack explicit inbound SVI policy | Their traffic may reach internal networks according to routing/default policy rather than an explicit authorization boundary | **UNRESOLVED** | Flag as **missing security control coverage**. Decision required before claiming complete segmentation. |

---

# 2. DESIGN GAP / UNSPECIFIED REGISTER

These are not contradictions. The source material simply does not provide enough information to complete the physical/implementation model.

| ID | Parameter | Missing Information | Impact | Source-supported workaround / next action | Status |
|---|---|---|---|---|---|
| **GAP-001** | Firewall external WAN IP | `FW-EDGE-01` external interface address | WAN routing/NAT path cannot be completely instantiated | Implementation may define a lab-only transit network **after explicit implementation decision** | **UNSPECIFIED** |
| **GAP-002** | Edge-router WAN addressing | IPs for `RTR-EDGE-01` interfaces toward firewall/ISP | Complete WAN path cannot be configured | Lab transit addressing may be introduced during implementation, but must be labelled **LAB WORKAROUND** | **UNSPECIFIED** |
| **GAP-003** | ISP public address block | Actual ISP-assigned public block is absent | NAT/PAT/public egress cannot be validated as a real deployment | Use a clearly labelled simulation-only public/test network if implementation requires it | **UNSPECIFIED** |
| **GAP-004** | Core interconnect | Exact interface range, speed and medium between `CORE-L3-01` and `CORE-L3-02` | Physical redundant core path is undefined | Current proposal: `Gi0/23–Gi0/24`, but this remains an **implementation proposal**, not extracted fact | **UNSPECIFIED** |
| **GAP-005** | AP/IP-phone ports | Floor 2/3 AP and phone switchport assignments absent | AP/phone physical implementation incomplete | Existing reserved service range may be considered during implementation, but cannot be promoted to source fact | **UNSPECIFIED** |
| **GAP-006** | CCTV ports | 16 CCTV assets exist but individual switchports are not assigned | CCTV physical topology cannot be completely reproduced | Implementation must explicitly decide how representative CCTV endpoints are modelled | **UNSPECIFIED** |
| **GAP-007** | PoE budget | Exact physical PoE allocation/budget per switch not documented | Real hardware capacity cannot be validated from current evidence | Packet Tracer may not represent physical power constraints; mark as **simulation limitation** if applicable | **UNSPECIFIED** |

---

# 3. CONFIGURATION / DESIGN CROSS-CHECK REGISTER

The five existing `.cfg` files remain **original implementation evidence**. They are not to be overwritten merely because Validation discovers a discrepancy. The extraction rules explicitly require config-vs-design differences to be reported without modifying either source.

| ID | Validation Area | Evidence Being Compared | Finding | Classification | Action |
|---|---|---|---|---|---|
| **CFG-001** | Core HA | Core inventory / HA design vs existing `.cfg` | Stacking/VSS assumption must be reconciled with HA scope | Design/configuration consistency issue | Preserve original `.cfg`; resolve in Implementation Decision Register |
| **CFG-002** | L3 gateway | `CORE-L3-01` SVI design vs core configurations | `CORE-L3-01` is defined as active L3 gateway; `CORE-L3-02` lacks corresponding active SVI gateway configuration except management | Potential intentional asymmetry, but requires explicit architectural decision | Do not "fix" CORE-02 automatically |
| **CFG-003** | ACL coverage | ACL policy matrix vs ACL configuration | Existing policy set covers DEV/FIN/HR/GUEST but does not establish inbound ACL coverage for QA/EXEC | Design coverage gap | Keep original configs; implementation decision required |
| **CFG-004** | Access-port allocation | Port allocation strategy vs switch configurations | Some configured endpoint ranges overlap reserved service ranges | Configuration/design discrepancy | Preserve original config; resolve affected interfaces before final implementation |
| **CFG-005** | Endpoint capacity | Asset inventory vs switchport configuration | Configured access-port capacity is much smaller than declared endpoint population | Physical-model discrepancy | Treat as simulation scope/capacity issue, not as evidence to fabricate more ports |

---

# 4. SECURITY VALIDATION REGISTER

| ID | Security Control | Expected Boundary | Current Evidence | Finding | Severity | Action |
|---|---|---|---|---|---|---|
| **SEC-001** | Port Security | User access ports limited to max 2 sticky MACs | `switchport port-security`, maximum 2, sticky, restrict | Control is explicitly defined | — | Validate in implementation |
| **SEC-002** | DHCP Snooping | User VLANs protected; uplinks trusted | Snooping enabled on VLANs 10–90; uplinks trusted | Control is defined | — | Validate rogue-DHCP scenario |
| **SEC-003** | BPDU Guard / PortFast | User edge ports protected from rogue switching | PortFast + BPDU Guard on user ports | Control is defined | — | Validate edge-port behavior |
| **SEC-004** | Guest isolation | VLAN 90 should not reach RFC1918 enterprise networks | `ACL_GUEST_IN` explicitly defines RFC1918 blocking | Policy is defined | — | Validate after WAN/routing path exists |
| **SEC-005** | HR → QA | HR should have restricted inter-VLAN access | No explicit HR → QA deny identified | **Security gap** | HIGH | Resolve before claiming complete segmentation |
| **SEC-006** | QA → internal networks | QA has no inbound SVI ACL | No explicit boundary policy | **Security gap** | HIGH | Define intended QA authorization policy |
| **SEC-007** | Executive → internal networks | Executive VLAN has no inbound SVI ACL | No explicit boundary policy | **Security gap** | HIGH | Define intended Executive authorization policy |

---

# 5. ROUTING / AVAILABILITY VALIDATION

| ID | Area | Expected Design | Validation Finding | Status |
|---|---|---|---|---|
| **RT-001** | Inter-VLAN routing | `CORE-L3-01` performs SVI routing | Explicitly defined with `ip routing` and SVI gateways | **CONSISTENT** |
| **RT-002** | Internet egress | Default route via `10.10.70.2` | Explicitly defined | **CONSISTENT** |
| **RT-003** | Core redundancy | Two-core architecture | Gateway redundancy mechanism is not fully defined because stacking/VSS is contradictory and no FHRP/dynamic routing is documented | **GAP / CONFLICT** |
| **RT-004** | EtherChannel | LACP active bundles from access toward core | EtherChannel is explicitly defined | **CONSISTENT at design level** |
| **RT-005** | Core-to-core link | Redundant physical interconnect expected by some implementation assumptions | Exact interface/medium not specified | **UNSPECIFIED** |

---

# 6. VLAN / LAYER-2 VALIDATION

| ID | Area | Finding | Classification |
|---|---|---|---|
| **L2-001** | VLAN inventory | VLANs 10,20,30,40,50,60,70,80,90 + Native 999 are consistently represented | **CONSISTENT** |
| **L2-002** | Native VLAN | VLAN 999 used as isolated native VLAN | **CONSISTENT** |
| **L2-003** | Trunk allowed list | VLAN 1 excluded; VLANs 10–90 allowed | **CONSISTENT** |
| **L2-004** | Rapid PVST+ | Rapid PVST+ defined globally | **CONSISTENT** |
| **L2-005** | Root bridge | CORE-L3-01 primary / CORE-L3-02 secondary | **CONSISTENT at STP-design level** |
| **L2-006** | Access/service ports | Global port-allocation strategy conflicts with switchport plan | **CONFLICT** |
| **L2-007** | Endpoint capacity | Port plan cannot accommodate declared asset count | **CONFLICT** |

---

# 7. INFERENCE REGISTER

These are **not facts** and must never be presented as directly extracted design decisions.

| ID | Inference | Evidence Basis | Confidence | Treatment |
|---|---|---|---|---|
| **INF-001** | `CORE-L3-02` may function primarily as a Layer-2 standby rather than an active L3 gateway | Its documented configuration lacks active SVI gateway addresses except management VLAN 70 | Medium | Label **INFERRED** |
| **INF-002** | `ACC-F3-01` uplinks may use copper because it is co-located with the core in the Floor 3 MDF | Physical co-location described in topology documentation | Medium | Label **INFERRED** |
| **INF-003** | ACL processing on Core SVI may benefit from hardware TCAM offloading | Routing/decision evidence identifies hardware processing | Medium | Label **INFERRED**; do not present as measured performance |
| **INF-004** | Guest VLAN should use public DNS rather than internal DNS | Guest isolation requirement + IP governance interpretation | Medium | Label **INFERRED** until explicitly documented |

---

# 8. IMPLEMENTATION DECISION REGISTER

This is the important addition before Packet Tracer.

Validation identifies problems; this table records what will actually be done.

| ID | Trigger | Implementation Decision | Source Status | Requires Design Source Modification? |
|---|---|---|---|---|
| **DEC-001** | CON-001 Core stacking conflict | Select and document one explicit Packet Tracer core-redundancy model | Implementation decision | **NO** — preserve original evidence |
| **DEC-002** | CON-002 port capacity | Use representative endpoints rather than modelling all declared physical endpoints | Simulation scope decision | **NO** |
| **DEC-003** | CON-003 port overlap | Resolve actual interfaces used in Packet Tracer and record the mapping separately | Implementation decision | **NO** |
| **DEC-004** | CON-004 HR → QA gap | Decide whether HR → QA should be denied before final ACL implementation | Security design decision | **NO** until formally adopted |
| **DEC-005** | CON-005 QA/EXEC ACL absence | Define whether QA/EXEC require explicit inbound segmentation policies | Security design decision | **NO** until formally adopted |
| **DEC-006** | GAP-001–003 WAN addressing | Introduce lab-only transit addressing if complete WAN simulation is required | Simulation workaround | **NO** |
| **DEC-007** | GAP-004 core interconnect | Choose physical interface(s) for the simulated core interconnect | Implementation decision | **NO** |
| **DEC-008** | GAP-005–006 endpoint service ports | Select representative AP/phone/CCTV connections | Implementation decision | **NO** |
| **DEC-009** | GAP-007 PoE budget | Treat physical PoE budget as outside Packet Tracer fidelity unless explicitly simulated | Simulation limitation | **NO** |

---

# 9. VALIDATION STATUS SUMMARY

| Category | Count | Status |
|---|---:|---|
| Documentation / Design Conflicts | **5** | UNRESOLVED |
| Unspecified / Design Gaps | **7** | OPEN |
| Config-vs-Design Checks | **5** | REVIEW REQUIRED |
| Security Findings | **7** | 3 major coverage gaps |
| Inferences | **4** | INFORMATIONAL |
| Implementation Decisions Required | **9** | OPEN |
| Clearly Consistent Core Design Areas | VLAN/L2, SVI routing, STP, LACP, basic access security | READY FOR IMPLEMENTATION |

---

# 10. FINAL VALIDATION GATE

The project should **NOT** claim:

> "The design is internally consistent and production-ready."

The defensible statement is:

> **"The design evidence has been cross-validated across the 10-batch extraction pipeline. Five unresolved documentation/design conflicts, seven unspecified implementation parameters, and several security/configuration coverage gaps were identified and isolated from the original evidence. Implementation decisions are therefore maintained separately from the source design."**

This preserves the evidence chain:

```text
SOURCE DOCUMENTS
      │
      ▼
BATCH 1–8 DESIGN EVIDENCE
      │
      ▼
BATCH 9 CONFIGURATION CROSS-CHECK
      │
      ▼
BATCH 10 SYNTHESIS
      │
      ▼
VALIDATION MATRIX
 ┌────┴──────────┐
 │               │
Conflicts      Gaps
 │               │
 └──────┬────────┘
        ▼
IMPLEMENTATION DECISION REGISTER
        │
        ▼
PACKET TRACER IMPLEMENTATION
        │
        ▼
EXECUTED VALIDATION TESTS
```

**Rule:** Original source files and original `.cfg` files remain untouched. The implementation baseline is derived **after** validation, not by rewriting the historical evidence.