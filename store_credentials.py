import keyring
from getpass import getpass
import sys

service_name = "Py_Cisco_IOS_Commands"
cred_username = "Py_Cisco_IOS_Commands_Username"
cred_password = "Py_Cisco_IOS_Commands_Password"
cred_enable = "Py_Cisco_IOS_Commands_Enable"

cred_list = [cred_username, cred_password, cred_enable]

if len(sys.argv) > 1 and sys.argv[1] == "-d":
    for cred in cred_list:
        try:
            keyring.delete_password(service_name, cred)
            print(f"Successfully deleted credentials for {cred}")
        except:
            print(f"Error: Credentials for {cred} under service '{service_name}' not found.")
else:
    username = getpass(f"Enter username: ")
    password = getpass(f"Enter password: ")
    enable = getpass(f"Enter enable: ")
    keyring.set_password(service_name, cred_username, username)
    keyring.set_password(service_name, cred_password, password)
    keyring.set_password(service_name, cred_enable, enable)
    print(f"Credentials saved successfully")