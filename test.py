import onkyo
import time

# This program will execute most of the available commands on an Onkyo or Integra receiver


# Open a connection to the receiver on serial port ttyS1
onkyo = onkyo.Onkyo('/dev/ttyS1')

# Turn on the receiver
onkyo.powerOn()

# wait a few seconds for the unit to turn on
time.sleep(10)

# tune to 540 KHz AM
time.sleep(1)
onkyo.setFreq(540)

# tune to 93.3 MHz FM
time.sleep(1)
onkyo.setFreq(93.3)

# set volume to 10
onkyo.setVolume(10)

# test each screen brightness level
time.sleep(1)
onkyo.setDimmer('off')
time.sleep(1)
onkyo.setDimmer('dim')
time.sleep(1)
onkyo.setDimmer('dark')
time.sleep(1)
onkyo.setDimmer('bright')

# go to the CD input
time.sleep(1)
onkyo.setInput('CD')

# increase the volume by 1
time.sleep(1)
onkyo.volUp()

# decrease the volume by 1
time.sleep(1)
onkyo.volDown()

# Close serial connection 
onkyo.close()