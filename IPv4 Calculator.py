from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QFileDialog, QGroupBox, QFormLayout, QHBoxLayout
from PyQt5.QtGui import QIntValidator
import sys
import ipaddress
import logging
import json
import csv

# Setup logging
logging.basicConfig(filename='subnet_calculator.log', level=logging.INFO)

# Function to determine the class of an IP address based on the prefix
def get_ip_class(ip, prefix):
    first_octet = int(ip.split('.')[0])
    if prefix == 8 and 1 <= first_octet <= 126:
        return 'A'
    elif prefix == 16 and 128 <= first_octet <= 191:
        return 'B'
    elif prefix == 24 and 192 <= first_octet <= 223:
        return 'C'
    else:
        return 'Classless'

# Function to calculate the wildcard mask
def calculate_wildcard_mask(subnet_mask):
    subnet_octets = map(int, str(subnet_mask).split('.'))
    wildcard_octets = [255 - octet for octet in subnet_octets]
    return ".".join(map(str, wildcard_octets))

# Function to calculate subnet details based on the prefix and class
def IPv4_Subnet_Calculator(ip, prefix):
    ip_class = get_ip_class(ip, prefix)
    network = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)
    
    # Default subnet mask for Class A, B, and C
    default_prefix = {'A': 8, 'B': 16, 'C': 24}.get(ip_class, prefix)
    custom_subnet_mask = network.netmask
    wildcard_mask = calculate_wildcard_mask(custom_subnet_mask)

    # Calculate total subnets based on default prefix for each class
    total_subnets = 2 ** (prefix - default_prefix) if prefix > default_prefix else 1

    total_host_addresses = network.num_addresses
    usable_addresses = total_host_addresses - 2 if total_host_addresses > 2 else 0

    # Calculate network address, broadcast address, and host range
    network_address = network.network_address
    broadcast_address = network.broadcast_address
    host_range = f"{network_address + 1} - {broadcast_address - 1}" if usable_addresses > 0 else "No usable hosts"
    first_usable = network_address + 1
    last_usable = broadcast_address - 1

    result = {
        "IP Class": ip_class,
        "Total Number of Subnets": total_subnets,
        "Network Address": network_address,
        "Custom Subnet Mask": custom_subnet_mask,
        "Broadcast Address": broadcast_address,
        "Wildcard Mask": wildcard_mask,
        "Host Range": host_range,
        "Total Number of Host Addresses": total_host_addresses,
        "Number of Usable Addresses": usable_addresses,
        "First Usable IP": first_usable,
        "Last Usable IP": last_usable,
    }

    return result

# Main PyQt5 Application Class
class SubnetCalculatorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Advanced IPv4 Subnet Calculator")
        self.setGeometry(100, 100, 500, 400)

        # Define main layout
        main_layout = QtWidgets.QVBoxLayout()

        # Title label
        title = QtWidgets.QLabel("IPv4 Subnet Calculator")
        title.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title)

        # Group box for input fields
        input_group = QGroupBox("Input")
        form_layout = QFormLayout()
        self.ip_entry = QtWidgets.QLineEdit()
        self.prefix_entry = QtWidgets.QLineEdit()
        self.ip_entry.setPlaceholderText("e.g. 192.168.1.1")
        self.prefix_entry.setPlaceholderText("e.g. 24")
        self.prefix_entry.setValidator(QIntValidator(0, 32, self))  # Validate prefix input
        form_layout.addRow("IP Address:", self.ip_entry)
        form_layout.addRow("Network Prefix:", self.prefix_entry)
        input_group.setLayout(form_layout)
        main_layout.addWidget(input_group)

        # Calculate and Clear buttons
        button_layout = QHBoxLayout()
        calculate_button = QtWidgets.QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_subnet)
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(calculate_button)
        button_layout.addWidget(clear_button)
        main_layout.addLayout(button_layout)

        # Creator label at the bottom
        creator_label = QtWidgets.QLabel("Created by Sami-Ur-Rehman")
        creator_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(creator_label)

        # Set main layout
        self.setLayout(main_layout)

        # Connect Enter key press to calculate subnet
        self.ip_entry.returnPressed.connect(self.calculate_subnet)
        self.prefix_entry.returnPressed.connect(self.calculate_subnet)

    # Clear input fields
    def clear_fields(self):
        self.ip_entry.clear()
        self.prefix_entry.clear()
        logging.info("Input fields cleared.")

    # Validate IP and calculate subnet
    def calculate_subnet(self):
        ip_address = self.ip_entry.text()
        prefix = self.prefix_entry.text()

        try:
            # Validate IP format
            ipaddress.IPv4Address(ip_address)
            prefix = int(prefix)

            # Validate prefix range
            if prefix < 0 or prefix > 32:
                raise ValueError("Prefix must be between 0 and 32.")

            subnet_info = IPv4_Subnet_Calculator(ip_address, prefix)
            self.show_report_popup(subnet_info)
            logging.info("Subnet calculation successful.")

        except ValueError as ve:
            QMessageBox.critical(self, "Error", str(ve))
            logging.error(f"ValueError: {str(ve)}")
        except ipaddress.AddressValueError:
            QMessageBox.critical(self, "Error", "Invalid IP address entered.")
            logging.error("Invalid IP address entered.")

    # Show detailed subnet report in a popup
    def show_report_popup(self, subnet_info):
        # Create a popup dialog
        report_popup = QMessageBox(self)
        report_popup.setWindowTitle("Subnet Calculation Result")
        
        # Format the report in the desired order
        report = ""
        report += f"IP Class: {subnet_info['IP Class']}\n"
        report += f"Total Number of Subnets: {subnet_info['Total Number of Subnets']}\n"
        report += f"Network Address: {subnet_info['Network Address']}\n"
        report += f"Custom Subnet Mask: {subnet_info['Custom Subnet Mask']}\n"
        report += f"Broadcast Address: {subnet_info['Broadcast Address']}\n"
        report += f"Wildcard Mask: {subnet_info['Wildcard Mask']}\n"
        report += f"Host Range: {subnet_info['Host Range']}\n"
        report += f"Total Number of Host Addresses: {subnet_info['Total Number of Host Addresses']}\n"
        report += f"Number of Usable Addresses: {subnet_info['Number of Usable Addresses']}\n"
        report += f"First Usable IP: {subnet_info['First Usable IP']}\n"
        report += f"Last Usable IP: {subnet_info['Last Usable IP']}\n"

        # Display the report
        report_popup.setText(report)
        
        # Ask user if they want to export the results
        export_button = report_popup.addButton("Export Results", QMessageBox.AcceptRole)
        report_popup.addButton("Close", QMessageBox.RejectRole)
        
        report_popup.exec_()  # Show the popup

        # Check which button was pressed after the dialog is closed
        if report_popup.clickedButton() == export_button:
            self.export_results(report)

    # Export results to a file
    def export_results(self, report):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Text Files (*.txt);;CSV Files (*.csv);;JSON Files (*.json);;All Files (*)")
        if file_name:
            if file_name.endswith('.txt'):
                with open(file_name, 'w') as file:
                    file.write(report)
                    logging.info(f"Report exported to {file_name}")
            elif file_name.endswith('.csv'):
                self.export_to_csv(file_name, report)
            elif file_name.endswith('.json'):
                self.export_to_json(file_name, report)

    # Export to CSV
    def export_to_csv(self, file_name, report):
        try:
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                # Split report into lines and write to CSV
                for line in report.splitlines():
                    writer.writerow([line])
                logging.info(f"CSV report exported to {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export to CSV: {e}")
            logging.error(f"Failed to export to CSV: {e}")

    # Export to JSON
    def export_to_json(self, file_name, report):
        try:
            with open(file_name, 'w') as file:
                json.dump(report, file)
                logging.info(f"JSON report exported to {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export to JSON: {e}")
            logging.error(f"Failed to export to JSON: {e}")

# Main execution
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    calculator = SubnetCalculatorApp()
    calculator.show()
    sys.exit(app.exec_())
