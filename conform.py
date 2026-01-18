# ✅ Android File Picker Version - Load files from anywhere

import os
import sys
import time
import random
import re
import json
import platform
import threading
import itertools
import base64
import hashlib
import subprocess
import socket
import ssl
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor as threadpol

import requests
import certifi
import openpyxl
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Android detection
ANDROID = 'ANDROID_DATA' in os.environ or 'ANDROID_ROOT' in os.environ

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

# Color codes
WHITE = '\x1b[1;97m'
GREEN = '\x1b[1;92m'
RED = '\x1b[1;91m'
DARK_GREEN = '\x1b[1;32m'
LIGHT_GRAY = '\x1b[1;37m'
CYAN = '\x1b[1;96m'
YELLOW = '\x1b[1;93m'
BLUE = '\x1b[1;94m'
MAGENTA = '\x1b[1;95m'
ORANGE = '\x1b[38;5;208m'
GOLD = '\x1b[38;5;220m'
VIOLET = '\x1b[38;5;141m'
TOXIC = '\x1b[38;2;170;200;0m'
PURPLE = '\x1b[38;2;150;80;200m'

opt_labels = [f"{GREEN}[{RED}{str(i).zfill(2)}{GREEN}]" for i in range(1, 8)]

l0 = f"{GREEN}[{RED}00{GREEN}]"
EKL = f"{CYAN}:{WHITE}"
LINE = f"{CYAN}┅━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┅"

# Global variables
print_lock = threading.Lock()
counter_lock = threading.Lock()

total_checked = 0
total_success = 0
total_failed = 0
total_error = 0
PROXIES = None
CURRENT_LOCALE = 'en_US'

SERVER_MAP = {
    1: 'm.facebook.com',
    2: 'mbasic.facebook.com',
    3: 'touch.facebook.com',
    4: 'free.facebook.com',
    5: 'm.alpha.facebook.com',
    6: 'm.beta.facebook.com',
    7: 'x.facebook.com'
}

# User variables (for Android)
user_nm = "Android User"
expr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def parse_proxy(proxy_str):
    if not proxy_str or proxy_str.strip() == '':
        return None
        
    proxy_str = proxy_str.strip()
    
    if '://' not in proxy_str:
        parts = proxy_str.split(':')
        if len(parts) == 4:
            ip, port, user, pwd = parts
            proxy_url = f"http://{user}:{pwd}@{ip}:{port}"
        elif len(parts) == 2:
            ip, port = parts
            proxy_url = f"http://{ip}:{port}"
        else:
            return None
    else:
        proxy_url = proxy_str
    
    return {'http': proxy_url, 'https': proxy_url}

COUNTRY_TO_LOCALE = {
    'AD': 'ca_ES', 'AE': 'ar_AR', 'AF': 'fa_IR', 'AG': 'en_US', 'AI': 'en_US', 'AL': 'sq_AL',
    'AM': 'hy_AM', 'AO': 'pt_PT', 'AQ': 'en_US', 'AR': 'es_LA', 'AS': 'en_US', 'AT': 'de_DE',
    'AU': 'en_GB', 'AW': 'nl_NL', 'AX': 'sv_SE', 'AZ': 'az_AZ', 'BA': 'bs_BA', 'BB': 'en_US',
    'BD': 'bn_IN', 'BE': 'nl_BE', 'BF': 'fr_FR', 'BG': 'bg_BG', 'BH': 'ar_AR', 'BI': 'fr_FR',
    'BJ': 'fr_FR', 'BL': 'fr_FR', 'BM': 'en_US', 'BN': 'ms_MY', 'BO': 'es_LA', 'BQ': 'nl_NL',
    'BR': 'pt_BR', 'BS': 'en_US', 'BT': 'dz_BT', 'BV': 'en_GB', 'BW': 'en_GB', 'BY': 'ru_RU',
    'BZ': 'en_US', 'CA': 'en_US', 'CC': 'en_GB', 'CD': 'fr_FR', 'CF': 'fr_FR', 'CG': 'fr_FR',
    'CH': 'de_DE', 'CI': 'fr_FR', 'CK': 'en_US', 'CL': 'es_LA', 'CM': 'fr_FR', 'CN': 'zh_CN',
    'CO': 'es_LA', 'CR': 'es_LA', 'CU': 'es_LA', 'CV': 'pt_PT', 'CW': 'nl_NL', 'CX': 'en_GB',
    'CY': 'el_GR', 'CZ': 'cs_CZ', 'DE': 'de_DE', 'DJ': 'fr_FR', 'DK': 'da_DK', 'DM': 'en_US',
    'DO': 'es_LA', 'DZ': 'ar_AR', 'EC': 'es_LA', 'EE': 'et_EE', 'EG': 'ar_AR', 'EH': 'ar_AR',
    'ER': 'ti_ET', 'ES': 'es_ES', 'ET': 'am_ET', 'FI': 'fi_FI', 'FJ': 'en_US', 'FK': 'en_GB',
    'FM': 'en_US', 'FO': 'da_DK', 'FR': 'fr_FR', 'GA': 'fr_FR', 'GB': 'en_GB', 'GD': 'en_US',
    'GE': 'ka_GE', 'GF': 'fr_FR', 'GG': 'en_GB', 'GH': 'en_GB', 'GI': 'en_GB', 'GL': 'da_DK',
    'GM': 'en_GB', 'GN': 'fr_FR', 'GP': 'fr_FR', 'GQ': 'es_ES', 'GR': 'el_GR', 'GS': 'en_GB',
    'GT': 'es_LA', 'GU': 'en_US', 'GW': 'pt_PT', 'GY': 'en_US', 'HK': 'zh_HK', 'HM': 'en_US',
    'HN': 'es_LA', 'HR': 'hr_HR', 'HT': 'fr_FR', 'HU': 'hu_HU', 'ID': 'id_ID', 'IE': 'en_GB',
    'IL': 'he_IL', 'IM': 'en_GB', 'IN': 'hi_IN', 'IO': 'en_GB', 'IQ': 'ar_AR', 'IR': 'fa_IR',
    'IS': 'is_IS', 'IT': 'it_IT', 'JE': 'en_GB', 'JM': 'en_US', 'JO': 'ar_AR', 'JP': 'ja_JP',
    'KE': 'en_GB', 'KG': 'ru_RU', 'KH': 'km_KH', 'KI': 'en_US', 'KM': 'fr_FR', 'KN': 'en_US',
    'KP': 'ko_KR', 'KR': 'ko_KR', 'KW': 'ar_AR', 'KY': 'en_US', 'KZ': 'ru_RU', 'LA': 'lo_LA',
    'LB': 'ar_AR', 'LC': 'en_US', 'LI': 'de_DE', 'LK': 'si_LK', 'LR': 'en_US', 'LS': 'en_GB',
    'LT': 'lt_LT', 'LU': 'fr_FR', 'LV': 'lv_LV', 'LY': 'ar_AR', 'MA': 'ar_AR', 'MC': 'fr_FR',
    'MD': 'ro_RO', 'ME': 'sr_RS', 'MF': 'fr_FR', 'MG': 'fr_FR', 'MH': 'en_US', 'MK': 'mk_MK',
    'ML': 'fr_FR', 'MM': 'my_MM', 'MN': 'mn_MN', 'MO': 'zh_TW', 'MP': 'en_US', 'MQ': 'fr_FR',
    'MR': 'ar_AR', 'MS': 'en_US', 'MT': 'en_GB', 'MU': 'en_GB', 'MV': 'dv_MV', 'MW': 'en_GB',
    'MX': 'es_MX', 'MY': 'ms_MY', 'MZ': 'pt_PT', 'NA': 'en_GB', 'NC': 'fr_FR', 'NE': 'fr_FR',
    'NF': 'en_GB', 'NG': 'en_GB', 'NI': 'es_LA', 'NL': 'nl_NL', 'NO': 'nb_NO', 'NP': 'ne_NP',
    'NR': 'en_US', 'NU': 'en_US', 'NZ': 'en_GB', 'OM': 'ar_AR', 'PA': 'es_LA', 'PE': 'es_LA',
    'PF': 'fr_FR', 'PG': 'en_US', 'PH': 'tl_PH', 'PK': 'ur_PK', 'PL': 'pl_PL', 'PM': 'fr_FR',
    'PN': 'en_GB', 'PR': 'es_LA', 'PS': 'ar_AR', 'PT': 'pt_PT', 'PW': 'en_US', 'PY': 'es_LA',
    'QA': 'ar_AR', 'RE': 'fr_FR', 'RO': 'ro_RO', 'RS': 'sr_RS', 'RU': 'ru_RU', 'RW': 'fr_FR',
    'SA': 'ar_AR', 'SB': 'en_US', 'SC': 'fr_FR', 'SD': 'ar_AR', 'SE': 'sv_SE', 'SG': 'en_GB',
    'SH': 'en_GB', 'SI': 'sl_SI', 'SJ': 'nb_NO', 'SK': 'sk_SK', 'SL': 'en_GB', 'SM': 'it_IT',
    'SN': 'fr_FR', 'SO': 'so_SO', 'SR': 'nl_NL', 'SS': 'en_GB', 'ST': 'pt_PT', 'SV': 'es_LA',
    'SX': 'nl_NL', 'SY': 'ar_AR', 'SZ': 'en_GB', 'TC': 'en_US', 'TD': 'fr_FR', 'TF': 'fr_FR',
    'TG': 'fr_FR', 'TH': 'th_TH', 'TJ': 'tg_TJ', 'TK': 'en_US', 'TL': 'pt_PT', 'TM': 'ru_RU',
    'TN': 'ar_AR', 'TO': 'en_US', 'TR': 'tr_TR', 'TT': 'en_US', 'TV': 'en_US', 'TW': 'zh_TW',
    'TZ': 'sw_KE', 'UA': 'uk_UA', 'UG': 'en_GB', 'UM': 'en_US', 'US': 'en_US', 'UY': 'es_LA',
    'UZ': 'uz_UZ', 'VA': 'it_IT', 'VC': 'en_US', 'VE': 'es_LA', 'VG': 'en_GB', 'VI': 'en_US',
    'VN': 'vi_VN', 'VU': 'en_US', 'WF': 'fr_FR', 'WS': 'en_US', 'YE': 'ar_AR', 'YT': 'fr_FR',
    'ZA': 'en_GB', 'ZM': 'en_GB', 'ZW': 'en_GB'
}

def get_locale_code(country_code):
    return COUNTRY_TO_LOCALE.get(country_code.upper(), 'en_US')

def get_ip_info(proxies=None):
    try:
        r = requests.get("http://ip-api.com/json/", proxies=proxies, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                'country': data.get('country', 'Unknown'),
                'countryCode': data.get('countryCode', 'US'),
                'timezone': data.get('timezone', 'Unknown')
            }
    except:
        pass
    return {'country': 'Unknown', 'countryCode': 'US', 'timezone': 'Unknown'}

def load_settings():
    try:
        with open('Setting.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def get_status_line():
    return f"\r{GREEN}[{WHITE}Mr-DHIRAJ{GREEN}] {WHITE}CHECKED:-{total_checked}{CYAN}|{GREEN}SUCCESS:-{total_success}{CYAN}|{YELLOW}FAILED:-{total_failed}{CYAN}|{RED}ERROR:-{total_error}"

def safe_print(text):
    with print_lock:
        sys.stdout.write('\r                                                                                \r')
        try:
            sys.stdout.write(str(text) + '\n')
        except UnicodeEncodeError:
            sys.stdout.write(str(text).encode('utf-8', 'ignore').decode('utf-8') + '\n')
        sys.stdout.write(get_status_line())
        sys.stdout.flush()

def update_counter(status, number=None, message=None, color=None, html_content=None):
    global total_success, total_failed, total_error, total_checked
    
    with counter_lock:
        if status == 'success':
            total_success += 1
        elif status == 'failed':
            total_failed += 1
        elif status == 'error':
            total_error += 1
            if html_content:
                save_error_html(message if message else "Unknown Error", html_content)
        
        total_checked += 1
    
    if message and number:
        if not color: color = WHITE
        safe_print(f"{color} {message} {number}")
        return
    
    if message:
        if not color: color = WHITE
        safe_print(f"{color} {message}")
        return

    with print_lock:
        sys.stdout.write(get_status_line())
        sys.stdout.flush()

SAVE_ERROR_LOGS = 'off'

def reset_counters():
    global total_checked, total_success, total_failed, total_error
    total_checked = 0
    total_success = 0
    total_failed = 0
    total_error = 0

def save_error_html(message, html_content):
    if SAVE_ERROR_LOGS.lower() != 'on':
        return

    try:
        if not os.path.exists('Error_Logs'):
            os.makedirs('Error_Logs')
            
        safe_msg = re.sub(r'[\\/*?:"<>|]', '', message)
        safe_msg = safe_msg.replace(' ', '_')
        safe_msg = safe_msg[:50]
        
        base_filename = f"Error_Logs/{safe_msg}.html"
        filename = base_filename
        counter = 1
        
        while os.path.exists(filename):
            filename = f"Error_Logs/{safe_msg}_{counter}.html"
            counter += 1
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"<!-- Error: {message} -->\n")
            f.write(html_content)
    except Exception as e:
        safe_print(f"{RED} Failed to save error log: {e}")

def clear_logo():
    os.system('clear')
    
    print(f"""{GREEN}
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  ╔══════════════════════════╗  ┃
    ┃  ║      𝔼𝕃𝔼𝕍𝕀𝕏 𝕋𝕆𝕆𝕃         ║  ┃
    ┃  ║   𝔽𝔸ℂ𝔼𝔹𝕆𝕆𝕂 𝔽𝕆ℝ𝔾𝔼𝕋        ║  ┃
    ┃  ║     {ORANGE}𝕍𝟛.𝟞 𝔼𝕕𝕚𝕥𝕚𝕠𝕟{WHITE}       ║  ┃
    ┃  ╚══════════════════════════╝  ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
{LINE}
 {GREEN}┣ {GREEN}ツ{GREEN}┫ OWNER        {CYAN}: {WHITE}DHIRAJ
 {GREEN}┣ {GREEN}ツ{GREEN}┫ TOOL         {CYAN}: {WHITE}FACEBOOK FORGET
 {GREEN}┣ {GREEN}ツ{GREEN}┫ STATUS       {CYAN}: {GREEN}PREMIUM""")

# SIMPLE FILE PICKER SYSTEM
def file_picker():
    clear_logo()
    print(f"{GREEN} ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"{GREEN} ┃      📁 FILE SELECTION MENU      ┃")
    print(f"{GREEN} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print(f"{LINE}")
    print(f" {opt_labels[0]} Enter full file path")
    print(f" {opt_labels[1]} Use default: /sdcard/numbers.txt")
    print(f" {opt_labels[2]} Browse current directory")
    print(f" {l0} Return to main menu")
    print(f"{LINE}")
    
    choice = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Choose option {EKL} ").strip()
    
    if choice in ('1', '01'):
        # Enter full path
        file_path = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Enter full file path {EKL} ").strip()
        if not file_path:
            print(f"{RED} ┣ {RED}✗{RED}┫ No file path entered!")
            time.sleep(2)
            return file_picker()
        
        return load_file(file_path)
        
    elif choice in ('2', '02'):
        # Use default /sdcard/numbers.txt
        default_path = "/sdcard/numbers.txt"
        print(f"{CYAN} ┣ {CYAN}⏳{CYAN}┫ Trying: {default_path}")
        return load_file(default_path)
        
    elif choice in ('3', '03'):
        # Browse current directory
        return browse_current_dir()
        
    elif choice in ('00', '0'):
        # Return to main menu
        return None
        
    else:
        print(f"{RED} ┣ {RED}✗{RED}┫ Invalid choice!")
        time.sleep(2)
        return file_picker()

def browse_current_dir():
    clear_logo()
    print(f"{GREEN} ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"{GREEN} ┃    📂 FILES IN DIRECTORY         ┃")
    print(f"{GREEN} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print(f"{LINE}")
    
    # Get all files in current directory
    files = []
    try:
        for item in os.listdir('.'):
            if os.path.isfile(item):
                size = os.path.getsize(item)
                files.append((item, size))
    except Exception as e:
        print(f"{RED} ┣ {RED}✗{RED}┫ Error reading directory: {e}")
        time.sleep(2)
        return file_picker()
    
    if not files:
        print(f"{YELLOW} ┣ {YELLOW}⚠{YELLOW}┫ No files found in current directory.")
        input(f"{WHITE} ┣ {WHITE}⏎{WHITE}┫ Press Enter to continue...")
        return file_picker()
    
    # Display files
    for idx, (filename, size) in enumerate(files, 1):
        size_kb = size / 1024
        print(f" {GREEN}[{RED}{idx:02d}{GREEN}] {WHITE}{filename} {CYAN}({size_kb:.1f} KB)")
    
    print(f"{LINE}")
    print(f" {GREEN}[{RED}00{GREEN}] Back to file menu")
    print(f"{LINE}")
    
    while True:
        choice = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Select file number {EKL} ").strip()
        
        if choice in ('00', '0'):
            return file_picker()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                filename = files[idx][0]
                print(f"{CYAN} ┣ {CYAN}✓{CYAN}┫ Selected: {filename}")
                return load_file(filename)
        
        print(f"{RED} ┣ {RED}✗{RED}┫ Invalid selection!")

def load_file(file_path):
    """Load phone numbers from any file"""
    try:
        # Expand home directory and environment variables
        file_path = os.path.expanduser(file_path)
        file_path = os.path.expandvars(file_path)
        
        if not os.path.exists(file_path):
            print(f"{RED} ┣ {RED}✗{RED}┫ File not found: {file_path}")
            time.sleep(2)
            return file_picker()
        
        if not os.path.isfile(file_path):
            print(f"{RED} ┣ {RED}✗{RED}┫ Not a file: {file_path}")
            time.sleep(2)
            return file_picker()
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:  # 10 MB limit
            print(f"{RED} ┣ {RED}✗{RED}┫ File too large ({file_size/1024/1024:.1f} MB). Max 10 MB.")
            time.sleep(2)
            return file_picker()
        
        print(f"{CYAN} ┣ {CYAN}⏳{CYAN}┫ Reading file: {file_path}")
        
        # Determine file type and read accordingly
        if file_path.lower().endswith('.txt'):
            # Read text file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            # Extract numbers from text
            numbers = []
            for line in lines:
                # Find all numbers in the line
                found_numbers = re.findall(r'\b\d{7,15}\b', line)
                numbers.extend(found_numbers)
            
            if not numbers:
                print(f"{YELLOW} ┣ {YELLOW}⚠{YELLOW}┫ No phone numbers found in file.")
                print(f"{CYAN} ┣ {CYAN}⏳{CYAN}┫ Trying to extract numbers differently...")
                
                # Try alternative extraction
                numbers = []
                for line in lines:
                    # Remove all non-digits and check if what remains is a valid number
                    cleaned = re.sub(r'\D', '', line)
                    if 7 <= len(cleaned) <= 15:
                        numbers.append(cleaned)
        
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            # Read Excel file
            try:
                wb = openpyxl.load_workbook(file_path, data_only=True)
                sheet = wb.active
                
                numbers = []
                for row in sheet.iter_rows(values_only=True):
                    for cell in row:
                        if cell:
                            cell_str = str(cell).strip()
                            # Find numbers in cell
                            found = re.findall(r'\b\d{7,15}\b', cell_str)
                            numbers.extend(found)
                            
                            # Also try cleaned version
                            cleaned = re.sub(r'\D', '', cell_str)
                            if 7 <= len(cleaned) <= 15 and cleaned not in numbers:
                                numbers.append(cleaned)
            except Exception as e:
                print(f"{RED} ┣ {RED}✗{RED}┫ Error reading Excel file: {e}")
                # Try as text file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                numbers = re.findall(r'\b\d{7,15}\b', content)
        
        else:
            # Try to read as text file anyway
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            numbers = re.findall(r'\b\d{7,15}\b', content)
        
        # Remove duplicates and empty entries
        numbers = list(set([n for n in numbers if n]))
        
        if not numbers:
            print(f"{RED} ┣ {RED}✗{RED}┫ No valid phone numbers found in file!")
            time.sleep(2)
            return file_picker()
        
        # Save to local Number_List.txt for processing
        with open('Number_List.txt', 'w', encoding='utf-8') as f:
            for num in numbers:
                f.write(num + '\n')
        
        print(f"{GREEN} ┣ {GREEN}✓{GREEN}┫ Successfully loaded {len(numbers)} numbers from {os.path.basename(file_path)}")
        print(f"{GREEN} ┣ {GREEN}✓{GREEN}┫ Saved to local Number_List.txt for processing")
        
        return numbers
        
    except Exception as e:
        print(f"{RED} ┣ {RED}✗{RED}┫ Error loading file: {e}")
        time.sleep(2)
        return file_picker()

def DHIRAJ_main():
    clear_logo()
    print(f"{GREEN} ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"{GREEN} ┃        📋 MAIN MENU             ┃")
    print(f"{GREEN} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print(f"{LINE}")
    print(f" {GREEN}┣ {WHITE}👤{GREEN}┫ User      {EKL} {user_nm}")
    print(f" {GREEN}┣ {WHITE}⏰{GREEN}┫ Expired   {EKL} {expr} (Utc)")
    print(f"{LINE}")
    print(f" {opt_labels[0]} 📲 FB FORGET")
    print(f" {opt_labels[1]} 📢 JOIN TELEGRAM")
    print(f" {l0} 🚪 EXIT")
    print(f"{LINE}")
    
    chic_opsn = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Choose option {EKL} ").strip().lower()
    
    if chic_opsn in ('1', '01', 'a'):
        # File picker for FB FORGET
        numbers = file_picker()
        if numbers:
            print(f"{LINE}")
            input(f"{WHITE} ┣ {WHITE}⏎{WHITE}┫ Press Enter to Start Forgetting {len(numbers)} Numbers...")
            autom_main(numbers)
        else:
            DHIRAJ_main()
        return
        
    elif chic_opsn in ('2', '02', 'b'):
        print(f"{CYAN} ┣ {CYAN}⏳{CYAN}┫ Opening Telegram...")
        try:
            import webbrowser
            webbrowser.open('https://t.me/mrDHIRAJtools')
        except:
            print(f"{YELLOW} ┣ {YELLOW}⚠{YELLOW}┫ Could not open browser. Visit: https://t.me/mrDHIRAJtools")
        time.sleep(2)
        DHIRAJ_main()
        return
        
    elif chic_opsn in ('00', '0'):
        print(f"{RED} ┣ {RED}✗{RED}┫ Exiting...{WHITE}")
        sys.exit(0)
        
    else:
        print(f"\n{RED} ┣ {RED}✗{RED}┫ Invalid option!")
        time.sleep(2)
        DHIRAJ_main()
        return

def get_proxy_list():
    """Get proxy input from user - FIXED to not skip when proxy is entered"""
    PROXY_LIST = []
    
    print(f"{LINE}")
    while True:
        try:
            proxy_input = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Enter Proxy (Format: ip:port OR ip:port:user:pass) [Enter to Skip] {EKL} ").strip()
            
            # If user presses Enter without input, break the loop
            if proxy_input == "":
                if not PROXY_LIST:
                    print(f"{YELLOW} ┣ {YELLOW}⚠{YELLOW}┫ No proxy selected. Running without proxy.")
                break
            
            # Parse the proxy
            parsed = parse_proxy(proxy_input)
            if parsed:
                try:
                    # Get IP info for the proxy
                    nfo = get_ip_info(parsed)
                    loc = get_locale_code(nfo['countryCode'])
                    PROXY_LIST.append({'proxy': parsed, 'locale': loc, 'country': nfo['country']})
                    print(f"{GREEN} ┣ {GREEN}✓{GREEN}┫ Proxy Location {EKL} {nfo['country']}")
                    print(f"{GREEN} ┣ {GREEN}✓{GREEN}┫ Locale      {EKL} {loc}")
                    
                    # Ask if user wants to add more proxies
                    more = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Add another proxy? (y/n) {EKL} ").strip().lower()
                    if more not in ('y', 'yes'):
                        break
                except:
                    print(f"{RED} ┣ {RED}✗{RED}┫ Failed to get proxy info. Proxy may still work.")
                    PROXY_LIST.append({'proxy': parsed, 'locale': 'en_US', 'country': 'Unknown'})
                    
                    more = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Add another proxy? (y/n) {EKL} ").strip().lower()
                    if more not in ('y', 'yes'):
                        break
            else:
                print(f"{RED} ┣ {RED}✗{RED}┫ Invalid proxy format! Try again.")
                
        except KeyboardInterrupt:
            print(f"\n{YELLOW} ┣ {YELLOW}⚠{YELLOW}┫ Proxy input cancelled.")
            break
        except Exception as e:
            print(f"{RED} ┣ {RED}✗{RED}┫ Error: {e}")
    
    return PROXY_LIST

def autom_main(numbers):
    if not numbers:
        print(f"{RED} ┣ {RED}✗{RED}┫ No numbers to process!")
        input(f"{WHITE} ┣ {WHITE}⏎{WHITE}┫ Press Enter to return...")
        DHIRAJ_main()
        return

    clear_logo()
    print(f"{GREEN} ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"{GREEN} ┃    🚀 STARTING PROCESS          ┃")
    print(f"{GREEN} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print(f"{LINE}")
    print(f"{GREEN} ┣ {WHITE}📊{GREEN}┫ Total Numbers: {len(numbers)}")
    
    settings = load_settings()
    server_set = settings.get('server_settings', {})
    server_id = server_set.get('tools_server_id', 1)
    server_domain = SERVER_MAP.get(server_id, 'm.facebook.com')

    # Get proxies from user
    print(f"{WHITE} ┣ {WHITE}🔧{WHITE}┫ Setting up Proxy System...")
    PROXY_LIST = get_proxy_list()
    PROXY_ITERATOR = itertools.cycle(PROXY_LIST) if PROXY_LIST else None
    
    # Browser selection (6 options only)
    print(f"{LINE}")
    print(f"{GREEN} ┣ {RED}▶{GREEN}┫ Select Browser Type:")
    print(f"{GREEN} [{RED}01{GREEN}] 🦁 Brave (Default)")
    print(f"{GREEN} [{RED}02{GREEN}] 🌐 Chrome")
    print(f"{GREEN} [{RED}03{GREEN}] 🦊 Firefox")
    print(f"{GREEN} [{RED}04{GREEN}] 📱 Samsung")
    print(f"{GREEN} [{RED}05{GREEN}] 🎭 Opera")
    print(f"{GREEN} [{RED}06{GREEN}] 🌍 UC Browser")
    print(f"{GREEN} [{RED}00{GREEN}] 🎲 Random")
    print(f"{LINE}")
    
    brow_inp = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Select Browser {EKL} ").strip()

    if brow_inp == '1' or brow_inp == '01': browser_type = 'Brave'
    elif brow_inp == '2' or brow_inp == '02': browser_type = 'Chrome'
    elif brow_inp == '3' or brow_inp == '03': browser_type = 'Firefox'
    elif brow_inp == '4' or brow_inp == '04': browser_type = 'Samsung'
    elif brow_inp == '5' or brow_inp == '05': browser_type = 'Opera'
    elif brow_inp == '6' or brow_inp == '06': browser_type = 'UC'
    elif brow_inp == '0' or brow_inp == '00': browser_type = 'Random'
    else: browser_type = 'Brave'
    
    print(f"{GREEN} ┣ {GREEN}✓{GREEN}┫ Selected Browser {EKL} {browser_type}")

    # Worker threads selection
    print(f"{LINE}")
    w_inp = input(f"{GREEN} ┣ {RED}▶{GREEN}┫ Enter number of Threads/Workers (30 recommended) {EKL} ")
    if w_inp.strip():
        maxworker = int(w_inp)
    else:
        maxworker = 30

    clear_logo()
    reset_counters()
    
    # Show process banner
    print(f"{GREEN} ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"{GREEN} ┃    ⚡ PROCESS RUNNING           ┃")
    print(f"{GREEN} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print(f"{LINE}")
    print(f"{GREEN} ┣ {WHITE}📱{GREEN}┫ Target: Facebook Account Recovery")
    print(f"{GREEN} ┣ {WHITE}🔗{GREEN}┫ Server: {server_domain}")
    print(f"{GREEN} ┣ {WHITE}🧵{GREEN}┫ Threads: {maxworker}")
    print(f"{GREEN} ┣ {WHITE}🌐{GREEN}┫ Browser: {browser_type}")
    print(f"{LINE}")
    
    sem = threading.Semaphore(maxworker + 10)
    
    try:
        with threadpol(max_workers=maxworker) as executor:
            remaining_numbers = list(numbers)
            
            for num in numbers:
                sem.acquire()
                
                proxy_data = next(PROXY_ITERATOR) if PROXY_ITERATOR else None
                current_proxy = proxy_data['proxy'] if proxy_data else None
                current_locale = proxy_data['locale'] if proxy_data else 'en_US'
                
                future = executor.submit(check, num, current_proxy, current_locale, browser_type, 0, server_domain)
                future.add_done_callback(lambda _: sem.release())
                
                if remaining_numbers:
                    remaining_numbers.pop(0)
                    with open('Number_List.txt', 'w') as f:
                        for n in remaining_numbers:
                            f.write(n + '\n')
    except:
        maxworker = 30

    with print_lock:
        sys.stdout.write('\r                                                                                \r')
        sys.stdout.flush()

    # Show results
    print(f"{LINE}")
    print(f"{GREEN} ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"{GREEN} ┃    📊 PROCESS COMPLETED         ┃")
    print(f"{GREEN} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print(f"{LINE}")
    print(f'{GREEN} ┣ {WHITE}✅{GREEN}┫ Completed Forgetting {WHITE}{total_checked}{GREEN} Numbers.')
    print(f'{GREEN} ┣ {GREEN}✓{GREEN}┫ Total Success: {GREEN}{total_success}{GREEN} Numbers.')
    print(f'{GREEN} ┣ {YELLOW}⚠{GREEN}┫ Total Failed: {YELLOW}{total_failed}{GREEN} Numbers.')
    print(f'{GREEN} ┣ {RED}✗{GREEN}┫ Total Error: {RED}{total_error}{GREEN} Numbers.')
    print(f"{LINE}")
    
    while True:
        try:
            choice = input(f"{WHITE} ┣ {WHITE}⏎{WHITE}┫ Press Enter to Start Again or Type 'M' for Main Menu {EKL} ")
            if choice.lower() in ('m', 'menu'):
                DHIRAJ_main()
                return
            break
        except Exception as e:
            print(f"{RED} ┣ {RED}✗{RED}┫ Error in loop {EKL} {e}")
            input(f"{WHITE} ┣ {WHITE}⏎{WHITE}┫ Press Enter to return...")
            DHIRAJ_main()
            return

def process_sms(session, resp_text, number, url, base_headers, server_domain):
    if 'id="contact_point_selector_form"' in resp_text and 'name="recover_method"' in resp_text:
        sms_options = re.findall('input type="radio" name="recover_method" value="(send_sms:.*?)".*?id="(.*?)"', resp_text)
        
        target_value = None
        for val, inp_id in sms_options:
            label_match = re.search('label for="' + re.escape(inp_id) + '".*?<div class="_52jc _52j9">(.*?)</div>', resp_text, re.DOTALL)
            if label_match:
                visible_text = label_match.group(1)
                vis_digits = ''.join(filter(str.isdigit, visible_text))
                
                if number.endswith(vis_digits):
                    target_value = val
                    safe_print(f"{CYAN} ┣ {CYAN}📨{CYAN}┫ SMS Option Found {EKL} {visible_text}")
                    break
                    
        if target_value:
            try:
                lsd = re.search('name="lsd" value="(.*?)"', resp_text).group(1) if re.search('name="lsd" value="(.*?)"', resp_text) else ''
                jazoest = re.search('name="jazoest" value="(.*?)"', resp_text).group(1) if re.search('name="jazoest" value="(.*?)"', resp_text) else ''
                
                action_match = re.search('<form.*?action="(.*?)".*?id="contact_point_selector_form"', resp_text, re.DOTALL)
                if action_match:
                    action_url = action_match.group(1).replace('&amp;', '&')
                    full_url = f"https://{server_domain}{action_url}"
                else:
                    full_url = f"https://{server_domain}/ajax/recover/initiate/"
                
                headers = base_headers.copy()
                headers.update({
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'cache-control': 'max-age=0',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': f"https://{server_domain}",
                    'referer': url
                })
                
                data = {
                    'lsd': lsd,
                    'jazoest': jazoest,
                    'recover_method': target_value,
                    'reset_action': 'Continue'
                }
                
                params = {
                    'c': '/login/',
                    'ctx': 'initate_view',
                    'sr': '0',
                    'ars': 'facebook_login'
                }
                
                DHIRAJ_respns = session.post(full_url, headers=headers, data=data, params=params)
                
                if 'action="/recover/code/' in DHIRAJ_respns.text:
                    update_counter('success', number, "SMS Sent Successfully", GREEN)
                    return True
                else:
                    update_counter('failed', number, "Code Sent Failed - Skipping...", RED)
                    return True
            except:
                pass
        else:
            update_counter('failed', number, "SMS Option Not Found/Mismatch - Skipping...", YELLOW)
            return True
            
    return False

def check(number, proxy=None, locale='en_US', browser_type='Brave', retry_count=0, server_domain='m.facebook.com'):
    DHIRAJ_respns = None
    session = requests.Session()
    
    if proxy:
        session.proxies.update(proxy)
    elif PROXIES:
        session.proxies.update(PROXIES)

    if browser_type == 'Random':
        browser_list = ['Brave', 'Chrome', 'Firefox', 'Samsung', 'Opera', 'UC']
        current_browser = random.choice(browser_list)
    else:
        current_browser = browser_type

    andro_ver = random.choice(['4.0.3', '4.0.4', '4.1.2', '4.2.2', '4.3', '4.4.2', '4.4.4', '5.0', '5.0.2', '5.1.1', '6.0', '6.0.1', '7.0', '7.1.1'])
    models = ['SM-G900F', 'SM-G920F', 'SM-G930F', 'SM-G935F', 'SM-J320F', 'SM-J500F', 'SM-J700F', 'SM-A300FU', 'SM-A500FU', 'SM-N910F', 'SM-N920C', 'LG-H815', 'LG-H850', 'LG-D855', 'LG-K420', 'XT1068', 'XT1092', 'XT1562', 'XT1635', 'E6653', 'F5121', 'D6603', 'ALE-L21', 'VNS-L31', 'PRA-LX1']
    model = random.choice(models)
    
    if andro_ver.startswith('4'):
        build_prefix = random.choice(['KOT49', 'KTU84', 'JZO54', 'JSS15'])
    elif andro_ver.startswith('5'):
        build_prefix = random.choice(['LRX21', 'LMY47', 'LRX22'])
    elif andro_ver.startswith('6'):
        build_prefix = random.choice(['MRA58', 'MMB29'])
    elif andro_ver.startswith('7'):
        build_prefix = random.choice(['NRD90', 'NMF26'])
    else:
        build_prefix = 'LMY47'
        
    build = f"{build_prefix}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{random.randint(35, 65)}"
    chrome_ver = f"{random.randint(35, 65)}.0.{random.randint(1500, 4000)}.{random.randint(40, 150)}"
    base_ua = f"Mozilla/5.0 (Linux; Android {andro_ver}; {model} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"
    
    base_headers = {}
    
    # Browser headers for 6 options
    if current_browser == 'Brave':
        ua = base_ua
        base_headers = {
            'sec-ch-ua': '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
        }
    elif current_browser == 'Chrome':
        ua = base_ua
        base_headers = {
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
        }
    elif current_browser == 'Firefox':
        rv_ver = random.randint(40, 60)
        ua = f"Mozilla/5.0 (Android {andro_ver}; Mobile; rv:{rv_ver}.0) Gecko/{rv_ver}.0 Firefox/{rv_ver}.0"
        base_headers = {
            'sec-ch-ua': '"Firefox";v="60", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
        }
    elif current_browser == 'Samsung':
        ua = f"{base_ua} SamsungBrowser/10.0"
        base_headers = {
            'sec-ch-ua': '"Samsung Internet";v="23", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
        }
    elif current_browser == 'Opera':
        ua = f"{base_ua} OPR/60.0.2254.12345"
        base_headers = {
            'sec-ch-ua': '"Opera";v="80", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
        }
    elif current_browser == 'UC':
        ua = f"{base_ua} UBrowser/13.4.0.1306"
        base_headers = {
            'sec-ch-ua': '"UC Browser";v="13", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
        }
    else:  # Default to Brave
        ua = base_ua
        base_headers = {
            'sec-ch-ua': '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
        }
        
    screen_res = random.choice(['320x480', '480x800', '540x960', '800x480', '854x480', '960x540', '720x1280', '1280x720', '1080x1920', '1920x1080', '1440x2560'])
    session.cookies.update({'m_pixel_ratio': '1', 'wd': screen_res})
    
    base_headers.update({
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': f"{locale},en;q=0.9",
        'priority': 'u=0, i',
        'sec-ch-ua-full-version-list': '"Chromium";v="143.0.0.0", "Not A(Brand";v="24.0.0.0"',
        'sec-ch-ua-model': f'"{model}"',
        'sec-ch-ua-platform-version': f'"{andro_ver}"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua
    })
    
    try:
        first_headers = base_headers.copy()
        first_headers.update({'sec-fetch-site': 'none'})
        
        if retry_count == 0:
            safe_print(f"{LIGHT_GRAY} ┣ {LIGHT_GRAY}🔍{LIGHT_GRAY}┫ Searching For {number}...")
            
        git_fb = session.get(f"https://{server_domain}/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0&__mmr=1&_rdr", headers=first_headers)
        
        if 'fr' not in session.cookies:
            pass
            
        try:
            lsd = re.search('name="lsd" value="(.*?)"', str(git_fb.text)).group(1)
        except:
            lsd = re.search('\\["LSD",\\[\\],\\{"token":"(.*?)"\\}', str(git_fb.text)).group(1)

        try:
            jazoest = re.search('name="jazoest" value="(.*?)"', str(git_fb.text)).group(1)
        except:
            jazoest = re.search('"initSprinkleValue":"(.*?)"', str(git_fb.text)).group(1)
            
        _data = {
            'lsd': lsd,
            'jazoest': jazoest,
            'email': number,
            'did_submit': 'Search'
        }
        
        post_headers = base_headers.copy()
        post_headers.update({
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': f"https://{server_domain}",
            'referer': f"https://{server_domain}/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0"
        })
        
        url = f"https://{server_domain}/login/identify/?ctx=recover&c=%2Flogin%2F&search_attempts=1&ars=facebook_login&alternate_search=0&show_friend_search_filtered_list=0&birth_month_search=0&city_search=0"
        DHIRAJ_respns = session.post(url, data=_data, headers=post_headers, allow_redirects=True)
        
        if 'id="login_identify_search_error_msg"' in DHIRAJ_respns.text:
            update_counter('failed', number, "Account Not Found", MAGENTA)
            return
            
        if 'action="/login/identify/?ctx=recover' in DHIRAJ_respns.text:
            update_counter('failed', number, "Multiple Account Found - Skipping...", GOLD)
            return

        if DHIRAJ_respns.url.startswith(f"https://{server_domain}/login/account_recovery/name_search/"):
            headers = base_headers.copy()
            headers.update({
                'referer': f"https://{server_domain}/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0&__mmr=1&_rdr"
            })
            DHIRAJ_respns = session.get(DHIRAJ_respns.url, headers=headers)
            
            safe_print(f"{VIOLET} ┣ {VIOLET}🔄{VIOLET}┫ Clicking Try to another way...")
            
            if 'action="/login/account_recovery/name_search/?flow=initiate_view' in DHIRAJ_respns.text:
                headers = base_headers.copy()
                headers.update({'referer': DHIRAJ_respns.url})
                DHIRAJ_respns = session.get(f"https://{server_domain}/recover/initiate/?c=%2Flogin%2F&fl=initiate_view&ctx=msite_initiate_view", headers=headers)
                
                if process_sms(session, DHIRAJ_respns.text, number, DHIRAJ_respns.url, base_headers, server_domain):
                    return

            if 'name="pass"' in DHIRAJ_respns.text and '/login/account_recovery/' in DHIRAJ_respns.text:
                update_counter('failed', number, "Only Password Option Found - Skipping...", ORANGE)
                return
            
            update_counter('error', number, "Unknown Page (No Selector) - Skipping...", ORANGE, html_content=DHIRAJ_respns.text)
            return

        elif DHIRAJ_respns.url.startswith(f"https://{server_domain}/login/device-based/ar/login/?ldata="):
            headers = base_headers.copy()
            headers.update({
                'referer': f"https://{server_domain}/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0&__mmr=1&_rdr"
            })
            DHIRAJ_respns = session.get(DHIRAJ_respns.url, headers=headers)
            
            if 'id="contact_point_selector_form"' in DHIRAJ_respns.text:
                try:
                    try_another_way_url = re.search('href="(/recover/initiate/\\?privacy_mutation_token=.*?)"', DHIRAJ_respns.text).group(1)
                    try_another_way_url = try_another_way_url.replace('&amp;', '&')
                except:
                    pass

                is_sms_checked = re.search('input type="radio" name="recover_method" value="send_sms:.*?".*?checked="1"', DHIRAJ_respns.text)
                if is_sms_checked:
                    if process_sms(session, DHIRAJ_respns.text, number, DHIRAJ_respns.url, base_headers, 'm.facebook.com'):
                        return
                    return
                
                headers = base_headers.copy()
                headers.update({'referer': DHIRAJ_respns.url})
                DHIRAJ_respns = session.get(f"https://{server_domain}{try_another_way_url}", headers=headers)
                
                safe_print(f"{VIOLET} ┣ {VIOLET}🔄{VIOLET}┫ Clicking Try to another way...")
                
                if process_sms(session, DHIRAJ_respns.text, number, DHIRAJ_respns.url, base_headers, server_domain):
                    return
                
                update_counter('error', number, "Unknown Page after try another way - Skipping...", ORANGE, html_content=DHIRAJ_respns.text)
                return

            if 'name="captcha_response"' in DHIRAJ_respns.text:
                try:
                    match = re.search('src="(https://.*?/captcha/tfbimage\\.php\\?.*?)"', DHIRAJ_respns.text)
                    if match:
                        captcha_img = match.group(1).replace('&amp;', '&')
                except:
                    pass
                update_counter('failed', number, "Captcha Found - Skipping...", PURPLE)
                return
            
            if '/help/121104481304395' in DHIRAJ_respns.text or '/help/103873106370583' in DHIRAJ_respns.text:
                update_counter('failed', number, "Account Disabled - Skipping...", TOXIC)
                return
            
            if 'class="area error"' in DHIRAJ_respns.text:
                if retry_count < 3:
                    check(number, proxy, locale, browser_type, retry_count + 1, server_domain)
                return

            update_counter('error', number, "Unknown Page (Device Based) - Skipping...", ORANGE, html_content=DHIRAJ_respns.text)
            return

        if 'window.MPageLoadClientMetrics' in DHIRAJ_respns.text:
             if retry_count < 3:
                check(number, proxy, locale, browser_type, retry_count + 1, server_domain)
                return
             update_counter('error', number, "Unknown Page (Bot Block) - Skipping...", RED, html_content=DHIRAJ_respns.text)
             return
        
        if '/r.php?next=' in DHIRAJ_respns.text or '/login.php?next=' in DHIRAJ_respns.text:
            if retry_count < 3:
                check(number, proxy, locale, browser_type, retry_count + 1, server_domain)
            return
            
        if "Your Request Couldn't be Processed" in DHIRAJ_respns.text:
             update_counter('error', number, "Your Request Couldn't be Processed", RED, html_content=DHIRAJ_respns.text)
             return
            
        update_counter('error', number, "Unknown Page - Skipping...", ORANGE, html_content=DHIRAJ_respns.text)

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.ChunkedEncodingError) as e:
        safe_print(f"{RED} ┣ {RED}🌐{RED}┫ Network Error {EKL} {e}")
        safe_print(f"{LIGHT_GRAY} ┣ {LIGHT_GRAY}⏳{LIGHT_GRAY}┫ Waiting 5 seconds before retrying...")
        time.sleep(5)
        
        err_content = str(e)
        if DHIRAJ_respns and hasattr(DHIRAJ_respns, 'text'):
            err_content = DHIRAJ_respns.text
            
        update_counter('error', f"Network Error: {e}", message=f"Network Error: {e}", html_content=err_content)

    except Exception as e:
        if retry_count < 3:
            check(number, proxy, locale, browser_type, retry_count + 1, server_domain)
            return
            
        err_content = str(e)
        if DHIRAJ_respns and hasattr(DHIRAJ_respns, 'text'):
            err_content = DHIRAJ_respns.text
            
        update_counter('error', number, f"Unexpected Error: {e}", RED, html_content=err_content)

def main():
    try:
        print(f"{GREEN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print(f"{GREEN}┃     🚀 TOOL STARTED            ┃")
        print(f"{GREEN}┃    🎯 ELEVIX FB FORGET         ┃")
        print(f"{GREEN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print(f"{LINE}")
        DHIRAJ_main()
    except KeyboardInterrupt:
        print(f"\n{RED} ┣ {RED}✗{RED}┫ EXITED BY USER{WHITE}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED} ┣ {RED}✗{RED}┫ ERROR: {e}{WHITE}")
        sys.exit(1)

if __name__ == '__main__':
    main()