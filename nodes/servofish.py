import serial

class ServoFish:
    def __init__(self,device='/dev/ttyUSB0',baud=115200):
        try:
            self.ser = serial.Serial(device,baud)  # open serial port)
        except: 
            print "error opening serial port!!"

        self.f = 0
        self.amp = 0
        self.bias = 0
        self.enable=0

    def fishenable(self):
        self.enable = 1
    def fishdisable(self):
        self.enable=0

    def writeCommand(self,f,bias,amp):
        self.f = f#rad/s
        self.bias = -bias#degrees...
        self.amp = amp
        command = '!'+str(int(self.enable))+","+str(int(self.f*10))+','+str(int(self.bias+45))+','+str(int(amp))+','
        self.ser.write(command)
        print command
        #print "wrote: "+str(f)+","+str(bias)+","+str(amp)


def main():
    pass

if __name__ == '__main__':
    main()