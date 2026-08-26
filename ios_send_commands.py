from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from netmiko import ConnectHandler
import copy
import sys
from getpass import getpass
import keyring
### Custom Import
import IGNORE_ios_devices as ios_devices


###### Functions ######
def send_ios_command(ios_device, ios_command):
    print(f"Connecting to: {ios_device["host"]}")
    with ConnectHandler(**ios_device) as net_connect:
        return [ios_device["host"], net_connect.send_command(ios_command)]

def get_arguments():
    save_to_file = False            # -stf
    save_credentials = False        # -sc

    if len(sys.argv) <= 1:
        print("Error: No arguments provdied")
        print("Example: ios_command -stf (Save to file) -sc (Save Credentials)")
        sys.exit(1)

    ios_command = None
    for index in range(1,len(sys.argv)):
        arg = sys.argv[index]
        if arg == "-stf":
            save_to_file = True
        elif arg == "-sc":
            save_credentials = True
        else:
            ios_command = arg

    if ios_command is None:
        print("No IOS Command provided")
        sys.exit(1)

    print(f"IOS Command: \"{ios_command}\"")
    print(f"Save results to file = {save_to_file}")
    print(f"Save Credentials = {save_credentials}")

    return ios_command, save_to_file, save_credentials

def get_cred(search_target, save_cred):
    mapping = {
        "username" : "Py_Cisco_IOS_Commands_Username",
        "password" : "Py_Cisco_IOS_Commands_Password",
        "enable" : "Py_Cisco_IOS_Commands_Enable",
    }
    cred = keyring.get_password("Py_Cisco_IOS_Commands", mapping[search_target])
    if cred is None: # Ask for credntials if not found
        cred = getpass(f"Enter {search_target}: ")
        return cred
    else:           # return credentials if found
        return cred
    
    
###### Main ######
ios_command, save_to_file, save_credentials = get_arguments()
max_threads = 10


ios_device_template = {
    #"device_type": "cisco_ios_telnet",
    "device_type": "cisco_ios",
    "host": "69.69.69.69",
    "username": get_cred("username", save_credentials),
    "password": get_cred("password", save_credentials),
    "secret" :  get_cred("enable", save_credentials),
}

# Build device list
device_list = []
for device_name, device_ip in ios_devices.ios_devices.items():
    ios_device = copy.deepcopy(ios_device_template)
    ios_device["host"] = device_ip
    device_list.append(ios_device)

# Start threads
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Map applies the function to every item concurrently
    results = executor.map(send_ios_command, device_list, repeat(ios_command))
    # Iterate over results (blocks until each item is ready)
    for result in results:
        device_ip = result[0]
        result_text = result[1]
        print_text = f"==== Host:{device_ip}\n{result_text}"
        if save_to_file == True:
            with open(f"HOST-{device_ip}.txt", "w", encoding="utf-8") as file:
                file.write(print_text)
        else:
            print(print_text)

print("All threads finished execution!")
