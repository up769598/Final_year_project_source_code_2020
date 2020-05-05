#holds common function that can be used in all of the .py files

import hashlib
from pathlib import Path
import socket
import os

def bitcheck8(binaryArray):
    is8 = True
    for number in binaryArray:
        if len(number) == 8:
            is8 = is8 and True
        else:
            is8 = is8 and False
    return is8

def chunckData(data, n):
    chunckData = [(data[i:i+n]) for i in range(0, len(data), n)]
    return chunckData

def importCSV(fileLocation):
    f = open(fileLocation,"r")
    contents = f.read()
    return contents

def importFile(fileLocation):
    f = open(fileLocation,"r")
    content = f.readlines()
    return content

def writeCSV(fileLocation,dataAray):
    output = open(fileLocation,"w+") 
    for data in dataAray:
        output.write(data + "\n")
        
def totalListLength(inputList):
    totalLength = len(inputList*8)
    return totalLength

def oddOrEvan(number):
    #Odd returns False
    #Evan returns True
    if (number % 2) == 0:
        return True
    else:
        return False   

def HashCalc(fileName):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(fileName, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def ValidFileName(fileName):
    if fileName =="":
        return False
    my_file = Path(fileName)
    return my_file.is_file()


def open_file_bin_array(fileLocation):
    f=open(fileLocation,"rb")
    content = f.read()
    f.close()
    return content

def dec_bit_array_to_pure_bin_srting(decArray):
    pureBin = ""
    for number in decArray:
        binNumber = format(number, "b")
        if len(binNumber) < 8:
            binNumber = ("0" * (8 - len(binNumber))) + binNumber
        pureBin = pureBin + binNumber
    return pureBin
def bin_array_dec_array(byteAray):
    outputArray = []
    for byte in byteAray:
        outputArray.append(int(byte,2))
    return outputArray


def dec_array_to_bin_array(decArray):
    binArray = []
    for num in decArray:
        binNum = "{0:b}".format(num).zfill(8)
        binArray.append(binNum)
    return binArray
          
def binArayToFile(byteArray, outputLocation):
    outputArray = bin_array_dec_array(byteArray)
    binary_format = bytearray(outputArray)
    f=open(outputLocation,"wb")
    f.write(binary_format)
    f.close()
    
def hexArrayToFile(hexArray, outputLocation):
    byteArray = hex_array_to_bin_arry(hexArray)
    binArayToFile (byteArray, outputLocation)
        
def get_Host_Name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP") 
        
        
def encode_into_MAC(inputArray):
    i = 0
    MACArray=[]
    while i < len(inputArray):   
        MAC = ""
        for j in range(8):
            if(i < len(inputArray)):
                MAC = MAC + str(format(inputArray[i], 'x').zfill(2)) + "-"
            i += 1
        # removes the last - from the MAC address
        MAC = MAC[:-1]
        MACArray.append(MAC)
    return MACArray

def decode_MAC(inputArray):
    #Takes an array of MAC addresses,
    decimalOutput=[]
    for MAC in inputArray:
        bytesArray = MAC.split("-")
        for byte in bytesArray:
            decimalOutput.append(int(byte,16))
    return decimalOutput


def decode_MAC_array(MACArray):
    hexArray = []
    for MACAddress in MACArray:
        hexArray += MACAddress.split("-")
    binArray = hex_array_to_bin_arry(hexArray)
    return binArray
    
def bin_array_to_hex_array(binArray):
    output = []
    for item in binArray:
        output.append(format(item, 'x').zfill(2))
    return output

def hex_array_to_bin_arry(hexArray):
    output = []
    for item in hexArray:
        output.append(bin(int(item, 16))[2:].zfill(8))
    return output
    
             
def get_speed_from_user():
    speed = input("Enter the desired stop gap between the loops in seccond \nLeave blank to remove delay: ")
    while not speed.isdigit():
        if not speed:
            speed = 0 
            break
        speed = input("Non integer detected  \nEnter a number of seconds: ")
    if int(speed) < 0:
        print("number less than 0 \n speed set to  0")
        speed = 0 
       
    return int(speed)


def concatinate_files_in_dir(directory, outputfile):
    fileList = os.listdir(directory)
    output = []
    for file in fileList:
        output.append(importCSV(directory + "/" + file))  
    writeCSV(outputfile, output)

     
    
def vaildate_IP_address(IPaddress):
    IP = IPaddress.split('.')
    
    if not len(IP) == 4:
        return False
    
    for digit in IP:
        if not digit.isdigit():
            return False
        
        i = int(digit)
        if i < 0 or i > 255:
            return False
    return True

def dose_file_already_exsist(proposedFileName):
    proposedFile = Path(proposedFileName)
    if proposedFile.is_file():
        fileName = proposedFileName.split(".")[0]
        if len(proposedFileName.split(".")) >=  2:
            #the . needs to be readded as the split removes it
            fileExstension = "." + proposedFileName.split(".")[1]
        else:
            fileExstension =""
        # if the file already exsists with (n) then awtempt to make a file with n+1       
        if fileName[-3:].find("(") == 0 and fileName[-1:].find(")") == 0:
            i = int(fileName[-2])
            #removes the privious number
            fileName = fileName[:-3]
        else:
            i = 0
        i += 1 
        newFileName = fileName + "(" + str(i) + ")" + fileExstension
        newFileName = dose_file_already_exsist(newFileName)
        
        return newFileName
    else:
        return proposedFileName
    