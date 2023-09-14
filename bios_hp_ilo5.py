import requests
import json
import time

requests.packages.urllib3.disable_warnings()

""" The BIOS setting script is specific for Vz HP Edgeline e920t, e910t, ProLiant DL360 Gen10 (iLO 5).  """


headers = {
    'Content-Type': 'application/json',
}

bmc_ip_address = input("BMC IP ADDRESS:")
bmc_user=input("BMC USER:")
bmc_password=input("BMC PASSWORD:")


workload_def_data = {"Attributes": {"RestoreDefaults": "Yes"}}

reset_data = {'ResetType': 'ForceRestart',}

workload_max_data = {"Attributes": {"WorkloadProfile": "Virtualization-MaxPerformance"}}

workload_custom_data = {"Attributes": {
"WorkloadProfile": "Custom",
"SubNumaClustering": "Disabled",
"MinProcIdlePower": "NoCStates",
"ProcTurbo": "Enabled",
"ProcHyperthreading": "Enabled",
"LlcPrefetch": "Enabled",
"Sriov": "Enabled",
"ProcessorConfigTDPLevel": "Level2"}}

# Step 1: Restore BIOS Defaults

default_bios= requests.patch(
    f'https://{bmc_ip_address}/redfish/v1/systems/1/bios/settings',
    headers=headers,
    json=workload_def_data,
    verify=False,
    auth=(bmc_user, bmc_password),
)


print(default_bios)

if default_bios.ok:
         print ('Step 1 - Restore BIOS Defaults: Success!')
        
else:         
          print ('Step 1 - Restore BIOS Defaults: error!')
          exit()

# Step 2 - Reboot System 
reboot_bmc= requests.post(
     f'https://{bmc_ip_address}/redfish/v1/Systems/1/Actions/ComputerSystem.Reset',
      headers=headers,
      json=reset_data,
      verify=False,
      auth=(bmc_user, bmc_password),)

print(reboot_bmc)

if reboot_bmc.ok:
   print ('Step 2 - Reboot System: Success!')
        
else:         
   print ('Step 2 - Reboot System: error!')
   exit()



print ('Waiting for reboot...')
time.sleep(330) # 5:30 minutes to reboot


# Wait Until Post State Complete OR  Post State Finished Post

check_reboot_status= requests.get(
        f'https://{bmc_ip_address}/redfish/v1/Systems/1/', 
        headers=headers, 
        verify=False, 
        auth=(bmc_user, bmc_password),)


check_reboot_status_json = check_reboot_status.json() 

json_string = json.dumps(check_reboot_status_json)

convert_data= json.loads(json_string)


post_state1 = "InPostDiscoveryComplete" 
post_state2 = "FinishedPost"

if post_state1 or post_state2 in json_string:
    print("Reset 1 - Wait Until Post State Complete OR  Post State Finished Post : Rebooted!")
elif not post_state1 and not post_state2 in json_string :
    print("Reset 1 - Wait Until Post State Complete OR  Post State Finished Post : error!")
    exit()
else:
    print("Reset 1 - Wait Until Post State Complete OR  Post State Finished Post: Rebooted!")




#Step 3: Set workload profile to virtualized max performance:

virtualized_max_performance = requests.patch(
    f'https://{bmc_ip_address}/redfish/v1/systems/1/bios/settings',
    headers=headers,
    json=workload_max_data,
    verify=False,
    auth=(bmc_user, bmc_password),
    )

print(virtualized_max_performance)

if virtualized_max_performance.ok:
         print ('Step 3: Set workload profile to virtualized max performance: Success!')
        
else:         
          print ('Step 3: Set workload profile to virtualized max performance: error!')
          exit()


# Reboot System 
reboot_bmc= requests.post(
     f'https://{bmc_ip_address}/redfish/v1/Systems/1/Actions/ComputerSystem.Reset',
      headers=headers,
      json=reset_data,
      verify=False,
      auth=(bmc_user, bmc_password),)

print(reboot_bmc)

if reboot_bmc.ok:
   print ('Step 4 - Reboot System: Success!')
        
else:         
   print ('Step 4 - Reboot System: error!')
   exit()



print ('Waiting for reboot...')
time.sleep(330)  


# Wait Until Post State Complete OR  Post State Finished Post

check_reboot_status= requests.get(
        f'https://{bmc_ip_address}/redfish/v1/Systems/1/', 
        headers=headers, 
        verify=False, 
        auth=(bmc_user, bmc_password),)


check_reboot_status_json = check_reboot_status.json() 

json_string = json.dumps(check_reboot_status_json)

convert_data= json.loads(json_string)


post_state1 = "InPostDiscoveryComplete" 
post_state2 = "FinishedPost"

if post_state1 or post_state2 in json_string:
    print("Reset 2: Rebooted!")
elif not post_state1 and not post_state2 in json_string :
    print("Reset 2: error!")
    exit()
else:
    print("Reset 2: Rebooted!")


# Check workload profile is now max performance:

check_workload_status= requests.get(
    f'https://{bmc_ip_address}/redfish/v1/Systems/1/BIOS/Settings',
    headers=headers,
    verify=False,
    auth=(bmc_user, bmc_password),
)


check_workload_status_json = check_workload_status.json() 

json_string = json.dumps(check_workload_status_json)

convert_data= json.loads(json_string)


post_state_work = "Virtualization-MaxPerformance"

if post_state_work in json_string:
     print("Step 5 - Check workload profile is now max performance: Workload is now max performance!")

else: 
        print("Step 5 - Check workload profile is now max performance: Error!")
        exit()


#Step 6 - Set workload profile to custom


workload_custom_profile = requests.patch(
    f'https://{bmc_ip_address}/redfish/v1/Systems/1/BIOS/Settings',
    headers=headers,
    json=workload_custom_data,
    verify=False,
    auth=(bmc_user, bmc_password),
)


if workload_custom_profile.ok:
         print ('Step 6 - Set workload profile to custom: Success!')
        
else:         
          print ('Step 6 - Set workload profile to custom: error!')
          exit()



# Reboot System 
reboot_bmc= requests.post(
     f'https://{bmc_ip_address}/redfish/v1/Systems/1/Actions/ComputerSystem.Reset',
      headers=headers,
      json=reset_data,
      verify=False,
      auth=(bmc_user, bmc_password),)

print(reboot_bmc)

if reboot_bmc.ok:
   print ('Step 7 - Reboot System: Success!')
        
else:         
   print ('Step 7 - Reboot System: error!')
   exit()



print ('Waiting for reboot...')
time.sleep(330) 

# Wait Until Post State Complete OR  Post State Finished Post

check_reboot_status= requests.get(
        f'https://{bmc_ip_address}/redfish/v1/Systems/1/', 
        headers=headers, 
        verify=False, 
        auth=(bmc_user, bmc_password),)


check_reboot_status_json = check_reboot_status.json() 

json_string = json.dumps(check_reboot_status_json)

convert_data= json.loads(json_string)


post_state1 = "InPostDiscoveryComplete" 
post_state2 = "FinishedPost"

if post_state1 or post_state2 in json_string:
    print("Reset 3 - Wait Until Post State Complete OR  Post State Finished Post: Rebooted!")
elif not post_state1 and not post_state2 in json_string :
    print("Reset 3 - Wait Until Post State Complete OR  Post State Finished Post: Error!")
    exit()
else:
    print("Reset 3 - Wait Until Post State Complete OR  Post State Finished Post: Rebooted!")



# Check workload profile is now custom:

check_workload_status= requests.get(
    f'https://{bmc_ip_address}/redfish/v1/Systems/1/BIOS/Settings',
    headers=headers,
    verify=False,
    auth=(bmc_user, bmc_password),
)


check_workload_status_json = check_workload_status.json() 

json_string = json.dumps(check_workload_status_json)

convert_data= json.loads(json_string)


post_state3 = "Level2"
post_state4 = "Custom"

if post_state3 or post_state4 in json_string:
    print("Step 8 - Check workload profile is now custom: Workload is now custom and all the steps have been completed!")
elif not post_state3 and not post_state4 in json_string :
    print("Step 8 - Check workload profile is now custom: Error!")
    exit()
else:
    print("Step 8 - Check workload profile is now custom: Workload is now custom and all the steps have been completed!")









