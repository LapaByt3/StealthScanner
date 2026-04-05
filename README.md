# StealthScanner
# StealthScanner v1.0

**StealthScanner** is a powerful and fast multi-CMS security testing tool designed for educational purposes and authorized penetration testing. It helps security researchers and website owners identify vulnerabilities in their own WordPress, Joomla, Laravel, and custom CMS websites.

## ⚠️ DISCLAIMER
> **This tool is for EDUCATIONAL PURPOSES and AUTHORIZED TESTING ONLY!**
> - Only use on websites you OWN or have WRITTEN PERMISSION to test
> - Unauthorized access is ILLEGAL
> - The author is NOT responsible for any misuse or damage caused by this tool

## 🚀 Features

- **WordPress Exploits**
  - WP-Install auto setup & shell upload
  - XML-RPC brute force
  - Weak password bypass

- **Joomla Exploits**
  - Admin login brute force
  - Authentication bypass

- **Laravel Exploits**
  - PHPUnit RCE (CVE-2026-24765)
  - .env file exposure check

- **Non-CMS Support**
  - 100+ weak password combinations
  - Auto-detect admin login URLs
  - Generic login form brute force

- **Performance**
  - 50 concurrent threads for super fast scanning
  - 3-second timeout for quick response
  - Automatic file format detection
  - No duplicate scanning with cache system

## 📁 Supported File Formats

- **Domain list format:** `domain.com | http://domain.com/wp-login.php`
- **Plain domains format:** `domain.com` (one per line)

## 🛠️ Requirements

- Python 3.7+
- requests library
- colorama library

## 📊 Output Files

| File | Description |
|------|-------------|
| `hasil_webshell.txt` | Uploaded webshell URLs |
| `hasil_bruteforce.txt` | Valid credentials found |
| `hasil_admin_url.txt` | Discovered admin login URLs |
| `hasil_wp_bruteforce.txt` | WordPress brute force results |
| `hasil_domain_mati.txt` | Expired/dead domains |

## 🔧 Installation

```bash
git clone https://github.com/yourusername/StealthScanner.git
cd StealthScanner
pip install -r requirements.txt
python stealthscanner.py
