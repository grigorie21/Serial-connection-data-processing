import question
import test
try:
    import serial
except:
    pass

import shelve
#import serial.tools.list_ports

'''p = str((test.serial_ports())[0])
a = serial.Serial(p, 9600)'''

class sensorData(object):
#Take the info from the serial

    def __init__(self):
        self.serialNumber = None
        self.ser = None
        self.port = None

    def b(self):
    #just for test    
        return 'rrr'
           

    def serialOpen(self):
        #if not working, see in Device manager the ComPorts
        try:
            self.serialNumber = str((test.serial_ports())[0])
            self.ser = serial.Serial(self.serialNumber, 9600)
        except:
            self.port = False
            pass
        
               
            
    def rawPack(self):
    #Save the raw data in the packet
        
        pack = []
        rawSymb = ''
        while 'b\'a\'' not in pack:
            while 'n' not in rawSymb:
                rawSymb  = str(self.ser.read())
                pack.append(rawSymb)    
        
        return pack

    def serialClose(self):
        try:
            self.ser.close()
        except:
            pass
        
    def data(self):
    #Return sensor data
        Packet = ''
        newPacket = ''
        sensor_1 = ''
        sensor_2 = ''
        sensor_3 = ''
        sensor_4 = ''
        sensor_5 = ''
        
        for i in self.rawPack(): #put the packet in the local list
            Packet += i
            
        #put the packet in the one more local list but without garbage symbols
        for i in Packet: 
            if i not in ("a","n","","b","r", " ", "'"):
                newPacket += i
                
        #read the data of the sensor_1
        for i in newPacket:
            if i!= ',':
                sensor_1 += i
            else:
                break
    
        #read the data of the sensor_2
        start =  len(sensor_1) + 1       

        for i in newPacket[start:]:
            if i!= ',':
                    sensor_2 += i
            else:
                break
            
        #read the data of the sensor_3
        start = len(sensor_1)+len(sensor_2) + 2
        
        for i in newPacket[start:]:
            if i!= ',':
                    sensor_3 += i
            else:
                break

        #read the data of the sensor_4
        start = len(sensor_1) + len(sensor_2) + len(sensor_3) + 3
        
        for i in newPacket[start:]:
            if i!= ',':
                    sensor_4 += i
            else:
                break

        #read the data of the sensor_5
        start = len(sensor_1) + len(sensor_2) + len(sensor_3) + len(sensor_4) + 4
        
        for i in newPacket[start:-2]:
            if i!= ',':
                    sensor_5 += i
            else:
                break
        
        sensorList = [sensor_1, sensor_2, sensor_3, sensor_4, sensor_5]
        return sensorList

    def calibrate(self):
    #Calibrate the data
        sensorList = self.data()
        sensClist = sensorList
        return sensClist

    def printData(self):
        sensClist = self.calibrate()
        sumData = 0

        for i in sensClist:
            sumData += int(i)
        print (sensClist)
        print ('Termo_1: ',sensClist[0], ' Termo_2: ', sensClist[1],' Termo_3: ',sensClist[2],'Pot: ', sensClist[3],' SolarBat: ', sensClist[4], ' Total: ', sumData)

class fileData(sensorData):

    def __init__(self):
        self.fileTxt = 'data.txt'
        self.fileDat = 'data.dat'       
        
        

    def writeData(self, sensorList, objectName):
        #write the data in the file       
      
        txtFile = open(self.fileTxt, 'w')
        txtFile.writelines(sensorList)
        txtFile.close()

        datFile = shelve.open(self.fileDat)
        datFile[objectName] = sensorList
        datFile.sync()
        datFile.close()

    def readData(self, objectName):
        
        datFile = shelve.open(self.fileDat)
        print(datFile[objectName])
        datFile.close()

    def printAll(self):
        datFile = shelve.open(self.fileDat)
        for key, item in datFile.items():
            print(key,': ', item)
        datFile.close()
        print()
        
    def changeData(self, objectName):
        datFile = shelve.open(self.fileDat)
        answer = question.ask_yes_no('Do you want to change object name? y/n: ')
        if answer == 'y':
            newKey = input('Type the new object name')
            datFile[newKey] = datFile.pop(objectName)
            objectName = newKey        
        answer = question.ask_yes_no('Do you want to change sensor data of the object? y/n: ')
        if answer == 'y':
            tData = sensorData()
            datFile[objectName] = tData.calibrate()
        datFile.close()

    def removeData(self, objectName):
        datFile = shelve.open(self.fileDat)
        answer = question.ask_yes_no('Do you really want to delete this object? y/n: ')
        if answer == 'y':
            del datFile[objectName]
        datFile.close()

    
def main():

      
    termoData = sensorData()
    termoData.serialOpen()     
    
        
    fileD = fileData()
    
    choice = None  
    while choice != "0":
        print \
        ("""
        Program "Nirvana" menu:
        0 - Quit
        1 - Show the list of the objects
        2 - Record a new object
        3 - Change name or sensor data of the object
        4 - Remove the object
        5 - Instantaneous sensor's readings
                
        """)
    
        choice = input("Choice: ")
        print()

        # exit
        if choice == "0":
            print("Good-bye.")

        # Show the list of the objects
        elif choice == "1":
            fileD.printAll()
        
        # Record a new object
        elif choice == "2":
            if termoData.port!= False:
                sensorList = termoData.calibrate()
                objectKey = input('What name do you want to give for the object? ')
                fileD.writeData(sensorList,objectKey)
            else:
                print('Serial port is not open!')
                
            
        # Change name or sensor data of the object
        elif choice == "3":
            if termoData.port!= False:
                fileD.printAll()
                objectKey = input('What object do you want to change? ')
                fileD.changeData(objectKey)#!!!Add test on the existing names!!!
            else:
                print('Serial port is not open!')

        #Remove the object 
        elif choice == "4":
            fileD.printAll()
            objectKey = input('What object do you want to remove? ')
            fileD.removeData(objectKey)#!!!Add test on the existing names!!!
       
                
        #Instantaneous sensor's readings
        elif choice == "5":
            if termoData.port!= False:
                termoData.printData()
            else:
                print('Serial port is not open!')
        # some unknown choice
        else:
            print("\nSorry, but", choice, "isn't a valid choice.")

    

    try:
        termoData.serialClose()     
    except:
        pass   
if __name__ == "__main__":


    main()
            

    #    termoData = sensorData()
    '''
    termoData.rawPack()
    termoData.data()
    termoData.writeData()
    print('--------------')
    for i in range(3):
       termoData.printData()
    print('--------------')
    termoData.readData()
    '''
    #termoData.serialClose()




