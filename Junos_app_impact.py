import os

storepath = os.getcwd() 

filename = storepath + '\\' + 'SRX-junos_defauts_applications.txt'

Junos_default_app_name = []
New_app_name_ls = []
Junos_default_prt = []
Junos_default_dest_port = []

#print (Junos_default_app_name)
#print (Junos_default_dest_port)

with open (filename) as device:
    config = device.read().splitlines()
    for idx,lines in enumerate(config):
        
        if 'applications application ' and ' protocol '  in lines:
            linessplit = lines.split()
            idex = linessplit.index('application')
            Junos_default_app_name.append(linessplit[idex + 1])
            idex2 = linessplit.index('protocol')
            Junos_default_prt.append(linessplit[idex2 + 1])
            
          
        elif 'applications application ' and ' destination-port '  in lines:
            linessplit = lines.split()
            idex3 = linessplit.index('destination-port')
            Junos_default_dest_port.append(linessplit[idex3 + 1])
       
        
        app_name_len = len(Junos_default_app_name)
        dest_port_len = len(Junos_default_dest_port)
        if app_name_len - dest_port_len == 2:
            Junos_default_dest_port.append(' ')
                   
    for idx,obj in enumerate(Junos_default_app_name):
        inc_idx = Junos_default_app_name[idx].find('-')
        app_name_split = Junos_default_app_name[idx].split('-')
        if inc_idx == -1:
            New_app_name_ls.append(app_name_split[0])
        else:
            New_app_name_ls.append(app_name_split[1])
          
print (len(Junos_default_app_name))   
print (len(New_app_name_ls))
print (len(Junos_default_prt))
print (len(Junos_default_dest_port))
print (Junos_default_app_name)
print (New_app_name_ls)
print (Junos_default_prt)
print (Junos_default_dest_port)

import os
import sys
import re
import time
import ipaddress
import openpyxl
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

IP = ('1.1.1.1')

username = input('Username: ')
password = getpass('Password: ')
#IP = input('IP add: ')

mac_table_vlan = []
mac_table_mac = []
mac_table_int = []
mac_table_ip =[]

arp_table_mac = []
arp_table_ip = []

desc_int = []
desc_desc =[]

total_int = []
total_mac = []
total_ip = []
total_vlan = []
total_desc = []

device = {
            'device_type': 'juniper_junos',
            'host': IP,
            'username': username,
            'password': password,
            'conn_timeout': 120,
            'timeout':120,
            }

net_connect = ConnectHandler(**device)
mac_table = net_connect.send_command('show ethernet-switching table')
for idx,line in enumerate(mac_table.splitlines()):
    if 'vlan' and 'ge-' in line:
        linechunk = line.split()
        #print (linechunk)
        mac_table_vlan.append(linechunk[0])
        mac_table_mac.append(linechunk[1])
        mac_table_int.append(linechunk[4])
        #print (vlan[idx] +'    '+ mac[idx] +'    '+int[idx]+'\n')
        
arp_table = net_connect.send_command('show arp')
for idx,line in enumerate(arp_table.splitlines()):
    if ':' in line:
        linechunk = line.split()
        #print (linechunk)
        arp_table_mac.append(linechunk[0])
        arp_table_ip.append(linechunk[1])

intfs_cmd = net_connect.send_command('show interfaces terse | match ge-')
for idx,line in enumerate(intfs_cmd.splitlines()):
    if 'ge-' and '.0' in line:
        linechunk = line.split()
        total_int.append(linechunk[0])
        
desc_cmd = net_connect.send_command('show interfaces descriptions | match ge-')
for idx,line in enumerate(desc_cmd.splitlines()):
    if 'ge-' in line:
        linechunk = line.split()
        if '.' not in linechunk[0]:
            n_int = linechunk[0]+'.0'
            desc_int.append(n_int)
            n_desc = ' '.join(linechunk[3:])
            desc_desc.append(n_desc)
        else: 
            desc_int.append(linechunk[0])
            n_desc = ' '.join(linechunk[3:])
            desc_desc.append(linechunk[3])
       
for idx in range(len(mac_table_mac)):
        #print (mac_table_mac[idx])
        idx2 = (arp_table_mac.index(mac_table_mac[idx]))
        mac_table_ip.append(arp_table_ip[idx2])
        #print (arp_table_ip[idx])

for idx in range(len(total_int)):
        #print (mac_table_mac[idx])
        idx2 = (mac_table_int.index(total_int[idx])) if total_int[idx] in mac_table_int else -1
        idx3 = (desc_int.index(total_int[idx])) if total_int[idx] in desc_int else -1
        if idx2 >= 0:
            total_mac.append(mac_table_mac[idx2])
            total_ip.append(mac_table_ip[idx2])
            total_vlan.append(mac_table_vlan[idx2])
        if idx3 >= 0:
            total_desc.append(desc_desc[idx3])
        else:
            total_mac.append('')
            total_ip.append('')
            total_vlan.append('')
            total_desc.append('')
       
#for idx in range(len(total_int)):
#    print (total_int[idx] +'    '+ total_desc[idx] +'    '+ total_mac[idx] +'    '+ total_ip[idx] +'    '+ total_vlan[idx] +'\n')
    
excel = openpyxl.Workbook()

IP_sheet_ws = excel.create_sheet(title = 'Interfaces', index=0)
IP_sheet_ws = excel.get_sheet_by_name('Interfaces')

IP_sheet_ws.append(['Interface','Description','Mac Address','IP','Vlan'])

for idx,obj in enumerate(total_int):
        IP_sheet_ws.append([total_int[idx], total_desc[idx], total_mac[idx], total_ip[idx], total_vlan[idx]])

excel.save(storepath + '\\' + 'imp_list.xlsx')
