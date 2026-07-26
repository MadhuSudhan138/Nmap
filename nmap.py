#!/usr/bin/env python3
"""
Interactive Nmap Scanner Pro
Clear numbering • Category menu • Execute scans
"""

import subprocess
import sys
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich import box
except ImportError:
    print("[!] Rich library required. Install with: pip install rich")
    sys.exit(1)

console = Console()

# ──────────────────────────────────────────────
# SCAN DATABASE
# ──────────────────────────────────────────────

categories = {
    "1": {
        "name": "Basic Scans",
        "color": "green",
        "opts": [
            ("1",  "Quick Scan (Top 100 ports)",      "nmap -T4 -F {t}"),
            ("2",  "Quick Scan Plus (Top 1000)",       "nmap -T4 --top-ports 1000 {t}"),
            ("3",  "Full Port Scan (All 65535)",       "nmap -T4 -p- {t}"),
            ("4",  "Full Scan + Version Detect",       "nmap -T4 -sV -p- {t}"),
            ("5",  "Ping Sweep (Host Discovery)",      "nmap -sn {t}"),
            ("6",  "Show Only Open Ports",             "nmap --open {t}"),
            ("7",  "Scan with Reverse DNS",            "nmap -R {t}"),
        ]
    },
    "2": {
        "name": "Scan Techniques",
        "color": "blue",
        "opts": [
            ("1",  "TCP SYN Scan (Stealth, root)",     "sudo nmap -sS -T4 {t}"),
            ("2",  "TCP Connect Scan (no root)",       "nmap -sT -T4 {t}"),
            ("3",  "TCP ACK Scan (Firewall Map)",      "nmap -sA {t}"),
            ("4",  "TCP Window Scan",                  "nmap -sW {t}"),
            ("5",  "TCP FIN Scan",                     "nmap -sF -T4 {t}"),
            ("6",  "TCP Xmas Scan",                    "nmap -sX -T4 {t}"),
            ("7",  "TCP Null Scan",                    "nmap -sN -T4 {t}"),
            ("8",  "TCP Maimon Scan",                  "nmap -sM -T4 {t}"),
            ("9",  "UDP Scan (Top 50)",                "nmap -sU --top-ports 50 {t}"),
            ("10", "UDP Scan (Top 100)",               "nmap -sU --top-ports 100 {t}"),
            ("11", "IP Protocol Scan",                 "nmap -sO {t}"),
            ("12", "SCTP INIT Scan",                   "nmap -sY {t}"),
        ]
    },
    "3": {
        "name": "Service & OS Detection",
        "color": "yellow",
        "opts": [
            ("1",  "Service Version Detection",        "nmap -sV {t}"),
            ("2",  "Light Version Detection",          "nmap -sV --version-light {t}"),
            ("3",  "Intense Version Detection",        "nmap -sV --version-all {t}"),
            ("4",  "Version + Intensity Level 5",      "nmap -sV --version-intensity 5 {t}"),
            ("5",  "OS Detection",                     "nmap -O {t}"),
            ("6",  "OS Detection + Guess",             "nmap -O --osscan-guess {t}"),
            ("7",  "OS + Version Combined",            "nmap -O -sV {t}"),
            ("8",  "Aggressive Scan (-A)",             "nmap -A {t}"),
            ("9",  "Traceroute Only",                  "nmap --traceroute {t}"),
        ]
    },
    "4": {
        "name": "NSE Script Scans",
        "color": "bright_red",
        "opts": [
            ("1",  "Default Scripts (-sC)",            "nmap -sC {t}"),
            ("2",  "Vulnerability Scan",               "nmap --script vuln {t}"),
            ("3",  "Exploit Check",                    "nmap --script exploit {t}"),
            ("4",  "Brute Force Attacks",              "nmap --script brute {t}"),
            ("5",  "Malware Detection",                "nmap --script malware {t}"),
            ("6",  "Intrusive Scans",                  "nmap --script intrusive {t}"),
            ("7",  "Safe Scripts Only",                "nmap --script safe {t}"),
            ("8",  "All Scripts",                      "nmap --script all {t}"),
            ("9",  "HTTP Enumeration",                 "nmap --script http-enum {t}"),
            ("10", "HTTP Security Headers",            "nmap --script http-security-headers {t}"),
            ("11", "SSL/TLS Cipher Enum",              "nmap --script ssl-enum-ciphers {t}"),
            ("12", "SMB Enumeration",                  "nmap --script smb-enum-shares,smb-os-discovery {t}"),
            ("13", "DNS Enumeration",                  "nmap --script dns-brute,dns-zone-transfer {t}"),
            ("14", "MySQL Audit",                      "nmap --script mysql-audit,mysql-enum {t}"),
            ("15", "FTP Enumeration",                  "nmap --script ftp-anon,ftp-brute {t}"),
            ("16", "SSH Enumeration",                  "nmap --script ssh2-enum-algos,ssh-hostkey {t}"),
            ("17", "SNMP Enumeration",                 "nmap --script snmp-info,snmp-interfaces {t}"),
            ("18", "RDP Enumeration",                  "nmap --script rdp-sec-check,rdp-enum-encryption {t}"),
        ]
    },
    "5": {
        "name": "Firewall Evasion",
        "color": "red",
        "opts": [
            ("1",  "Packet Fragmentation",             "nmap -f {t}"),
            ("2",  "Max Fragmentation",                "nmap -ff {t}"),
            ("3",  "Custom MTU (32)",                  "nmap --mtu 32 {t}"),
            ("4",  "Decoy Scan (5 decoys)",            "nmap -D RND:5,ME {t}"),
            ("5",  "Decoy with Custom IPs",            "nmap -D 10.0.0.1,10.0.0.2,ME {t}"),
            ("6",  "Source Port Spoof (53/DNS)",       "nmap --source-port 53 {t}"),
            ("7",  "Source Port Spoof (20/FTP)",       "nmap --source-port 20 {t}"),
            ("8",  "Append Random Data",               "nmap --data-length 200 {t}"),
            ("9",  "Sneaky Speed (T1)",                "nmap -T1 {t}"),
            ("10", "Polite Speed (T2)",                "nmap -T2 {t}"),
            ("11", "Spoof MAC Address",                "nmap --spoof-mac 0 {t}"),
            ("12", "Randomize Host Order",             "nmap --randomize-hosts {t}"),
            ("13", "Send Bad Checksum",                "nmap --badsum {t}"),
            ("14", "TTL Spoof (128)",                  "nmap --ttl 128 {t}"),
            ("15", "Route Through Tor/Proxy",          "nmap --proxies socks4://127.0.0.1:9050 {t}"),
            ("16", "Idle Zombie Scan",                 "nmap -sI ZOMBIE_IP {t}"),
        ]
    },
    "6": {
        "name": "Timing & Performance",
        "color": "magenta",
        "opts": [
            ("1",  "Paranoid (T0 - IDS safe)",         "nmap -T0 {t}"),
            ("2",  "Sneaky (T1)",                      "nmap -T1 {t}"),
            ("3",  "Polite (T2)",                      "nmap -T2 {t}"),
            ("4",  "Normal (T3 - Default)",            "nmap -T3 {t}"),
            ("5",  "Aggressive (T4)",                  "nmap -T4 {t}"),
            ("6",  "Insane (T5 - Max speed)",          "nmap -T5 {t}"),
            ("7",  "Min Rate (100 pkts/sec)",          "nmap --min-rate 100 {t}"),
            ("8",  "Max Rate (50 pkts/sec)",           "nmap --max-rate 50 {t}"),
            ("9",  "Host Timeout (5 min)",             "nmap --host-timeout 5m {t}"),
            ("10", "Scan Delay (1 second)",            "nmap --scan-delay 1s {t}"),
            ("11", "Small Parallel Groups",            "nmap --min-hostgroup 1 --max-hostgroup 16 {t}"),
            ("12", "Large Parallel Groups",            "nmap --min-hostgroup 64 --max-hostgroup 128 {t}"),
            ("13", "Zero Retries",                     "nmap --max-retries 0 {t}"),
            ("14", "Max Retries (5)",                  "nmap --max-retries 5 {t}"),
        ]
    },
    "7": {
        "name": "Output & Reporting",
        "color": "bright_blue",
        "opts": [
            ("1",  "Save Normal Output",               "nmap {a} -oN scan_{t}_{d}.txt {t}"),
            ("2",  "Save XML Output",                  "nmap {a} -oX scan_{t}_{d}.xml {t}"),
            ("3",  "Save All Formats (Normal+XML+Greppable)", "nmap {a} -oA scan_{t}_{d} {t}"),
            ("4",  "Verbose Output (-v)",              "nmap -v {t}"),
            ("5",  "Very Verbose (-vv)",               "nmap -vv {t}"),
            ("6",  "Debug Output (-d)",                "nmap -d {t}"),
            ("7",  "Show Reason for Port State",       "nmap --reason {t}"),
            ("8",  "Packet Trace",                     "nmap --packet-trace {t}"),
            ("9",  "Stats Every 10 Seconds",           "nmap --stats-every 10s {t}"),
        ]
    },
    "8": {
        "name": "Specialized Scans",
        "color": "cyan",
        "opts": [
            ("1",  "IPv6 Scan",                        "nmap -6 {t}"),
            ("2",  "Scan via Interface (eth0)",        "nmap -e eth0 {t}"),
            ("3",  "Skip DNS Resolution",              "nmap -n {t}"),
            ("4",  "Use Custom DNS (8.8.8.8)",         "nmap --dns-servers 8.8.8.8 {t}"),
            ("5",  "Disable ARP Ping",                 "nmap --disable-arp-ping {t}"),
            ("6",  "Exclude Specific Hosts",           "nmap --exclude 192.168.1.1 {t}"),
            ("7",  "Scan from Target File",            "nmap -iL targets.txt {t}"),
            ("8",  "Exclude from File",                "nmap --excludefile exclude.txt {t}"),
            ("9",  "List Interfaces & Routes",         "nmap --iflist"),
            ("10", "Show Nmap Version",                "nmap -V"),
            ("11", "Custom Nmap Command",              "CUSTOM"),
        ]
    },
}

quick_picks = [
    ("1", "Quick Scan (Top 100)",                       "nmap -T4 -F {t}"),
    ("2", "Aggressive Scan (-A)",                       "nmap -A {t}"),
    ("3", "Full Port + Version Detection",              "nmap -T4 -sV -p- {t}"),
    ("4", "Vulnerability Scan",                         "nmap --script vuln {t}"),
    ("5", "Ping Sweep (Host Discovery)",                "nmap -sn {t}"),
    ("6", "SYN Stealth Scan (needs root)",              "sudo nmap -sS -T4 {t}"),
    ("7", "OS Detection",                               "nmap -O {t}"),
    ("8", "UDP Scan (Top 50)",                          "nmap -sU --top-ports 50 {t}"),
    ("9", "Default Scripts (-sC)",                      "nmap -sC {t}"),
    ("10", "Firewall Evasion Pack",                     "nmap -f --source-port 53 -T2 {t}"),
]


def banner():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan] Nmap Scanner Pro[/bold cyan]     [dim]Interactive • Menu-driven • 60+ scans[/dim]",
        border_style="cyan", padding=(1, 2)
    ))
    console.print()

def main_menu():
    banner()
    console.print("[bold]Select a category:[/bold]\n", style="white")
    for k, v in categories.items():
        console.print(f"  [bold yellow]{k}.[/bold yellow]  {v['name']}")
    console.print(f"  [bold yellow]9.[/bold yellow]  [green]⭐ Quick Picks (most common scans)[/green]")
    console.print(f"  [bold yellow]0.[/bold yellow]  Exit")
    console.print()

def show_scans(cat_key):
    """Show scans for a category in a clean numbered list."""
    cat = categories[cat_key]
    banner()
    console.print(f"[bold {cat['color']}]━━━ {cat['name']} ━━━[/bold {cat['color']}]")
    console.print()
    for opt_id, name, _ in cat["opts"]:
        console.print(f"  [bold yellow]{opt_id.rjust(2)}.[/bold yellow]  {name}")
    console.print()
    console.print(f"  [bold]b[/bold]  ← Back to main menu")
    console.print(f"  [bold]q[/bold]  ← Quit")
    console.print()

def show_quick():
    banner()
    console.print("[bold green]━━━ ⭐ Quick Picks (Most Common Scans) ━━━[/bold green]")
    console.print()
    for opt_id, name, _ in quick_picks:
        console.print(f"  [bold yellow]{opt_id.rjust(2)}.[/bold yellow]  {name}")
    console.print()
    console.print(f"  [bold]b[/bold]  ← Back to main menu")
    console.print(f"  [bold]q[/bold]  ← Quit")
    console.print()

def execute(scan_name, cmd_tpl, target, **kwargs):
    """Execute the scan."""
    d = datetime.now().strftime("%Y%m%d_%H%M%S")
    extra = kwargs.get("extra", "")

    # Handle custom command
    if cmd_tpl == "CUSTOM":
        cmd = Prompt.ask("[bold]Enter your full nmap command[/bold]")
    else:
        cmd = cmd_tpl.format(t=target, d=d, a=extra)

    console.print(f"\n[bold]Scan:[/bold] [green]{scan_name}[/green]")
    console.print(f"[bold]Target:[/bold] [cyan]{target}[/cyan]")
    console.print(f"[bold]Command:[/bold] [dim]{cmd}[/dim]\n")

    confirm = Prompt.ask("[bold]Run?[/bold]", choices=["y", "n"], default="y")
    if confirm.lower() != "y":
        console.print("[yellow]Cancelled.[/yellow]")
        return

    console.print(f"\n[bold yellow]▶ Running... (Ctrl+C to abort)[/bold yellow]\n")
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            console.print(line, end="")
        proc.wait()
        if proc.returncode == 0:
            console.print(f"\n[bold green]✅ Done.[/bold green]")
        else:
            console.print(f"\n[red]Exit code: {proc.returncode}[/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]⛔ Aborted.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")

def pick_target_and_run(name, cmd):
    """Prompt for target and run."""
    target = Prompt.ask("[bold]Target IP or hostname[/bold]")
    extra = ""
    if "{a}" in cmd:
        extra = Prompt.ask("[bold]Additional flags (optional)[/bold]", default="")
    execute(name, cmd, target, extra=extra)


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    try:
        while True:
            main_menu()
            choice = Prompt.ask("[bold]Enter choice[/bold]").strip()

            if choice == "0":
                console.print("\n[bold cyan]Goodbye! Stay ethical. 🛡️[/bold cyan]")
                break

            if choice == "9":
                # Quick Picks
                while True:
                    show_quick()
                    q = Prompt.ask("[bold]Scan number[/bold]").strip().lower()
                    if q == "b":
                        break
                    if q == "q":
                        console.print("\n[bold cyan]Goodbye![/bold cyan]")
                        sys.exit(0)
                    found = None
                    for n, na, c in quick_picks:
                        if q == n:
                            found = (na, c)
                            break
                    if not found:
                        console.print("[red]Invalid number.[/red]")
                        Prompt.ask("[dim]Press Enter...[/dim]")
                        continue
                    pick_target_and_run(found[0], found[1])
                    Prompt.ask("\n[dim]Press Enter...[/dim]")
                continue

            if choice not in categories:
                console.print("[red]Invalid choice.[/red]")
                Prompt.ask("[dim]Press Enter...[/dim]")
                continue

            # Inside a category
            while True:
                show_scans(choice)
                q = Prompt.ask("[bold]Scan number[/bold]").strip().lower()
                if q == "b":
                    break
                if q == "q":
                    console.print("\n[bold cyan]Goodbye![/bold cyan]")
                    sys.exit(0)

                found = None
                for n, na, c in categories[choice]["opts"]:
                    if q == n:
                        found = (na, c)
                        break
                if not found:
                    console.print("[red]Invalid number.[/red]")
                    Prompt.ask("[dim]Press Enter...[/dim]")
                    continue
                pick_target_and_run(found[0], found[1])
                Prompt.ask("\n[dim]Press Enter...[/dim]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)

if __name__ == "__main__":
    main()
