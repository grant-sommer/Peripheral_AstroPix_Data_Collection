'''
written to read input from ethernet the input of 2 digital multimeters once per second
must manually change the plot y label to be whatever is read off the multimeter
'''

import socket
import datetime
import time
import argparse
import os
import matplotlib.pyplot as plt

def main(args):
    start_time_full_object=datetime.datetime.now()
    start_time=start_time_full_object.strftime('%Y%m%d-%H%M%S')
    print(args.Plot,type(args.Plot))
    if args.Plot=='False': plot_bool=False 
    else: plot_bool=True
    
    if plot_bool:
        fig,axes=plt.subplots(figsize=(10,6))
        axes.set_title(f'Digital Multimeter Reading for Run Starting at:\n{start_time}')
        axes.set_xlabel('Time After Start (sec)')
        axes.set_ylabel('Voltage (V)') # MANUALLY CHANGE LABEL HERE
        plt.pause(0.1)
        fig.canvas.draw()
        fig.canvas.flush_events()
    # handling output file name
    if os.path.exists(args.outdir) == False:
        os.mkdir(args.outdir)
    fname='DMM_output_Reading_' if not args.name else args.name+'_'
    output_csv_file_name = args.outdir +'/' + fname + start_time + '.csv'
    
    interval_sec=1/args.Frequency # Hz to sec
    # opening socket connection
    with socket.create_connection((args.IP_Address_1,5025),timeout=5) as s_1: # initialzing connection to DMM_1
        with socket.create_connection((args.IP_Address_2,5025),timeout=5) as s_2: # initialzing connection to DMM_1
            s_1.sendall(b'*RST\n')
            s_2.sendall(b'*RST\n')
            
            s_1.sendall(b'CONF:VOLT:DC AUTO\n')
            s_2.sendall(b'CONF:VOLT:DC AUTO\n')
        
            with open(output_csv_file_name,'w') as write_file:
                write_file.write('timestamp,voltage_1,voltage_2\n')

                continue_bool=True
                delta_list=[]
                response_1_list=[]
                response_2_list=[]
                while continue_bool:
                    try:
                        s_1.sendall(b'READ?\n')
                        s_2.sendall(b'READ?\n')

                        response_1=s_1.recv(1024).decode().strip()
                        response_2=s_2.recv(1024).decode().strip()
                        
                        timestamp_full_object=datetime.datetime.now()
                        timestamp=timestamp_full_object.strftime("%Y%m%d-%H%M%S")
                        delta=timestamp_full_object-start_time_full_object
                        write_file.write(f'{timestamp},{response_1},{response_2}\n')
                        print(f'{timestamp}, {response_1} V, {response_2} V')
                        if plot_bool:
                            delta_list.append(delta.seconds)
                            response_1_list.append(float(response_1))
                            response_2_list.append(float(response_2))
                            axes.plot(delta_list,response_1_list,'.-',color='C0')
                            axes.plot(delta_list,response_2_list,'.-',color='C1')
                            fig.canvas.draw()
                            fig.canvas.flush_events()
                        time.sleep(interval_sec)
                    except KeyboardInterrupt: # clean exit with KeyboardInterrupt
                        if plot_bool:
                            print('KeyboardInterrupt, exit plot to stop script')
                            plt.show()
                        else:
                            print('KeyboardInterrupt, stopping script')
                        continue_bool=False



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DMM Reading Code')
    parser.add_argument('-IP_1','--IP_Address_1',type=str,default='169.254.4.10',required=False,
                        help='IP Address of first digital multimeter, default: 169.254.4.10')
    parser.add_argument('-IP_2','--IP_Address_2',type=str,default='169.254.4.61',required=False,
                        help='IP Address of second digital multimeter, default: 169.254.4.61')
    parser.add_argument('-F','--Frequency',type=float,default=1.,required=False,
                        help='Frequency of DMM readout in Hertz, default: 1')
    parser.add_argument('-o', '--outdir', default='.', required=False,
                        help='Output Directory for all datafiles')
    parser.add_argument('-n', '--name', default='', required=False,
                        help='Option to give additional name to output files upon running')
    parser.add_argument('-p','--Plot',type=str,default=True,required=False,
                        help='Boolean argument to live plot the DMM data as it is being recorded, default: True')
    parser.add_argument
    args = parser.parse_args()

    main(args)
