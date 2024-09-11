import os
import time
from itertools import repeat
from netmiko import SSHDetect, ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
from concurrent.futures import ThreadPoolExecutor
from getpass import getpass
from datetime import datetime
import json

date = datetime.now().strftime("%d%m%y-%H%M")

storepath = os.getcwd()

if os.path.isfile('./FW_int_desc_'+ date +'.txt'):
    print('FW_int_desc_'+ date +'.txt exist, please delete and run the script again')
    quit()
else:
    outputfile = open(storepath + '\FW_int_desc_'+ date +'.txt', 'a')

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
    intf_ls = []
    intf_sts = []
    intf_ls_n = []
    intf_sts_n = []
    device = {
                'device_type': 'fortinet',
                'host': IP,
                'username': username,
                'password': password,
                'conn_timeout': 120,
                'banner_timeout': 60,
                'auth_timout': 60,
                'read_timeout': 60,
                'timeout':120,
                'session_log': 'netmiko_session_log_'+IP+'.txt'
                }
    
    net_connect = ConnectHandler(**device)
    hostname=net_connect.send_command_timing('get system status | grep Hostname', delay_factor=4).split()[1]
    print('Connected to device: ' + IP + ' : ' + hostname )
    outputfile.write(IP + ' : ' + hostname+'\n')
    net_connect.send_command_timing('config global', delay_factor=4)
    interface = net_connect.send_command_timing('get system interface physical', delay_factor=4)
    
    for line in interface.splitlines():
        if 'onboard' not in line and '==' in line:
            intf_ls.append(line.split()[0])
        if 'status' in line:
            intf_sts.append(line.split()[1])
    
    intf_ls = [intf.replace('==[', '') for intf in intf_ls]
    intf_ls = [intf.replace(']', '') for intf in intf_ls]
    
    for idx in range(len(intf_sts)):
        if intf_sts[idx] == 'up':
            if 'ha' in intf_ls[idx] or 'mgmt' in intf_ls[idx] or 'port' in intf_ls[idx]:
                intf_ls_n.append(intf_ls[idx])
                intf_sts_n.append(intf_sts[idx])
    
    for idx in range(len(intf_ls_n)):
        interface_conf = net_connect.send_command_timing('show system interface '+ intf_ls_n[idx], delay_factor=4)
        for line in interface_conf.splitlines():
            if 'edit' in line:
                #print(line)
                outputfile.write(line+'\n')
            if 'vdom' in line:
                #print(line)
                outputfile.write(line+'\n')
            if 'description' in line:
                #print(line)
                outputfile.write(line+'\n')
    
    interface_vlan = net_connect.send_command_timing('show system interface | grep -f vlan', delay_factor=4)
    for line in interface_vlan.splitlines():
        if 'edit' in line:
            #print(line)
            outputfile.write(line+'\n')
        if 'vdom' in line:
            #print(line)
            outputfile.write(line+'\n')
        if 'description' in line:
            #print(line)
            outputfile.write(line+'\n')
        if 'set interface' in line:
            #print(line)
            outputfile.write(line+'\n')
            
    outputfile.write('\n++++++++++++++++++++++++++++++++++++++++++\n')

    print ('Completed device :' + IP + ' : ' + hostname )
    
    net_connect.disconnect()

import os
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

if os.path.isfile('./FW_syslog_'+ date +'.txt'):
    print('FW_syslog_'+ date +'.txt exist, please delete and run the script again')
    quit()
else:
    outputfile = open(storepath + '\FW_syslog_'+ date +'.txt', 'a')

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
                'device_type': 'fortinet',
                'host': IP,
                'username': username,
                'password': password,
                'conn_timeout': 120,
                'timeout':120,
                #'session_log': 'netmiko_session_log_'+IP+'.txt'
                }
    
    net_connect = ConnectHandler(**device)
    hostname=net_connect.send_command_timing('get system status | grep Hostname', delay_factor=4).split()[1]
    print('Connected to device: ' + IP + ' : ' + hostname )
    outputfile.write(IP + ' : ' + hostname+'\n')
    net_connect.send_command_timing('config global', delay_factor=4)
    syslog_cmd = net_connect.send_command_timing('show log syslogd setting', delay_factor=4)
    #print (syslog_cmd)
    outputfile.write('\n'+syslog_cmd)
    net_connect.send_command_timing('end', delay_factor=4)
    net_connect.send_command_timing('config vdom', delay_factor=4)
    net_connect.send_command_timing('edit MGMT', delay_factor=4)
    splunk_cmd = net_connect.send_command_timing('show firewall addrgrp SPLUNK_GRP', delay_factor=4)
    #print (splunk_cmd)
    outputfile.write('\n'+splunk_cmd)
    outputfile.write('\n++++++++++++++++++++++++++++++++++++++++++\n')
    
    
    print ('Completed device :' + IP + ' : ' + hostname )
    
    net_connect.disconnect()

import os
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

if os.path.isfile('./FW_vdom_name_'+ date +'.txt'):
    print('FW_vdom_name_'+ date +'.txt exist, please delete and run the script again')
    quit()
else:
    outputfile = open(storepath + '\FW_vdom_name_'+ date +'.txt', 'a')

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
    vd_name = []
    device = {
                'device_type': 'fortinet',
                'host': IP,
                'username': username,
                'password': password,
                'conn_timeout': 120,
                'timeout':120,
                #'session_log': 'netmiko_session_log_'+IP+'.txt'
                }
    
    net_connect = ConnectHandler(**device)
    hostname=net_connect.send_command_timing('get system status | grep Hostname', delay_factor=4).split()[1]
    print('Connected to device: ' + IP + ' : ' + hostname )
    outputfile.write(IP + ' : ' + hostname+'\n')
    net_connect.send_command_timing('config global', delay_factor=4)
    vdom_name = net_connect.send_command_timing('diagnose sys vd list | grep name', delay_factor=4)
    
    for vdom_name in vdom_name.splitlines():
        vd_name.append(vdom_name.split()[0])
    
    vd_name = [name.replace('name=', '') for name in vd_name]
    
    vd_name = [ele for ele in vd_name if 'vsys' not in ele]
    
    vd_name = [name.split('/')[0] for name in vd_name]
    
    #print (*vd_name, sep='\n')
    
    outputfile.write('\n'.join(vd_name))
    outputfile.write('\n++++++++++++++++++++++++++++++++++++++++++\n')
    
    
    print ('Completed device :' + IP + ' : ' + hostname )
    
    net_connect.disconnect()

import os
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

if os.path.isfile('./FW_vdom_name_'+ date +'.txt'):
    print('FW_vdom_name_'+ date +'.txt exist, please delete and run the script again')
    quit()
else:
    outputfile = open(storepath + '\FW_vdom_name_'+ date +'.txt', 'a')

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
    vd_name = []
    device = {
                'device_type': 'fortinet',
                'host': IP,
                'username': username,
                'password': password,
                'conn_timeout': 120,
                'timeout':120,
                #'session_log': 'netmiko_session_log_'+IP+'.txt'
                }
    
    net_connect = ConnectHandler(**device)
    hostname=net_connect.send_command_timing('get system status | grep Hostname', delay_factor=4).split()[1]
    print('Connected to device: ' + IP + ' : ' + hostname )
    outputfile.write(IP + ' : ' + hostname+'\n')
    net_connect.send_command_timing('config global', delay_factor=4)
    vdom_name = net_connect.send_command_timing('diagnose sys vd list | grep name', delay_factor=4)
    
    for vdom_name in vdom_name.splitlines():
        vd_name.append(vdom_name.split()[0])
    
    vd_name = [name.replace('name=', '') for name in vd_name]
    
    vd_name = [ele for ele in vd_name if 'vsys' not in ele]
    
    vd_name = [name.split('/')[0] for name in vd_name]
    
    #print (*vd_name, sep='\n')
    
    outputfile.write('\n'.join(vd_name))
    outputfile.write('\n++++++++++++++++++++++++++++++++++++++++++\n')
    
    
    print ('Completed device :' + IP + ' : ' + hostname )
    
    net_connect.disconnect()
