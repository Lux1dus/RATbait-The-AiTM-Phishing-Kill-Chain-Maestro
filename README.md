#### ⚠️ Disclaimer

This project is a Proof of Concept (PoC) developed for educational purposes, cybersecurity research, and testing in an authorized Lab environment. The author is not responsible for any misuse, damage, or illegal activities arising from the use of this project. Using this tool on systems without explicit permission can be a serious violation of the law.
<br>

---

# 🎣 Automated Kill Chain Orchestrator (RATbait)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![GoPhish](https://img.shields.io/badge/GoPhish-API-blueviolet?style=for-the-badge&logo=go&logoColor=white)
![Evilginx](https://img.shields.io/badge/Evilginx-AiTM-red?style=for-the-badge&logo=nginx&logoColor=white)

--- 

## System Preview

Below is the Orchestrator Console interface of **RATbait** while listening to data from Evilginx.

<p align="center">
  <img src="assets/images/ratbaitui.png" alt="RATbait Orchestrator Preview" width="450">
</p>

**Want to see what RATbait looks like during a simulation?**

[👉 Kill Chain Simulation (KILLCHAIN.md)](docs/KILLCHAIN.md)

---

## I. The Backstory & Motivation

### Origin of the idea
For a long time, Phishing to me was just basic concepts like 'don't click strange links' or 'check the sender carefully'. However, one day, while watching the video **[Russia's Most Wanted Hacker](https://www.youtube.com/watch?v=ZhfI0EboPU0)** which is directly related to **[The Bundestag Hack 2015](https://cyberlaw.ccdcoe.org/wiki/Bundestag_Hack_(2015))**, I began to dig deeper into attacks targeting high-level personnel (Spear Phishing/Whaling). And right then, I realized this is an extremely dangerous human vulnerability that I needed to seriously research.

**RATbait** was born from that curiosity. It was also the right time for me to combine it with my **[labRAT](https://github.com/Lux1dus/LabRAT-C2-Framework)** project, creating a complete hypothetical Kill Chain: from the moment the victim receives a fake email until the Agent is officially executed on the target machine.

### Personal Goals
*   Delve into the operational mechanism of modern Phishing attacks bypassing MFA.
*   Build an Orchestration system capable of connecting disjointed security tools.
*   Develop a **Purple Team** mindset: Understand automated attacks to design more effective defense strategies.

---

## II. Project Overview

### Executive Summary
- **RATbait** is an Automated Kill Chain Framework, integrating Evilginx 3.0 and the GoPhish API.

- The system acts as a Middleware, continuously monitoring Evilginx's database. As soon as it detects a new victim, it automatically extracts the Session Cookie and triggers "double-bullet" phishing campaigns (Combo Mode) to distribute malware.

- The entire process from Token theft to RAT execution on the victim's machine is automated, minimizing the Operator's manual interaction time.

### Tech Stack
The system combines top-tier technologies in the Red Team community to create a continuous attack chain:

| Component | Tech | Role & Features |
| :--- | :--- | :--- |
| **Orchestrator** | `Python (Threaded)` | The "brain" of the system. Monitors DB, handles attack logic, and coordinates APIs. |
| **AiTM Engine** | `Evilginx 3.0` | Acts as a reverse proxy to steal Session Cookies and bypass MFA. |
| **Phishing API** | `GoPhish` | Manages sending lure emails, tracks clicks, and distributes the executable file. |
| **RAT Agent** | `Python (labRAT)` | Remote-controlled malware, supporting persistence and evasion (Safe Mode). |
| **Database** | `JSON` | Stores victim data, tokens, and campaign statuses. |

---

## Getting Started - Lab Setup

[👉 See detailed installation for other components before running RATbait (LAB_SETUP.md)](docs/LAB_SETUP.md)

To deploy RATbait in a Lab environment (Kali Linux/Debian), perform the following steps:

### 1. Environment Setup
Download the source code and install dependencies:
```bash
git clone <this repo>
cd RATbait
pip install -r requirements.txt
```

### 2. Environment Variables Configuration
Create a `.env` file from the example file and set up important connection parameters:
```bash
cp .env.example .env
# Use nano or vim to edit the following parameters:
```
**Key parameters in `.env`:**
*   `GOPHISH_API_KEY`: Obtained from the Settings configuration on the GoPhish admin interface.
*   `EVILGINX_DB_PATH`: Absolute path to Evilginx's `data.db` file (usually `/root/.evilginx/data.db`).
*   `C2_SERVER_URL`: IP address of the server listening for connections from the malware (labRAT).
*   `PAYLOAD_URL`: Download link for the decoy malware file (displayed in the phishing email).

### 3. Adjust RATbait.py (If needed)
Open the `RATbait.py` file, check the default configuration variables at the top of the file to ensure they match your Lab environment (e.g., SMTP Config and default Templates).

### 4. Activate the Conductor
Run the Orchestrator with root privileges (to read the Evilginx DB):
```bash
sudo python3 RATbait.py
```
*After running, you can select the attack mode (Enterprise, Friend, or Combo) right on the CLI interface.*

---

### Workflow
The **RATbait** system operates in an automated attack chain comprising 6 closed steps:

<p align="center">
  <img src="assets/images/quytrinhhoatdong.png" alt="Workflow">
</p>

| Step | Phase | Tool | Description |
| :---: | :--- | :---: | :--- |
| **1** | **Initial Lure** | `Attacker` | The attacker initiates by sending a link spoofing a reputable login page. The victim visits and proceeds to log in. |
| **2** | **AiTM Harvesting** | `Evilginx 3.0` | Acts as a Reverse Proxy, collecting `Username/Password`, bypassing MFA authentication, completely hijacking the **Session Cookie**, and saving it to `data.db`. |
| **3** | **Continuous Sniffing** | 🧠 `RATbait` | Continuously monitors `data.db`. As soon as there's a new Session Cookie, the system automatically extracts the information.<br><br> *> Supports CLI for the Operator to quickly extract Cookies for Pass-the-Cookie.* |
| **4** | **Automated Orchestration** | `RATbait`<br> `GoPhish API` | Based on the collected data, RATbait automatically calls GoPhish's API to initiate a follow-up attack campaign (stage 2) to the victim's email. |
| **5** | **Payload Delivery** | `GoPhish` | Sends psychologically manipulative emails (e.g., security alerts). The attachment is `labRAT.exe` but disguised as a document (PDF/DOCX) using **RTLO**. |
| **6** | **Execution & Reverse C2** | `labRAT` | The victim downloads and runs the attachment. The malware activates silently, creating a reverse connection (Reverse C2). The attacker has **full control** of the device. |

## III. Orchestration & API Flow

The RATbait system is designed based on an **Asynchronous Multi-threading** model, ensuring data monitoring happens continuously in real-time without interrupting the Operator's manual control experience.

### 1. Dual-Thread Architecture
| Processing Thread | Function Name | Core Tech | Main Task |
| :--- | :--- | :--- | :--- |
| **Daemon Thread**<br>*(Background)* | `sniffer_thread()` | `File I/O Polling` &<br>`Regex Parsing` | Continuously reads the tail of Evilginx's `data.db` file. Uses Regex to quickly extract login credentials (`username/password`) right when the victim submits them. |
| **Main Thread**<br>*(Foreground)* | `interactive_console()` | `CLI Input Loop` &<br>`JSON Processing` | Provides a Cyberpunk interactive interface. Allows the Operator to type commands (e.g., `show cookies <email>`). This thread parses complex JSON structures to accurately filter out the Session Token. |

### 2. GoPhish API Flow & "Double-Bullet" Logic
Instead of configuring campaigns manually, the `trigger_payloads()` thread will fully automate the process of interacting with the GoPhish API through these steps:

1. **Target Generation (`POST /api/groups`)**: Automatically creates a new target Group containing only the email of the victim who just fell for the trap.
2. **Campaign Launch (`POST /api/campaigns`)**: Combines the newly created Group with available Email Templates and SMTP Configs to launch the campaign.
3. **Combo Mode Logic**: If the Operator selects mode 3 (Combo Mode), the system will execute the **Follow-up attack** algorithm:

   - Fire API campaign 1 (Enterprise Lure).
   - Pause exactly `30 seconds` (`time.sleep(30)`) to create a Natural Delay, avoiding Spam Filters.
   - Proceed to fire API campaign 2 (Friend Lure) to maximize the chance of the victim clicking the Payload.

---

## IV. Current Limitations & Risks

Despite being a powerful Framework, **RATbait** currently has some architectural limitations to keep in mind:

| Limitation | Technical Cause | Risk |
| :--- | :--- | :--- |
| **Local DB Dependency** | Requires direct read access to Evilginx's `data.db` file on the same Server. | Hard to deploy in a distributed architecture (Separate C2 Server and Phishing). |
| **Unproxied API Calls** | Requests to the GoPhish API (Port 3333) are currently sent directly without a Proxy. | Traffic could be intercepted by Blue Team, leading to the C2 IP being Blacklisted. |
| **Plaintext Token Exposure** | Extracted Session Cookies are displayed in Plaintext on the Operator's Terminal. | Risk of sensitive Token leakage via screen/logs if the control machine is monitored. |

---

## V. Future Roadmap

Direction for upgrading RATbait into a more distributed and intelligent C2 Orchestrator system:

| Phase | Upgrade Module | Detailed Description & Goal |
| :---: | :--- | :--- |
| **Phase 2** | **Remote DB Support** | Support reading data from a remote Evilginx Server via SSH or gRPC protocols. |
| **Phase 3** | **C2 Notification Integrations**| Integrate bot to notify of new trapped victims directly via Telegram or Discord. |
| **Phase 4** | **Generative AI Lures** | Use LLMs (GPT API) to automatically analyze context and draft personalized phishing emails. |
| **Phase 5** | **Payload Evasion** | Integrate Dynamic Encoders for `labRAT` to bypass modern EDR systems during delivery. |

---

## VI. Key Learnings & Concepts

During the process of building **RATbait**, the project has helped reinforce advanced defensive and offensive mindsets:

| Concept | Technical Details & Applications |
| :--- | :--- |
| **AiTM Automation** | Deep understanding of the mechanism of stealing and directly manipulating Session Tokens to bypass MFA barriers. |
| **Security Orchestration** | Mastering how to link disjointed security tools (Evilginx, GoPhish) via API to form a seamless attack supply chain (Kill Chain). |
| **Real-time Processing** | Applying Multi-threading and I/O Polling techniques to process large data in real-time without crashing the application. |
| **Social Engineering** | Successfully applying the "Double-dip" technique to maximize the phishing success rate. |

---

<p align="center">
  <b>Made with 💻 and ☕ by <a href="https://github.com/Lux1dus">Lux1dus</a></b>
</p>
