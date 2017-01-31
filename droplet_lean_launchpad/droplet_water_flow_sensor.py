import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#Name input and output pins
TRIG = 23
ECHO = 24

print "Distance Measurement In Progress"

#Set input and output pins
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# Allow 2 seconds for the TRIG pin to settle
GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

#Set TRIG pin to high for 10us and then set it to low
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

#Capture the timestamp of the pulse in 0 state and 1 state
while GPIO.input(ECHO)==0:
  pulse_start = time.time()

while GPIO.input(ECHO)==1:
  pulse_end = time.time()

pulse_duration = pulse_end - pulse_start

#To calculate rate of water flow in cubic ft/ second, speed = volume of water/pulse_duration
#distance between the two sensors = 3 inches
#diameter of pipe = 1 inch
#Calculate volume in cubic feet
volume_of_water = 3.14*0.5*0.5*3/(12*12*12)
speed = volume_of_water/pulse_duration

speed = round(speed, 2)
print "Rate of water flow:",speed,"cm"
GPIO.cleanup()