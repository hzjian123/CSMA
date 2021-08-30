#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
#import matplotlib.pyplot as plt
import numpy as np
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import random
GPIO.setwarnings(False)
idn,fixspd,windown,winup,datalen,tlim,delay = 1,-1,4,7,20,90,0
with open("conf.txt","r") as f:
    conf = f.read()
    idn = [int(q) for q in conf.split()][0]
with open("confs.txt","r") as f:
    confs= f.read()
    fixspd,windown,winup,datalen,tlim,delay = [int(q) for q in confs.split()]
time.sleep(delay)
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2], [0xc2, 0xc2, 0xc2, 0xc2, 0xc3], [0xc2, 0xc2, 0xc2, 0xc2, 0xc4], [0xc2, 0xc2, 0xc2, 0xc2, 0xc5], [0xc2, 0xc2, 0xc2, 0xc2, 0xc6]]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(1, 17)
radio.setRetries(0,0)      #（可选）增加重试之间的延迟和重试次数 
radio.setPayloadSize(32)
radio.setChannel(0x60)       #0110 0000  频道设置     94约等于100M？

radio.setDataRate(NRF24.BR_250KBPS)         #数据速率
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(False)                    #自动确认集
radio.enableDynamicPayloads()             #启用动态有效载荷we
#radio.enableAckPayload()                  #启用反馈负荷
#radio.closeread()
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.openReadingPipe(0, pipes[0])
c=1
difs = 2
bf = 0
bfs = [2**n-1 for n in range(windown,winup)]
inc = 0
first = 1#1
cs = []
status = ''
count = 0
spd = [0]
success =  0
endflag=0
success1 = 0
success2 = 0
fail1 = 0
fail2  =0
rate = 2
wins = []
winsact = []
cds = []
spds=[]
acks = []
merges = []
if delay:
    countdown = 20
else:
    countdown = 0
radio.startListening()
def cd():
    ics = 0
    radio.startListening()
    while 1:
        ics+=1
        re = radio.available([1])
        if ics>35:
            break
    radio.stopListening()
    return re
def setspd(spd):
    if spd == [1]:
        radio.setDataRate(NRF24.BR_1MBPS)
    elif spd == [2]:
        radio.setDataRate(NRF24.BR_2MBPS)
    else:
        radio.setDataRate(NRF24.BR_250KBPS)
def modspd(spd,inst):
    spd = spd[0]
    if inst == 'up':
        nspd = [spd+1]
    elif inst == 'down':
        nspd = [spd-1]
    #print(nspd)
    if nspd[0]>2 or nspd<[0]:
        nspd=[spd]
    return nspd
def ack():
    tq = time.time()
    radio.startListening()
    pipe = [1]
    ack_acc = 0
    res = False
    ack_buffer = []
    while ack_acc < 75:
        ack_acc += 1
        if radio.available(pipe):
            radio.read(ack_buffer, radio.getDynamicPayloadSize())
            #if len(ack_buffer) == 2
            if ack_buffer[0] == idn and len(ack_buffer)==2:
                res = ack_buffer
                break
   # print(ack_buffer,idn)
    radio.stopListening()
   # print(time.time()-tq)
    return res
qq = 0
old = 0
t5=0
cd_all = 0
cd_act = 0
tstart = time.time()
for q in range(100000):
    if status == 'send':
        pass
        res = 0
    else:
        #tcd = time.time()
        res = cd()
        cd_act += res
        cd_all += 1
        #print("CD t",time.time()-tcd)
    if res == 1:
        status = "occupied"
        #print("occupied")
        pass  
    else:  
        if status == 'occupied':
            status = 'backoff'# state transfer
        if status == 'backoff':
            if bf == 0:
                bf = random.randint(1,bfs[inc])
                wins += [inc]
                winsact += [bf]
                #print("Backoff:",bf)
            bf -= 1
            if bf == 0:
                status = 'send'
        else:
            count += 1
            cds += [round(cd_act/cd_all,3)]
            cd_act, cd_all = 0,0
            t2 = time.time()
            if fixspd>=0:
                spd = [fixspd]
            if countdown:
                countdown -= 1
                merge = 1
            else:
                merge = 0
            radio.write(spd+[idn]+[merge])
            setspd(spd)#spd
            spds += [spd]
            #print(count,"Speed",radio.getDataRate())
            t3 = 0
            time.sleep(0.005)
            num_pack = datalen
            t4a = time.time()
            for q in range(num_pack):  
                buf = [q]+[e for e in range(31)]
                # send a packet to receiver   发送数据包给接收者
                #t1 = time.time()
                ts = time.time()
                radio.write(buf)#round 0.00164s
                #time.sleep(0.001)
                t3 += time.time()-ts
            ##print("Time",t3)#"Sup frame t",time.time()-t2)
            t4 = time.time()
            ackres = ack()
            #t5 = time.time()-t4
            #print("TIME",t4-t2,t5)
            if ackres:#radio.isAckPayloadAvailable()
                success += 1
                acks += [1]
                if ackres[1] == 233 :
                    endflag=1
                #if ackres[1] == 1:
                    #merges += [1]
                #else:
                    #merges += [0]
                merges += [ackres[1]]
                #print ("Received back:",ackres,success,count,round(success/count,3))
                if inc> 0:
                    inc=0
                #print (pl_buffer)
                if success1:
                    spd = modspd(spd,'up')
                    success1 = 0
                else:
                    success1 = 1
            else:
                acks += [0]
                #print ("No!!!!: Ack only, no payload")
                if fail1:
                    spd = modspd(spd,'down')
                    fail = 0
                else:
                    fail1 = 1
                if inc<len(bfs)-1:
                    inc += 1
            status = 'backoff'
            setspd([0])
            if endflag or (time.time()-tstart)>tlim:
                print("End!!!! my id is",idn,"Success rate",\
                round(success/count,3),success,count,\
                "Merge happens at",[i for i,q in enumerate(merges) if q==1] )
                break
if 0:
    plt.figure(1)
    plt.bar([q for q in range(len(wins))],[bfs[w] for w in wins],color='C1',alpha=0.5)
    plt.plot(winsact)
    plt.show()
if 0:
    plt.figure(2)
    plt.plot(cds)
    plt.show()
if 0:
    plt.figure(3)
    plt.plot(spds)
    plt.show()
if 0:
    plt.figure(4)
    plt.plot(acks)
    plt.show()
np.save("cd.npy",cds)
np.save("wins.npy",wins)
np.save("winsact.npy",winsact)
np.save("spds.npy",spds)
np.save("acks.npy",acks)
if merges:
    merges[-1] = 0
np.save("merges.npy",merges)
