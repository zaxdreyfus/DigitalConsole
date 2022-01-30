from typing import Text
from tkinter import *
import colorsys

callsignList = []

# Keep track of callsigns we have seen
def seenCallsign(callsign, milliseconds, freq, snr):
    global callsignList

    found = 0
    index = 0

    # Ignore unidentified callsign
    if callsign=="<...>":
        return found 

    # Remove angle brackets for inferred callsigns
    if callsign[0:1]=="<":
        callsign = callsign[1:-1]

    for cs, vl, fr, sn in callsignList:
        if cs == callsign:
            found = 1
            break
        index = index+1

    if found == 0:
        callsignList.append((callsign, milliseconds, freq, snr))

    if found == 1:
        cs, vl, fr, sn = callsignList[index]
        callsignList[index] = (cs, milliseconds, freq, snr) # Update with latest time and frequency

    return found

# Refresh screen with recent callsigns seen
def drawStatus(theCanvas, milliseconds):
    canvas_width = theCanvas.winfo_width()
    canvas_height = theCanvas.winfo_height()
    scale = 0.91

    # Clear screen
    theCanvas.delete(ALL)
    theCanvas.create_rectangle(1,1, canvas_width, canvas_height,fill="white", outline="white") 

    # Draw scale
    theCanvas.create_line(0, canvas_height/2, canvas_width, canvas_height/2, fill="#000000")
    for x in range(0, canvas_width, 40):
        if (x%200)==0:
            theCanvas.create_line(x*scale, (canvas_height/2)-10, x*scale, (canvas_height/2)+10, fill="#000000")            
        else:
            theCanvas.create_line(x*scale, (canvas_height/2)-5, x*scale, (canvas_height/2)+5, fill="#000000")

    # Draw scale labels
    for x in range(500, 2501, 500):
        theCanvas.create_text(int((x/2.5)*scale), (canvas_height/2), fill="blue", text=x)

    # Draw activity blocks and corresponding callsigns
    for cs, vl, fr, sn in callsignList:
        x = int(fr*0.4)

        if abs(milliseconds - vl) < 60000: # Callsign recently seen?
            if (vl)%15==0:
                y=(canvas_height/2)+10
            else:
                y=(canvas_height/2)-30

            if sn > 10:
                sn = 10
            if sn < -21:
                sn = -21

            sn = sn + 21
            snrHue = sn/200

            rcol, gcol, bcol = colorsys.hls_to_rgb(snrHue, 0.5, 1)
            hexcol = "#{}{}{}".format(hex(int(rcol*255))[2:].zfill(2), hex(int(gcol*255))[2:].zfill(2), hex(int(bcol*255))[2:].zfill(2))
            
            theCanvas.create_rectangle(x*scale,y, (x+40)*scale,y+20,fill=hexcol, outline=hexcol)

            if (vl)%15==0:
                theCanvas.create_text((x+25)*scale, y+25, anchor="nw", angle=270, text=cs)  
            else:
                theCanvas.create_text((x+20)*scale, y-5, anchor="nw", angle=90, text=cs)  

# Determine time from milliseconds
def timeFromMillis(millis):
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    hours = int(hours)

    thetime = "%02d:%02d:%02d" % (hours, minutes, seconds)
    return thetime

