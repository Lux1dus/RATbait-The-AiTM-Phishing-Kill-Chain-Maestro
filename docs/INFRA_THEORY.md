# 🌐 Lý thuyết Hạ tầng & Giả lập (Infrastructure Theory)

Tài liệu này giải thích cơ chế vận hành của RATbait trong môi trường **Local Lab** và sự khác biệt so với triển khai **Thực tế (Real World)**.

---

## I. Mô hình Lab nội bộ (Local Lab Architecture)

Trong môi trường Lab, chúng ta không sở hữu các tên miền thật (ví dụ: `github.com`). Do đó, chúng ta phải sử dụng các kỹ thuật giả lập để đánh lừa hệ thống và trình duyệt.

### 1. Giả lập DNS (Hosts File)
Thay vì truy vấn các DNS Server trên Internet, chúng ta ép buộc máy tính ánh xạ các tên miền giả định về IP của máy tấn công (Kali Linux).

**Thao tác thực hiện:**
Bạn cần chỉnh sửa file `/etc/hosts` (trên Linux) **VÀ** `C:\Windows\System32\drivers\etc\hosts` (trên Windows) để cả hai hệ thống đều nhận diện được tên miền ảo trỏ về IP của máy Kali:

```text
# Thay X.X.X.X bằng IP máy Kali Linux của bạn
X.X.X.X github-lab.local www.github-lab.local api.github-lab.local assets.github-lab.local
```

### 2. Giả lập SSL/TLS (mkcert)
Evilginx yêu cầu HTTPS để hoạt động. Vì `github-lab.local` không phải tên miền thật, bạn không thể xin chứng chỉ từ Let's Encrypt. Giải pháp là sử dụng **mkcert** để tạo một **Local Root CA** riêng.

**Quy trình thiết lập chính xác:**

1.  **Cài đặt Root CA vào hệ thống:**
    ```bash
    mkcert -install
    ```
    *Lệnh này biến máy bạn thành một tổ chức cấp phát chứng chỉ tin cậy (Root CA).*

2.  **Xác định vị trí file Root CA (Để cài vào trình duyệt nạn nhân):**
    ```bash
    mkcert -CAROOT
    ```
    *Bạn cần copy file `rootCA.pem` tại thư mục này và cài vào mục "Authorities" trong trình duyệt của máy nạn nhân.*

3.  **Tạo chứng chỉ cho tên miền Lab:**
    ```bash
    mkcert -cert-file fullchain.cer -key-file private.key github-lab.local "*.github-lab.local"
    ```

4.  **Di chuyển chứng chỉ vào thư mục cấu hình Evilginx:**
    Evilginx tìm kiếm chứng chỉ trong thư mục `/root/.evilginx/crt/`. Bạn cần tạo thư mục tương ứng với tên miền:
    ```bash
    sudo mkdir -p /root/.evilginx/crt/github-lab.local
    sudo mv fullchain.cer private.key /root/.evilginx/crt/github-lab.local/
    ```

---

## II. Triển khai Thực tế (Real World Deployment)

Trong môi trường thực tế, kẻ tấn công sẽ không có quyền truy cập vào file `hosts` của nạn nhân để điều hướng DNS thủ công. Thay vào đó, quy trình triển khai đòi hỏi các hạ tầng thực thụ trên mạng Internet. Kẻ tấn công thường bắt đầu bằng việc đăng ký các tên miền có vẻ ngoài đáng tin cậy nhưng thực chất là giả mạo (kỹ thuật Typosquatting), ví dụ như `githuub.com` hoặc `github-security.net`. 

Sau khi sở hữu tên miền, chúng sẽ cấu hình các bản ghi DNS (A record, CNAME) trên các nhà cung cấp dịch vụ như Cloudflare hoặc Namecheap để trỏ về địa chỉ IP Public của một máy chủ VPS (Virtual Private Server). 

Một điểm khác biệt quan trọng nữa là việc xin chứng chỉ SSL/TLS; trong thực tế, Evilginx có thể tự động tích hợp với Let's Encrypt để lấy các chứng chỉ hợp lệ được mọi trình duyệt tin cậy mà không cần bất kỳ thao tác cài đặt Root CA thủ công nào lên máy nạn nhân. Toàn bộ hạ tầng này tạo nên một môi trường "trong suốt" khiến nạn nhân rất khó phát hiện điểm bất thường về mặt kỹ thuật.

---

## III. So sánh Lab vs Thực tế (The Comparison)

Bảng dưới đây tóm tắt các điểm khác biệt cốt lõi giữa việc giả lập trong Lab và triển khai thực chiến:

| Thành phần | Môi trường Lab (Local) | Môi trường Thực tế (Public) |
| :--- | :--- | :--- |
| **Tên miền** | Tên miền ảo tự đặt (`.local`, `.test`). | Tên miền đăng ký chính thức (`.com`, `.net`). |
| **DNS** | Sửa file `hosts` trên từng máy. | Cấu hình bản ghi DNS trên Internet. |
| **SSL/TLS** | Tự cấp phát bằng `mkcert` (Cần cài Root CA). | Chứng chỉ hợp lệ từ Let's Encrypt (Tin cậy 100%). |
| **Hạ tầng IP** | IP nội bộ (LAN / Host-only). | IP Public trên VPS. |
| **Độ phức tạp** | Cao (Do phải cấu hình giả lập thủ công). | Thấp (Mọi thứ đều vận hành tự động theo tiêu chuẩn). |

---
**Điều hướng (Navigation):**
[🏠 Trang chủ](../README.md) | [⚙️ Thiết lập Lab](LAB_SETUP.md) | **[🌐 Lý thuyết Hạ tầng](INFRA_THEORY.md)** | [🚀 Quy trình Demo](KILLCHAIN.md)
