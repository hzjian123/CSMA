# Installation & user guide 
## Introduction
This guide is based on the Python version of [RF24 library](https://github.com/hzjian123/pynrf24) for NRF24L01+ RF module 
## Requirements
### Software
* Same from the link above ( not required for Raspbian )
* Numpy (for data recording)
* Matplotlib (optional)
### Hardware
* Raspberry Pi
* Nrf24l01+
* accessories
## Connection
![connection](connect.png)
![example](example.png)
## Installation
### List of files
* ``send.py`` Main function for senders.
* ``recv.py`` Main function for the receiver.
* ``command.sh`` Include all functions for the master.
* ``ploter.py`` Plotting function for the master.
* ``lib_nrf24.py`` Library function for all nodes.
* ``conf.txt`` Number of each node (0~10)
* ``conf.txt`` Stands for: 

|Meaning|Variables in ``confs.txt``|
| - | - |
|Speed selection|fixspd|
|backoff window lowerbound|windown|
|backoff window upperbound|winup|
|number of packages in the whole *super frame*|datalen|
|time limit for each SSH session|tlim|
|delay of the main function|delay|

### Steps
* Name all Raspberry Pi as *node n[^n] and set node 0 as the receiver, node 1~10 as the senders.
[^n]: 0-10 in our case
* Connect all nodes to the same Access Point (can be one Raspberry Pi) and obtain all IP address.
* Put all IP into ``hosts.txt`` so that the lowest IP stands for the receiver such as the one below.
```
192.168.88.116
192.168.88.117
192.168.88.118
################
```
* Create another file ``hosts2.txt`` and include all IP that you want to have the delay.
* Send ``conf.txt`` to the all to assign node number.
* Send ``send.py`` to all but the receiver (uncomment ``send`` in ``command.sh`` and call by``./command.sh``).
* Send ``recv.py`` to the receiver and change the name to ``send.py``.
* Call ``main`` in ``command.sh``.
* Obtain data from the senders.
  
* Use ``plot`` in ``command.sh`` to obtain thoughtput data from receiver.
  
|File|Meaning|Data length|
| - | - | - |
|cd.npy|Carrier Detection (0 or 1) |time slots|
|acks.npy|Sender receive ack or not|number of packages sent|
|spds.npy|Speed selection|number of packages sent|
|wins.npy,winsact.npy|backoff window selection| number of packages sent|

## Test result
### Initially 5->1,then 10->1
* ``cd,spds,acks,wins,winsact(1~3)`` Data from the senders 
* ``ts10to5_n.npy`` Throughput records
### 1->1
* ``ts.npy``
### 10->1
* ``ts10.npy``
## MATLAB simulation
### Intro
* ``collision.m`` Call ``Bianchi_eqns.m`` to getn ideal data loss 
* ``cd.m`` FFT analysis for carrier detection.
* ``CSMA.m``Main function for simulation. 