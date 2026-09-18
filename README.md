# Week-01 — Cybersecurity Asset Inventory System

A menu-driven console application that helps a security administrator maintain
an inventory of an organization's IT assets — workstations, servers, routers,
switches and applications — and track the security risk attached to each one.

Managing assets on paper or in scattered spreadsheets makes it hard to answer
the question that matters most during an incident: *which machines need
attention right now?* This project keeps every asset in one place, classifies
it by type and risk level, and produces a summary that highlights the assets
that are critical, high risk or vulnerable.

---

## Features

- **Add** one or many assets in a single session
- **Display** the complete inventory in a formatted report with a summary block
- **Search** by Asset ID, Asset Name, Asset Type or Risk Level (partial and
  case-insensitive)
- **Update** any field of an existing asset
- **Delete** an asset with a confirmation prompt
- **Security summary** with risk, status and type breakdowns, percentages, and
  a list of assets requiring immediate attention
- **Input validation** for IP addresses, duplicate Asset IDs, empty fields and
  all fixed-choice fields
- **Persistent storage** in `data/assets.json`, so the inventory survives
  restarts

---

## Repository Structure

```
Week-01-Cybersecurity-Asset-Inventory/
│
├── src/
│   └── asset_inventory.py
│
├── data/
│   └── assets.json
│
├── tests/
│   └── test_cases.md
│
├── screenshots/
│   ├── 01-add-asset.png
│   ├── 02-display-assets.png
│   ├── 03-search-asset.png
│   ├── 04-update-asset.png
│   ├── 05-delete-asset.png
│   ├── 06-security-summary.png
│   └── 07-input-validation.png
│
└── README.md
```

---

## Requirements

- Python 3.6 or later
- No external libraries — only the standard library (`json`, `os`, `re`)

---

## How to Run

```bash
git clone https://github.com/<your-username>/Week-01-Cybersecurity-Asset-Inventory.git
cd Week-01-Cybersecurity-Asset-Inventory
python3 src/asset_inventory.py
```

On Windows, use `python src\asset_inventory.py`.

The repository ships with three sample assets in `data/assets.json`. To start
from an empty inventory, replace the contents of that file with `[]`.

---

## Data Fields

| Field | Description | Allowed Values |
|-------|-------------|----------------|
| Asset ID | Unique identifier | Any non-empty text, must be unique |
| Asset Name | Friendly name of the asset | Any non-empty text |
| Asset Type | Category of the asset | Workstation, Server, Router, Switch, Application |
| IP Address | IPv4 address | Valid IPv4 (e.g. 192.168.1.10) |
| Operating System | OS or firmware running on the asset | Any non-empty text |
| Department | Owning department | Any non-empty text |
| Risk Level | Assessed risk | Low, Medium, High, Critical |
| Security Status | Current security posture | Secure, Warning, Vulnerable |

---

## Sample Run

**Input**

```
Enter number of assets: 3

Asset 1
Asset ID: A101
Asset Name: HR-PC-01
Asset Type: Workstation
IP Address: 192.168.1.10
Operating System: Windows 11
Department: HR
Risk Level: Medium
Security Status: Secure

Asset 2
Asset ID: A102
Asset Name: Web-Server
Asset Type: Server
IP Address: 192.168.1.20
Operating System: Ubuntu
Department: IT
Risk Level: Critical
Security Status: Vulnerable

Asset 3
Asset ID: A103
Asset Name: Core-Router
Asset Type: Router
IP Address: 192.168.1.1
Operating System: Cisco IOS
Department: Network
Risk Level: High
Security Status: Warning
```

**Output**

```
=========================================
     CYBERSECURITY ASSET INVENTORY
=========================================
Asset ID       : A101
Asset Name     : HR-PC-01
Asset Type     : Workstation
IP Address     : 192.168.1.10
OS             : Windows 11
Department     : HR
Risk Level     : Medium
Status         : Secure
-----------------------------------------
Asset ID       : A102
Asset Name     : Web-Server
Asset Type     : Server
IP Address     : 192.168.1.20
OS             : Ubuntu
Department     : IT
Risk Level     : Critical
Status         : Vulnerable
-----------------------------------------
Asset ID       : A103
Asset Name     : Core-Router
Asset Type     : Router
IP Address     : 192.168.1.1
OS             : Cisco IOS
Department     : Network
Risk Level     : High
Status         : Warning
=========================================
Total Assets        : 3
Critical Assets     : 1
High Risk Assets    : 1
Medium Risk Assets  : 1
Low Risk Assets     : 0
Vulnerable Assets   : 1
=========================================
```

**Security Summary**

```
=========================================
        SECURITY SUMMARY REPORT
=========================================
Risk Level Breakdown
-----------------------------------------
Low         :   0  (  0.0%)
Medium      :   1  ( 33.3%)
High        :   1  ( 33.3%)
Critical    :   1  ( 33.3%)

Security Status Breakdown
-----------------------------------------
Secure      :   1  ( 33.3%)
Warning     :   1  ( 33.3%)
Vulnerable  :   1  ( 33.3%)

Asset Type Breakdown
-----------------------------------------
Workstation :   1
Server      :   1
Router      :   1

Assets Requiring Immediate Attention
-----------------------------------------
A102     Web-Server     Critical   Vulnerable
A103     Core-Router    High       Warning
=========================================
```

---

## Testing

Twenty-four manual test cases covering every menu option, all validation rules
and data persistence are documented in
[`tests/test_cases.md`](tests/test_cases.md), with matching screenshots in
`screenshots/`.

---

## Concepts Practised

- Dictionaries and lists for structured record storage
- File handling and JSON serialisation for persistence
- Input validation and defensive programming
- Regular expressions for IP address validation
- Modular function design and a menu-driven control loop
- Formatted console output using string formatting

---

## Author

Weekly Mini Project 01 — B.E. Computer Science and Engineering (Cybersecurity)
