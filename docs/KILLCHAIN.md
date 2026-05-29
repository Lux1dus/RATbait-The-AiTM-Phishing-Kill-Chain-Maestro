# 🚀 Simulated Kill Chain Process

This document details the stages of executing a complete simulated attack scenario, from the initial approach to gaining full system control via the **RATbait** Framework.

---

## Stage 0: Setting up (Prerequisites)

Before launching the campaign, the Lab infrastructure needs to be ready:

1.  **System:** Complete the setup of Root CA, TLS certificates, and hostname resolution on the workstation.
2.  **Intercepting Service:** Activate **MailHog** to monitor and collect simulated emails in the internal environment.
3.  **Phishing Platform:** Start **GoPhish** and access the Web UI admin interface.
4.  **AiTM Tool:** Run **Evilginx** in developer mode (`--developer`).

---

## Stage 1: Setting the Lure (Initial Lure)

The goal of this stage is to create a fake login page capable of deceiving users and bypassing security mechanisms.

1.  **Configure Phishlet:** Set up the configuration for a specific target (e.g., `github`) by loading the `.yaml` file into the Evilginx configuration directory.
2.  **Initialize Lure URL:** Once the configuration is complete, the system will generate a fake URL for a valid login page.

<p align="center">
  <img src="../assets/images/lurephatsinh.png" alt="Generated Lure URL" width="600">
</p>

3.  **Launch the Campaign:** Embed the lure URL into the Email Template on GoPhish and send it to the target list from the `dataset/targets.csv` file.

- The **MailHog** monitoring system will confirm the successful email sending:

<p align="center">
  <img src="../assets/images/campaignmailhogthanhcong.png" alt="Campaign recorded by MailHog" width="1200">
</p>

- The lure email interface from the victim's perspective:

<p align="center">
  <img src="../assets/images/giaodienemailgiamao1.png" alt="Initial fake email content" width="1200">
</p>

---

## Stage 2: Session Hijacking (AiTM Harvesting)

This is the key stage using the Adversary-in-the-Middle technique to hijack the account without breaking the MFA code.

1.  **Activate RATbait:** Launch the coordinator by running `sudo python3 RATbait.py` and select the attack mode (e.g., **Combo Mode**).

<p align="center">
  <img src="../assets/images/ratbaitdanglangnghe.png" alt="RATbait interface listening to Evilginx" width="450">
</p>

2.  **Data Collection:** When the victim accesses the fake page and logs in, Evilginx acts as a reverse Proxy to collect credentials and authentication codes.

<p align="center">
  <img src="../assets/images/giaodiendangnhapgia.png" alt="Fake login page interface" width="1200">
</p>

3.  **Extract Session Cookies:** As soon as the victim completes two-factor authentication (MFA), Evilginx will hijack the valid session and record it in the `data.db` database.

<p align="center">
  <img src="../assets/images/thongtindabibat.png" alt="Sensitive data has been captured" width="1200">
</p>

4.  **Session Exploitation:** Through RATbait, we can precisely extract the Cookie using the command `show cookies <victim_email>`. Using tools like "Cookie-Editor" to load this identifier into the browser, we will officially hijack the account without needing a password or OTP code.

<p align="center">
  <img src="../assets/images/khaithacsessioncookie.png" alt="Hijacking the victim's account via Session Cookie" width="700">
</p>

---

## Stage 3: Automated Attack Orchestration

After gaining account access, **RATbait** will automate the next steps to distribute the Payload.

1.  **Follow-up Attack:** Based on the selected configuration, RATbait calls the GoPhish API to launch a second campaign targeting directly the victim who just fell for the trap.
2.  **"Double Bullet" Tactic (Combo Mode):**
    *   **Email 1 (Enterprise):** Sends a system security notice, requesting the victim to execute a diagnostic file (actually the `labRAT.exe` malware).
    *   **Email 2 (Personal):** Sent automatically after 30 seconds under the name of a colleague or friend to confirm, aiming to maximize trust.

**⚠️ Note:** In the Lab environment, I use a personal Gmail as a valid sender to ensure emails bypass security filters like SPF or DKIM.

<p align="center">
  <img src="../assets/images/ratbaitguimailcombo.png" alt="Follow-up attack emails sent consecutively" width="450">
</p>

- Illustration of corporate and personal fake email interfaces sent to the victim:

| Enterprise Mode | Friend Mode |
| :---: | :---: |
| <img src="../assets/images/chedoenterprise.png" width="1200"> | <img src="../assets/images/chedofriend.png" width="1550"> |

---

## Stage 4: Control and Persistence (Post-Exploitation)

The final stage of the kill chain, when the malware is executed and the attacker officially controls the device.

1.  **Malware Execution:** Assuming the victim downloaded and executed the attached file on the Windows workstation out of anxiety.
2.  **Reverse Connection (Reverse C2):** The `labRAT.exe` malware runs in the background, sending a Check-in signal to the command server.
3.  **Target Administration:** Through the `labRAT` command-line interface, we can execute remote commands, monitor system resources, and establish mechanisms for long-term access persistence.

<p align="center">
  <img src="../assets/images/giaodianlabrat.png" alt="labRAT control interface officially hijacking the system" width="1200">
</p>

---

## Conclusion

The simulated kill chain has been successfully completed, demonstrating the danger of combined attacks between AiTM and automated Social Engineering techniques.

**System Navigation:**
[🏠 Home](../README.md) | [⚙️ Lab Setup](LAB_SETUP.md) | [🌐 Infrastructure Theory](INFRA_THEORY.md) | **[🚀 Demo Kill Chain](KILLCHAIN.md)**
