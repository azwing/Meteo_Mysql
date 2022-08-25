#!/usr/bin/env python

import bme680
import time
from datetime import datetime

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="meteo",
  password="bme680",
  database="meteo"
)

print("""temperature-pressure-humidity.py - Displays temperature, pressure, and humidity.

If you don't need gas readings, then you can read temperature,
pressure and humidity quickly.

Press Ctrl+C to exit

""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

print('Polling:')
try:
    while True:
        if sensor.get_sensor_data():
            now = datetime.now()
            temperature = sensor.data.temperature
            pression = sensor.data.pressure
            humidite = sensor.data.humidity
            Date = now.strftime("%Y/%m/%d")
            Heure = now.strftime("%H:%M:%S")
            
            #print (Date , Heure, temperature, pression, humidite)

            mycursor = mydb.cursor()
            sql = "INSERT INTO valeurs (Date, Heure, Temperature, Pression, Humidite) VALUES (%s, %s, %s, %s, %s)"
            val = (Date, Heure, temperature, pression, humidite)
            mycursor.execute(sql, val)
            mydb.commit()
            time.sleep(300)
except KeyboardInterrupt:
    pass
