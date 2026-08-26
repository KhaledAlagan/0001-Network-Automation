# Rename this file to "ignore_devices.py"

import getpass

ios_device_template = {
    #"device_type": "cisco_ios_telnet",
    "device_type": "cisco_ios",
    "host": "69.69.69.69",
    "username": getpass.getpass("Enter SSH Username: "),
    "password": getpass.getpass("Enter SSH password: "),
    "secret" :  getpass.getpass("Enter Enable Secret: "),
}

ios_devices = {
    "GW1": "192.168.1.1",
    "GW2": "192.168.1.2",
}