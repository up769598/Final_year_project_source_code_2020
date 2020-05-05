import os
from scapy.all import *
import Common as Common 
from progressbar import ProgressBar
Delay = 0

def send_payload(payload, destination,source):
    global Delay
    # must stay below ff = 254
    packetSize= 10
    packets= []
    i = 0
    while i < len(payload)/packetSize:
        msg = ""
        for cylce in range(packetSize):
            try:
                index = ((i*packetSize) + cylce)
                msg += payload[index]
            except IndexError:
                break
                
        # second octect is length of the message string + 2 i.e \x10 can take a message of length 14 the 2 ochtets are the \x00
        packets.append(IP(src=source, dst=destination, options=IPOption("\x1e\xff" + msg)))
        i += 1
    
   
    print("Sending Packets: ")
    pbar = ProgressBar()
    for Packet in pbar(packets):
        delayDuration = random.random() * Delay
        time.sleep(delayDuration)        
        send(Packet, verbose=0) 
        
    

def send_file(fileLocation, destination,fileNameSrc,fileContentSrc):
    fileContent = Common.open_file_bin_array(fileLocation)
    payload = Common.bin_array_to_hex_array(fileContent)
    fileName = os.path.basename(fileLocation)
    encodedFileName = Common.bin_array_to_hex_array(fileName.encode("ascii"))
    
    send_payload(encodedFileName, destination,fileNameSrc)
    send_payload(payload, destination,fileContentSrc)
    
def retrive_payload(packets):
    payload = ""
    for packet in packets:
        data = str(packet.options[0][0])
        #removes the ' from the end of the string
        data = data[:-1]
        data = remove_last_x00(data)
        # removes any \x** fro, the beginning of the string
        data = data[4*data.count("\\x") + (2 * data.count("b'")) :]
        payload += data
    return  payload

def remove_last_x00(payload):
    #since using in built merthords cannot remove the last \x00 added to not full packets this will have to do
    #convert strign to ascii array and look for the last 4 number sequence 92 120 48 48
    #remove any numebr of the sequences then convert back to string with the \x00 removed
    removed = False
    asciiEncoded = payload.encode("ascii")
    while not removed:
        if asciiEncoded[-4] == 92 and asciiEncoded[-3] == 120 and asciiEncoded[-2] == 48 and asciiEncoded[-1] == 48:
            asciiEncoded = asciiEncoded[:-4]
        else:
            removed = True
    output = asciiEncoded.decode("ascii")        
    return output

def split_packets(packets, fileNameSrc, fileContentSrc):
    fileName= []
    fileContent = []
    for packet in packets:
        if packet[1].src == fileContentSrc:
            fileContent.append(packet)
        elif packet[1].src == fileNameSrc:
            fileName.append(packet)
    return fileName , fileContent
    
def decode_file_name(fileNamePackets):
    fileName = ""
    encodedFileName = retrive_payload(fileNamePackets)
    encodedFileName = Common.chunckData(encodedFileName, 2)
    encodedFileName = Common.hex_array_to_bin_arry(encodedFileName)
    
    for num in encodedFileName:
        fileName += chr(int(num,2))
    return fileName
 
    
def listen_for_packets(fileNameSrc,fileContentSrc):
    cont =""
    t = AsyncSniffer(filter="host " + fileNameSrc + " or host " + fileContentSrc)
    t.start()
    print("reciving connections")
    while not cont == "Q": 
        cont = input("Enter Q to stop: ")
    packets = t.stop()
    print("recived: " + str(len(packets)) + " of packets")
    if len(packets)  == 0:
        sys.exit("No Packets recived closing program")
    fileNamePackets , fileContentPacket = split_packets(packets, fileNameSrc, fileContentSrc)
    return fileNamePackets , fileContentPacket

def Reciving_part(fileNameSrc,fileContentSrc):
    fileNamePackets , fileContentPacket = listen_for_packets(fileNameSrc,fileContentSrc)
    fileName = decode_file_name(fileNamePackets)
    fileContent = retrive_payload(fileContentPacket)
    fileContent = Common.chunckData(fileContent, 2)
    fileOutput = Common.hex_array_to_bin_arry(fileContent)
    outputFileName = Common.dose_file_already_exsist(fileName)
    Common.binArayToFile(fileOutput,outputFileName)
    print("The recived File Has been outputed to: " + outputFileName)

def retrive_sending_information_user():
    global Delay 
    fileLocation =  input("Enter file location: ")
    while not Common.ValidFileName(fileLocation):
        fileLocation =  input("File name entered is invalid \n Enter file location: ")
    
    destination =  input("Enter destination address: ")
    while not Common.vaildate_IP_address(destination):    
        destination =  input("Enter valid destination address: ")
        
    Delay = Common.get_speed_from_user()

    
    fileNameSrc, fileContentSrc = retrive_receiving_information_user()
    
    return fileLocation, destination, fileNameSrc, fileContentSrc



def retrive_receiving_information_user():
    fileNameSrc =  input("Enter file name Source address e.g: 1.1.1.1: ")
    while not Common.vaildate_IP_address(fileNameSrc):    
        fileNameSrc =  input("Enter valid Source address e.g: 1.1.1.1: ")

    fileContentSrc =  input("Enter file content Source address e.g: 1.1.1.2: ")
    while not Common.vaildate_IP_address(fileNameSrc):  
        fileContentSrc =  input("Enter valid Source address e.g: 1.1.1.2: ")
            
    return fileNameSrc, fileContentSrc


def main():
    correctChoise = False
    while correctChoise == False:      
        option = input("Select an option \n 1.Send \n 2.Recive \n ")
        if option == "1":
            print("sending")
            correctChoise = True
            fileLocation, destination, fileNameSrc , fileContentsrc = retrive_sending_information_user()
            send_file(fileLocation, destination, fileNameSrc , fileContentsrc)
            
        elif option =="2":
            print("reciving")
            correctChoise = True
            fileNameSrc, fileContentSrc = retrive_receiving_information_user()
            Reciving_part(fileNameSrc, fileContentSrc)
        else:
            print("Please select correct option")


