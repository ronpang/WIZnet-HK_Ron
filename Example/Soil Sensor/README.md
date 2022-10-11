# Soil Moisture Sensor coding method

The soil moisture sensor is directly feeding signal to the ADC pin 0 (A0 - pin 31) of the Raspberry PI PICO ([Connection Diagram][link - TCP readme])

Accoding to circuit python coding, the receving values for analogio is 0 - 65535 range.

The basic theory of the soil moisture sensor is: more water = more conductive = more voltage  = larger digital value 

However, it is required to determine the dry value (the value taking in air) and wet value (the value taking in water) for finding the actual range of the sensor

My Coding method: (The coding method is my way of coding, it doesn't mean it is the best method for setting range to the Soil Mositure Sensor)

1. Collect 100 samples for dry value 
2. Take the average of dry value
3. Time to change to collect wet value
4. Collect 100 samples for wet value
5. Take the average of wet value
6. Reduce the average dry value for the starting point of calulation
7. Coverting to percentage values (%) by dividing the range of dry and wet value 

[link - TCP readme]: https://github.com/ronpang/WIZnet-HK_Ron/tree/main/TCP#readme
