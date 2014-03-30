#!/usr/bin/env python
#
#  working more with the class for the AD958 dds 
#
#
#  Written:  March 30, 2014
#            R.C. Aurand
#---------------------------------------------------------

import sys
import serial
import math
import os


class ad9858():

    def __init__(self):
        self.cr=chr(13)
        self.F0=10000.
        self.F1=1001.
        self.F2=2002.
        self.F3=3003.
        self.fx=150000.
        self.control=0
        self.cfr=90
        self.two=math.pow(2,32)
   
        self.ser=serial.Serial(
            port="/dev/ttyACM0",
            baudrate=9600,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            )
        self.clear_buffer()
        
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
            self.ser.write(msg + self.cr)

        for msg in msg1:
            self.ser.write(msg + self.cr)

    def __del__(self):
        self.ser.close()

    def new_F0(self, f):
        self.F0=f
        self.go_F(3, self.F0)
 
    def new_F1(self, f):
        self.F1=f
        self.go_F(5, self.F1)
            
    def new_F2(self, f):
        self.F2=f
        self.go_F(7, self.F2)

    def new_F3(self, f):
        self.F3=f
        self.go_F(9, self.F3)

    def new_control(self, ctl):
        self.control=ctl
        self.go_control()

    def new_cfr(self, cfr):
        self.cfr=cfr
        self.control=0
        w="{0:032b}".format(int(self.cfr))  # found on stackexchange
        self.go_control()
        self.send_bits(w)
        self.freq_update()

    def go_control(self):
        w="{0:08b}".format(int(self.control))
        self.send_bits(w)
        self.clear_buffer()

    def go_F(self, ctl, F):
        self.control=ctl
        w="{0:032b}".format(int((self.two*float(F))/self.fx))  # found on stackexchange
        self.go_control()
        self.send_bits(w)
        self.freq_update()
        self.clear_buffer()

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
    
    def clear_buffer(self):
        """This method will clear the buffer from the Atria"""
        return self.ser.read(2000)
   
    def freq_update(self):
        self.ser.write("let fud = 1" + self.cr)
        self.ser.write("let fud = 0" + self.cr)

    def toggle(self):
        while 1:
            self.ser.write("let sdio=!sdio" + cr)

    def reset(self):
        self.ser.write("let reset = 1" + cr)  #  Do a chip reset
        self.ser.write("let reset = 0" + cr)
     
    def ioreset(self):
        self.ser.write("let ioreset = 1" + cr)
        self.ser.write("let ioreset = 0" +cr)



def main():
    os.system("clear")

    prompt0=[]
    prompt0.append("\n")
    prompt0.append("print      print the register values")
    prompt0.append("reset      reset the DDS")
    prompt0.append("ioreset    ioreset the DDS")
    prompt0.append("F0         change the F0 register")
    prompt0.append("F1         change the F1 register")
    prompt0.append("F2         change the F2 register")
    prompt0.append("F3         change the F3 register")
    prompt0.append("cfr        change the control function register")
    prompt0.append("options    relist these options")
    prompt0.append("q or quit  quit")

    for msg in prompt0:
        print msg

    dds0=ad9858()
        
    i="1"
    while i:                #<>"quit" and i<>"q":
        if i=="open":
            ser=open_port()
        if i=="close":
            close_port(ser)
        if i=="init":
            initialize_variables(ser)
        if i=="print":
            print "F0 = ", dds0.F0
            print "F1 = ", dds0.F1
            print "F2 = ", dds0.F2
            print "F3 = ", dds0.F3
            print "control = ", dds0.control
            print "cfr = ", dds0.cfr
        if i=="reset":
            dds0.reset()
        if i=="ioreset":
            dds0.ioreset()
        if i=="F0":
            dds0.new_F0(raw_input("Enter the new F0 register value "))
        if i=="F1":
            dds0.new_F1(raw_input("Enter the new F1 register value "))
        if i=="F2":
            dds0.new_F2(raw_input("Enter the new F2 register value "))
        if i=="F3":
            dds0.new_F3(raw_input("Enter the new F3 register value "))
        if i=="cfr":
            dds0.new_cfr(raw_input("Enter the new CFR value "))
        if i=="options":
            main()
        if i=="q":
            del(dds0)
            sys.exit()
        if i=="q":
           del(dds0)
           sys.exit()
        i=raw_input("select action\n")

if __name__=="__main__":
    main()

    #print int(instruction, 2)    # Use this if the variable instruction is base 2 (binary)
    #print int(instruction, 16)   # Use this if the variable instruction is base 16 (hex)

