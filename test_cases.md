# Test Cases — Cybersecurity Asset Inventory System

All tests were run manually against `src/asset_inventory.py` using Python 3.
Screenshots of each run are stored in the `screenshots/` folder.

| # | Test Case | Input | Expected Output | Actual Output | Status | Screenshot |
|---|-----------|-------|-----------------|---------------|--------|------------|
| 1 | Add a single asset | Menu `1`, count `1`, ID `A104`, Name `Sw-01`, Type `Switch`, IP `192.168.1.5`, OS `Cisco IOS`, Dept `Network`, Risk `Low`, Status `Secure` | Asset saved, message `1 asset(s) added successfully` | As expected | Pass | `01-add-asset.png` |
| 2 | Add multiple assets | Menu `1`, count `3`, details of A101/A102/A103 | All three assets stored in `data/assets.json` | As expected | Pass | `01-add-asset.png` |
| 3 | Display all assets | Menu `2` | Formatted inventory report with the summary block | As expected | Pass | `02-display-assets.png` |
| 4 | Display when inventory is empty | Menu `2` with empty `assets.json` | `[!] Inventory is empty. Add an asset first.` | As expected | Pass | `02-display-assets.png` |
| 5 | Search by Asset ID | Menu `3`, option `1`, term `A102` | Web-Server record displayed | As expected | Pass | `03-search-asset.png` |
| 6 | Search by Asset Name (partial) | Menu `3`, option `2`, term `server` | Web-Server record displayed (case-insensitive match) | As expected | Pass | `03-search-asset.png` |
| 7 | Search by Risk Level | Menu `3`, option `4`, term `Critical` | All critical assets listed | As expected | Pass | `03-search-asset.png` |
| 8 | Search with no match | Menu `3`, option `1`, term `A999` | `[!] No asset found matching 'a999'.` | As expected | Pass | `03-search-asset.png` |
| 9 | Update risk level | Menu `4`, ID `A101`, field `6`, new value `High` | Risk level changed to High and saved | As expected | Pass | `04-update-asset.png` |
| 10 | Update IP address | Menu `4`, ID `A103`, field `3`, new value `10.0.0.1` | IP address updated | As expected | Pass | `04-update-asset.png` |
| 11 | Update non-existent asset | Menu `4`, ID `A999` | `[!] Asset 'A999' not found.` | As expected | Pass | `04-update-asset.png` |
| 12 | Delete an asset (confirm) | Menu `5`, ID `A104`, confirm `y` | Asset removed from inventory and file | As expected | Pass | `05-delete-asset.png` |
| 13 | Delete an asset (cancel) | Menu `5`, ID `A101`, confirm `n` | `[i] Delete cancelled.`, asset retained | As expected | Pass | `05-delete-asset.png` |
| 14 | Delete non-existent asset | Menu `5`, ID `A999` | `[!] Asset 'A999' not found.` | As expected | Pass | `05-delete-asset.png` |
| 15 | Security summary | Menu `6` | Risk / status / type breakdown with percentages and the "requires attention" list | As expected | Pass | `06-security-summary.png` |
| 16 | Reject duplicate Asset ID | Add asset with existing ID `A101` | `[!] Asset ID 'A101' already exists.` and re-prompt | As expected | Pass | `07-input-validation.png` |
| 17 | Reject invalid IP address | IP `999.1.1.1` | `[!] Invalid IP address. Expected format: 192.168.1.10` and re-prompt | As expected | Pass | `07-input-validation.png` |
| 18 | Reject invalid asset type | Type `Printer` | `[!] Invalid choice.` and re-prompt with valid options | As expected | Pass | `07-input-validation.png` |
| 19 | Reject invalid risk level | Risk `Extreme` | `[!] Invalid choice.` and re-prompt | As expected | Pass | `07-input-validation.png` |
| 20 | Reject empty field | Asset Name left blank | `[!] This field cannot be empty.` and re-prompt | As expected | Pass | `07-input-validation.png` |
| 21 | Reject non-numeric asset count | Count `abc` | `[!] Please enter a whole number.` and re-prompt | As expected | Pass | `07-input-validation.png` |
| 22 | Reject invalid menu choice | Menu `9` | `[!] Invalid choice. Please enter a number between 1 and 7.` | As expected | Pass | `07-input-validation.png` |
| 23 | Data persistence | Add asset → exit (`7`) → restart program → Menu `2` | The added asset is still present after restart | As expected | Pass | `02-display-assets.png` |
| 24 | Corrupted / missing data file | Delete `data/assets.json` and start the program | Program starts with an empty inventory instead of crashing | As expected | Pass | — |

## Summary

- Total test cases: 24
- Passed: 24
- Failed: 0

## Notes

- Choice fields (Asset Type, Risk Level, Security Status) accept input in any
  case (`server`, `Server`, `SERVER`) and are normalised before storage.
- Searching is case-insensitive and supports partial matches.
- Every add, update and delete writes immediately to `data/assets.json`, so no
  data is lost if the program is closed unexpectedly.
