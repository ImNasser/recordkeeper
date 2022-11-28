import pickle
import sys
import os
import unittest       
#This class contains the core record keeping and management methods such as add new record, delete record, search record etc. It only contains the business logic.
#This class can also save/load the record keeping contents in the disk using the pickle module.
class RecordKeeper():
    #init constructor
    def __init__(self):
        self.record={"name":"","phone":"","address":"","misc":""}
        self.recordList=[]
        self.path=os.path.dirname(__file__)
        print("CWD: {0}".format(self.path))
        self.retrieveRecords()
        
        
        
    #to save the records in a file records.rec
    def saveRecords(self):
        file=open("records.rec","wb")
        self.recordList=pickle.dump(self.recordList,file)
        print("Successfully stored records")
        return self.recordList
        
    

    #a method to display the contents of a record in a text format and return it
    def getRecordText(self,record):
        text="name: {0}, phone: {1}, address: {2}".format(record["name"],record["phone"],record["address"])
        return str(text)
    
    #used for testing, a method to display the contents of a record in a text format and print it
    def printRecord(self,record):
        print("name: {0}, phone: {1}, address: {2}".format(record["name"],record["phone"],record["address"]))
    #a method to view all the records, iterate each of them and display the name, address, misc fields
    def viewRecords(self,records):
        i=0
        for record in records:
            i=i+1
            print(str(i)+": Name: {0}, Phone: {1} address: {2}, Misc: {3}".format(record["name"],record["phone"],record["address"],record["misc"]))

    #a method to add a new record with details to the record keeper list
    def add(self,name,phone=None,address=None,misc=None): #phone,address and misc are optional attributes
        phone=str(phone)
        self.record["name"]=name
        if (not phone==""):
            if (not str.isdigit(phone)):
                print("Failed to add record, phone num validation failed")
                return -1
            
        pos=self.searchBinary(self.retrieveRecords(),name)
        self.record["phone"]=phone
        self.record["address"]=address
        self.record["misc"]=misc
        #self.recordList.append(self.record)
        self.recordList.insert(pos+1,self.record)
        print("Record added successfully")
        return 1
        
    #a method to retrieve the record keeper list, when this method is called for the first time, it 
    # opens the records.rec to retrieve the records
    def retrieveRecords(self):
        if (len(self.recordList)==0):
            file=open(self.path+"/records.rec","rb")
            self.recordList=pickle.load(file)
            print("Successfully retrieved records")
           
        return self.recordList
    #a method to delete a record when a record name is specified. It performs binary search on the record list
    #  to quickly retrieve the record, if the record is found, it deletes the record from the list
    # please note, the record is deleted from the memory but is still part of the disk storage file records.rec
    # To delete the record from records.rec too, the save() method needs to be called
    def deleteRecord(self,name):
        record=self.searchBinary(self.retrieveRecords(),name)
        try:
            if (self.recordList.remove(record)==None):
                print("Removed")
                return 1
            else:
                return 0
        except ValueError as ep:
            return 0

        
    #This method performs an efficient binary search to search for the record by name using the record list as input
    # It is a recursive method and returns the record if it is found, or an int index of the last record searched if the record is not found
    def searchBinary(self, list,name):
        #To search record using binary search as records are sorted
        name=name.lower()
        if (len(list)==1):
            record=list[0]
            
            if (record["name"].lower()==name):
                return record
            else:
                origIndex=self.recordList.index(record)
                return origIndex


        if (len(list)>1):
            mid=len(list)/2
            mid=int(mid)
            midRecord=list.__getitem__(mid)
            if (midRecord["name"].lower()==name):
                return midRecord
            if (name>midRecord["name"].lower()):
                llist=len(list)
                rightList=list[mid:llist]
                return self.searchBinary(rightList,name)
            if (name<midRecord["name"].lower()):
                leftList=list[0:mid]
                return self.searchBinary(leftList,name)
                
        else:
            return 0

        
        


    
    


#A main class written for command line interface, it uses the record keeper internally to carry out it's functionalties.
# It also shows menu to the user and waits for input from the user. 
class Main():
    def __init__(self):
        print("Running")
        self.recordKeeper=RecordKeeper()
        self.recordKeeper.retrieveRecords()
        
    #Show a text menu to the user and wait for input, giving them all the possible interface of the record keeper clas
    def showMenu(self):
        
        print("Welcome to the RecordBook")
        print("Menu")
        print("1: Create a new record")
        print("2: View records")
        print("3: Search a record")
        print("4: Delete a record")
        print("5: Quit")
        userInput=input()
        userInput=int(userInput)
        return userInput
    
    #The main class, this class is the first class which is executed by the python main class
    # it shows the menu to the user and navigates them to the right method
    def main(self):
        userInput=self.showMenu()
        print("user input: {0}".format(userInput))
        if (userInput==1):
            #print("You have pressed 1")
            print("Enter the name of the record please")
            name=input()
            print("Enter the address of the record please (optional)")
            address=input()
            print("Enter the phone num of the record please (optional) ")
            phone=input()
            print("Enter the misc details of the record please (optional) ")
            misc=input()
            self.recordKeeper.add(name,phone, address,misc)
        elif (userInput==2):
            records=self.recordKeeper.retrieveRecords()
            self.recordKeeper.viewRecords(records)
        elif (userInput==3):
            print ("Please enter the name of the record")
            name=input()
            record=self.recordKeeper.searchBinary(self.recordKeeper.retrieveRecords(),name)
            if (record==0):
                print("Record was not found")
            else:
                self.recordKeeper.printRecord(record)

        elif (userInput==4):
            print("Enter the record name to delete")
            name=input()
            self.recordKeeper.deleteRecord(name)
        elif (userInput==5):
            #the user is exiting, so we need to save the updated record list to the disk file
            self.recordKeeper.saveRecords()
            return
        print("Do you want to go back to the menu or quit, write y/yes for menu and q/quit for quitting")
        response=input()
        if (response=="y" or response =="yes"):
            self.main()
        else:
            #before quitting save the results
            self.recordKeeper.saveRecords()
            return





#A very important class to validate and verify the working of the record keeper class.
#For each method of the record keeper class, this class contains a unit test method and 
#inherits from TestCase, this way an automated testing of the record keeper class can be made
#Each method in the class needs a test data and an expected data, the unit test executes the original method
#obtains return values and then compares it with the expected data. If both the values match, the test passes,
#otherwise the unit test fails 
class TestRecordKeeper(unittest.TestCase):
     
    @unittest.skip("")
    def testInsertRecord(self):
        recordKeeper=RecordKeeper()
        name="John"
        address="15 London Street, LE7 88D"
        phone=188
        misc="This is a test data"

        name2="Oliver"
        address2="15 London Street, LE7 88D"
        phone2=188
        misc2="This is a test data"

        name3="Zee"
        address3="15 London Street, LE7 88D"
        phone3="XY188"
        misc3="This is a test data"
        recordKeeper.add(name,phone,address,misc)
        result1=recordKeeper.searchBinary(recordKeeper.retrieveRecords(),"John")
        
        recordKeeper.add(name2,phone2,address2,misc2)
        result2=recordKeeper.searchBinary(recordKeeper.retrieveRecords(),"Oliver")
        result3=recordKeeper.add(name3,phone3,address3,misc3)  #invalid phone format, result must be 0
        
        
        if (result1==0 or result2==0 or result3==1):
            print("testInsertRecord unit test has failed")
        else:
            print("testInsertRecord: All tests have passed")
    
    @unittest.skip("")
    def testDeleteRecord(self):
        recordKeeper=RecordKeeper()
        name="John"
        address="15 London Street, LE7 88D"
        phone=188
        misc="This is a test data"

        name2="Oliver"
        address2="15 London Street, LE7 88D"
        phone2=188
        misc2="This is a test data"

        recordKeeper.add(name,phone,address,misc)
        recordKeeper.add(name2,phone2,address2,misc2)

        #now delete the second record
        result1=recordKeeper.deleteRecord("John")       
        self.assertEqual(result1,1)
        
    @unittest.skip("")
    def testSearchRecord(self):
        recordKeeper=RecordKeeper()
        name="John"
        address="15 London Street, LE7 88D"
        phone=188
        misc="This is a test data"

        name2="Oliver"
        address2="15 London Street, LE7 88D"
        phone2=188
        misc2="This is a test data"

        recordKeeper.add(name,phone,address,misc)
        recordKeeper.add(name2,phone2,address2,misc2)
        result=recordKeeper.searchBinary(recordKeeper.retrieveRecords(),"Oliver")
        self.assertEqual(result["name"],"Oliver")
    def testPhoneFormat(self):
        recordKeeper=RecordKeeper()
        name="John"
        address="15 London Street, LE7 88D"
        phone=183730
        misc="This is a test data"

        name2="Oliver"
        address2="15 London Street, LE7 88D"
        phone2="XDF888"
        misc2="This is a test data"

        result1=recordKeeper.add(name,phone,address,misc)#should pass result1=1
        result2=recordKeeper.add(name2,phone2,address2,misc2)#should fail result2=0
        self.assertEqual(result1,1)
        self.assertEqual(result2,0)







        
        
#main method without the class, this is executed first when this file is run
#it creates an instance of the Main class  and execute it's main method
if (__name__=="__main__"):
    Main().main()
    #TestRecordKeeper().testInsertRecord()
    #TestRecordKeeper().testDeleteRecord()
    #TestRecordKeeper().testSearchRecord()
    #unittest.main()

    
