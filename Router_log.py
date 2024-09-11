import os
from re import search
from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
import pandas as pd
import concurrent.futures

username = input('username: ')
password = getpass('password: ')

print("Initializing.")

file_name = r"IPsheet.xlsx"
df = pd.read_excel(file_name,sheet_name='DeviceList',dtype=str, skiprows=0)
df = df.dropna(subset = ['IPlist'])
IPlist = df['IPlist'].to_list()
df = df.dropna(subset = ['Model'])
Modellist = df['Model'].to_list()

print('.')

def commands(IP,Model):  
  
    file_name = r"IPsheet.xlsx"
    df = pd.read_excel(file_name,sheet_name=Model,dtype=str, skiprows=0)
    df = df.dropna(subset = ['Commands'])
    prechecks = df['Commands'].to_list()
    
    print('.')
    
    if Model != 'Nexus 9K':
        device = {
                    'device_type': 'cisco_ios',
                    'host': IP,
                    'username': username,
                    'password': password,
                    'conn_timeout': 60,
                    'timeout':60,
                    #'session_log': IP + '_session.log',
                    }
    
    net_connect = ConnectHandler(**device)
    print('Connecting to device: '  )
    hostname = net_connect.send_command('show run | i host',  read_timeout=90).split()[1]
    #print(hostname)
    print('Connecting to device: ' + IP + ' : ' + hostname )
    date = datetime.now().strftime("%d%m%y-%H%M")
    
    storepath = os.getcwd()
    if os.path.exists(hostname + '_' + date + '_' + '.txt'):
    	print( hostname + '_' + date + '_' + '.txt exist, please delete file')
    	quit()
    else:
        outputfile = open(storepath +'\\' + hostname + '_' + date + '_' + '.txt' ,'a')
    
    print('Starting: ' + IP + ' : ' + hostname )
    for command in prechecks:
       
        output=net_connect.send_command(command, read_timeout=90)
        #print (command +'\n')
        #print (output +'\n')
        outputfile.write(command +'\n\n')
        outputfile.write(output +'\n')
        outputfile.flush()
        #print ("++++++++++++++++++++++++++++++++++++\n")
        outputfile.write("++++++++++++++++++++++++++++++++++++\n")
        outputfile.flush()
    
    route_map_cmd = 'show route-map'
    route_map_net_cmd = net_connect.send_command(route_map_cmd, read_timeout=90)
    #print (route_map_cmd +'\n')
    #print (route_map_net_cmd +'\n')
    outputfile.write(route_map_cmd +'\n\n')
    outputfile.write(route_map_net_cmd +'\n')
    outputfile.flush()
    #print ("++++++++++++++++++++++++++++++++++++\n")
    outputfile.write("++++++++++++++++++++++++++++++++++++\n")
    outputfile.flush()
    
    if route_map_net_cmd != '':
    
        route_map_net_cmd_name = net_connect.send_command('show route-map', read_timeout=90, use_textfsm=True)
        
        for mapname in route_map_net_cmd_name:
            
            routemap_name_command = 'show route-map ' + mapname['name']
            routemap_name = net_connect.send_command(routemap_name_command, read_timeout=90)
            #print (routemap_name_command +'\n')
            outputfile.write(routemap_name_command +'\n\n')
            outputfile.flush()
            #print (routemap_name)
            outputfile.write(routemap_name)
            #print ("++++++++++++++++++++++++++++++++++++\n")
            outputfile.write("++++++++++++++++++++++++++++++++++++\n")
            outputfile.flush()


    ip_bgp_cmd = 'show ip bgp'
    ip_bgp_net_cmd = net_connect.send_command(ip_bgp_cmd, read_timeout=90)
    #print (ip_bgp_cmd +'\n')
    #print (ip_bgp_net_cmd +'\n')
    outputfile.write(ip_bgp_cmd +'\n\n')
    outputfile.write(ip_bgp_net_cmd +'\n')
    #print ("++++++++++++++++++++++++++++++++++++\n")
    outputfile.write("++++++++++++++++++++++++++++++++++++\n")
    outputfile.flush()
    
    if search(ip_bgp_cmd, '% BGP not active') is False:
        
        bgp_summary_cmd = ('show ip bgp all summary')
        bgp_summary = net_connect.send_command(bgp_summary_cmd, read_timeout=90)
        outputfile.write(bgp_summary_cmd +'\n\n')
        outputfile.write(bgp_summary +'\n\n')          
        outputfile.flush()
        #print ("++++++++++++++++++++++++++++++++++++\n")
        outputfile.write("++++++++++++++++++++++++++++++++++++\n")
        outputfile.flush()
        
        
        bgp_summary_ip = net_connect.send_command('show ip bgp all summary', read_timeout=90, use_textfsm=True)
           
        for neigh in bgp_summary_ip:
            
            bgp_add_neigh_command = 'show ip bgp neighbor ' + neigh['bgp_neigh'] + ' advertised-routes'
            bgp_rec_neigh_command = 'show ip bgp neighbor ' + neigh['bgp_neigh'] + ' received-routes'
            bgp_add_neigh = net_connect.send_command(bgp_add_neigh_command, read_timeout=90)
            bgp_rec_neigh = net_connect.send_command(bgp_rec_neigh_command, read_timeout=90)

            #print (bgp_add_neigh_command +'\n')
            outputfile.write(bgp_add_neigh_command +'\n\n')          
            #print (bgp_add_neigh +'\n')
            outputfile.write(bgp_add_neigh +'\n')
            outputfile.flush()
            #print ("++++++++++++++++++++++++++++++++++++\n")
            outputfile.write("++++++++++++++++++++++++++++++++++++\n")
            outputfile.flush()
            
            #print (bgp_rec_neigh_command +'\n')
            outputfile.write(bgp_rec_neigh_command +'\n\n')
            #print (bgp_rec_neigh +'\n')
            outputfile.write(bgp_rec_neigh +'\n')
            #print ("++++++++++++++++++++++++++++++++++++\n")
            outputfile.write("++++++++++++++++++++++++++++++++++++\n")
            outputfile.flush()
    
    vrf_cmd = 'show vrf'
    vrf_net_cmd = net_connect.send_command(vrf_cmd, read_timeout=90)
    #print (vrf_cmd + '\n')
    outputfile.write(vrf_cmd + '\n\n')
    #print (vrf_net_cmd +'\n')
    outputfile.write(vrf_net_cmd +'\n')
    #print ("++++++++++++++++++++++++++++++++++++\n")
    outputfile.write("++++++++++++++++++++++++++++++++++++\n")
    outputfile.flush()
    
    vrf_net_cmd_name = net_connect.send_command('show vrf', read_timeout=90, use_textfsm=True)
   
    for vrf_name in vrf_net_cmd_name:
        ip_route_vrf_cmd = 'show ip route vrf ' + vrf_name['name']
        outputfile.write(ip_route_vrf_cmd + '\n\n')
        #print (ip_route_vrf_cmd +'\n')
        ip_route_vrf_net_cmd = net_connect.send_command(ip_route_vrf_cmd, read_timeout=90)
        #print (ip_route_vrf_net_cmd +'\n')
        #print ("++++++++++++++++++++++++++++++++++++\n")
        outputfile.write(ip_route_vrf_net_cmd + '\n')
        outputfile.write("++++++++++++++++++++++++++++++++++++\n")
        outputfile.flush()    
    
    print('Completed for device: ' + hostname) 
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    for idx,ip in enumerate(IPlist):
        executor.map(commands, ip.splitlines(), Modellist[idx].splitlines())
