#!/usr/bin/python
fsize = 20
tlim = 360
clim = 4000
import RPi.GPIO as GPIO
import numpy as np
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from lib_nrf24 import NRF24
import time
import spidev
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2], [0xc2, 0xc2, 0xc2, 0xc2, 0xc3], [0xc2, 0xc2, 0xc2, 0xc2, 0xc4], [0xc2, 0xc2, 0xc2, 0xc2, 0xc5], [0xc2, 0xc2, 0xc2, 0xc2, 0xc6]]
radio2 = NRF24(GPIO, spidev.SpiDev())
radio2.begin(1, 17)
radio2.setRetries(0,0)
radio2.setPayloadSize(32)
radio2.setChannel(0x60)
radio2.setDataRate(NRF24.BR_250KBPS)
radio2.setPALevel(NRF24.PA_MIN)
radio2.setAutoAck(False)
radio2.enableDynamicPayloads()
#radio2.enableAckPayload()
radio2.openWritingPipe(pipes[1])
radio2.openReadingPipe(1, pipes[0])
#radio2.printDetails()
cc = 0
radio2.startListening()
ts = []
c=0
fails = 0
success  =0
endsig = 0
mergepos = []
countdown = 0
froms = [0]*12
def w_ack(cont):
    radio2.stopListening()
    time.sleep(0.004)
    radio2.write(cont)
    radio2.startListening()
def modspd(spd):
    if spd == 2:
        radio2.setDataRate(NRF24.BR_2MBPS)
    elif spd == 1:
        radio2.setDataRate(NRF24.BR_1MBPS)
    else:
        radio2.setDataRate(NRF24.BR_250KBPS)
t1 = time.time()
start = 1
while True:
    c += 1
    spdcnt = 0
    while 1:
        if time.time()-t1>tlim:
            endsig=233
        spdcnt += 1
        spd_buffer = []
        if radio2.available([1]):
            radio2.read(spd_buffer, radio2.getDynamicPayloadSize())
            if len(spd_buffer) == 3:
           # print(spd_buffer)
                break
        if spdcnt>1000:
            spdcnt = 0
            if not start:
                fails += 1
                print("fail")
            radio2.stopListening()
            radio2.startListening()
    if endsig == 233:
        break
    spd = spd_buffer[0]
    From = spd_buffer[1]
    if spd_buffer[2]:
        countdown = 5
        print("Merge")
        mergepos += [c]
    else:
        endsig  = 0
    if countdown:
        countdown -= 1
        endsig = 1
    modspd(spd)
    crc = 1
    err = [0 for q in range(fsize)]
    for f in range(fsize):
        scnt = 0
        buf = [f]+[e for e in range(31)]
        rbuf = []
        while scnt<100 and not rbuf:
            scnt += 1
            if radio2.available([1]):
                radio2.read(rbuf, radio2.getDynamicPayloadSize())
            #print(scnt,scnt<150)
        if rbuf != buf:
            crc = 0
            err[f] = 1
            #print(buf[:10],rbuf[:10])
            break
    if time.time()-t1>tlim or c==clim:
        endsig = 233
    if crc:
        froms[From-1] += 1
        w_ack([From,endsig])
        success += 1
        #print("Success")
        ts += [time.time()-t1]
    else:
        pass
        #print("CRC error!",err)
    if c%100==0:
        print("All",c,"success",success,"Accp rate",success/c,froms,"throu",round(success/(time.time()-t1),3))
        pass
    modspd(0)
    if endsig == 233:
        print("All",c,"success",success,"Accp rate",success/c,froms,"fails",fails,"throu",\
        round(success/(time.time()-t1),3),"Merge pos",mergepos)
        radio2.stopListening()
        for r in range(50):
            radio2.write([From,endsig])
            time.sleep(0.1)
        break
    #time.sleep(0.5)
np.save("ts.npy",ts)
