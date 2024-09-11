import os
import sys
import re
import time
from itertools import repeat
from netmiko import SSHDetect, ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
from concurrent.futures import ThreadPoolExecutor
from getpass import getpass
from datetime import datetime

date = datetime.now().strftime("%d%m%y-%H%M")

storepath = os.getcwd()

if os.path.isfile('./Sw_username-serial_'+ date +'.txt'):
    print('Sw_username-serial_'+ date +'.txt exist, please delete and run the script again')
    quit()
else:
    outputfile = open(storepath + '\Sw_username-serial_'+ date +'.txt', 'a')

username = input('Username: ')
password = input('Password: ')

IP_list = []

ip_num = int(input('Enter number of IP: '))
print ('Enter IP address:')
for i in range (0,ip_num):
    elements = str(input())
    IP_list.append(elements)
    
print (IP_list)

print("Initializing.")

for IP in IP_list:
    
    device = {
            'device_type': 'autodetect',
            'host': IP,
            'username': username,
            'password': password,
            'conn_timeout': 60,
            'timeout':60,
            #'session_log': 'netmiko_session_log_'+IP+'.txt'
            }
            
    guesser = SSHDetect(**device)
    best_match = guesser.autodetect()
            
    device['device_type'] = best_match
    #print (IP+','+best_match)
    try:
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        #outputfileexception.write("Authetication failure, " + IP +'\n')
        print("Authetication failure: " + IP)
    except (NetMikoTimeoutException):
        #outputfileexception.write("Time out from device, " + IP +'\n')
        print("Time out from device: " + IP)
    except (SSHException):
        #outputfileexception.write("Not able to SSH, "+ IP +'\n')
        print("Not able to SSH: "+ IP)
    except Exception as unknown_error:
        #outputfileexception.write("other, " + unknown_error + IP +'\n')
        print("other: " + unknown_error + IP)
    
    if best_match == 'cisco_xe':
        hostname = net_connect.send_command('show version | in uptime').split()[0]
        version_pre = net_connect.send_command('show version | in Software')
        regex_version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)')
        version_p = regex_version.findall(version_pre)
        version = (''.join(version_p))
        inventory = net_connect.send_command('show inventory', use_textfsm=True)
        model_l = [item['pid'] for item in inventory if 'c93xx Stack' in item['name'] or 'Chassis' in item['name']]
        model = (''.join(model_l))
        serial_ls = [item['sn'] for item in inventory if ('Switch' in item['name'] and 'C9300' in item['descr']) or 'Chassis' in item['name']]
        serials = (','.join(serial_ls))
        usernames_ls = []
        username_cmd = net_connect.send_command('show run | i username')
        for line in username_cmd.splitlines():
            usernames_ls.append(line.split()[1])
        outputfile.write('\n' + hostname + ',' + IP + ',' + model + ',' + version + ',' + serials)
        usernames = (','.join(usernames_ls))
        print ('\n' + hostname + ',' + IP + ',' + model + ',' + version + ',' + serials + ',' +  usernames)
        outputfile.write('\n' + hostname + ',' + IP + ',' + model + ',' + version + ',' + serials + ',' +  usernames)
        net_connect.disconnect()
        
    elif best_match == 'cisco_nxos':
    
        hostname = net_connect.send_command('show version | in "Device name:"').split()[2]
        model = net_connect.send_command('show version | in "cisco Nexus"').split()[2]
        version = net_connect.send_command('show version | in "NXOS: version"').split()[2]
        inventory = net_connect.send_command('show inventory', use_textfsm=True)
        serial_ls = [item['sn'] for item in inventory if 'Chassis' in item['name']]
        serials = (','.join(serial_ls))
        usernames_ls = []
        username_cmd = net_connect.send_command('show run | i username.*network-admin')
        for line in username_cmd.splitlines():
            usernames_ls.append(line.split()[1])
        usernames = (','.join(usernames_ls))
        print ('\n' + hostname + ',' + IP + ',' + model + ',' + version + ',' + serials + ',' +  usernames)
        outputfile.write('\n' + hostname + ',' + IP + ',' + model + ',' + version + ',' + serials + ',' +  usernames)
        net_connect.disconnect()
        
