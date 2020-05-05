import socket
import datetime
import random
import Common as Common
import time
import statistics 
from progressbar import ProgressBar
import os
Delay = 0 

def listen_Loop(clientIP):
    timeStamps = []
    listen = True
    fileNameSeen = False
    while listen:
        TCP_PORT = 5005
        BUFFER_SIZE = 1024 
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((clientIP, TCP_PORT))
        s.listen(1)
        
        conn, addr = s.accept()
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            timeStamps.append(datetime.datetime.now().timestamp())
            if data.decode() == "halt":
                listen = False
                #removes the last time stamp added from the halut packet 
                timeStamps = timeStamps[:-1]
            if not fileNameSeen:
                fileName = data.decode()
                fileNameSeen = True
                print("File recived with name: " + fileName)
        conn.close()
    return timeStamps, fileName

def send_Packet(message, destination):  
    TCP_IP = destination
    TCP_PORT = 5005
    MESSAGE = str(message).encode()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    s.close()    
    
    
def data_to_packets(BinString,destination,FileName):
    pbar = ProgressBar()
    send_Packet(FileName,destination)
    for bit in pbar(BinString):
        if Common.oddOrEvan(int(bit)):
            time.sleep(Delay + 1 + random.randint(1,Delay))
         # without this ocational error when 2 connectonse where attempted at once
        time.sleep(0.001 * random.randint(1,Delay))
        send_Packet("heartbeat",destination)
    #neede to enser the halt packet is seen.
    time.sleep(0.1)
    send_Packet("halt",destination)
   
   
def timestamp_Array_to_data(timeStampArray):
    timeDiff = []
    arrayIndex = 0
    timeStampLength = len(timeStampArray) -1
    for timeStamp in timeStampArray:
        if arrayIndex < timeStampLength:
            nextTime = timeStampArray[arrayIndex + 1]
            timeDiff.append(nextTime - timeStamp)
        arrayIndex += 1 
    return timeDiff

def time_diff_to_bin_string(timeDiffArray):
    bitString = ""
    exspectedTimeDiff = calculate_exspectedTimeDiff(timeDiffArray)
    for timeDiff in timeDiffArray:
        if timeDiff < exspectedTimeDiff:
            bitString += "1"
        else:
            bitString += "0"
    return bitString
            

def calculate_exspectedTimeDiff(timeDiffArray):
    usersTimedelay = input("Enter the time delay used for sending: \n")
    while not usersTimedelay.isdigit():
        usersTimedelay = input("Non-digit inputed \n Enter the time delay used for sending: \n")
        
    
    exspectedTimeDiff = int(usersTimedelay) + 1
    
    return exspectedTimeDiff


def bit_string_byte_array(bitString):
    i = 0
    byteArray = []
    while i < len(bitString)/8:
        j = 0
        byteTemp = ""
        while j< 8:
            byteTemp += bitString[i+j]
            j += 1
        byteArray.append(byteTemp)
        i += 1
    
    return byteArray
 
def retreive_users_inputs_listen():
    clientIP = input("Enter the Client IP: ")
    while not Common.vaildate_IP_address(clientIP):
        clientIP = input("Invalid IP address \n Enter the Client IP: ")
    return   clientIP 

def retreive_users_inputs_send():
    global Delay
    destination = input("Enter the Destination IP: ")
    while not Common.vaildate_IP_address(destination):
        destination = input("Not valid IP address \nEnter the Destination IP: ")
        
    fileLocation =  input("Enter file location: ")    
    while not Common.ValidFileName(fileLocation):
        fileLocation =  input("File name entered is invalid \n Enter file location: ")    
    Delay = Common.get_speed_from_user()
    
    return fileLocation, destination
    

def main():
    Common.get_Host_Name_IP()
    mode = input("Chose Mode: \n 1: listen: \n 2: Send: \n")
    if mode == "1":
        clientIP = retreive_users_inputs_listen()
        timeStamps , fileName = listen_Loop(clientIP)
        timeDiff = timestamp_Array_to_data(timeStamps)
        output = time_diff_to_bin_string(timeDiff)
        output = Common.chunckData(output, 8)
        outputFileName = Common.dose_file_already_exsist(fileName)
        Common.binArayToFile(output, outputFileName)
        print("File outputted to: " + outputFileName)
    elif mode =="2":
        fileLocation, destination = retreive_users_inputs_send()
        fileName = os.path.basename(fileLocation)
        data = Common.open_file_bin_array(fileLocation)
        data = Common.dec_bit_array_to_pure_bin_srting(data)
        data_to_packets(data,destination,fileName)
        print("data sending compleate")
    else:
        mode = input("No mode selected \nChose mode: \n 1: listen: \n 2: Send: \n")
        


