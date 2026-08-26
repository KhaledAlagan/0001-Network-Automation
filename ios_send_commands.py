from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from netmiko import ConnectHandler
import copy
import sys
### Custom Import
import ignore_devices as devices

### Functions ###
def send_command(ios_device, ios_command):
    print(f"Connecting to: {ios_device["host"]}")
    with ConnectHandler(**ios_device) as net_connect:
        return [ios_device["host"], net_connect.send_command(ios_command)]

### Main ###
if len(sys.argv) < 2:
    print("No IOS Command provided")
    sys.exit()

save_to_file = False
if len(sys.argv) == 3:
    if sys.argv[2] == "-save":
        save_to_file = True
        print("Saving result to file = True")


ios_command = sys.argv[1]
print(f"Running command: \"{ios_command}\"")
max_threads = 10

# Build device list
device_list = []
for device_name, device_ip in devices.ios_devices.items():
    ios_device = copy.deepcopy(devices.ios_device_template)
    ios_device["host"] = device_ip
    device_list.append(ios_device)

# Start threads
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Map applies the function to every item concurrently
    results = executor.map(send_command, device_list, repeat(ios_command))
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
