# 🔬 Thiết lập Công cụ Lab (Lab Setup)

Tài liệu này hướng dẫn chi tiết quy trình cài đặt và khởi chạy các công cụ bên thứ ba cần thiết để vận hành hệ sinh thái **RATbait**.

---

## 1. MailHog (Local SMTP Server)
**MailHog** đóng vai trò là trạm thu nhận email giả lập, cho phép bạn kiểm duyệt nội dung phishing trước khi gửi đi mà không cần cấu hình máy chủ SMTP phức tạp.

### Cài đặt (Installation)
```bash
# Tải bản thực thi cho Linux
wget https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64
chmod +x MailHog_linux_amd64

# Chuyển vào thư mục hệ thống để sử dụng mọi nơi
sudo mv MailHog_linux_amd64 /usr/local/bin/mailhog
```

### Khởi chạy (Execution)
Mở một terminal mới và chạy lệnh:
```bash
mailhog -ui-bind-addr 0.0.0.0:8025 -api-bind-addr 0.0.0.0:8025 -smtp-bind-addr 0.0.0.0:1025
```
*   **SMTP Port**: `1025` (Cấu hình vào GoPhish Sending Profile)
*   **Web UI/API**: `http://localhost:8025` (Xem các email đã nhận)

---

## 2. GoPhish (Phishing Framework)
**GoPhish** là nền tảng quản lý các chiến dịch phishing, được RATbait điều khiển thông qua API để tự động hóa việc bắn email.

### Cài đặt (Installation)
```bash
# Tạo thư mục và tải GoPhish
mkdir -p ~/tools/gophish && cd ~/tools/gophish
wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
unzip gophish-v0.12.1-linux-64bit.zip
```

### Cài đặt và Tránh Xung Đột Cổng (Port Conflict)
**⚠️ QUAN TRỌNG:** Mặc định, GoPhish sử dụng cổng `80` cho máy chủ Phishing. Điều này sẽ gây xung đột và làm sập Evilginx2 (vì Evilginx cũng cần cổng 80). Bạn bắt buộc phải đổi cổng của GoPhish:

1. Mở file `config.json` trong thư mục GoPhish.
2. Tìm dòng `"phish_server": { "listen_url": "0.0.0.0:80" }`
3. Sửa số `80` thành `8080` (hoặc bất kỳ cổng nào khác đang rảnh). Lưu lại.

### Khởi chạy (Execution)
```bash
sudo ./gophish
```
*   **Admin UI**: `https://localhost:3333`
*   **Lưu ý**: Trong lần chạy đầu tiên, hãy kiểm tra terminal để lấy mật khẩu đăng nhập tạm thời cho tài khoản `admin`.

---

## 3. Evilginx 2 (3.3.0) (AiTM Engine)
**Evilginx** là trái tim của cuộc tấn công AiTM, dùng để vượt qua lớp bảo mật MFA bằng cách đánh cắp Session Cookie.

### Cài đặt (Installation)
Trên Kali Linux, bạn có thể cài đặt trực tiếp từ kho lưu trữ chính thức:
```bash
sudo apt update
sudo apt install evilginx2
```

### Khởi chạy (Execution)
Để chạy trong môi trường Lab với tên miền `.local`, bạn **BẮT BUỘC** phải sử dụng tham số `--developer` để vô hiệu hóa việc tự động xin chứng chỉ từ Let's Encrypt:

```bash
sudo evilginx2 --developer
```

**⚠️ QUAN TRỌNG:** Tại sao phải dùng `--developer`?

Nếu không có tham số này, Evilginx sẽ báo lỗi: `failed to set up TLS certificates: [github-lab.local] Obtain: subject does not qualify for a public certificate`. Do đuôi `.local` là tên miền nội bộ, các tổ chức như Let's Encrypt sẽ từ chối cấp chứng chỉ công khai. Chế độ developer cho phép bạn sử dụng chứng chỉ tự cấp phát từ `mkcert`.

### Cấu hình cơ bản (Basic Config inside CLI)
1.  Thiết lập Domain: `config domain github-lab.local`
2.  Thiết lập IP: `config ipv4 <YOUR_KALI_IP>`
3.  Cấu hình Hostname cho Phishlet: `phishlets hostname github github-lab.local`
4.  Bật Phishlet: `phishlets enable github`
5.  Tạo Lure: `lures create github`

---

## Bảng tóm tắt Port (Port Mapping)

| Công cụ | Giao diện Web | Cổng Service | Vai trò |
| :--- | :--- | :--- | :--- |
| **MailHog** | `8025` | `1025` (SMTP) | Xem email giả mạo |
| **GoPhish** | `3333` | `8080` / `443` | Gửi payload |
| **Evilginx** | `CLI` | `80` / `443` (Proxy) | Đánh cắp Token |
| **RATbait** | `CLI` | `N/A` | Nhạc trưởng điều phối |

---
**Điều hướng (Navigation):**
[🏠 Trang chủ](../README.md) | **[⚙️ Thiết lập Lab](LAB_SETUP.md)** | [🌐 Lý thuyết Hạ tầng](INFRA_THEORY.md) | [🚀 Quy trình Demo](KILLCHAIN.md)
