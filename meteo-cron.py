#!/usr/bin/env python
#cron sript ran cron
#insert below line into /etc/crontab
#replace path wirh your's
#*/5 * * * * alain /home/user/bin/meteo-cron.py

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

try:
    if sensor.get_sensor_data():
        now = datetime.now()
        temperature = sensor.data.temperature
        pression = sensor.data.pressure
        humidite = sensor.data.humidity
        Date = now.strftime("%Y/%m/%d")
        Heure = now.strftime("%H:%M:%S")
        mycursor = mydb.cursor()
        sql = "INSERT INTO valeurs (Date, Heure, Temperature, Pression, Humidite) VALUES (%s, %s, %s, %s, %s)"
        val = (Date, Heure, temperature, pression, humidite)
        mycursor.execute(sql, val)
        mydb.commit()
        #print (sql)
except KeyboardInterrupt:
    pass
