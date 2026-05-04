# plot_temperatures.py - Creates numpy plots from scanner data file.
# Janeth Valverde - valverde@llr.in2p3.fr
# Requires Python v.? or higher.


import matplotlib.pyplot as plt
import numpy as np
import time
import argparse

parser = argparse.ArgumentParser(description='Plotter for temperature scanner')
parser.add_argument('--File_Name', '-n', type=str, required=False, default='scanner_data.txt', help='Name of text document to read data from, defaults to scanner_data.txt')
parser.add_argument('--Thermocouple_Number', '-t', type=int, required=False, default=1, help='Number of thermocouple boxes used, assuming each box can have 12 probes attached')
args = parser.parse_args()


# with open('scanner_data.txt', 'r') as data_file:
with open(args.File_Name, 'r') as data_file:
    t_zero_row = data_file.readline().replace('#', '')
    _, _, *tc_labels = data_file.readline().replace('#', '', 1).split(',')
    first_line_list=data_file.readline().split(',')[2:]
    usecols_list=[1]
    for index,readout in enumerate(first_line_list):
        if "OPEN" not in readout:
            usecols_list.append(index+2)

number_of_thermocouple_boxes=args.Thermocouple_Number
first_data=np.genfromtxt(args.File_Name, usecols=usecols_list,delimiter=',',invalid_raise=False)

colors_12=plt.cm.tab20(np.linspace(0,1,12))

fig,axes = plt.subplots(number_of_thermocouple_boxes,1,figsize=(14, 4*number_of_thermocouple_boxes))
fig.suptitle(t_zero_row, ha= 'left')

#for i in range(1,len(first_data[0])):
for data_index,probe_number in enumerate(np.array(usecols_list[1:])-1):
   if number_of_thermocouple_boxes==1:
      axes.plot(first_data[:,0], first_data[:,data_index+1], '.-', color=colors_12[probe_number-1], label=tc_labels[probe_number-1])
   else:
      thermocouple_box_number=int(np.floor(probe_number/12))
      axes[thermocouple_box_number].plot(first_data[:,0], first_data[:,data_index+1], '.-', color=colors_12[probe_number-(1+thermocouple_box_number*12)], label=tc_labels[probe_number-(1+thermocouple_box_number*12)])
      # if probe_number<=12:
      #    axes[0].plot(first_data[:,0], first_data[:,data_index+1], '.-', color=colors_12[probe_number-1], label=tc_labels[probe_number-1])
      # elif probe_number<=24:
      #    axes[1].plot(first_data[:,0], first_data[:,data_index+1], '.-', color=colors_12[probe_number-13], label=tc_labels[probe_number-1])
      # else:
      #    axes[2].plot(first_data[:,0], first_data[:,data_index+1], '.-', color=colors_12[probe_number-25], label=tc_labels[probe_number-1])

if number_of_thermocouple_boxes==1:
   axes.set_ylabel('Temperature [°C]')
   axes.set_xlabel('Time since START [Minutes]')
   axes.legend(bbox_to_anchor=(1.,1.))
   axes.grid(linestyle=':')

else:
    for i in range(number_of_thermocouple_boxes):
      axes[i].set_ylabel('Temperature [°C]')
      axes[i].set_xlabel('Time since START [Minutes]')
      axes[i].legend(bbox_to_anchor=(1.,1.))
      axes[i].grid(linestyle=':')

plt.pause(0.1)
fig.tight_layout()
fig.canvas.draw()
fig.canvas.flush_events()

    
len_data = len(first_data)
print(f'Print {len_data}.')
continue_bool=True
while continue_bool:
    try:
        time.sleep(3)
        print('Loading new data.')
        data=np.genfromtxt(args.File_Name, usecols=usecols_list,delimiter=',',invalid_raise=False)[(len_data-1):]
        if len(data)>1:
            print(f'Found {len(data)-1} new measurement sets.')
            for data_index,probe_number in enumerate(np.array(usecols_list[1:])-1):
            #for i in range(1,len(first_data[0])):
               if number_of_thermocouple_boxes==1:
                  axes.plot(data[:,0], data[:,data_index+1], '.-', color=colors_12[probe_number-1])

               else:
                  thermocouple_box_number=int(np.floor(probe_number/12))
                  axes[thermocouple_box_number].plot(data[:,0], data[:,data_index+1], '.-', color=colors_12[probe_number-(1+thermocouple_box_number*12)])
                  # if probe_number<=12:
                  #    axes[0].plot(data[:,0], data[:,data_index+1], '.-', color=colors_12[probe_number-1])
                  # elif probe_number<=24:
                  #    axes[1].plot(data[:,0], data[:,data_index+1], '.-', color=colors_12[probe_number-13])
                  # else:
                  #    axes[2].plot(data[:,0], data[:,data_index+1], '.-', color=colors_12[probe_number-25])
            fig.canvas.draw()
            fig.canvas.flush_events()
            len_data = len_data + len(data)-1
    except KeyboardInterrupt:
        continue_bool=False
        print('Keyboard Interrupt, close plot to exit plotting script')

plt.show()
