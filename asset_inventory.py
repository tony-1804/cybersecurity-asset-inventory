"""
Cybersecurity Asset Inventory System
Weekly Mini Project - 01

A menu-driven console application that lets a security administrator
add, search, update, delete and display IT assets, and view a
security summary of the organization's inventory.

Data is persisted in data/assets.json.
"""

import json
import os
import re

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

ASSET_TYPES = ["Workstation", "Server", "Router", "Switch", "Application"]
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
SECURITY_STATUS = ["Secure", "Warning", "Vulnerable"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "assets.json")

LINE = "=" * 41
DASH = "-" * 41

IP_PATTERN = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")


# --------------------------------------------------------------------
# Storage helpers
# --------------------------------------------------------------------

def load_assets():
    """Read the asset list from the JSON file. Returns [] if missing."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        print("Warning: data file is not a list. Starting with empty inventory.")
        return []
    except (json.JSONDecodeError, OSError) as err:
        print("Warning: could not read data file ({}). Starting empty.".format(err))
        return []


def save_assets(assets):
    """Write the asset list back to the JSON file."""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(assets, f, indent=4)
        return True
    except OSError as err:
        print("Error: could not save data ({}).".format(err))
        return False


# --------------------------------------------------------------------
# Validation helpers
# --------------------------------------------------------------------

def is_valid_ip(ip):
    """Return True for a well formed IPv4 address."""
    match = IP_PATTERN.match(ip.strip())
    if not match:
        return False
    return all(0 <= int(part) <= 255 for part in match.groups())


def input_non_empty(prompt):
    """Keep asking until the user types something that is not blank."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [!] This field cannot be empty. Please try again.")


def input_choice(prompt, options):
    """Ask the user to pick one of a fixed set of options (case-insensitive)."""
    menu = " / ".join(options)
    while True:
        print("  Options: {}".format(menu))
        value = input(prompt).strip()
        for option in options:
            if value.lower() == option.lower():
                return option
        print("  [!] Invalid choice. Please enter one of the listed options.")


def input_ip(prompt):
    """Ask for an IPv4 address until a valid one is given."""
    while True:
        value = input(prompt).strip()
        if is_valid_ip(value):
            return value
        print("  [!] Invalid IP address. Expected format: 192.168.1.10")


def input_unique_id(assets, prompt):
    """Ask for an Asset ID that is not already used."""
    while True:
        value = input_non_empty(prompt)
        if find_asset(assets, value) is None:
            return value.upper()
        print("  [!] Asset ID '{}' already exists. Enter a different ID.".format(value))


def input_int(prompt, minimum=0):
    """Ask for an integer that is at least `minimum`."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("  [!] Please enter a whole number.")
            continue
        if number < minimum:
            print("  [!] Please enter a number greater than or equal to {}.".format(minimum))
            continue
        return number


# --------------------------------------------------------------------
# Core operations
# --------------------------------------------------------------------

def find_asset(assets, asset_id):
    """Return the asset dict with the given ID, or None."""
    for asset in assets:
        if asset["asset_id"].lower() == asset_id.strip().lower():
            return asset
    return None


def read_asset(assets, index=None):
    """Collect all fields for one asset from the user."""
    if index is not None:
        print("\nAsset {}".format(index))
    asset_id = input_unique_id(assets, "Asset ID: ")
    name = input_non_empty("Asset Name: ")
    asset_type = input_choice("Asset Type: ", ASSET_TYPES)
    ip_address = input_ip("IP Address: ")
    os_name = input_non_empty("Operating System: ")
    department = input_non_empty("Department: ")
    risk_level = input_choice("Risk Level: ", RISK_LEVELS)
    status = input_choice("Security Status: ", SECURITY_STATUS)

    return {
        "asset_id": asset_id,
        "asset_name": name,
        "asset_type": asset_type,
        "ip_address": ip_address,
        "operating_system": os_name,
        "department": department,
        "risk_level": risk_level,
        "security_status": status,
    }


def add_assets(assets):
    """Add one or more assets to the inventory."""
    count = input_int("Enter number of assets: ", minimum=1)
    for i in range(1, count + 1):
        assets.append(read_asset(assets, index=i))
    save_assets(assets)
    print("\n[+] {} asset(s) added successfully.".format(count))


def print_asset(asset):
    """Print a single asset in the required report format."""
    print("Asset ID       : {}".format(asset["asset_id"]))
    print("Asset Name     : {}".format(asset["asset_name"]))
    print("Asset Type     : {}".format(asset["asset_type"]))
    print("IP Address     : {}".format(asset["ip_address"]))
    print("OS             : {}".format(asset["operating_system"]))
    print("Department     : {}".format(asset["department"]))
    print("Risk Level     : {}".format(asset["risk_level"]))
    print("Status         : {}".format(asset["security_status"]))


def display_assets(assets):
    """Print the full inventory followed by the summary block."""
    if not assets:
        print("\n[!] Inventory is empty. Add an asset first.")
        return

    print("\n" + LINE)
    print("     CYBERSECURITY ASSET INVENTORY")
    print(LINE)
    for position, asset in enumerate(assets):
        print_asset(asset)
        if position < len(assets) - 1:
            print(DASH)
    print(LINE)
    print("Total Assets        : {}".format(len(assets)))
    print("Critical Assets     : {}".format(count_by(assets, "risk_level", "Critical")))
    print("High Risk Assets    : {}".format(count_by(assets, "risk_level", "High")))
    print("Medium Risk Assets  : {}".format(count_by(assets, "risk_level", "Medium")))
    print("Low Risk Assets     : {}".format(count_by(assets, "risk_level", "Low")))
    print("Vulnerable Assets   : {}".format(count_by(assets, "security_status", "Vulnerable")))
    print(LINE)


def search_asset(assets):
    """Search the inventory by ID, name, type or risk level."""
    if not assets:
        print("\n[!] Inventory is empty. Nothing to search.")
        return

    print("\nSearch by: 1. Asset ID  2. Asset Name  3. Asset Type  4. Risk Level")
    field_map = {
        "1": "asset_id",
        "2": "asset_name",
        "3": "asset_type",
        "4": "risk_level",
    }
    choice = input("Enter choice (1-4): ").strip()
    field = field_map.get(choice)
    if field is None:
        print("[!] Invalid search option.")
        return

    term = input_non_empty("Enter search term: ").lower()
    matches = [a for a in assets if term in a[field].lower()]

    if not matches:
        print("\n[!] No asset found matching '{}'.".format(term))
        return

    print("\n{} match(es) found:".format(len(matches)))
    print(DASH)
    for asset in matches:
        print_asset(asset)
        print(DASH)


def update_asset(assets):
    """Update selected fields of an existing asset."""
    if not assets:
        print("\n[!] Inventory is empty. Nothing to update.")
        return

    asset_id = input_non_empty("Enter Asset ID to update: ")
    asset = find_asset(assets, asset_id)
    if asset is None:
        print("[!] Asset '{}' not found.".format(asset_id))
        return

    print("\nCurrent details:")
    print(DASH)
    print_asset(asset)
    print(DASH)

    print("\nWhich field do you want to update?")
    print(" 1. Asset Name      4. Operating System")
    print(" 2. Asset Type      5. Department")
    print(" 3. IP Address      6. Risk Level")
    print(" 7. Security Status")
    choice = input("Enter choice (1-7): ").strip()

    if choice == "1":
        asset["asset_name"] = input_non_empty("New Asset Name: ")
    elif choice == "2":
        asset["asset_type"] = input_choice("New Asset Type: ", ASSET_TYPES)
    elif choice == "3":
        asset["ip_address"] = input_ip("New IP Address: ")
    elif choice == "4":
        asset["operating_system"] = input_non_empty("New Operating System: ")
    elif choice == "5":
        asset["department"] = input_non_empty("New Department: ")
    elif choice == "6":
        asset["risk_level"] = input_choice("New Risk Level: ", RISK_LEVELS)
    elif choice == "7":
        asset["security_status"] = input_choice("New Security Status: ", SECURITY_STATUS)
    else:
        print("[!] Invalid option. No changes made.")
        return

    save_assets(assets)
    print("\n[+] Asset '{}' updated successfully.".format(asset["asset_id"]))


def delete_asset(assets):
    """Delete an asset after confirmation."""
    if not assets:
        print("\n[!] Inventory is empty. Nothing to delete.")
        return

    asset_id = input_non_empty("Enter Asset ID to delete: ")
    asset = find_asset(assets, asset_id)
    if asset is None:
        print("[!] Asset '{}' not found.".format(asset_id))
        return

    print("\nAsset to be deleted:")
    print(DASH)
    print_asset(asset)
    print(DASH)

    confirm = input("Are you sure you want to delete this asset? (y/n): ").strip().lower()
    if confirm == "y":
        assets.remove(asset)
        save_assets(assets)
        print("\n[+] Asset '{}' deleted successfully.".format(asset["asset_id"]))
    else:
        print("\n[i] Delete cancelled.")


def count_by(assets, field, value):
    """Count assets whose `field` equals `value`."""
    return sum(1 for asset in assets if asset[field] == value)


def security_summary(assets):
    """Print risk/status breakdowns and list the assets needing attention."""
    if not assets:
        print("\n[!] Inventory is empty. Nothing to summarize.")
        return

    total = len(assets)
    print("\n" + LINE)
    print("        SECURITY SUMMARY REPORT")
    print(LINE)

    print("Risk Level Breakdown")
    print(DASH)
    for level in RISK_LEVELS:
        count = count_by(assets, "risk_level", level)
        percent = (count / total) * 100
        print("{:<12}: {:>3}  ({:5.1f}%)".format(level, count, percent))

    print("\nSecurity Status Breakdown")
    print(DASH)
    for status in SECURITY_STATUS:
        count = count_by(assets, "security_status", status)
        percent = (count / total) * 100
        print("{:<12}: {:>3}  ({:5.1f}%)".format(status, count, percent))

    print("\nAsset Type Breakdown")
    print(DASH)
    for asset_type in ASSET_TYPES:
        count = count_by(assets, "asset_type", asset_type)
        if count:
            print("{:<12}: {:>3}".format(asset_type, count))

    attention = [
        a for a in assets
        if a["risk_level"] in ("High", "Critical") or a["security_status"] == "Vulnerable"
    ]

    print("\nAssets Requiring Immediate Attention")
    print(DASH)
    if attention:
        for asset in attention:
            print("{:<8} {:<14} {:<10} {}".format(
                asset["asset_id"],
                asset["asset_name"],
                asset["risk_level"],
                asset["security_status"],
            ))
    else:
        print("None. All assets are within acceptable risk levels.")
    print(LINE)


# --------------------------------------------------------------------
# Menu
# --------------------------------------------------------------------

def show_menu():
    print("\n" + LINE)
    print("   CYBERSECURITY ASSET INVENTORY SYSTEM")
    print(LINE)
    print(" 1. Add Asset")
    print(" 2. Display All Assets")
    print(" 3. Search Asset")
    print(" 4. Update Asset")
    print(" 5. Delete Asset")
    print(" 6. Security Summary")
    print(" 7. Exit")
    print(LINE)


def main():
    assets = load_assets()
    actions = {
        "1": add_assets,
        "2": display_assets,
        "3": search_asset,
        "4": update_asset,
        "5": delete_asset,
        "6": security_summary,
    }

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "7":
            save_assets(assets)
            print("\nInventory saved. Exiting the system. Stay secure!\n")
            break

        action = actions.get(choice)
        if action is None:
            print("\n[!] Invalid choice. Please enter a number between 1 and 7.")
        else:
            action(assets)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted. Exiting.\n")
