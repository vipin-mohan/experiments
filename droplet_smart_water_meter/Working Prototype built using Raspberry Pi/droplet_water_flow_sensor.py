import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#Name input and output pins
TRIG = 23
ECHO = 24

print "+++++++++++++++++++++++++++++++++++++++"
print "Water Flow Rate Measurement In Progress"
print "+++++++++++++++++++++++++++++++++++++++"

#Set input and output pins
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

var = 10
while var > 0 :
  # Allow 2 seconds for the TRIG pin to settle
  GPIO.output(TRIG, False)
  #print "Waiting For Sensor To Settle"
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

  #To calculate rate of water flow in cubic ft/ second, flow rate = volume of water/pulse_duration
  #diameter of pipe = 0.75 inch
  #Calculate volume in cubic feet
  volume_of_water = 3.14*0.375*0.375*1/(12*12)
  flow_rate = volume_of_water/pulse_duration

  #Convert cubic feet to gallons (1 cubic foot = 7.48 gallons)
  flow_rate = flow_rate * 7.48
  flow_rate = round(flow_rate, 2)
  print "[Droplet Smart Water Meter] Rate of water flow:",flow_rate,"gallons per minute"

GPIO.cleanup()
