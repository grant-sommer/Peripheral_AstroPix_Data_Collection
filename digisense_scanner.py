# digisense_scanner.py - Manages port connection and serial communication.
# Joe Adams - joseph.s.adams@nasa.gov
# Janeth Valverde - valverde@llr.in2p3.fr
# Requires Python v.? or higher.

import serial
import sys

def convert_binary_string_to_string_and_remove_control_chars(the_binary_string):
        newstring=the_binary_string.decode('ascii')

        newstring = newstring.replace('\r', '')

        return newstring
    
def open_port_with_canonical_settings(portname):
    timeout_s=4
    #imeout_s=None

    ser = serial.Serial(port = portname,
                    baudrate = 19200,
                    bytesize =serial.SEVENBITS,
                    parity=serial.PARITY_ODD,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=timeout_s,
                    xonxoff=False,
                    rtscts=False,
                    dsrdtr=False,
                    write_timeout=None)

    print(f"ser={ser}")
    assert(ser.is_open)

    return ser

class digisense_scanner:
    def __init__(self,portname=None,verbosity=1):
        self.ser=None
        self.portname=portname
        self.verbosity=verbosity


    def open(self,portname=None):
        if portname is not None:
            self.portname=portname

        self.ser=open_port_with_canonical_settings(self.portname)        

    def close(self):
        self.ser.close()
  
        
    def initialize_instrument_after_power_up(self,portname=None):
            # From section 1.4 of the interface manual
            #
            # The control computer would then send the enquire <ENQ>
            # command in response to the active RTS line. Upon
            # receiving the <ENQ> command, all satellites with an
            # active RTS line would disable its receive and transmit
            # buffers to the satellites below it in the daisy
            # chain. Next the scanners would respond with one of the
            # following strings depending on its model number and
            # version.
            
            # <STX>S?0<CR> = Thermocouple Bench Scanner
            # <STX>S?1<CR> = Thermocouple Wall Scanner
            # <STX>S?2<CR> = Platinum RTD Bench Scanner
            # <STX>S?3<CR> = Platinum RTD Wall Scanner
            # <STX>S?4<CR> = Thermistor Bench Scanner
            # <STX>S?5<CR> = Thermistor Wall Scanner
            # The control computer would only see the response from the first satellite in the chain since
            # communications with the others is now blocked. The control computer would then send back
            # <STX>Snn<CR> with nn being a number starting with 01 for the first satellite and incrementing for each
            # satellite up to a maximum of 8
            
        self.send_enq()

        ##this sometimes returns with a
        ## S?0 sometimes not
        ## maybe only the first time after boot?, otherwise no return
        ## so we can read response with timeout or have some extra data

        response=self.read_response()
        if self.verbosity > 4:
           print(f"ENQ response={response}")

        self.set_instrument_address_to_one()
        

    def send_enq(self):
        cmd=b"\05"
        if self.verbosity > 2:
            print(f"Writing ENQ=<{cmd}>")
            sys.stdout.flush()
            
        self.ser.write(cmd)
        
    def set_instrument_address_to_one(self):
        #### send the instrument address
        cmd="S01"
        self.send_command(cmd)

 
 
            
    def request_all_temperatures(self):
        cmd="S01R6"
        self.send_command(cmd)
        
        response=self.read_response()
        return response

    def send_command(self,msg):
        STX=b'\02'
        EOL=b'\r'
        ## we need to convert the unicode python string to ascii
        payload = msg.encode('ascii')  

        cmd=STX+payload+EOL

        if self.verbosity > 2:
            print(f"Writing cmd=<{cmd}>")
            sys.stdout.flush()
            
        self.ser.write(cmd)

    def read_byte(self):

        if self.verbosity > 8:
            print(f"Waiting for read")
            sys.stdout.flush()
        


        s=self.ser.read(size=1)
        
        if self.verbosity >8:
           print(f"Read 1 byte ={s}")
        elif self.verbosity > 4:
            print(f"{s}",end="")
            
        return s

    def read_response(self):

        if self.verbosity > 8:
            print(f"Waiting for read")
            sys.stdout.flush()
        
        x=b""
        
        while True:
            s=self.ser.read(size=1)
            
            if self.verbosity >8:
                print(f"Read {len(s)} bytes ={s}")
            elif self.verbosity > 4:
                print(f"{s}")

            if len(s) == 0:
                #if self.verbosity >4:
                if True:    
                    print(f"Timeout in read response: {x}")
                    sys.stdout.flush()
                break
                
            x=x+s

            if s==b"\r":
                break

        if self.verbosity > 4:
            print(f"x={x}")

        response=convert_binary_string_to_string_and_remove_control_chars(x)    
        return response


  
        

########################################
#
#
#   main
#
#
########################################


if __name__ == '__main__':

    print("________________")

    dev=digisense_scanner()

    dev.open("/dev/ttyUSB0")

    dev.send_command("S01R6")

    s=dev.read_byte()

    dev.close()
