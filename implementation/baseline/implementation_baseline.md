# IMPLEMENTATION BASELINE (RECONCILED & FINALIZED)
> **Enterprise Network Infrastructure Blueprint — Packet Tracer Build Specification**  
> **Document Version:** v1.0-Final | **Status:** Reconciled with Implemented Codebase & Validation Matrix  
> **Governance Rule:** Historical design evidence (Batch 1–8) and 5 legacy `.cfg` files remain untouched as historical audit trails.

---

## 1. RECONCILIATION SUMMARY (XỬ LÝ DỮ LIỆU CHUẨN HÓA)

* **Legacy Configs (5 files):** `CORE-L3-01.cfg`, `ACC-F1-01.cfg`, `ACC-F2-01.cfg`, `ACC-F3-01.cfg`, `RTR-EDGE-01.cfg` (Giữ nguyên làm Historical Evidence).
* **Implemented Configs (7 files):** Sinh ra từ Baseline này để nạp trực tiếp vào Packet Tracer (`CORE-L3-01_implemented.cfg`, `CORE-L3-02_implemented.cfg`, `ACC-F1-01_implemented.cfg`, `ACC-F2-01_implemented.cfg`, `ACC-F3-01_implemented.cfg`, `RTR-EDGE-01_implemented.cfg`, `FW-EDGE-01_implemented.cfg`)[cite: 5].
* **Port Conflict Resolution (DEC-008 & LACP):** Giải quyết dứt điểm xung đột cổng `Fa0/23-24`. Các cổng `Fa0/23-24` trên tất cả Access Switches được **ưu tiên cố định 100% cho LACP Uplinks** nối lên Core[cite: 5]. CCTV Cameras được điều chỉnh sang cổng người dùng còn trống (`Fa0/19-20`)[cite: 5].
* **VLAN / SVI Allocation:** Xác định chính xác **9 Production User SVIs** (VLAN 10–90) có L3 Routing Gateway; **VLAN 999 (NATIVE_ISOLATED)** là L2-Only Native VLAN không có SVI[cite: 5].

---

## 2. DECISION REGISTER (TẬP QUYẾT ĐỊNH TRIỂN KHAI TRIỆT ĐỂ)

### A. Core Architecture & Interconnect Decisions

| Issue ID | Trigger & Validation Finding[cite: 5] | Final Implementation Decision[cite: 5] | Treatment Status[cite: 5] | Target Codebase Artifact[cite: 5] |
| :--- | :--- | :--- | :---: | :--- |
| **DEC-001** | **CON-001:** Mâu thuẫn giữa `physical_device_inventory.csv` (ghi StackWise/LACP) và `High_Availability.md` (loại trừ Stacking/VSS)[cite: 5]. | **Active/Standby L2 Core Simulation Model:**<br>1. `CORE-L3-01`: Đóng vai trò Primary L3 Core Active Gateway (giữ 9 Production SVIs Gateways và `ip routing`)[cite: 5].<br>2. `CORE-L3-02`: Đóng vai trò Secondary L2 Core Standby Switch (chỉ giữ Management VLAN 70 IP, `no ip routing`)[cite: 5].<br>3. Không giả lập Stacking/VSS phần cứng[cite: 5]. | `SIMULATION DECISION`[cite: 5] | `CORE-L3-01_implemented.cfg`<br>`CORE-L3-02_implemented.cfg`[cite: 5] |
| **DEC-007** | **GAP-004:** Cổng kết nối trực tiếp Core-to-Core chưa được định nghĩa trong tài liệu gốc[cite: 5]. | **Redundant L2 Trunk Interconnect:**<br>Nối 2 dây cáp chéo `CORE-L3-01 (Gi0/23-24)` $\leftrightarrow$ `CORE-L3-02 (Gi0/23-24)`[cite: 5]. Cấu hình 802.1Q Trunking cho phép VLANs 10–90, 999[cite: 5].<br>*Ghi chú:* Đây là 2 liên kết Trunk vật lý riêng biệt hoạt động dưới Rapid PVST+ (không gom LACP EtherChannel)[cite: 5]. | `LAB WORKAROUND`[cite: 5] | `CORE-L3-01_implemented.cfg`<br>`CORE-L3-02_implemented.cfg`[cite: 5] |

---

### B. Capacity & Physical Port Mapping Decisions

| Issue ID | Trigger & Validation Finding[cite: 5] | Final Implementation Decision[cite: 5] | Treatment Status[cite: 5] | Target Codebase Artifact[cite: 5] |
| :--- | :--- | :--- | :---: | :--- |
| **DEC-002** | **CON-002:** Tầng 2 có 100 máy (80 Dev + 20 QA) nhưng switchport plan chỉ cấp 20 cổng physical[cite: 5]. | **Representative Endpoints Model:**<br>Mô phỏng quy mô 150 người dùng bằng các máy trạm đại diện (2 PC Dev, 2 PC QA, 2 PC HR, 2 PC Fin, 2 PC Exec, 1 Server Git, 1 Guest PC)[cite: 5]. | `SIMULATOR LIMITATION`[cite: 5] | `packettracer/enterprise_network_v1.0.pkt`[cite: 5] |
| **DEC-003** | **CON-003:** Chồng chéo giữa Chiến lược chia cổng chung (`Fa0/13-20` Voice/AP) và Switchport Plan thực tế (`Fa0/1-16` Dev)[cite: 5]. | **Strict Functional Port Mapping:**<br>1. `Fa0/1–16`: Cố định cho Workstations người dùng phòng ban[cite: 5].<br>2. `Fa0/17–18`: Cố định cho QA Workstations / Executive / Servers[cite: 5].<br>3. `Fa0/19–20`: Dành riêng cho CCTV Cameras đại diện[cite: 5].<br>4. `Fa0/21`: Cố định cho Access Point (VLAN 90)[cite: 5].<br>5. `Fa0/22`: Cố định cho IP Phone (VLAN 80)[cite: 5].<br>6. `Fa0/23–24`: **Bắt buộc dành riêng 100% cho LACP Uplinks**[cite: 5]. | `IMPLEMENTATION DECISION`[cite: 5] | `ACC-F1-01_implemented.cfg`<br>`ACC-F2-01_implemented.cfg`<br>`ACC-F3-01_implemented.cfg`[cite: 5] |
| **DEC-008** | **GAP-005/006:** Mâu thuẫn giữa cắm CCTV trên `Fa0/23-24` và đường LACP Uplinks[cite: 5]. | **Reconciled Service Ports Allocation:**<br>Chuyển CCTV Cameras đại diện từ `Fa0/23-24` sang dải cổng `Fa0/19-20`[cite: 5]. Giải phóng hoàn toàn `Fa0/23-24` làm LACP Active EtherChannel Trunk Uplinks nối lên Core[cite: 5]. | `RECONCILED WORKAROUND`[cite: 5] | `ACC-F1-01_implemented.cfg`<br>`ACC-F2-01_implemented.cfg`<br>`ACC-F3-01_implemented.cfg`[cite: 5] |
| **DEC-009** | **GAP-007:** Thiếu thông số PoE Budget vật lý trong tài liệu[cite: 5]. | **Outside Simulation Fidelity:** Xem hạn mức công suất PoE nằm ngoài phạm vi mô phỏng của Packet Tracer[cite: 5]. | `OUT OF SCOPE`[cite: 5] | N/A |

---

### C. Security Policy & Extended ACL Decisions

| Issue ID | Trigger & Validation Finding[cite: 5] | Final Implementation Decision[cite: 5] | Treatment Status[cite: 5] | Target Codebase Artifact[cite: 5] |
| :--- | :--- | :--- | :---: | :--- |
| **DEC-004** | **CON-004 / SEC-005:** `ACL_HR_IN` thiếu câu lệnh chặn chéo HR $\rightarrow$ QA Subnet (`10.10.20.0/24`)[cite: 5]. | **Security Boundary Revision:**<br>Bổ sung câu lệnh `deny ip 10.10.30.0 0.0.0.255 10.10.20.0 0.0.0.255` trực tiếp vào danh sách ACL trong file cấu hình thực thi của Core L3[cite: 5]. | `DESIGN REVISION`[cite: 5] | `CORE-L3-01_implemented.cfg`[cite: 5] |
| **DEC-005** | **CON-005 / SEC-006/007:** Subnet QA (VLAN 20) và Executive (VLAN 50) hoàn toàn thiếu Inbound SVI ACL[cite: 5]. | **Extended Boundary Protection:**<br>1. **Thêm `ACL_QA_IN`:** Cho phép QA truy cập Internet/Server, chặn chéo sang Subnet Finance (`10.10.40.0/24`) và HR (`10.10.30.0/24`)[cite: 5].<br>2. **Thêm `ACL_EXEC_IN`:** Cho phép Executive truy cập toàn bộ tài nguyên nội bộ, chặn chéo sang Guest VLAN 90[cite: 5]. | `DESIGN REVISION`[cite: 5] | `CORE-L3-01_implemented.cfg`[cite: 5] |

---

### D. Egress Addressing & WAN Routing Decisions

| Issue ID | Trigger & Validation Finding[cite: 5] | Final Implementation Decision[cite: 5] | Treatment Status[cite: 5] | Target Codebase Artifact[cite: 5] |
| :--- | :--- | :--- | :---: | :--- |
| **DEC-006** | **GAP-001/002/003:** Thiếu IP WAN, Transit IP giữa Router-Firewall và Public Subnet[cite: 5]. | **Lab-Defined Egress Transit Scheme:**<br>1. **Core $\leftrightarrow$ FW Inside:** `10.10.70.10/24` (Core SVI 70) $\leftrightarrow$ `10.10.70.2/24` (FW Inside)[cite: 5].<br>2. **FW Outside $\leftrightarrow$ Router LAN:** `192.168.100.2/30` (FW Outside) $\leftrightarrow$ `192.168.100.1/30` (RTR LAN)[cite: 5].<br>3. **Router WAN $\leftrightarrow$ ISP Cloud:** `203.0.113.2/30` (RTR WAN) $\leftrightarrow$ `203.0.113.1/30` (ISP Gateway)[cite: 5]. | `LAB-DEFINED ADDRESSING`[cite: 5] | `CORE-L3-01_implemented.cfg`<br>`FW-EDGE-01_implemented.cfg`<br>`RTR-EDGE-01_implemented.cfg`[cite: 5] |

---

## 3. MASTER IMPLEMENTATION CODEBASE STRUCTURE

Cấu trúc lưu trữ artifacts chính thức sau khi đối chiếu Baseline:

```text
enterprise-network-infrastructure-blueprint/
│
├── configs/                                       # LEGACY HISTORICAL EVIDENCE (UNTOUCHED)[cite: 5]
│   ├── CORE-L3-01.cfg                             # Original 5 legacy config files[cite: 5]
│   ├── ACC-F1-01.cfg
│   ├── ACC-F2-01.cfg
│   ├── ACC-F3-01.cfg
│   └── RTR-EDGE-01.cfg
│
└── implementation/
    ├── baseline/
    │   └── implementation_baseline.md             # File Baseline Reconciled này[cite: 5]
    │
    ├── configs/                                   # 7 RECONCILED IMPLEMENTATION CONFIGS[cite: 5]
    │   ├── 01_CORE-L3-01_implemented.cfg          # Active Core L3 (9 Production SVIs + Expanded ACLs)[cite: 5]
    │   ├── 02_CORE-L3-02_implemented.cfg          # Standby Core L2 (Management VLAN 70 IP)[cite: 5]
    │   ├── 03_ACC-F1-01_implemented.cfg           # Floor 1 Access (HR/Fin + Reconciled Service Ports)[cite: 5]
    │   ├── 04_ACC-F2-01_implemented.cfg           # Floor 2 Access (Dev/QA + Reconciled Service Ports)[cite: 5]
    │   ├── 05_ACC-F3-01_implemented.cfg           # Floor 3 Access (Exec/Srv + Reconciled Service Ports)[cite: 5]
    │   ├── 06_RTR-EDGE-01_implemented.cfg         # Edge WAN Router (Lab NAT Overload & Egress)[cite: 5]
    │   └── 07_FW-EDGE-01_implemented.cfg          # ASA Firewall (Inside/Outside Transit)[cite: 5]
    │
    ├── packettracer/
    │   └── enterprise_network_v1.0.pkt            # Integrated Packet Tracer Implementation File[cite: 5]
    │
    └── verification/                              # EXECUTED TEST CASES & EVIDENCE (CHỜ CHẠY)[cite: 5]
        ├── 01_connectivity_matrix.md
        ├── 02_security_acl_tests.md
        └── 03_ha_etherchannel_tests.md