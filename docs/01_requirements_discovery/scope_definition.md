# Design Decisions & Technical Scope Definition

## 1. Context & Case Study Assumptions
Bài toán thiết kế hạ tầng được xây dựng dựa trên bối cảnh giả lập cho một doanh nghiệp vừa tại Việt Nam (**ABC Digital Solutions**):
* **Quy mô:** 150 nhân viên, làm việc tại văn phòng 3 tầng, áp dụng mô hình Hybrid Working.
* **Architectural Assumption:** Hiện tại, ABC Digital Solutions đang sử dụng mô hình mạng phẳng (Flat Layer-2 Network), toàn bộ thiết bị và phòng ban nằm chung một broadcast domain, gây ra rủi ro cao về nghẽn mạng và đứt gãy bảo mật.

Nhiệm vụ của dự án là tái thiết kế hạ tầng mạng nội bộ (Enterprise Network) an toàn, hiệu năng cao, phân vùng rõ ràng và dễ dàng mở rộng.

---

## 2. Evidence-Based Requirements & Interpretation

Phạm vi kỹ thuật của dự án được quyết định thông qua quy trình: **Collect Evidence -> Interpret Requirements -> Engineering Decision**.

* **Explicit Dataset Evidence:** Khảo sát ngẫu nhiên từ *Vietnam Job Market Dataset* (157 job postings vị trí IT Support/Helpdesk/Junior Network, chi tiết tại `research/data/raw_jobs.csv`) chỉ ra tần suất xuất hiện trực tiếp của các công nghệ: Active Directory (9 JDs), Routing (7 JDs), DNS (7 JDs), DHCP (6 JDs), VPN (5 JDs), Firewall (3 JDs) và VLAN (2 JDs) tại các doanh nghiệp như Axon, CyberLogitec, TechValley, Reeracoen, Manpower... (Tham chiếu báo cáo: `docs/Requirements_Discovery.md`).
* **Implicit Review & Qualitative Analysis:** Một đánh giá định tính trên tập mẫu (Qualitative Review) chỉ ra rằng nhiều mô tả công việc không ghi trực tiếp từ khóa "VLAN" mà sử dụng các thuật ngữ vận hành cấp cao hơn như "Quản trị hệ thống LAN/WAN" hoặc "Cấu hình Cisco Switches". Điều này gợi ý rằng vị trí công việc đòi hỏi kỹ năng quản trị Switch Layer-2, trong đó VLAN là một công nghệ ứng dụng phổ biến (Commonly Implemented).
* **Engineering Interpretation:** Dữ liệu cho thấy các vị trí tuyển dụng khởi điểm (Entry-level) luôn yêu cầu ứng viên làm chủ vững vàng kỹ năng vận hành Hạ tầng Mạng lõi (Network Fundamentals) trước khi bước sang Quản trị Định danh (Identity Management) hay Giám sát Nâng cao (Monitoring/SIEM).

---

## 3. Scope Definition for Version 1.0 (In-Scope)
Dựa trên phần diễn giải (Interpretation) ở trên, Version 1.0 tập trung xây dựng hoàn chỉnh và vững chắc **Hạ tầng Mạng lõi (Core Enterprise Network Infrastructure)**:

* **Network Segmentation (VLANs):** Tách biệt các dải mạng phòng ban (HR, Kế toán, Developers, Sales/Ops, Management, Guest, Native). *Lý do:* Giảm Broadcast Storm, bảo vệ dữ liệu nhạy cảm Kế toán/HR.
* **Automatic IP Allocation (VLSM & DHCP):** Quy hoạch IP Private chuẩn hóa bằng kỹ thuật VLSM và cấu hình DHCP Server tự động cấp IP theo VLAN. *Lý do:* Tránh xung đột IP tĩnh, tối ưu vận hành Helpdesk.
* **Inter-VLAN Routing:** Triển khai định tuyến Inter-VLAN qua Router/Layer 3 Switch (mô hình Router-on-a-Stick). *Lý do:* Cho phép lưu lượng hợp pháp luân chuyển giữa các tầng dưới sự kiểm soát.
* **Access Control & Guest Isolation (ACL):** Viết Access Control List cách ly hoàn toàn mạng Wi-Fi Guest ra Internet và chặn phòng Dev truy cập chéo vào Subnet Kế toán/HR. *Lý do:* Ngăn ngừa nguy cơ lây nhiễm mã độc (Ransomware).
* **Layer 2 Security Baseline:** Cấu hình Spanning Tree Protocol (STP) và Port Security cơ bản trên Access Switches. *Lý do:* Chống loop mạng và ngăn cắm thiết bị lạ (Rogue Switches).

---

## 4. Explicit Out-of-Scope (Planned for Future Versions)
Để đảm bảo sự tập trung cao nhất vào chất lượng hạ tầng Core Network, các công nghệ sau cố ý dời sang các phiên bản nâng cấp:

* **Active Directory / Windows Server Domain (Version 2.0):** Mặc dù có tần suất yêu cầu cao (9 JDs), AD thuộc mảng Quản trị Hệ thống (System Administration). Việc tích hợp AD sẽ thực hiện ở Ver 2.0 sau khi hạ tầng L2/L3 vận hành ổn định.
* **Remote Access VPN / Site-to-Site VPN (Version 1.5):** Dành cho kết nối từ xa, sẽ tích hợp ở bản cập nhật tiếp theo.
* **SIEM / Centralized Monitoring (Version 3.0):** Thuộc phạm vi Giám sát An toàn thông tin nâng cao (Security Operations).

---

## 5. Requirement Traceability Matrix

| Quyết định Kỹ thuật (v1.0) | Căn cứ Tuyển dụng (Source: docs/Requirements_Discovery.md) | Diễn giải Kỹ thuật (Interpretation) | Rủi ro Nghiệp vụ Giải quyết |
| :--- | :--- | :--- | :--- |
| **VLAN Segmentation** | CyberLogitec, TechValley (Explicit) + Manpower (Implied) | Quản trị Switch L2 yêu cầu phân vùng mạng | Lộ dữ liệu Kế toán/HR, tràn ngập Broadcast Storm |
| **DHCP Server** | 6 JDs (Axon, TechValley, Reeracoen...) | Cần thiết cho vận hành cấp phát IP tự động | Xung đột IP tĩnh, tốn công Helpdesk |
| **Inter-VLAN Routing** | 7 JDs (TechValley, Reeracoen, FedEx...) | Yêu cầu kiểm soát luồng giao tiếp L3 | Mất kết nối liên phòng ban |
| **Guest Network Isolation** | Firewall 3 JDs + Troubleshooting 8 JDs | An toàn thông tin mạng không dây cho Khách | Ransomware lây lan từ thiết bị ngoài |
| **Port Security & STP** | Troubleshooting 8 JDs (DXC, Intel...) | An toàn vật lý và ổn định hạ tầng Layer 2 | Sập mạng do Loop hoặc cắm Router chui |

---

## 6. Dataset Limitations
* **Recruitment vs. Architecture:** Dữ liệu thu thập từ bài đăng tuyển dụng (JDs tại `research/data/raw_jobs.csv`) phục vụ mục đích tuyển dụng, không phải tài liệu kiến trúc kỹ thuật. Một số công nghệ hạ tầng được ngầm định (Implied) thay vì liệt kê chi tiết.
* **Sample Scope:** Tập dữ liệu 157 JDs cung cấp góc nhìn thực tế (Snapshot) về yêu cầu tuyển dụng Entry-level tại Việt Nam, đóng vai trò làm căn cứ tham chiếu để xác định phạm vi cho dự án bài lab cá nhân này.