
import cv2
import Common as Common
from progressbar import ProgressBar
import sys
import os


def usageCheck(binAray,image_location):
    img = get_image(image_location)
    hight = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    totalCapacity = hight * width  * channels    
    usage = (Common.totalListLength(binAray)/ totalCapacity) * 100
    if Common.totalListLength(binAray) <= totalCapacity:
        print("Full data encoded onto the image using " + str(usage) + "% of avalable space" )
    else:
        print("there is not enough space in the image to encode all of the information in the file. \n " + str(usage) + "% of avalable space has been used")
        decision = input("Chose: \n 1. Encode as much data as possible \n 2. Stop the process \n default option 1 \n")
        if decision == "2":
            sys.exit(0)
        else:
            print("Trunkating data")
            totalBitsSpace = (totalCapacity // 8)
            binAray = binAray[:totalBitsSpace]
            usage = (Common.totalListLength(binAray)/ totalCapacity) * 100
            print(usage)
    return binAray
    
1
def get_image(image_location):
    img = cv2.imread(image_location)
    return img

def stringToBinaryUnicode(strInput):
    outputArray = []
    for letter in strInput:
        outputArray.append(format(ord(letter), "b"))
    
    return outputArray

def bitcheck8(binaryArray):
    is8 = True
    for number in binaryArray:
        if len(number) == 8:
            is8 = is8 & True
        else:
            is8 = is8 & False
    return is8



def binaryUnicodeToString(inputAray):
    outputStr = ""
    for letter in inputAray:
        outputStr = outputStr + chr(int(letter, 2))
    return outputStr  

def BinArayToImg(imageLocation,binAray,outputImageLocation):
    pbar = ProgressBar()
    img = get_image(imageLocation)
    #Append a null char to look for to signify the end of the encoded infromation 
    hight = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    coloum = 0 
    row = 0
    channel = 0
    counter = 0 
    seenNullChar = False
    
    for byte in pbar(binAray):
        missing0 = 0        
        #checks to see if any 0's where lost.     
        if len(byte) < 8 and seenNullChar == False:
            missing0 = 8 - len(byte)
        
        #seenNullChar being True indicates the next binary number is 32 bits & is the file length  
        if seenNullChar:
            if len(byte) < 32:
                missing0 = 32 - len(byte)            
            seenNullChar = False
        
        #replaces the leading zeros that where lost.    
        byteString = "0" * missing0 + str(byte)
        
        if byteString == "00000000":
            seenNullChar = True
        
        for bit in byteString:
            if channel >= channels:
                channel = 0
                row += 1            
            #moves the aray along
            if row >= hight:
                coloum += 1
                row = 0

            currentValue = img.item(row,coloum,channel)
            
            #dose it need to change
            if doseItNeedToChange(int(bit) ,currentValue):
                #stops overflow error

                # if evan then + 1 else -1
                if Common.oddOrEvan(currentValue):
                    # fixes overflow error
                    if currentValue == 255:
                        currentValue -= 2                    
                    img.itemset((row,coloum,channel), currentValue + 1)
                else:
                    # fixes underflow error
                    if currentValue == 0:
                        currentValue += 2            
                    img.itemset((row,coloum,channel), currentValue - 1)
                

            channel += 1
            counter += 1 
    cv2.imwrite(outputImageLocation,img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    print("Image has been saved to:" + outputImageLocation) 
        
                
                
                
            
def doseItNeedToChange(desiredValue,value):
    if Common.oddOrEvan(desiredValue) == Common.oddOrEvan(value):
        return False
    else:
        return True
    
def fileToBinAray(fileLocation):
    f=open(fileLocation,"rb")
    content = f.read()
    f.close()
    outputArray = []
    for letter in content:
        outputArray.append(format(letter, "b"))
    fileLength = len(outputArray)
    fileName = os.path.basename(fileLocation)
    fileName = stringToBinaryUnicode(fileName)
    outputArray =  fileName + ["0"] + [format(fileLength, "b")] + outputArray
    return outputArray

def retriveFileInformation(inputImageLocation):
    img = get_image(inputImageLocation)
    hight = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    coloum = 0 
    row = 0
    channel = 0 
    seenNullChar = False
    fileName = []
    fileSize = ""
    while not seenNullChar:
        byte = ""
        for bit in range(8):
            if channel >= channels:
                channel = 0
                row += 1            
            #moves the aray along
            if row >= hight:
                coloum += 1
                row = 0
            currentValue = img.item(row,coloum,channel)
            if Common.oddOrEvan(currentValue):
                byte += "0"
            else:
                byte += "1"
            channel += 1
            
        if byte == "0"*8:
            seenNullChar = True
        else:
            fileName.append(byte)
    for bit in range(32):
        if channel >= channels:
            channel = 0
            row += 1            
        #moves the aray along
        if row >= hight:
            coloum += 1
            row = 0
        currentValue = img.item(row,coloum,channel)
        if Common.oddOrEvan(currentValue):
            fileSize += "0"
        else:
            fileSize += "1"
        channel += 1
    fileSize = int(fileSize,2)
    fileName = binaryUnicodeToString(fileName)
    print(fileSize)
    return fileName, fileSize, row, coloum, channel      
    
def imgToBinAray(imageLocation, fileSize, row, coloum, channel):     
    imgInput = get_image(imageLocation)
    hight = imgInput.shape[0]
    width = imgInput.shape[1]
    channels = imgInput.shape[2]
    coloum = coloum 
    row = row
    channel = channel 
    byteAray = []
    # Change While loop So it Counts the file Least gives in the image rather than the entire image.
    while len(byteAray) < fileSize:
        byte = ""
        for bit in range(8):
            if channel >= channels:
                channel = 0
                row += 1      
            #moves the aray along
            if row >= hight:
                coloum += 1
                row = 0
            if coloum > width:
                print("trying to read outside of the image")
                
            currentValue = imgInput.item(row,coloum,channel)
            if Common.oddOrEvan(currentValue):
                byte += "0"
            else:
                byte += "1"
            channel += 1
        byteAray.append(byte)
    return byteAray
            

def main():
    run = True
    while run:
        print("CSV to Image Encoding and decoding")
        mode = input("Choose an Option: \n 1.Encode a file in to a image \n 2.Decode an image into a file \n Q.Close program \n")
        if mode == "1":
            outputLocation = "output.png"
            fileLocation =  input("Enter file location: ")
            while not Common.ValidFileName(fileLocation):
                fileLocation =  input("File name entered is invalid \n Enter file location: ")
            image_location =  input("Enter input Image file location: ")
            while not Common.ValidFileName(image_location):
                image_location =  input("Input image file name entered is invalid \n Enter input Image file location:  ")               
            outputLocation =  input("Enter output .png location(if left blank defults to output.png): ")
            if outputLocation == "":
                outputLocation = "output.png"
                print("Invaled filename using defult")
            
            binAray = fileToBinAray(fileLocation)
            binAray = usageCheck(binAray, image_location)
            BinArayToImg(image_location,binAray,outputLocation)
            
        elif mode == "2":
            image_location =  input("Enter encoded .PNG file location\n")
            while not Common.ValidFileName(image_location):
                image_location =  input("PNG file name entered is invalid \n Enter encoded .PNG file location: ")            
             
            fileName, fileSize, row, coloum, channel = retriveFileInformation(image_location)
            outputLocation = Common.dose_file_already_exsist(fileName)
            print("The file will be outputed to: " + outputLocation)
            outputBinaryAray = imgToBinAray(image_location, fileSize, row, coloum, channel)
            Common.binArayToFile(outputBinaryAray, outputLocation)
            
            
        elif mode.lower() == "q":
            run = False
        else:
            print("select valid option")
         