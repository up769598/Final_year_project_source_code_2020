from faker import Faker
import csv
import random

fake = Faker()

def generate_National_insurance():
    ispossible = False
    
    possibleLetersFirst = ['A', 'B', 'C', 'E', 'G', 'H','J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z']
    possibleLetersSecond = ['A', 'B', 'C', 'E', 'G', 'H','J', 'K', 'L', 'M', 'N','P', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z']
    possibleLetersThird = ['A', 'B', 'C', 'D']
    
    canotBe = ["BG", "GB", "NK", "KN", "TN", "NT", "ZZ"]
    
    while not ispossible:
        first = random.choice(possibleLetersFirst) + random.choice(possibleLetersSecond)
        if not first in canotBe:
            ispossible = True
            
    numberSection ="%0.2d" % random.randint(0,99) + " " +"%0.2d" % random.randint(0,99) + " " + "%0.2d" % random.randint(0,99) 
    lastLetter =  random.choice(possibleLetersThird) 
    
    nationalInsurance = first + " " + numberSection + " " + lastLetter
    return nationalInsurance



def main():
    i = 1
    numberOfRows = input("enter the number of rows requred : \n")
    while not numberOfRows.isnumeric():
        numberOfRows = input("A number was not entered \n Enter the number of rows requred : \n")
    numberOfRows = int(numberOfRows)    
    outputFileName = input("Enter the file name output: \n")
    
    while i <= numberOfRows:
        name = fake.name()
        DOB= str(fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=99))
        address = fake.address().replace('\n', ' ').replace('\r', '')
        cardNumber = fake.credit_card_number(card_type=None)
        cv2 = fake.credit_card_security_code(card_type=None)
        expirayDate = fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")    
        phonenumber = "07" + str(random.randint(000000000,999999999))
        nationalInsurance =  generate_National_insurance()
        data = [name,DOB,address,phonenumber,nationalInsurance,cardNumber,cv2,expirayDate]
        i += 1
        with open(outputFileName+'.csv', newline='', mode='a+') as fake_data:
            fake_data_writer = csv.writer(fake_data, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fake_data_writer.writerow(data)

            
    