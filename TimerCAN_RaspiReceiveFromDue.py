#!/usr/bin/python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import os
import can
import queue
from threading import Thread

count = 0
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
#msg = can.Message(arbitration_id=0x7de,data=[0, 25, 0, 1, 3, 1, 4, 1])
#bus.send(msg)
#notifier = can.Notifier(bus, [can.Printer()])

triggerInputPin = 4
plus = 0

def can_rx_task():
    while True:
        message = bus.recv()
        q.put(message)            # Put message into queue

q = queue.Queue()
t = Thread(target = can_rx_task)    # Start receive thread
t.start()

def callbackFromDue10ms(triggerInputPin):
    global plus
    global count

#    message = bus.recv()    # Wait until a message is received.
#    if message.arbitration_id == 0x401:
#        c = '{0:f} {1:x} {2:x} '.format(message.timestamp, message.arbitration_id, message.dlc)
#        s=''
#        for i in range(message.dlc ):
#            s +=  '{0:x} '.format(message.data[i])
#        print(plus, ' {}'.format(c+s))

# spread q.message to search the number that I want!!!!!!!!!!!!!
    if q.empty() != True:    # Check if there is a message in queue
        message = q.get()
        c = '{0:f} {1:d} {2:x} {3:x} '.format(message.timestamp,count, message.arbitration_id, message.dlc)
        s=''
        for i in range(message.dlc ):
            s +=  '{0:x} '.format(message.data[i])
        outstr = c+s
        print('\r {} qsize:{}       '.format(outstr,q.qsize()),end ='') # Print data and queue size on screen
        count += 1


    #-------receive--------

    plus += 1
    #print(plus)

GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerInputPin, GPIO.IN)
GPIO.add_event_detect(triggerInputPin, GPIO.BOTH)
GPIO.add_event_callback(triggerInputPin, callbackFromDue10ms)

try:
    plus = 0
    while True:
        time.sleep(10)

finally:
    GPIO.cleanup()
    os.system("sudo /sbin/ip link set can0 down")
