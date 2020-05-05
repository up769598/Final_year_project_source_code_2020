import smtplib, ssl, imaplib, email, os, math, time
import Common as Common
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser


# initialize global varables
loginuser = ""
loginpassword = ""

def send_email(MACContentAddressArray, MACNameAddressArray, receiver_email, subject):
    global loginuser, loginpassword
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = loginuser
    message["To"] = receiver_email
    
    message["X-MAC"] = " ".join(MACContentAddressArray)
    message["N-MAC"] = " ".join(MACNameAddressArray)
    
    # Create the plain-text and HTML version of your message
    html = """\
    <html>
      <body>
        <p>test,<br>
        </p>
      </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))

    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(loginuser, loginpassword)
        server.sendmail(loginuser, receiver_email, message.as_string())
    


def import_format_data(fileLocation):
    fileName = os.path.basename(fileLocation)
    binArray = Common.open_file_bin_array(fileLocation)
    MACContentArray = Common.encode_into_MAC(binArray)
    MACNameArray = Common.encode_into_MAC(fileName.encode("ascii"))
    return MACContentArray, MACNameArray
   
   
def export_data(MACArray, fileName):
    MACtoDEC = Common.decode_MAC(MACArray)
    BinaryString = Common.dec_bit_array_to_pure_bin_srting(MACtoDEC)
    BinaryArray = Common.chunckData(BinaryString,8)
    Common.binArayToFile(BinaryArray, fileName)    
    


def read_email_from_gmail(sender, subject):
    global loginuser, loginpassword
    MACOutput = []
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(loginuser,loginpassword)
    mail.select('inbox')
    # FROM "anjali sinha"
    type, data = mail.search(None, '(FROM "' + sender + '" SUBJECT "' + subject + '")')
    mail_ids = data[0]
    
    id_list = mail_ids.split()
    print(str(len(id_list)) + " Emails found")
    for i in id_list:
        typ, data = mail.fetch(str(i)[2:-1], '(RFC822)' )
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode())
                MACContent = msg["X-MAC"]
                MACFileName = msg["N-MAC"]
                
                MACOutput += MACContent.split(" ")
                MACFileName = MACFileName.split(" ")
    return MACOutput , MACFileName
    
def decode_bin_array_to_file_name(binArray):
    output = ""
    for char in binArray:
        output += chr(int(char,2))
    return output   
    
    
def sending_part(fileName, receiver_email, subject):
    maxMACLenght = 3000
    MACContentArray, MACNameArray = import_format_data(fileName) 
    numOfEmails = math.ceil(len(MACContentArray)/maxMACLenght)    
    print("sending " + str(numOfEmails) +" emails")
    i = 0 
    while i < numOfEmails:
        send_email(MACContentArray[i*maxMACLenght:(i+1)*maxMACLenght], MACNameArray, receiver_email, subject)
        time.sleep(speedOffset)
        i += 1
    print("Emails sent")
        

def reciveing_part(sendersEmail, subject):
    MACContentArray, MACNameArray = read_email_from_gmail(sendersEmail, subject)
    fileContent = Common.decode_MAC_array(MACContentArray)
    encodedFileName = Common.decode_MAC_array(MACNameArray)
    fileName = decode_bin_array_to_file_name(encodedFileName)
    outputFileName = Common.dose_file_already_exsist(fileName)
    Common.binArayToFile(fileContent, outputFileName)
    print("File Outputed to: " + outputFileName)


def config_read():
    global loginuser, loginpassword
    config = configparser.ConfigParser()
    config.read('config.ini')
    if "Email" in config:
        loginuser = config["Email"]["User"]
        loginpassword = config["Email"]["Password"]
    else:
        user_login_get_from_user()
    
    
def user_login_get_from_user():
    global loginuser, loginpassword
    loginuser = input("Enter the login Email: ")
    loginpassword = input("Enter the login Password: ")


def main():
    global speedOffset
    config_read()
    while True:
        mode = input("Chose operation mode: \n1: send data \n2: assemble data from emails\n")
        if mode == "1":
            # gather user inputs.
            speedOffset = Common.get_speed_from_user()
            fileLocation =  input("file to be encoded\n")
            while not Common.ValidFileName(fileLocation):
                fileLocation =  input("file name invalied\nenter file location: ")   
            
            recipiantsEmail = input("Enter the recipients email address: ")
            while not recipiantsEmail:
                recipiantsEmail = input("Blank input\nEnter the recipients email address: ")
             
            subject = input("Enter the email subject: ")
            while not subject:
                subject = input("Blank input\nEnter the email subject: ")  
               
            sending_part(fileLocation, recipiantsEmail, subject)
            break
        elif mode == "2":
            sendersEmail = input("Enter the senders email address: ")
            while not sendersEmail:
                sendersEmail = input("Blank input\nEnter the senders email address: ")
            
            subject = input("Enter the email subject: ")
            while not subject:
                subject = input("Blank input\nEnter the email subject: ")  
            
            reciveing_part(sendersEmail, subject)
            
            break
        else:
            print("invalid option choose again \n")
     
    
    

                
# To do:
# Finished