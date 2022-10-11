import board
import digitalio
import analogio
import time
import busio

# Set A0 for receving data from the soil hudmidity module
soil = analogio.AnalogIn(board.A0)

# Set LED for checking the network system  working
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#Waiting time for changing to collecting dry value
delay_counter = 0
while delay_counter < 10:
    delay_counter = delay_counter + 1
    print("Please change to collect dry value..." + str(delay_counter))
    time.sleep(1)

# Collecting the dry value 
dry_counter= 0
dry_number = 0
dry_average = 0
while dry_counter < 100: #collect 100 samples
    dry_counter= dry_counter + 1
    dry_number = soil.value + dry_number
    time.sleep(0.1)
    print ("Dry value counting..." + str(dry_counter))

#Average dry value
dry_average = dry_number / dry_counter
print('Average(dry): '+ str(dry_counter) +' '+ str(dry_average))

#Waiting time for changing to collecting wet value
delay_counter = 0
while delay_counter < 10:
    delay_counter = delay_counter + 1
    print("Please change to collect wet value..." + str(delay_counter))
    time.sleep(1)

# Collecting the wet value
wet_counter= 0
wet_number = 0
wet_average = 0
while wet_counter <100: #collect 100 samples 
    wet_counter = wet_counter + 1
    wet_number  = soil.value + wet_number
    time.sleep(0.1)
    print ("Wet value counting..." + str(wet_counter))

#Average wet value
wet_average = wet_number / wet_counter
print('Average(wet): '+ str(wet_counter) +' '+ str(wet_average))

time.sleep(5) #delay for collecting actual moisture value

#Collect moisture value 
while True: 
    if soil.value < dry_average or soil.value > wet_average:
        print("Error value, please put the sensor to your plant")
    else:
        per_value = (soil.value - dry_average) / ((wet_average - dry_average)/100) #calculate the 
        print("Percentage: " + str(per_value))
        led.value = not led.value
        time.sleep(1)
    
    
