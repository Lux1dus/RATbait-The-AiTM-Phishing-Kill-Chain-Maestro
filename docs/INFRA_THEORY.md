# 🌐 Infrastructure Theory

This document explains the operational mechanism of RATbait in a **Local Lab** environment and its differences compared to a **Real World** deployment.

---

## I. Local Lab Architecture

In a Lab environment, we do not own real domain names (e.g., `github.com`). Therefore, we must use simulation techniques to deceive the system and the browser.

### 1. DNS Simulation (Hosts File)
Instead of querying DNS Servers on the Internet, we force the computer to map hypothetical domain names to the IP of the attacker's machine (Kali Linux).

**Execution steps:**
You need to edit the `/etc/hosts` file (on Linux) **AND** `C:\Windows\System32\drivers\etc\hosts` (on Windows) so that both systems recognize the virtual domain name pointing to the Kali machine's IP:

```text
# Replace X.X.X.X with your Kali Linux machine's IP
X.X.X.X github-lab.local www.github-lab.local api.github-lab.local assets.github-lab.local
```

### 2. SSL/TLS Simulation (mkcert)
Evilginx requires HTTPS to operate. Since `github-lab.local` is not a real domain name, you cannot request a certificate from Let's Encrypt. The solution is to use **mkcert** to create a private **Local Root CA**.

**Exact setup process:**

1.  **Install the Root CA into the system:**
    ```bash
    mkcert -install
    ```
    *This command turns your machine into a trusted certificate authority (Root CA).*

2.  **Determine the Root CA file location (To install in the victim's browser):**
    ```bash
    mkcert -CAROOT
    ```
    *You need to copy the `rootCA.pem` file in this directory and install it in the "Authorities" section in the victim machine's browser.*

3.  **Create a certificate for the Lab domain name:**
    ```bash
    mkcert -cert-file fullchain.cer -key-file private.key github-lab.local "*.github-lab.local"
    ```

4.  **Move the certificate to the Evilginx configuration directory:**
    Evilginx searches for certificates in the `/root/.evilginx/crt/` directory. You need to create a directory corresponding to the domain name:
    ```bash
    sudo mkdir -p /root/.evilginx/crt/github-lab.local
    sudo mv fullchain.cer private.key /root/.evilginx/crt/github-lab.local/
    ```

---

## II. Real World Deployment

In a real-world environment, the attacker will not have access to the victim's `hosts` file to manually redirect DNS. Instead, the deployment process requires real infrastructures on the Internet. The attacker usually starts by registering domain names that look trustworthy but are actually fake (Typosquatting technique), such as `githuub.com` or `github-security.net`. 

After owning the domain name, they will configure DNS records (A record, CNAME) on service providers like Cloudflare or Namecheap to point to the Public IP address of a VPS (Virtual Private Server). 

Another important difference is requesting SSL/TLS certificates; in reality, Evilginx can automatically integrate with Let's Encrypt to get valid certificates trusted by all browsers without requiring any manual Root CA installation on the victim's machine. This entire infrastructure creates a "transparent" environment making it very difficult for the victim to detect technical anomalies.

---

## III. Lab vs Real World Comparison

The table below summarizes the core differences between simulating in a Lab and deploying in combat:

| Component | Lab Environment (Local) | Real Environment (Public) |
| :--- | :--- | :--- |
| **Domain** | Self-named virtual domain (`.local`, `.test`). | Officially registered domain (`.com`, `.net`). |
| **DNS** | Edit `hosts` file on each machine. | Configure DNS records on the Internet. |
| **SSL/TLS** | Self-issued with `mkcert` (Requires Root CA installation). | Valid certificate from Let's Encrypt (100% Trusted). |
| **IP Infrastructure** | Internal IP (LAN / Host-only). | Public IP on a VPS. |
| **Complexity** | High (Due to manual simulation configuration). | Low (Everything operates automatically according to standards). |

---
**Navigation:**
[🏠 Home](../README.md) | [⚙️ Lab Setup](LAB_SETUP.md) | **[🌐 Infrastructure Theory](INFRA_THEORY.md)** | [🚀 Demo Kill Chain](KILLCHAIN.md)
