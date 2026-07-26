#  Nmap Scanner Pro

- An **interactive, menu-driven Nmap wrapper** with 60+ pre-built scan types organized into 8 categories. Pick a scan, enter a target, and go — no need to remember flags.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Nmap](https://img.shields.io/badge/nmap-7.80%2B-red)

---

##  Features

| Feature | Description |
|---|---|
| **60+ Scan Types** | Basic scans, techniques, OS detection, NSE scripts, evasion, timing, output, specialized |
| **8 Categories** | Logically grouped for quick navigation |
| **⭐ Quick Picks** | 10 most common scans for rapid use |
| **Interactive Menu** | Numbered lists — select, enter target, execute |
| **Live Output** | See nmap results stream in real-time |
| **Rich Formatting** | Color-coded terminal UI via the `rich` library |
| **No Memorization** | Every scan's flags are pre-built and explained |

---
# Useage

Pick category → Pick scan → Enter IP → Confirm → Done

# Nmap Scanner Pro Install cmd

```bash
pip install rich
git clone https://github.com/MadhuSudhan138/Nmap.git
python3 nmap.py
```
#	Category	Scans

- 1	Basic Scans	7
- 2	Scan Techniques	12
- 3	Service & OS Detection	9
- 4	NSE Script Scans	18
- 5	Firewall Evasion	16
- 6	Timing & Performance	14
- 7	Output & Reporting	9
- 8	Specialized Scans	11
- 9	⭐ Quick Picks	10

#	Scan	Command (Basic Scans)

- 1	Quick Scan (Top 100)	nmap -T4 -F {t}
- 2	Aggressive (-A)	nmap -A {t}
- 3	Full Port + Version	nmap -T4 -sV -p- {t}
- 4	Vulnerability Scan	nmap --script vuln {t}
- 5	Ping Sweep	nmap -sn {t}
- 6	SYN Stealth (root)	sudo nmap -sS -T4 {t}
- 7	OS Detection	nmap -O {t}
- 8	UDP Scan (Top 50)	nmap -sU --top-ports 50 {t}
- 9	Default Scripts (-sC)	nmap -sC {t}
- 10	Firewall Evasion	nmap -f --source-port 53 -T2 {t}

# ⚠️ Disclaimer

For authorized testing only. Unauthorized scanning is illegal
