# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS
import random
import datetime
import time
from send_data_to_influxdb import Influx_Write

url = 'http://localhost:8086'
bucket = 'ASTEP_Testing_2'
org = 'ASTEP'
token='REDACTED'


influx_object=Influx_Write(url=url,org=org,bucket=bucket,api_token=token)
while True:
    for i in range(20):
        now_time=datetime.datetime.now(datetime.UTC)

        random_layer=random.randint(0,2)
        random_chipID=random.randint(0,3)
        random_location=random.randint(0,34)
        random_isCol=random.randint(0,1)
        random_tot=round(100*random.random(),2)

        influx_object.write_unmatched_tot_point(random_layer,random_chipID,random_location,random_isCol,random_tot,timestamp=now_time)

        if (i+1)%10==0:
            random_temp=round(100*random.random(),2)
            random_voltage=round(100*random.random(),2)
            random_current=round(100*random.random(),2)
            random_counts=int(round(100*random.random()))
        
            influx_object.write_housekeeping_point(random_temp, random_voltage, random_current, random_counts, timestamp=now_time)
            print(f'Housekeeping Point {(i+1)/10} is written')
        print(f'ToT Point {i+1} is written')
        time.sleep(round(random.random()/2,2))

    influx_object.send_points_to_influx()
    print('Points sent to Influx')