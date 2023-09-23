import machine
import dht
import time

# Temperature reading function (dht11)
# Use the D0 pin of the ESP8266 connected to the data pin of the sensor, then connect the GND of the sensor to the GND of the ESP and the VCC of the sensor to the 3V pin of the ESP.
# Pass the pin number 16 to the function parameter, which corresponds to the GPIO pin for D0 on the ESP8266.
def read_temperature(pin):
    d = dht.DHT11(machine.Pin(pin))
    while True:
        try:
            d.measure()
            temp = d.temperature()
            print("Temperature: {}°C".format(temp))
        except Exception as e:
            print("Error reading temperature: {}".format(e))
        time.sleep(2)

# Humidity reading function (dht11)
# Same pin setup as the temperature reading function.
def read_humidity(pin):
    d = dht.DHT11(machine.Pin(pin))
    while True:
        try:
            d.measure()
            hum = d.humidity()
            print("Humidity: {}%".format(hum))
        except Exception as e:
            print("Error reading humidity: {}".format(e))
        time.sleep(2)

# Motion sensor function
# Use the D2 pin of the ESP8266 connected to the OUT pin of the sensor, then connect the GND of the sensor to the GND of the ESP and the VCC of the sensor to the 3V pin of the ESP.
# Pass the pin number 4 to the function parameter, which corresponds to the GPIO pin for D2 on the ESP8266.
def detect_motion(pin):
    pir = machine.Pin(pin, machine.Pin.IN)
    while True:
        if pir.value():
            print("Motion detected!")
        else:
            print("No motion.")
        time.sleep(1)

# Buzzer function
# Use the D1 pin of the ESP8266, then connect the GND of the buzzer to the GND of the ESP and the VCC of the buzzer to the 3V pin of the ESP.
# Pass the pin number 5 to the function parameter, which corresponds to the GPIO pin for D1 on the ESP8266.
def sound_buzzer(pin, duration, frequency):
    buzzer = machine.PWM(machine.Pin(pin))
    buzzer.freq(frequency)
    buzzer.duty(512)
    time.sleep(duration)
    buzzer.deinit()
