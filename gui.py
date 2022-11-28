import tkinter as tk
from tkinter import messagebox
import sys
from recordkeeper import RecordKeeper
#Class for graphical user interface, provides the GUI forms and uses the standard Tkiner library. 
# Contains the TKinter GUI components and logic, it uses record keeper for its internal functions
class GUI:
    def __init__(self):
       self.parent=None
       self.recordKeeper=RecordKeeper()
       self.lastItemClicked=None
   
    #messagebox to confirm the user choice
    def showConfirmationBox(self,text,title=None):
        box=messagebox.askokcancel(title,text,parent=self.parent)
        return box
    #generic messagebox to show some info
    def showMessageBox(self,text,title=None,parent=None):
        box=messagebox.showinfo(title,text,parent=parent)
        
        box.mod
        
    #function to add record to the record keeper by taking input from input elements
    def addRecord(self,name,phone,address,misc):
        box=self.showConfirmationBox("Do you want to add record with name: {0}, phone:{1}, address: {2} and misc: {3} details".format(name,phone,address,misc),"Add record confirmation")
        if (box==False):
            return

        result=self.recordKeeper.add(name,phone,address,misc)
        if (result==1):
            self.showMessageBox("Record has been added successfully","RecordKeeper")
        elif (result==-1):
            self.showMessageBox("Please enter the phone number in the correct format, must only contain numbers","Failed to add record")
        else:
            self.showMessageBox("Failed to add record, due to some error","RecordKeeper")
    #function to delete record from the record keeper by taking input from GUI elements
    def deleteRecord(self,window):
        item=self.lastItemClicked
        records=self.recordKeeper.retrieveRecords()
        if (isinstance(item,int)):
         record=records[item]
        else:
            self.showMessageBox("The selected item couldn't be found","Item not found",window)
 
        name=record["name"]
        phone=record["phone"]
        address=record["address"]
        misc=record["misc"]
        recordText="Name: {0} Phone: {1} Address: {2} Misc: {3}".format(name,phone,address,misc)
        box=self.showConfirmationBox("Do you want to delete record with name: {0}, phone:{1}, address: {2} and misc: {3} details".format(name,phone,address,misc),"Add record confirmation")
        if (box==False):
            return

        result=self.recordKeeper.deleteRecord(name)
        if (result==1):
            self.showMessageBox("Record has been deleted successfully","RecordKeeper")
        else:
            self.showMessageBox("Failed to delete record, due to some error","RecordKeeper")

        window.close()
        self.showDeleteForm()


            

    #function to search for a record from the record keeper by taking input from GUI elements
    def searchRecord(self,name,list,resultLabel):
        
    
        print("searchRecord name input: {0}".format(name))
        result=self.recordKeeper.searchBinary(self.recordKeeper.retrieveRecords(),name)
        if (isinstance(result,int)):
            resultLabel.set("Record was not found")
        else:
            
            resultLabel.set("Record found")
            record=result
            
            list.insert(list.size(),self.recordKeeper.getRecordText(record))
         
            

            
            
    #Shows the search form with the search field input and results view
    def showSearchForm(self):
        root=tk.Tk()
        root.title("Search Record")
        window=tk.Frame(root,width=300,height=400)
        
        label=tk.Label(master=window,text="Please enter a record name to search for it")
        nameLabel=tk.Label(master=window,text="Name/Tag:")
        nameLine=tk.Entry(master=window)
        
        resultsLabel=tk.Label(master=window,text="Result History")
        listWidget=tk.Listbox(master=window,width=50,height=10)
        resultLabel=tk.StringVar(master=window,value="")
        label2=tk.Label(master=window,text="Results",textvariable=resultLabel,fg="red")
        searchButton=tk.Button(master=window,text="Search Record",command=lambda: self.searchRecord(nameLine.get(),listWidget,resultLabel) )
        components=[window,label,nameLabel,nameLine,resultsLabel,listWidget,label2,searchButton]
        self.setPaddingPackLayout(components)
    
    #Shows the add form with the GUI elements to input name, phone, address, misc
    def showAddForm(self):
        parent=tk.Tk()
        parent.title("Add a new record")
        frame=tk.Frame(parent,width=300,height=300)
        
        label=tk.Label(master=frame,text="Please enter the record details")
        nameLabel=tk.Label(master=frame,text="Name:")
        nameLine=tk.Entry(master=frame,text="Name here")
        phoneLabel=tk.Label(master=frame,text="Phone:")
        phoneLine=tk.Entry(master=frame,text="phone here")
        addressLabel=tk.Label(master=frame,text="Address:")
        addressLine=tk.Entry(master=frame,text="address here")
        miscLabel=tk.Label(master=frame,text="Misc:")
        miscLine=tk.Entry(master=frame,text="misc here")
        addButton=tk.Button(master=frame,text="Add Record",command=lambda: self.addRecord(nameLine.get(),phoneLine.get(),addressLine.get(),miscLine.get()))
        
        
        label.grid(row=0,column=1,padx=20,pady=10)
        components=[frame,nameLabel,nameLine,phoneLabel,phoneLine,addressLabel,addressLine,miscLabel, miscLine, addButton]
        i=1
        for c in components:
            if (isinstance(c,tk.Label)):
                c.grid(row=i,column=0,pady=10)
                
            else:
             c.grid(row=i,column=1,pady=10)
             i=i+1
            
        
        
        
        


    def list_item_clicked(self,item):
        item=item.curselection()[0]
        print("you clicked:{0}".format(item))
        self.lastItemClicked=item
        
    #Emulates a GUI based table using the tkinter entry(inputLine), since there is no Table view widget in tkinter
    def createTable(self,rows,headers,startRow,window):
        #self.e = Entry(root, width=20, fg='blue',font=('Arial',16,'bold'))
        print("Creating a table")
        for i in range(0,len(headers)):
            label=tk.Label(master=window,text=headers[i])
            label.grid(row=startRow,column=i)

        for i in range(0,len(rows)):
            for j in range(0,len(rows[i])):
             col=rows[i][j]
             col=str(col)
             e=tk.Entry(master=window,width=20)
             
             print("Column found:{2} row:{0}, col:{1}".format(i,j,col))
             e.insert(tk.END,col)
             e.grid(row=1+startRow+i,column=j)
             #e.config(state="readonly")


    
    #method to execute when sort list button is called, it simplies closes the current window
    #and opens up the view form again with the correct argument can be 'asc' for ascdending and 'dsc' for descending sort
    def sortRecords(self,root,sort):
        root.destroy()
        self.showViewForm(sort)
    
    #Shows the View form with the list of all the records in the tkinter list widget
    def showViewForm(self,sort=None):
        root=tk.Tk()
        root.grid_rowconfigure(0,weight=1)
        root.grid_columnconfigure(0,weight=1)
        root.title("View Records")
        window=tk.Frame(master=root,width=300,height=300)
        window.grid(row=0,column=0)
        label=tk.Label(master=window,text="Viewing all records")
        
        buttonSortAcscending=tk.Button(master=window,text="Sort-Name-Asc",command=lambda: self.sortRecords(root,"asc"))
        buttonSortDescending=tk.Button(master=window,text="Sort-Name-Dsc)", command=lambda: self.sortRecords(root,"dsc"))
        buttonSortAcscending.grid(row=0,column=0)
        buttonSortDescending.grid(row=0,column=1)
        label.grid(row=1,column=0)
        
        
        listRecords=self.recordKeeper.retrieveRecords()
        if (sort=="asc"):
         listRecords.sort(key=lambda x: x['name'] )
        elif (sort=="dsc"):
            listRecords.sort(key=lambda x: x['name'],reverse=True )
        
        headers=["name","phone","address","misc"]
              
        rows=[]
        
        i=0
        for record in listRecords:
         cols=[]
         name=record["name"]
         phone=record["phone"]
         address=record["address"]
         misc=record["misc"]
         #recordText="Name: {0} Phone: {1} Address: {2} Misc: {3}".format(name,phone,address,misc)
         cols.append(str(i))
         cols.append(name)
         cols.append(phone)
         cols.append(address)
         cols.append(misc)
         rows.append(cols)
         i=i+1
         
         
        list=self.createTable(rows,headers,2,window)
        closebutton=tk.Button(master=window,text="Close Button",command=lambda: root.destroy())
        closebutton.grid(row=3+len(listRecords),column=0,pady=10)
        
         
       
        
    def setPaddingPackLayout(self,components):
        for c in components:
            c.pack(pady=10,padx=10)
    #Shows the delete form, it shows all the records in a list and allows user to click on the record
    #to delete it, before deleting it askes for the user confirmation
    def showDeleteForm(self):
      
        root=tk.Tk()
        root.title("Delete a record")
        self.deleteParent=root
        window=tk.Frame(root,width=300,height=300)
        window.pack()
        label=tk.Label(master=window,text="Please select the record from the list to delete it")
        list=tk.Listbox(window,width=50,height=10)
        listRecords=self.recordKeeper.retrieveRecords()
        i=0
        for record in listRecords:
         name=record["name"]
         phone=record["phone"]
         address=record["address"]
         misc=record["misc"]
         recordText="Name: {0} Phone: {1} Address: {2} Misc: {3}".format(name,phone,address,misc)
         print("Insert record:{0} at location:{1}".format(record,i))
         list.insert(i,recordText)
         i=i+1
         
         
        deleteButton=tk.Button(master=window,text="Delete Record",command=lambda : self.deleteRecord(window))
        components=[label,list,deleteButton]
        self.setPaddingPackLayout(components)
        list.bind("<<ListboxSelect>>",lambda ev: self.list_item_clicked(list))
        
        
    # a method which is called whenever the user presses any button on the main window containing options, by reading the button text, we can have different business logic for each button    
    def on_button_click(self,button):
        print("Button clicked")
      
        text=button.config()['text'][4].lower()
        print(text)
        if ("add" in text):
             print("Button clicked add")
             self.showAddForm()

        elif ("delete" in text):
            print("delete button clicked")
            self.showDeleteForm()
        elif ("search" in text):
            print("search button clicked")
            self.showSearchForm()
        elif ("view" in text):
            print("view button clicked")
            self.showViewForm()
        elif ("save" in text):
            print("Saving records")            
            self.recordKeeper.saveRecords()
        elif ("exit" in text):
            print("Exiting")            
            sys.exit()
        
        
        
        
           

        
    #creates the main gui window with add/deletesearch/exit buttons
    def createMainWindow(self):
       
        label=tk.Label(master=self.parent,text="Welcome to the RecordKeeper")
        addButton=tk.Button(master=self.parent,text="Add record",command=lambda: self.on_button_click(addButton))
        deleteButton=tk.Button(master=self.parent,text="Delete record",command=lambda: self.on_button_click(deleteButton))
        searchButton=tk.Button(master=self.parent,text="Search record",command=lambda: self.on_button_click(searchButton))
        viewButton=tk.Button(master=self.parent,text="View/Sort records",command=lambda: self.on_button_click(viewButton))
        saveButton=tk.Button(master=self.parent,text="Save records",command=lambda: self.on_button_click(saveButton))
        exitButton=tk.Button(master=self.parent,text="Exit",command=lambda: self.on_button_click(exitButton))
        

        label.grid(row=1,column=0,pady=10)
        addButton.grid(row=2,column=0,pady=10)
        deleteButton.grid(row=3,column=0,pady=10)
        searchButton.grid(row=4,column=0,pady=10)
        viewButton.grid(row=5,column=0,pady=10)
        saveButton.grid(row=6,column=0,pady=10)
        exitButton.grid(row=7,column=0,pady=10)
        buttons=[addButton,deleteButton,searchButton,viewButton,saveButton,exitButton]
        for btn in buttons:
            btn.config(width=30)
        
             
        # wid=QtWidgets.QWidget()
        # wid.setLayout(layout)
        # win.setCentralWidget(wid)
        

    def on_exit_click(self):
        print("Exit clicked")
        sys.exit()
    
    
    #creates the menu, currently only contains save and exit options
    def createMenu(self):
        menu=tk.Menu(self.parent)
        file=tk.Menu(menu,tearoff=0)
        save=file.add_command(label="Save",command=self.recordKeeper.saveRecords)
        exit=file.add_command(label="Exit",command=lambda: sys.exit())
        menu.add_cascade(label="File",menu=file)
        #file.addMenu(exit)
        return menu
        

    #entry point for the tkinter application
    def runApp(self):
        app=tk.Tk()
        
        app.title("RecordKeeper GUI Application")
        self.parent=app #save the app
        app.geometry('500x400+50+50')
        app.grid_rowconfigure(0,weight=1)
        app.grid_columnconfigure(0,weight=1)
        self.createMainWindow()
        menuBar=self.createMenu()#sys.exit(app.exec_()) 
        app.config(menu=menuBar)
        app.mainloop()
        

        
        
      
if __name__=="__main__":
    app=GUI()
    app.runApp()
