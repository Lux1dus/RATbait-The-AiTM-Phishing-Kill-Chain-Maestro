# 🔬 Lab Setup

This document provides a detailed guide on the installation and execution process of the third-party tools required to operate the **RATbait** ecosystem.

---

## 1. MailHog (Local SMTP Server)
**MailHog** acts as a simulated email receiving station, allowing you to review phishing content before sending without needing a complex SMTP server configuration.

### Installation
```bash
# Download the executable for Linux
wget https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64
chmod +x MailHog_linux_amd64

# Move it to the system directory for global usage
sudo mv MailHog_linux_amd64 /usr/local/bin/mailhog
```

### Execution
Open a new terminal and run the command:
```bash
mailhog -ui-bind-addr 0.0.0.0:8025 -api-bind-addr 0.0.0.0:8025 -smtp-bind-addr 0.0.0.0:1025
```
*   **SMTP Port**: `1025` (Configure this in the GoPhish Sending Profile)
*   **Web UI/API**: `http://localhost:8025` (View received emails)

---

## 2. GoPhish (Phishing Framework)
**GoPhish** is a platform for managing phishing campaigns, controlled by RATbait via API to automate email sending.

### Installation
```bash
# Create a directory and download GoPhish
mkdir -p ~/tools/gophish && cd ~/tools/gophish
wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
unzip gophish-v0.12.1-linux-64bit.zip
```

### Configuration and Avoiding Port Conflict
**⚠️ IMPORTANT:** By default, GoPhish uses port `80` for the Phishing server. This will cause a conflict and crash Evilginx2 (because Evilginx also needs port 80). You must change GoPhish's port:

1. Open the `config.json` file in the GoPhish directory.
2. Find the line `"phish_server": { "listen_url": "0.0.0.0:80" }`
3. Change the number `80` to `8080` (or any other available port). Save it.

### Execution
```bash
sudo ./gophish
```
*   **Admin UI**: `https://localhost:3333`
*   **Note**: On the first run, check the terminal to get the temporary login password for the `admin` account.

---

## 3. Evilginx 2 (3.3.0) (AiTM Engine)
**Evilginx** is the heart of the AiTM attack, used to bypass MFA security by stealing Session Cookies.

### Installation
On Kali Linux, you can install it directly from the official repository:
```bash
sudo apt update
sudo apt install evilginx2
```

### Execution
To run in a Lab environment with a `.local` domain, you **MUST** use the `--developer` parameter to disable automatic certificate requests from Let's Encrypt:

```bash
sudo evilginx2 --developer
```

**⚠️ IMPORTANT:** Why use `--developer`?

Without this parameter, Evilginx will report an error: `failed to set up TLS certificates: [github-lab.local] Obtain: subject does not qualify for a public certificate`. Since the `.local` suffix is an internal domain, organizations like Let's Encrypt will refuse to issue a public certificate. Developer mode allows you to use self-signed certificates from `mkcert`.

### Basic Config inside CLI
1.  Set up Domain: `config domain github-lab.local`
2.  Set up IP: `config ipv4 <YOUR_KALI_IP>`
3.  Configure Hostname for Phishlet: `phishlets hostname github github-lab.local`
4.  Enable Phishlet: `phishlets enable github`
5.  Create Lure: `lures create github`

---

## Port Mapping Summary

| Tool | Web Interface | Service Port | Role |
| :--- | :--- | :--- | :--- |
| **MailHog** | `8025` | `1025` (SMTP) | View fake emails |
| **GoPhish** | `3333` | `8080` / `443` | Send payload |
| **Evilginx** | `CLI` | `80` / `443` (Proxy) | Steal Token |
| **RATbait** | `CLI` | `N/A` | Coordinating Conductor |

---
**Navigation:**
[🏠 Home](../README.md) | **[⚙️ Lab Setup](LAB_SETUP.md)** | [🌐 Infrastructure Theory](INFRA_THEORY.md) | [🚀 Demo Kill Chain](KILLCHAIN.md)
