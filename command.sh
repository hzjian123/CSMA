#!/bin/bash
SECONDS=0
count=0
## Read all IP from hosts.txt (10 senders + 1 receiver)
while read hosts;do
count=`expr ${count} + 1`
ips[count]=$hosts
done < hosts.txt
count2=0 
## Read n IP from senders for delay purpose
while read hosts2;do
count2=`expr ${count2} + 1`
ips2[count2]=$hosts2
done < hosts2.txt 

## Main program 
main(){
for hosts in ${ips[*]};do
{
echo "Start to read!!!!"
echo $hosts
ssh pi@$hosts << EOF
cd Desktop
#echo "Ready to send"
python3 send.py
EOF
}&
done
wait
echo "END!!!"
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
}

## Replace IP in the list (not in use)
modid(){
    sed -i '' 's/cat/dog/' hosts.txt
}

## Receive file from nodes
obtain(){
scp pi@192.168.88.118:Desktop/send.py recv.py
scp pi@192.168.88.107:Desktop/trans.py trans.py
}

## Send file to nodes
send(){
for hosts in ${ips[*]};do #use ips2
{
echo $hosts
ssh pi@$hosts << EOF
cd Desktop
rm -f send.py
#rm -f confs.txt
exit
EOF
scp confs.txt pi@$hosts:Desktop/
scp send.py pi@$hosts:Desktop/
}&
done
wait
#scp lib_nrf24.py  pi@192.168.88.121:Desktop/
#scp pi@192.168.4.7:/send.py 
}

## Plot throughput vs time 
plot(){
    rm ts.npy
    ## use receiver's IP
    scp pi@192.168.88.118:Desktop/ts.npy ts10to5_3.npy 
    python3 tcp.py
}
auto(){
    cd
    ssh-copy-id -i .ssh/id_rsa.pub pi@192.168.88.118
}
#send
main