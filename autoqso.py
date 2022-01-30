import time
import socket
from utils import *
from tkinter import *

#########################################################
# TODO list
#
# 1.Non blocking socket receive - Done!
# 2.Scale output to match WSJT waterfall - Done!
# 3.Country indicator
# 4.SNR trend indicator
# 5.Your TX channel is busy indicator
# 6.Station monitor -> SNR reach a certain level and then reply to CQ?
#
#########################################################

#########################################################
# Globals
#########################################################

UDP_IP = "127.0.0.1"
UDP_PORT = 2237
haltRequested = 0
canvas_width = 1100
canvas_height = 200

#########################################################
# Routines
#########################################################


#########################################################
# Initialisation
#########################################################

print("Initialising...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

master = Tk()
master.title("Callsign monitor")
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height,)
w.pack()

#########################################################
# Main loop
#########################################################
sock.setblocking(0) # put socket in non blocking mode

while haltRequested==0: # Currently will only halt after a message has been received as the sock.recvfrom waits forever...
   try: 
      data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
   except:
      data = "" 

   if len(data)>0:
      msgType =  int.from_bytes(data[8:12], "big", signed=True)

      if msgType==2:
          myStr = bytes.decode(data, 'ISO-8859-1')   
          msgTextLen = int.from_bytes(data[48:52], "big", signed=True) # Remember stupid python doesn't include byte 52!
          msgSnr = int.from_bytes(data[27:31], "big", signed=True)
          msgText = myStr[52:52+msgTextLen]
          msgFreq = int.from_bytes(data[39:43], "big", signed=False)
          milliseconds = int.from_bytes(data[23:27], "big", signed=True)

          # Process the message text: extract the callsign
          # Maintain entry in database for callsign with latest frequency
          wordArray = msgText.split()
          if len(wordArray) > 1:
               if wordArray[0]=="CQ":
                   callsign = ""
                   for segment in wordArray: 
                       if len(segment) > 2:     # Skip over any short strings CQ, DX, EU etc. First non-short string is assumed to be the callsign
                           callsign = segment
                           break
               else:
                   callsign = wordArray[1]

               seenCallsign(callsign, milliseconds, msgFreq, msgSnr)
               print(callsign, msgFreq)
               
               drawStatus(w, milliseconds)

   master.update()   
   time.sleep(0.1)  # Lowers CPU usage              

print ("Ended")

####################################
# Data packet format
# Full details available here: https://sourceforge.net/p/wsjt/wsjtx/ci/master/tree/Network/NetworkMessage.hpp
####################################
# 0-3 fixed value 0xadbccbda
# 4-7 schema number
# 8-11 message type
# 23-26 time (milliseconds since midnight)
# 27-30 snr
# 31-38 delta time
# 39-42 delta frequency
# 48-51 message text length
# 52 start of message text
####################################  

# Hue 0 to 40
# Sat 255
# Lum 125