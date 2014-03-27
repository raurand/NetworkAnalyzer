#!/usr/bin/env python
#
#  First attempt to create a class for the AD9858 dds 
#
#
#  Written:  March 9, 2014
#            R.C. Aurand
#---------------------------------------------------------

import sys
import serial
import math
import os

class ad9858():
    cr=chr(13)
    freq="5002."
    #control=0
    ser=serial.Serial(
        port="/dev/ttyACM1",
        baudrate=9600,
        timeout=1,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        )

    print "frequency = ", freq


#
#  methods needed by AD9858
#   1.  Needs a method to send a string of bits
#   2.  Needs a method to initialize the AD9858
#   3.  Needs a method to convert frequency (in kHz) to a tuning word
#   4.  Needs a method to set the control register
#   5.  Needs a method to reset
#   6.  Needs a method to ioreset
#   7.  Needs a method to FUD
#   8.  Needs a method to send a frequency
#
    def __init__(self):
        

        msg0=[]
        msg0.append("new")
        msg0.append("dim reset as pin pth3 for digital output")
        msg0.append("dim ps0 as pin pth4 for digital output")
        msg0.append("dim ps1 as pin pte4 for digital output")
        msg0.append("dim fud as pin pte5 for digital output")
        msg0.append("dim ioreset as pin pte6 for digital output")
        msg0.append("dim sdo as pin pte7 for digital input")
        msg0.append("dim sdio as pin ptg0 for digital output")
        msg0.append("dim cs0 as pin pta2 for digital output")
        msg0.append("dim cs1 as pin ptg3 for digital output")
        msg0.append("dim clk as pin ptg1 for digital output")
        
        msg1=[]
        msg1.append("let reset = 0")
        msg1.append("let ps0 = 0")
        msg1.append("let ps1 = 0")
        msg1.append("let fud = 0")
        msg1.append("let ioreset = 0")
        msg1.append("let sdio = 0")
        msg1.append("let cs0 = 1")
        msg1.append("let cs1 = 1")
        msg1.append("let clk = 0")

        for msg in msg0:
            print msg
            self.ser.write(msg + self.cr)

        for msg in msg1:
            print msg
            self.ser.write(msg + self.cr)

    def __del__(self):
        self.ser.close()
        print "port closed"

    def f(self, f):
        two=math.pow(2,32)
        fx=100000
        
        w="{0:032b}".format(int((two*float(f))/fx))  # found on stackexchange
        instruction="00000011"
        self.send_bits(instruction)
        self.freq_update()
        self.send_bits(w)
        self.freq_update()

    def send_bits(self, a_byte):
        mask = 1
        msb=1

        if msb:                         # if msb = 1 then load the data msb first.
            d = (int(a_byte[::-1], 2))  # this step reverses the bit order
        else:                           # found somewhere on StackExchange
            d = int(a_byte, 2)
      
        for dx in a_byte:
            self.ser.write("let cs0 = 0" + self.cr)
            
            if (d & mask):
                self.ser.write("let sdio = 1" + self.cr)
            else:
                self.ser.write("let sdio = 0" + self.cr)
            d = d >> 1
            self.ser.write("let clk = 1" + self.cr)
            self.ser.write("let clk = 0" + self.cr)
            self.ser.write("let cs0 = 1" + self.cr)
    
    def freq_update(self):
        self.ser.write("let fud = 1" + self.cr)
        self.ser.write("let fud = 0" + self.cr)

#----------------------------------------------Everything above this line works


    def toggle(ser):
        while 1:
            ser.write("let sdio=!sdio" + cr)

    def reset(ser):
        ser.write("let reset = 1" + cr)  #  Do a chip reset
        ser.write("let reset = 0" + cr)
     
    def ioreset(ser):
        ser.write("let ioreset = 1" + cr)
        ser.write("let ioreset = 0" +cr)
     
    def load_control_register(ser):
        msb=1
        #register0="00000000000000000000000001011010"
        #register0="00000000000000000000000000000000"
        register0="00000000000000000000000001000010"
        #register0="11111111111111111111111111111111"
        instruction="00000000"                # Load the instruction register and
      
        send_byte(instruction, msb, ser)      # point to register 0
        freq_update(ser)
        send_byte(register0, msb, ser)
        freq_update(ser)

    def control_1(ser):
        msb=1
        #register0="00000000000000000000000001011010"
        #register0="00000000000000000000000000000000"
        register0="00000000000000000000000001100010"
        #register0="11111111111111111111111111111111"
        instruction="00000000"                # Load the instruction register and
      
        send_byte(instruction, msb, ser)      # point to register 0
        freq_update(ser)
        send_byte(register0, msb, ser)
        freq_update(ser)

    def load_frequency_register_3(ser):
        msb=1
        #register3="01100000000000000000000000000110"
        register3="01000000000000000000000000000000"
        #register3="00001111111111111111111111110000"

        instruction="00000011"      # Load the instruction register and
        send_byte(instruction, msb, ser)      # point to register 3
        freq_update(ser)
        send_byte(register3, msb, ser)
        freq_update(ser)

    def byte(ser):
        msb=1
        by=raw_input("Enter the byte ")
        instruction="00000011"
        send_byte(instruction, msb, ser)
        freq_update(ser)
        send_byte(by + "000000000000000000000000", msb, ser)
        freq_update(ser)

    def load_register_4(ser):
        msb=1
        register4="0000000000000000"
        instruction="00000100"
        send_byte(instruction, msb, ser)
        freq_update(ser)
        send_byte(register4, msb, ser)
        freq_update(ser)

    def freq(ser):
        msb=1
        two=math.pow(2,32)
        fx=100000
        
        f=raw_input("Enter the frequency in kHz ")
        w="{0:032b}".format(int((two*float(f))/fx))  # found on stackexchange
        print "tuning word = ", w
        print "tuning word = ", int((float(f)*two)/fx)
        instruction="00000011"
        send_byte(instruction, msb, ser)
        freq_update(ser)
        send_byte(w, msb, ser)
        freq_update(ser)

def main():
    #os.system("clear")

    prompt0=[]
    prompt0.append("\n")
#    prompt0.append("open       open the serial port")
#    prompt0.append("close      close the serial port")
#    prompt0.append("init       load the pin names")
    prompt0.append("reset      reset the DDS")
    prompt0.append("ioreset    ioreset the DDS")
    prompt0.append("control    load the control register")
    prompt0.append("control1   turn off the sync clock")
    prompt0.append("f3         load frequency register 3")
    prompt0.append("byte       load a byte into register 3")
    prompt0.append("fud        do a frequency update")
    prompt0.append("toggle     toggle a programmed pin")
    prompt0.append("f          enter a frequency in kHz")
    prompt0.append("options    relist these options")
    prompt0.append("q or quit  quit")

    for msg in prompt0:
        print msg

    dds0=ad9858()
    print "dds0 frequency is ", (dds0.freq)
    print(dds0.freq)

    i="1"
    while i:                #<>"quit" and i<>"q":
        if i=="open":
            ser=open_port()
            print "port open"
        if i=="close":
            close_port(ser)
        if i=="init":
            initialize_variables(ser)
            #ser.write("let cs0 = 0" + cr)
        if i=="reset":
            reset(ser)
        if i=="ioreset":
            ioreset(ser)
        if i=="control":
            load_control_register(ser)
        if i=="control1":
            control_1(ser)
        if i=="f3":
            load_frequency_register_3(ser)
        if i=="fud":
            freq_update(ser)
        if i=="toggle":
            toggle(ser)
        if i=="f":
            f=raw_input("Enter the frequency in kHz ")
            dds0.f(f)
            #freq(ser)
        if i=="options":
            main()
        if i=="byte":
            byte(ser)
        if i=="q":
#            ser.write("let cs0 = 1" + cr)
            del(dds0)
            sys.exit()
        if i=="quit":
           ser.write("let cs0 = 1" + cr)
           sys.exit()
        i=raw_input("select action\n")

if __name__=="__main__":
    main()

    #print int(instruction, 2)    # Use this if the variable instruction is base 2 (binary)
    #print int(instruction, 16)   # Use this if the variable instruction is base 16 (hex)

