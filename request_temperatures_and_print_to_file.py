#!/usr/bin/env python3

# request_temperature_and_print_to_file.py - Creates temperatures data files from serial response.
# Janeth Valverde - valverde@llr.in2p3.fr
# Requires Python v.? or higher.

import os
import time
import digisense_scanner
from datetime import datetime
import argparse

FILE_NAME = 'scanner_data.txt'
TIME_HEADERS = '#DateTime,dTime[Min]'

######################################
# AUXILIARY FUNCTIONS

def indexed_file_name(original, index):
    filename, extension = original.rsplit(".", 1)
    return f"{filename}_{index}.{extension}"

def archive_data_file(original):
    available_index = 0
    while available_index < 10000:
        available_file_name = indexed_file_name(original, available_index)
        if not os.path.isfile(available_file_name): 
            break
        available_index += 1
    
    if available_index >= 10000:
        raise Exception(f"Too many existing {indexed_file_name(original, '###')} files.")

    os.rename(original, available_file_name)
    print(f'Renamed existing file {original} to {available_file_name}.')

def format_time(datetime_object):
    return datetime_object.strftime('%Y-%m-%d %H:%M:%S.%f')

def format_delta_in_minutes(timedelta_object):
    return round(timedelta_object.total_seconds()/60, 2)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Recording data for temperature scanner.')
    parser.add_argument('--number_of_ports', '-N', default=3, type=int, help="Number of ports being used, an integer. Defaults to 3")
    parser.add_argument('--portname_0', '-p0', default='/dev/ttyUSB0', help="Name of serial port 0. Defaults to: /dev/ttyUSB0")
    parser.add_argument('--portname_1', '-p1', default='/dev/ttyUSB1', help="Name of serial port 1. Defaults to: /dev/ttyUSB1")
    parser.add_argument('--portname_2', '-p2', default='/dev/ttyUSB2', help="Name of serial port 2. Defaults to: /dev/ttyUSB2")
    parser.add_argument('--tc1', default='Heatstrap right', help="Label for thermocouple #1. Defaults to: (TC1) Shroud.")
    parser.add_argument('--tc2', default='Tray lower middle left', help="Label for thermocouple #2. Defaults to: (TC2) Plate front left.")
    parser.add_argument('--tc3', default='Heatstrap left', help="Label for thermocouple #3. Defaults to: (TC3) Plate back right.")
    parser.add_argument('--tc4', default='Tray top left corner', help="Label for thermocouple #4. Defaults to: (TC4).")
    parser.add_argument('--tc5', default='Tray top middle', help="Label for thermocouple #5. Defaults to: (TC5).")
    parser.add_argument('--tc6', default='Tray top right corner', help="Label for thermocouple #6. Defaults to: (TC6).")
    parser.add_argument('--tc7', default='Tray middle right', help="Label for thermocouple #7. Defaults to: (TC7).")
    parser.add_argument('--tc8', default='Tray lower right corner', help="Label for thermocouple #8. Defaults to: (TC8).")
    parser.add_argument('--tc9', default='Tray bottom middle', help="Label for thermocouple #9. Defaults to: (TC9).")
    parser.add_argument('--tc10', default='Tray rib bottom middle', help="Label for thermocouple #10. Defaults to: (TC10).")
    parser.add_argument('--tc11', default='Tray rib middle right', help="Label for thermocouple #11. Defaults to: (TC11).")
    parser.add_argument('--tc12', default='Tray rib upper middle', help="Label for thermocouple #12. Defaults to: (TC12).")


    parser.add_argument('--tc13', default='Tray rib top left', help="Label for thermocouple #13. Defaults to: (TC13).")
    parser.add_argument('--tc14', default='Lane 4 chip 3', help="Label for thermocouple #14. Defaults to: (TC14).")
    parser.add_argument('--tc15', default='Lane 12 chip 3', help="Label for thermocouple #15. Defaults to: (TC15).")
    parser.add_argument('--tc16', default='Lane 17 chip 2', help="Label for thermocouple #16. Defaults to: (TC16).")
    parser.add_argument('--tc17', default='Lane 15 chip 8', help="Label for thermocouple #17. Defaults to: (TC17).")
    parser.add_argument('--tc18', default='Lane 9 chip 11', help="Label for thermocouple #18. Defaults to: (TC18).")
    parser.add_argument('--tc19', default='Lane 1 chip 10', help="Label for thermocouple #19. Defaults to: (TC19).")
    parser.add_argument('--tc20', default='Lane 15 chip 14', help="Label for thermocouple #20. Defaults to: (TC20).")
    parser.add_argument('--tc21', default='Lane 17 chip 17', help="Label for thermocouple #21. Defaults to: (TC21).")
    parser.add_argument('--tc22', default='Lane 11 chip 16', help="Label for thermocouple #22. Defaults to: (TC22).")
    parser.add_argument('--tc23', default='Lane 2 chip 16', help="Label for thermocouple #23. Defaults to: (TC23).")
    parser.add_argument('--tc24', default='Shroud right', help="Label for thermocouple #24. Defaults to: (TC24).")

    parser.add_argument('--tc25', default='Platen back right', help="Label for thermocouple #25. Defaults to: (TC25).")
    parser.add_argument('--tc26', default='Platen back left', help="Label for thermocouple #26. Defaults to: (TC26).")
    parser.add_argument('--tc27', default='Platen front right', help="Label for thermocouple #27. Defaults to: (TC27).")
    parser.add_argument('--tc28', default='Platen front left', help="Label for thermocouple #28. Defaults to: (TC28).")
    parser.add_argument('--tc29', default='Platen right of htr blk', help="Label for thermocouple #29. Defaults to: (TC29).")
    parser.add_argument('--tc30', default='Platen left of htr blk', help="Label for thermocouple #30. Defaults to: (TC30).")
    parser.add_argument('--tc31', default='Heater block right', help="Label for thermocouple #31. Defaults to: (TC31).")
    parser.add_argument('--tc32', default='Heater block mid', help="Label for thermocouple #32. Defaults to: (TC32).")
    parser.add_argument('--tc33', default='Heater block left', help="Label for thermocouple #33. Defaults to: (TC33).")
    parser.add_argument('--tc34', default='Shroud', help="Label for thermocouple #34. Defaults to: (TC34).")
    parser.add_argument('--tc35', default='No connect', help="Label for thermocouple #35. Defaults to: (TC35).")
    parser.add_argument('--tc36', default='No connect', help="Label for thermocouple #36. Defaults to: (TC36).")
    parser.add_argument('--File_Name', '-n', default ='scanner_data.txt', help='Name of text document to output to, defaults to scanner_data.txt') # If file name already exists, renames to scanner_data_[index].txt for an available index
    return parser.parse_args()

# END OF AUXILIARY FUNCTIONS
######################################

if __name__ == '__main__':
    args = parse_arguments()

    FILE_NAME=args.File_Name
    if os.path.isfile(FILE_NAME):
        archive_data_file(FILE_NAME)

    open(FILE_NAME, "w").close()

    loop_counter=0
    start_time = datetime.now()
    with open(FILE_NAME, 'a') as file:
        file.write(f'#START: {format_time(start_time)}\n')
        table_header = TIME_HEADERS
        for i in range(1,args.number_of_ports*12+1):
            tclabel = getattr(args, f'tc{i}')
            if len(tclabel)>0:
                table_header += f',(TC{i}) {tclabel}'
            else:
                table_header += f',(TC{i})'
        file.write(f'{table_header}\n')

    dev0 = digisense_scanner.digisense_scanner(verbosity=4)
    dev0.open(args.portname_0)
    dev0.initialize_instrument_after_power_up() # this is only needed after a power cycle but we do it every time

    if args.number_of_ports>=2:
        dev1 = digisense_scanner.digisense_scanner(verbosity=4)
        dev1.open(args.portname_1)
        dev1.initialize_instrument_after_power_up() # this is only needed after a power cycle but we do it every time

    if args.number_of_ports==3:
        dev2 = digisense_scanner.digisense_scanner(verbosity=4)
        dev2.open(args.portname_2)
        dev2.initialize_instrument_after_power_up() # this is only needed after a power cycle but we do it every time
        print('trying port 2...')
        request_2=dev2.request_all_temperatures()
        print(f'request 2: {request_2}')

    while True:
        print(f"{loop_counter})",end= "\t")
        if args.number_of_ports==1:
                response = dev0.request_all_temperatures()
        elif args.number_of_ports==2:
                response = dev0.request_all_temperatures() + ',' + dev1.request_all_temperatures()
        elif args.number_of_ports==3:
                response = dev0.request_all_temperatures() + ',' + dev1.request_all_temperatures() + ',' + dev2.request_all_temperatures()
        print('Type: ',type(response))
        print(f"response={response}")
        if response != "":
            response_time_finished = datetime.now()
            print(f'Response received at {format_time(response_time_finished)}')
            delta_in_minutes = format_delta_in_minutes(response_time_finished - start_time)
            list_of_measurements_as_strings = response.split(',')
            table_line = ','.join([format_time(response_time_finished), str(delta_in_minutes), *list_of_measurements_as_strings])

            with open(FILE_NAME, 'a') as file:
                print(f'Printing to {FILE_NAME} the line: "{table_line}"')
                file.write(table_line + '\n')


        time.sleep(1)
        loop_counter=loop_counter+1
    # dev.close()
