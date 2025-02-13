# Advanced IPv4 Subnet Calculator

## Overview
The **Advanced IPv4 Subnet Calculator** is a GUI-based subnet calculator built using **PyQt5**. It allows users to input an IP address and a network prefix to calculate subnet details such as network address, broadcast address, total and usable host addresses, wildcard mask, and more.

## Features
- Determine IP class based on the prefix
- Calculate subnet mask, wildcard mask, and host range
- Display network and broadcast addresses
- Compute total subnets and usable host addresses
- Export subnet details to **TXT, CSV, and JSON** formats
- Simple and user-friendly PyQt5 interface

## Technologies Used
- **Python 3**
- **PyQt5** for GUI
- **ipaddress** module for subnet calculations
- **Logging** for tracking application activity
- **CSV & JSON** support for exporting results

## Installation
### Prerequisites
Ensure you have Python 3 installed. Then, install the required dependencies using:
```bash
pip install PyQt5
```

## Usage
### Running the Application
Run the script using:
```bash
python subnet_calculator.py
```

### How to Use
1. Enter an **IP Address** (e.g., `192.168.1.1`).
2. Enter the **Network Prefix** (e.g., `24`).
3. Click the **Calculate** button to display subnet details.
4. View the report in a popup window.
5. (Optional) Click **Export Results** to save data in TXT, CSV, or JSON format.

### Clearing Input Fields
Click the **Clear** button to reset the input fields.

## Example Output
```
IP Class: C
Total Number of Subnets: 1
Network Address: 192.168.1.0
Custom Subnet Mask: 255.255.255.0
Broadcast Address: 192.168.1.255
Wildcard Mask: 0.0.0.255
Host Range: 192.168.1.1 - 192.168.1.254
Total Number of Host Addresses: 256
Number of Usable Addresses: 254
First Usable IP: 192.168.1.1
Last Usable IP: 192.168.1.254
```

## Logging
The application logs important actions and errors in `subnet_calculator.log`, allowing users to track activity and troubleshoot issues.

## Author
**Sami-Ur-Rehman**

