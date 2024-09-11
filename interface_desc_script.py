import os
import sys
import re
import time
from itertools import repeat
from getpass import getpass
from datetime import datetime
from netmiko import SSHDetect, ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
import logging
#import pdb; pdb.set_trace()
logging.basicConfig(filename='ssh.log', level=logging.DEBUG)


date = datetime.now().strftime("%d%m%y-%H%M")

storepath = os.getcwd()

if os.path.isfile('./Cisco_interface_desc_'+ date +'.txt'):
    print('Cisco_interface_desc_'+ date +'.txt exist, please delete and run the script again')
    quit()
else:
    outputfile = open(storepath + '\Cisco_interface_desc_'+ date +'.txt', 'a')

print('Starting')
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
        print('Connected to device: ' + IP + ' : ' + hostname )
        outputfile.write(IP + ' : ' + hostname+'\n')
        interface_desc_cmd = net_connect.send_command('show inter desc')
        interface_desc_cmd1 = net_connect.send_command('show inter desc | in Gi0/0')
        interface_desc_cmd2 = net_connect.send_command('show inter desc | in Vl1')
        outputfile.write(interface_desc_cmd+'\n')
        outputfile.write('\n----------------------\n')
        outputfile.write(interface_desc_cmd1+'\n')
        outputfile.write('\n----------------------\n')
        outputfile.write(interface_desc_cmd2+'\n')
        outputfile.write('\n++++++++++++++++++++++++++++++++++++++++++\n')
        print ('Completed device :' + IP + ' : ' + hostname )
        net_connect.disconnect()
        
    elif best_match == 'cisco_nxos':
        hostname = net_connect.send_command('show version | in "Device name:"').split()[2]
        print('Connected to device: ' + IP + ' : ' + hostname )
        outputfile.write(IP + ' : ' + hostname+'\n')
        interface_desc_cmd = net_connect.send_command('show inter desc')
        interface_desc_cmd1 = net_connect.send_command('show inter desc | in mgmt0')
        interface_desc_cmd2 = net_connect.send_command('show inter desc | in Vlan1')
        interface_desc_cmd3 = net_connect.send_command('show inter desc | in Lo0')
        outputfile.write(interface_desc_cmd+'\n')
        outputfile.write('\n----------------------\n')
        outputfile.write(interface_desc_cmd1+'\n')
        outputfile.write('\n----------------------\n')
        outputfile.write(interface_desc_cmd2+'\n')
        outputfile.write('\n----------------------\n')
        outputfile.write(interface_desc_cmd3+'\n')
        outputfile.write('\n++++++++++++++++++++++++++++++++++++++++++\n')
        print ('Completed device :' + IP + ' : ' + hostname )
        net_connect.disconnect()
