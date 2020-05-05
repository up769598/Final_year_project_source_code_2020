import os
from scapy.all import *
import Common as Common 
import socket


def send_payload(payload, destination,source):
    originalTTL = 64
    packets= []
    for byte in payload:
        byteshift = byte
        packets.append(IP(src=source, dst=destination, ttl = originalTTL + byteshift))
    send(packets)
    
    
def send_file(fileLocation, destination,fileNameSrc,fileContentSrc):
    fileContent = Common.open_file_bin_array(fileLocation)
    fileName = os.path.basename(fileLocation)
    encodedFileName = fileName.encode("ascii")
    
    send_payload(encodedFileName, destination,fileNameSrc)
    send_payload(fileContent, destination,fileContentSrc)

def split_packets(packets, fileNameSrc, fileContentSrc):
    #packet[1].ttl for time to live
    fileName= []
    fileContent = []
    for packet in packets:
        if packet[1].src == fileContentSrc:
            fileContent.append(packet)
        elif packet[1].src == fileNameSrc:
            fileName.append(packet)
    return fileName , fileContent

    
def listen_for_packets(fileNameSrc,fileContentSrc):
    cont =""
    t = AsyncSniffer(filter="host " + fileNameSrc + " or host " + fileContentSrc)
    t.start()
    print("reciving connections")
    while not cont == "Q": 
        cont = input("Enter Q to stop: ")
    packets = t.stop()
    print("recived: " + str(len(packets)) + " of packets")
    fileNamePackets , fileContentPacket = split_packets(packets, fileNameSrc, fileContentSrc)
    return fileNamePackets , fileContentPacket


def split_packets(packets, fileNameSrc, fileContentSrc):
    fileName= []
    fileContent = []
    for packet in packets:
        if packet[1].src == fileContentSrc:
            fileContent.append(packet)
        elif packet[1].src == fileNameSrc:
            fileName.append(packet)
    return fileName , fileContent

def listen_for_packets(fileNameSrc,fileContentSrc):
    cont =""
    t = AsyncSniffer(filter="host " + fileNameSrc + " or host " + fileContentSrc)
    t.start()
    print("reciving connections")
    while not cont == "Q": 
        cont = input("Enter Q to stop: ")
    packets = t.stop()
    print("recived: " + str(len(packets)) + " of packets")
    fileNamePackets , fileContentPacket = split_packets(packets, fileNameSrc, fileContentSrc)
    return fileNamePackets , fileContentPacket

def retrive_ttl(packets):
    #packet[1].ttl for time to live    
    originalTTL = 64
    payload = []
    for packet in packets:
        data = packet[1].ttl
        data = data - originalTTL 
        payload.append(data)
    return  payload

def decode_file_name(fileNameEncoded):
    fileName = ""
    for char in fileNameEncoded:
        fileName += chr(char)
    return fileName
        
    

def Reciving_part(fileNameSrc, fileContentSrc):
    fileNamePackets , fileContentPacket = listen_for_packets(fileNameSrc, fileContentSrc)
    fileContentDec = retrive_ttl(fileContentPacket)
    fileContentBin = Common.dec_array_to_bin_array(fileContentDec)
    fileNameEncoded = retrive_ttl(fileNamePackets)
    fileName = decode_file_name(fileNameEncoded)
    fileOutputName = Common.dose_file_already_exsist(fileName)
    Common.binArayToFile(fileContentBin,fileOutputName)
    print("The recived File Has been outputed to: " + fileOutputName)
 
def retrive_sending_information_user():
    fileLocation =  input("Enter file location: ")
    while not Common.ValidFileName(fileLocation):
        fileLocation =  input("File name entered is invalid \n Enter file location: ")
    
    destination =  input("Enter destination address: ")
    while not Common.vaildate_IP_address(destination):    
        destination =  input("Enter valid destination address: ")

    fileNameSrc, fileContentSrc = retrive_receiving_information_user()
    
    return fileLocation, destination, fileNameSrc, fileContentSrc



def retrive_receiving_information_user():
    fileNameSrc =  input("Enter file name Source address e.g: 1.1.1.1: ")
    while not Common.vaildate_IP_address(fileNameSrc):
        fileNameSrc =  input("Invaild IP address \n Enter file name Source address: ")
        
    fileContentSrc =  input("Enter file content Source address e.g: 1.1.1.2: ")
    while not Common.vaildate_IP_address(fileContentSrc):
        fileContentSrc =  input("Invaild IP address \n Enter valid Source address e.g: 1.1.1.2: ")
            
    return fileNameSrc, fileContentSrc
    

def main():
    correctChoise = False
    while correctChoise == False:      
        option = input("Select an option \n 1.Send \n 2.Recive \n ")
        if option == "1":
            print("sending")
            correctChoise = True
            fileLocation, destination, fileNameSrc, fileContentsrc = retrive_sending_information_user()
            send_file(fileLocation, destination, fileNameSrc , fileContentsrc)
            
        elif option =="2":
            print("reciving")
            correctChoise = True
            fileNameSrc, fileContentSrc = retrive_receiving_information_user()
            Reciving_part(fileNameSrc, fileContentSrc)
        else:
            print("Please select correct option")

