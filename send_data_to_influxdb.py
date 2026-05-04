'''
script to take int arguments and send them to specified influx database
'''

import influxdb_client
import datetime

class Influx_Write:
    def __init__(self, url:str, org:str, bucket:str, api_token:str, write_precision:str='US'):
        '''
        initialize client and write api with arguments url, org, bucket, and api token
        specifying timing precision is optional with microsecond precision being the default\n
        timing precision options: 
            S: seconds 
            MS: milliseconds 
            US: microseconds 
            NS: nanoseconds
        '''
        self.url = url
        self.org = org
        self.bucket = bucket
        self.api_token = api_token

        if write_precision=='S': # timing precision set to seconds
            self.write_precision=influxdb_client.WritePrecision.S
        elif write_precision=='MS': # timing precision set to milliseconds
            self.write_precision=influxdb_client.WritePrecision.MS
        elif write_precision=='NS': # timing precision set to nanoseconds
            self.write_precision=influxdb_client.WritePrecision.NS
        else: # timing precision set to microseconds, the default
            self.write_precision=influxdb_client.WritePrecision.US
        
        # initialize the client and write API
        self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.api_token, org=self.org)
        self.write_api = self.client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS,write_precision=self.write_precision)

        self.points=[] # holds all points to write, set back to empty after sending to influxdb

    def write_unmatched_tot_point(self, layer:int, chip:int, location:int, isCol:int, ToT:float, timestamp=None) -> None:
        '''
        takes decoded layer, chip, location, isCol, and ToT as input, add these to a influx record object for ToT 
        and appends this record object to the self.points array

        isCol in the form of an int 
        optional timestamp arguement
        '''
        if timestamp is None:
            timestamp=datetime.datetime.now(datetime.UTC)
        point=influxdb_client.Point('ToT_Point').tag('Layer',layer).tag('Chip',chip).tag('Location',location).tag('IsCol',isCol).field('ToT',ToT).time(timestamp)
        self.points.append(point)
    
    def write_matched_tot_point(self, layer:int, chip:int, row:int, col:int, ToT:float, timestamp=None) -> None:
        '''
        takes decoded layer, chip, row, col, and ToT as input, add these to a influx record object for ToT 
        and appends this record object to the self.points array

        optional timestamp arguement
        '''
        if timestamp is None:
            timestamp=datetime.datetime.now(datetime.UTC)
        point=influxdb_client.Point('ToT_Point').tag('Layer',layer).tag('Chip',chip).tag('row',row).tag('col',col).field('ToT',ToT).time(timestamp)
        self.points.append(point)
    
    def write_housekeeping_point(self, temp, current, voltage, counts, timestamp=None) -> None:
        '''
        takes decoded temp, current, voltage, and fpga_counts as input, add these to a influx record object for housekeeping 
        and appends this record object to the self.points array

        optional timestamp arguement
        '''
        if timestamp is None:
            timestamp=datetime.datetime.now(datetime.UTC)
        point=influxdb_client.Point('Housekeeping_Point').field('Temp', temp).field('Current',current).field('Voltage',voltage).field('FPGA Counts',counts).time(timestamp)
        self.points.append(point)
    
    def send_points_to_influx(self):
        '''
        takes no input, sends self.points array object to influx, resets self.points
        '''
        self.write_api.write(bucket=self.bucket, org=self.org, record=self.points)
        self.points=[]