## README
This tool is primary used for parsing VIRL topology file to build its topology using qemu + linux bridge

currentlly support devices: xrv9k, csr1000v, asav, n9k, linux

### How TO USE

usage: loadVIRL.py [-h] -f FILE [-m MANAGEMENT] {show,build,remove,qemu}

-f FILE, must specify the topology file exported from VIRL client GUI Maestro


-m MANAGEMENT, specify the management bridge to connect all nodes mgmt interfaces


positional arguments: 

	show -> show topology	
	build -> build topology
	remove -> remove topolgy
	qemu -> check qemu startup parameter

Please find the attached file "example.txt" for details examples

Action 1: build topology


 	sudo ./loadVIRL.py -f topology.virl -m mgmt build

Action 2: show topology


 	sudo ./loadVIRL.py -f topology.virl -m mgmt show

Action 3: remove topology


 	sudo ./loadVIRL.py -f topology.virl -m mgmt remove
  

### Notes
	1. Please make sure run this script as root user or sudo

	2. Please make sure qemu, brctl, kvm are installed and enabled on your linux server

	3. Please input the absolute directory of image on target linux server when draw the topology on VIRL VM Maestro

	4. The pre-configuration not support currenlly, must config manually after login
	
	5. Please make sure remove the current acive topology before build the another one, this tool will not delete image, so these removed topology can be restore any time you want 
