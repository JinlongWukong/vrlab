#/bin/bash

function listKvmPro() {
    filter=$1
    if [ "$1" = "all" -o $# -eq 0 ]; then
        filter="qemu-system"
    fi
    echo -e "Below devices are running...\n"

    ps -e -o pid,cmd | grep qemu-system | grep $filter | egrep -v "grep|\\[kvm-pit" | awk '
BEGIN{
   print "Pid      Name            serial-port              vnc-port\n---------------------------------------------------------------------"
}
{
array[0] = "-"
array[1] = "-"
array[2] = "-"
for(i=1;i<NF;i++) {
   if ($i == "-name" ) {
      j=i+1
      array[0]=$j
   }
   if ($i == "-serial" && array[1] == "-") {
      j=i+1
      array[1]=$j
      gsub(",server,nowait", "",array[1])
      gsub(",nowait,server", "",array[1])
   }
   if ($i == "-vnc" ) {
      j=i+1
      array[2]=$j
   }
}
printf "%-8d %-15s %-25s %-15s\n", $1,array[0],array[1],array[2]
}
END{
   print "---------------------------------------------------------------------"
}
'
}

###listKvmPro iosxr2
###listKvmPro all

function fetMac() {
        if [ $# -ne 1 -o "$1" = "" ]; then
                exit 1
        fi
        echo $1|md5sum|sed 's/^\(..\)\(..\)\(..\)\(..\)\(..\).*$/02:\1:\2:\3:\4:\5/'
}

####ret=`fetMac "cisco"`

####build liunx bridge by given names
function buildLink() {
        if [ $# -ne 2 ]; then
                echo "Error, input paramer not right"
                exit 1
        else
                bridgeName=$1$2
                ifconfig $bridgeName >> /dev/null 2>&1
                if [ $? -eq 1 ]; then
                        sudo brctl addbr $bridgeName
                        sudo ifconfig $bridgeName up
                fi
                sudo /sbin/brctl addif $bridgeName $1
                sudo /sbin/brctl addif $bridgeName $2
                sudo ifconfig $1 up
                sudo ifconfig $2 up
        fi
}

####delete liunx bridge by given names
function delLink() {
        if [ $# -ne 1 ]; then
                echo "Error, input paramer not right"
                exit 1
        else
                bridgeName=$1
                ifconfig $bridgeName >> /dev/null 2>&1
                if [ $? -eq 0 ]; then
                        sudo ifconfig $bridgeName down
                        sudo /sbin/brctl delbr $bridgeName
                else
                        echo "given bridge name not existed"
                fi
        fi
}

function killProcess() {
        if [ $# -eq 1 ]; then
                echo "Will kill pid:$1"
                sudo kill $1
        elif [ $# -eq 2 ]; then
                ps -ef | grep ${2} | grep qemu | grep -v grep > /var/tmp/tempf
                count=`cat /var/tmp/tempf | wc -l`
                if [ $count -ne 1 ];then
                        echo "Multi process or none found, action quit!"
                        exit 1
                else
                        pid=`cat /var/tmp/tempf | awk '{print $2}'`
                        echo "Will kill pid:${pid}"
                        sudo kill $pid
                fi
        else
                echo "error! input param not right"
        fi
}

#### main body ###
if [[ "${BASH_SOURCE[0]}" = "${0}" ]]; then
    if [[ $# -ge 1 ]]; then 
        case $1 in  
            fetmac | mac)
                fetMac $2
            ;;
            listKvmPro | kvm)
                listKvmPro $2
            ;;
            buildLink | build)
                buildLink $2 $3
            ;;
            delLink | delete)
                delLink $2
            ;;
            killProcess | kill)
                killProcess $2 $3
            ;;
            *)
            echo -e "please give right option:
example   1. ./tools_lib.sh mac <tap name>      -> return mac address(md5checksum) based on given tap name
          2. ./tools_lib.sh kvm <filter name>   -> list using kvm started device info include pid, serial port, vnc port, output all if filer not given 
          3. ./tools_lib.sh build tapXX tapXX   -> build a link(linux bridge) betwoon two given tap name
          4. ./tools_lib.sh delete brxx         -> delete linux bridge 
          5. ./tools_lib.sh kill <pid> or <device name>  -> kill given pid process or a running kvm device name" 
            ;;
       esac
    fi
fi
