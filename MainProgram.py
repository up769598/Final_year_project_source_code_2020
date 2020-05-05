import error404 , Email_headers, imagesteganographyV2, IPOptions, TimeControlV2, ttlManipulation, DataGenerator, Common

run = True
while run:
     mode = input("Chose Runnning Mode: \n 1: 404 error \n 2: Email header \n 3: Image steganography \n 4: IP Options \n 5: Timing control \n 6: TTL Manipulation \n 7: Data generator \n 8: Hash file \n")
     if mode =="1":
          print("404 error")
          error404.main()
          run = False
     elif mode == "2":
          print("Email header")
          Email_headers.main()
          run = False
     elif mode == "3":
          print("Image steganography")
          imagesteganographyV2.main()
          run = False          
     elif mode == "4":
          print("IP Options")
          IPOptions.main()
          run = False          
     elif mode == "5":
          print("Timing control")
          TimeControlV2.main()
          run = False          
     elif mode == "6":
          print("TTL Manipulation")
          ttlManipulation.main()
          run = False 
     elif mode == "7":
          print("Data generator")
          DataGenerator.main()
          run = False
     elif mode == "8":
          fileLocation =  input("File to be hashed\n")
          while not Common.ValidFileName(fileLocation):
               fileLocation =  input("File name invalied\nEnter file to be hased: ")          
          fileHash = Common.HashCalc(fileLocation)
          print(fileHash)
          run = False           
     else:
          print("Please enter correct selection \n")