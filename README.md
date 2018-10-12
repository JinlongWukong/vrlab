## README
This tool is primary used for parsing VIRL topology file to build its topology using qemu + linux bridge

currently supported devices: xrv9k, csr1000v, asav, n9k, linux

### How TO USE

usage: loadVIRL.py [-h] -f FILE [-m MANAGEMENT] {show,build,remove,qemu}

-f FILE, must specify the topology file exported from VIRL client GUI Maestro


-m MANAGEMENT, specify the management bridge to connect all nodes through mgmt interfaces


positional arguments: 

	show -> show topology	
	build -> build topology
	remove -> remove topolgy
	qemu -> check qemu startup parameter

Please find the attached file "example.txt" for more detailed examples


![alt text](https://github.com/JinlongWukong/vrlab/blob/master/topology.PNG)


Action 1: build topology

    chmod +x loadVIRL.py
 	sudo ./loadVIRL.py -f topology.virl -m mgmt build

Action 2: show topology

    chmod +x loadVIRL.py
 	sudo ./loadVIRL.py -f topology.virl -m mgmt show

Action 3: remove topology

    chmod +x loadVIRL.py
 	sudo ./loadVIRL.py -f topology.virl -m mgmt remove
  

### Notes
	1. Please make sure run this script as root user or sudo
	
	2. This program only verified on python2.7 and don't need any additional module installed 

	3. Please make sure qemu, brctl, kvm are installed on your linux server

	4. Please input the absolute directory of image on target linux server when draw the topology on VIRL VM Maestro

	5. The pre-configuration not support currentlly, have to config manually after login
	
	6. Please make sure remove the current acive topology before build the another one, this tool will not delete image, so these removed topology can be restore any time you want 
