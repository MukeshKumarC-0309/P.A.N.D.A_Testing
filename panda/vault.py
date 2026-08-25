"""
PandaVault: the database-backed record management system.

This module is kept as one large DATABASE() function with nested
sub-functions per table, preserved from the original implementation.
It works correctly as-is; splitting it into a proper class-based
structure (one method per table, a shared connection object passed
in rather than relying on module-level globals) is a natural next
refactor once the rest of the project is stable. See README.md for
notes on that.

The database is embedded SQLite (Python's stdlib sqlite3), not a MySQL
server: the vault is a single local file per device (see config.DB_PATH),
created empty on first run from schema.sql. This makes PandaVault a
zero-install, offline, per-user tool.
"""
import re
import sqlite3

from tabulate import tabulate

from panda.db import connection as conobj, cursor as cur
from panda.auth import check_password

# SQL parameters (?) can bind VALUES but never IDENTIFIERS (table/column
# names). For the free-form Search/Show features, validate identifiers
# against a strict whitelist before interpolating them into SQL.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _safe_identifier(name):
    """Return name if it is a valid SQL identifier, else raise ValueError.

    A valid identifier is a letter/underscore followed by any number of
    letters, digits, or underscores — so quotes, spaces, semicolons and
    other injection vectors are rejected.
    """
    if _IDENTIFIER_RE.match(name):
        return name
    raise ValueError("Invalid identifier: {!r}".format(name))


def DATABASE():
    def Emergency():
        cur.execute("select* from Emergency order by Patient_ID")
        r=cur.fetchall()
        header=["Patient_ID","Name","Age","Blood_Group","Chronic_Disease","Doctor_Name","Doctor_Phone","Allergic_Medications"]
        conobj.commit()
        print(tabulate(r,headers=header,tablefmt="grid"))
    def EDIT_EMERGENCY():
        Choice=input("What do you want to do ? ( Add | Edit | Delete ) : ")
        if Choice.upper()=="ADD":        
            l=[]
            Patient_ID=input("Enter Patient ID : ")
            l.append(Patient_ID)
            Name=input("Enter Patient Name : ")
            l.append(Name)
            Age=int(input("Enter Patient Age : "))
            l.append(Age)
            Blood_Group=input("Enter Blood Group : ")
            l.append(Blood_Group)
            Chronic_Disease=input("What disease is he/she suffering from? : ")
            l.append(Chronic_Disease)
            Doctor_Name=input("Enter the name of the doctor : ")
            l.append(Doctor_Name)
            Doctor_Phone=input("Enter doctor's phone number : ")
            l.append(Doctor_Phone)
            Allergic_Medications=input("What medicines is he/she allergic to ? ( please specify within curly brackets {} ) : ")
            l.append(Allergic_Medications)
            t=tuple(l)
            header=["Patient_ID","Name","Age","Blood_Group","Chronic_Disease","Doctor_Name","Doctor_Phone","Allergic_Medications"]
            execute="insert into emergency values(?,?,?,?,?,?,?,?)"
            try:   
                cur.execute(execute,t)
            except sqlite3.Error:
                print("P.A.N.D.A : There has been an error in adding values")
                print("P.A.N.D.A :Please check the values again")
            else:
                conobj.commit()
                print("No.of records added:",cur.rowcount)
                cur.execute("select* from Emergency order by Patient_ID")
                r3=cur.fetchall()
                print(tabulate(r3,headers=header,tablefmt="grid"))
        elif Choice.upper()=="DELETE":
            a=()
            ID=input("Enter the ID of the patient whose record you want to remove : ")
            a+=(ID,)
            execute1="delete from Emergency where Patient_ID=?"
            try:
                cur.execute(execute1,a)
            except sqlite3.Error:
                print("P.A.N.D.A : An unexpected error has occured")
                print("P.A.N.D.A : Please check the values again")
            else:
                conobj.commit()
                header=["Patient_ID","Name","Age","Blood_Group","Chronic_Disease","Doctor_Name","Doctor_Phone","Allergic_Medications"]
                cur.execute("select* from Emergency order by Patient_ID")
                r4=cur.fetchall()
                print(tabulate(r4,headers=header,tablefmt="grid"))
        elif Choice.upper()=="EDIT":
            t1=()
            field=input("which field do you want to change? : ")
            patient_ID=input("Enter ID of patient whose value is to be changed : ")
            new=input("Enter new value ( If Allergic Medications are specified,please put them in curly brackets ) : ")
            t1+=(new,patient_ID,)
            count1=0
            while True:
                if field.upper()=="NAME":
                    execute2="Update Emergency set Name=? where Patient_ID=?"
                    try:    
                        cur.execute(execute2,t1)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="AGE":
                    execute2="Update Emergency set Age=? where Patient_ID=?"
                    try:    
                        cur.execute(execute2,t1)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="BLOOD GROUP":
                    execute2="Update Emergency set Blood_Group=? where Patient_ID=?"
                    try:    
                        cur.execute(execute2,t1)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="CHRONIC DISEASE":
                    execute2="Update Emergency set Chronic_Disease=? where Patient_ID=?"
                    try:    
                        cur.execute(execute2,t1)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="DOCTOR NAME":
                    execute2="Update Emergency set Doctor_Name=? where Patient_ID=?"
                    try:    
                        cur.execute(execute2,t1)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="DOCTOR PHONE":
                    execute2="Update Emergency set Doctor_Phone=? where Patient_ID=?"
                    try:    
                        cur.execute(execute2,t1)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="ALLERGIC MEDICATIONS":
                    execute2="Update Emergency set Allergic_Medications=? where Patient_ID=?"
                    try:    
                        cur.execute(execute2,t1)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif count1==3:
                    print("P.A.N.D.A : Please try using 'Help' command.")
                else:
                    print("P.A.N.D.A : Error !")
                    count1+=1
            conobj.commit()
            header=["Patient_ID","Name","Age","Blood_Group","Chronic Disease","Doctor Name","Doctor Phone","Allergic Medications"]
            cur.execute("select* from Emergency order by Patient_ID")
            r5=cur.fetchall()
            print(tabulate(r5,headers=header,tablefmt="grid"))
        print()
    def Medicine():
        cur.execute("select* from Medicine")
        r1=cur.fetchall()
        header1=["Disease","Medicine_Name","Manufacturer","Duration","Quantity","Amount","Remark"]
        conobj.commit()
        print(tabulate(r1,headers=header1,tablefmt="grid"))
        print()
    def EDIT_MEDICINE():
        Choice1=input("What do you want to do ? ( Add | Edit | Delete ) : ")
        if Choice1.upper()=="ADD":
            l1=[]
            disease=input("Enter the name of the disease : ")
            l1.append(disease)
            medicine_name=input("Enter the name of the medicine : ")
            l1.append(medicine_name)
            manufacturer=input("Enter the manufacturer : ")
            l1.append(manufacturer)
            duration=input("Enter Medicine Duration : ")
            l1.append(duration)
            quantity=input("Enter Quantity : ")
            l1.append(quantity)
            amount=input("Enter amount : ")
            l1.append(amount)
            remark=input("Enter the remarks : ")
            l1.append(remark)
            tup=tuple(l1)
            header1=["Disease","Medicine_Name","Manufacturer","Duration","Quantity","Amount","Remark"]
            execute="insert into Medicine values(?,?,?,?,?,?,?)"
            try:
                cur.execute(execute,tup)
            except sqlite3.Error:
                    print("P.A.N.D.A : An unexpected error has occured")
                    print("P.A.N.D.A : Please check the values again")
            else:
                conobj.commit()
                print("No.of records added:",cur.rowcount)
                cur.execute("select* from Medicine")
                r6=cur.fetchall()
                print(tabulate(r6,headers=header1,tablefmt="grid"))
        elif Choice1.upper()=="DELETE":
            a1=()
            disease1=input("Enter Disease of the patient whose record you want to remove : ")
            a1+=(disease1,)
            execute2="delete from Medicine where Disease=?"
            try:    
                cur.execute(execute2,a1)
            except sqlite3.Error:
                    print("P.A.N.D.A : An unexpected error has occured")
                    print("P.A.N.D.A : Please check the values again")
            else:
                conobj.commit()
                header1=["Disease","Medicine_Name","Manufacturer","Duration","Quantity","Amount","Remark"]
                cur.execute("select* from Medicine")
                r7=cur.fetchall()
                print(tabulate(r7,headers=header1,tablefmt="grid"))
        elif Choice1.upper()=="EDIT":
            t3=()
            field1=input("Enter the field whose value you want to change : ")
            disease2=input("Enter the disease of the patient whose record you want to change : ")
            new1=input("Enter New Value")
            t3+=(new1,disease2,)
            count2=0
            while True:
                if field1.upper()=="MEDICINE NAME":
                    execute3="update Medicine set Medicine_Name=? where Disease=?"
                    try:    
                        cur.execute(execute3,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="MANUFACTURER":
                    execute3="update Medicine set Manufacturer=? where Disease=?"
                    try:    
                        cur.execute(execute3,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="DURATION":
                    execute3="update Medicine set Duration=? where Disease=?"
                    try:    
                        cur.execute(execute3,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="QUANTITY":
                    execute3="update Medicine set Quantity=? where Disease=?"
                    try:    
                        cur.execute(execute3,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="AMOUNT":
                    execute3="update Medicine set Amount=? where Disease=?"
                    try:    
                        cur.execute(execute3,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="REMARK":
                    execute3="update Medicine set Remark=? where Disease=?"
                    try:    
                        cur.execute(execute3,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif count2==3:
                    print("P.A.N.D.A : Please try using 'Help' command.")
                else:
                    print("P.A.N.D.A : Error !")
                    count2+=1
            conobj.commit()
            header1=["Disease","Medicine_Name","Manufacturer","Duration","Quantity","Amount","Remark"]
            cur.execute("select* from Medicine")
            r8=cur.fetchall()
            print(tabulate(r8,headers=header1,tablefmt="grid"))
        print()
    def MARKSHEET():
        cur.execute("select Exam_Name,Physics,Chemistry,Mathematics,English,Computer_Science,(Physics+Chemistry+Mathematics+English+Computer_Science)as Total,(Physics+Chemistry+Mathematics+English+Computer_Science)/5.0 as Average from Student_Marks")
        r9=cur.fetchall()
        header3=["Exam Name","Physics","Chemistry","Mathematics","English","Computer Science","Total","Average"]
        conobj.commit()
        print(tabulate(r9,headers=header3,tablefmt="grid"))
        print()
    def EDIT_MARKSHEET():
        Choice2=input("What do you want to do ? ( Add | Edit | Delete ) : ")
        if Choice2.upper()=="ADD":
            l2=[]
            exam_name=input("Enter Exam Name : ")
            l2.append(exam_name)
            phy=input("Enter Physics Marks : ")
            l2.append(phy)
            chem=input("Enter Chemistry Marks : ")
            l2.append(chem)
            math=input("Enter Mathematics Marks : ")
            l2.append(math)
            eng=input("Enter English Marks : ")
            l2.append(eng)
            cs=input("Enter Computer Science Marks : ")
            l2.append(cs)
            tup1=tuple(l2)
            header3=["Exam Name","Physics","Chemistry","Mathematics","English","Computer Science","Total","Average"]
            execute4="insert into Student_Marks values(?,?,?,?,?,?)"
            try:
                cur.execute(execute4,tup1)
            except sqlite3.Error:
                print("An unexpected error has occured")
                print("Please check the values again")
            else:    
                conobj.commit()
                cur.execute("select Exam_Name,Physics,Chemistry,Mathematics,English,Computer_Science,(Physics+Chemistry+Mathematics+English+Computer_Science)as Total,(Physics+Chemistry+Mathematics+English+Computer_Science)/5.0 as Average from Student_Marks")
                r10=cur.fetchall()
                print(tabulate(r10,headers=header3,tablefmt="grid"))
        elif Choice2.upper()=="DELETE":
            a2=()
            exam=input("Enter name of the exam whose record you want to remove : ")
            a2+=(exam,)
            execute5="delete from Student_Marks where Exam_Name=?"
            try:    
                cur.execute(execute5,a2)
            except sqlite3.Error:
                print("P.A.N.D.A : An unexpected error has occured")
                print("P.A.N.D.A : Please check the values again")
            else:    
                conobj.commit()
                header3=["Exam Name","Physics","Chemistry","Mathematics","English","Computer Science","Total","Average"]
                cur.execute("select Exam_Name,Physics,Chemistry,Mathematics,English,Computer_Science,(Physics+Chemistry+Mathematics+English+Computer_Science)as Total,(Physics+Chemistry+Mathematics+English+Computer_Science)/5.0 as Average from Student_Marks")
                r11=cur.fetchall()
                print(tabulate(r11,headers=header3,tablefmt="grid"))
        elif Choice2.upper()=="EDIT":
            t3=()
            field2=input("Enter Which Field you want to change : ")
            exam_name1=input("Enter exam name whose record you want to change : ")
            new2=input("Enter New Value : ")
            t3+=(new2,exam_name1,)
            count3=0
            while True:
                if field2.upper()=="PHYSICS":
                    execute6="update Student_Marks set Physics=? where Exam_Name=?"
                    try:    
                        cur.execute(execute6,t3)
                    except sqlite3.Error:
                        print("An unexpected error has occured")
                        print("Please check the values again") 
                    else:    
                        break
                elif field2.upper()=="CHEMISTRY":
                    execute6="update Student_Marks set Chemistry=? where Exam_Name=?"
                    try:    
                        cur.execute(execute6,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field2.upper()=="MATHEMATICS":
                    execute6="update Student_Marks set Mathematics=? where Exam_Name=?"
                    try:    
                        cur.execute(execute6,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field2.upper()=="ENGLISH":
                    execute6="update Student_Marks set English=? where Exam_Name=?"
                    try:    
                        cur.execute(execute6,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field2.upper()=="COMPUTER SCIENCE":
                    execute6="update Student_Marks set Computer_Science=? where Exam_Name=?"
                    try:    
                        cur.execute(execute6,t3)
                    except sqlite3.Error:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif count3==3:
                    print("P.A.N.D.A : Please try using 'Help' command.")
                else:
                    print("P.A.N.D.A : Error !")
                    count3+=1
            conobj.commit()
            header3=["Exam Name","Physics","Chemistry","Mathematics","English","Computer Science","Total","Average"]
            cur.execute("select Exam_Name,Physics,Chemistry,Mathematics,English,Computer_Science,(Physics+Chemistry+Mathematics+English+Computer_Science)as Total,(Physics+Chemistry+Mathematics+English+Computer_Science)/5.0 as Average from Student_Marks")
            r12=cur.fetchall()
            print(tabulate(r12,headers=header3,tablefmt="grid"))
        print()
    def SHOW_TABLES():
        #To display all the tables stored in the vault
        cur.execute("select name from sqlite_master where type='table' order by name")
        r23=cur.fetchall()
        conobj.commit()
        header7=["Tables"]
        print(tabulate(r23,headers=header7,tablefmt="grid"))
        print()
    def HELP():
        #PANDA HELPDESK
        print("-"*100)
        print("Welcome to the Panda Vault. Listed below are commands that will help you  navigate through the Vault.")
        print()
        print("P.A.N.D.A PHARMACY : P.A.N.D.A with its list of diseases and their medication acts as your personal pharmacist ")
        print("P.A.N.D.A CARE : P.A.N.D.A helps out during emergencies by giving a consolidated view of one's medical records")
        print("P.A.N.D.A MARKSHEET : P.A.N.D.A keeps track of exam scores to encourage academic improvement")
        print("\nBelow listed are commands that will help you access the features of P.A.N.D.A databases")
        print("\nSHOW TABLES:This command allows you to see what tables you have created so far")
        print("DEVELOPER MODE:This command allows you to make changes to the record structure of the table(can only be accessed through our special passcode)")
        print("CREATOR MODE:This command allows you to create your own tables and maintain your own record")
        print("-"*100)
    def USER():
        #DEVELOPER MODE where you ( the developer ) can directly input code
        while True:
            try:
                inp=input("What do you want to do ? ")
                cur.execute(inp)
                conobj.commit()
            except Exception:
                print("P.A.N.D.A : An unexpected error has occurred.")
                print("P.A.N.D.A : Please try again.")
            inp5=input("Do you want to continue using DEVELOPER MODE ? ")
            if inp5.upper()=="YES":
                continue
            else:
                print("Exiting DEVELOPER MODE...")
                return
    def panda_create():
        ch=input("Enter table name : ")
        execute15="create table if not exists {}(Serial_No TEXT)".format(ch)
        cur.execute(execute15)
        while True:
            inp1=input("Enter field name (enter 'exit' to exit) : ")
            if inp1.upper()=="EXIT":
                break
            else:
                execute16="alter table {} add column {} TEXT".format(ch,inp1)
                try:
                    cur.execute(execute16)
                except sqlite3.Error:
                    print("P.A.N.D.A : An unexpected error has occured")
                    print("P.A.N.D.A : Please check the values again")
                else:
                    conobj.commit()
        ch2=input("Do you want to add values ? ")
        if ch2.upper()=="YES":
            panda_add()
        print()
    def panda_add():
        ch=input("Enter your table name : ")
        inp1=int(input("How many fields are there ? "))
        while True:
            a=()
            inp2=input("Do you want to add records ? ")
            if inp2.upper()=="YES": 
                for i in range(inp1):
                    a+=(input("Enter Field 1 Value : "),)
                print(a)
                execute17="insert or ignore into {} values{}".format(ch,a)
                try:
                    cur.execute(execute17)
                except sqlite3.Error:
                    print("P.A.N.D.A : An unexpected error has occured")
                    print("P.A.N.D.A : Please check the values again")
                else:
                    conobj.commit()
            else:
                break
        print()
    def SEARCH():
        inp7=input("Enter Table Name :")
        field1=input("Enter field name")
        val=input("Enter field value")
        try:
            table=_safe_identifier(inp7)
            field=_safe_identifier(field1)
        except ValueError:
            print("P.A.N.D.A : Invalid table or field name.")
            print("P.A.N.D.A : Use letters, digits and underscores only.")
            print()
            return
        # Identifiers validated above; the value is bound as a parameter.
        execute19="select * from {} where {} = ?".format(table,field)
        try:
            cur.execute(execute19,(val,))
        except sqlite3.Error:
            print("P.A.N.D.A : An unexpected error has occured")
            print("P.A.N.D.A : Please check the values again")
        else:
            r25=cur.fetchall()
            for i in r25:
                print(i)
        print()
    def SHOW():
        inp8=input("Enter table name")
        try:
            table=_safe_identifier(inp8)
        except ValueError:
            print("P.A.N.D.A : Invalid table name.")
            print("P.A.N.D.A : Use letters, digits and underscores only.")
            print()
            return
        execute20="select * from {}".format(table)
        try:
            cur.execute(execute20)
        except sqlite3.Error:
            print("P.A.N.D.A : An unexpected error has occured")
            print("P.A.N.D.A : Please check the values again")
        else:
            r26=cur.fetchall()
            for i in r26:
                print(i)
        print()
    def PRE_SEARCH():
        inp9=input("Enter table name : ")
        field2=input("Enter field name : ")
        val1=input("Enter field value : ")
        # The table must be one of the known built-ins (dict membership is
        # the whitelist); the field is validated; the value is bound.
        if inp9 not in header_dictionary:
            print("P.A.N.D.A : Unknown table.")
            print("P.A.N.D.A : Please check the values again")
            print()
            return
        try:
            field=_safe_identifier(field2)
        except ValueError:
            print("P.A.N.D.A : Invalid field name.")
            print("P.A.N.D.A : Use letters, digits and underscores only.")
            print()
            return
        inp10=header_dictionary[inp9]
        execute21="select * from {} where {} = ?".format(inp9,field)
        try:
            cur.execute(execute21,(val1,))
        except sqlite3.Error:
            print("P.A.N.D.A : An unexpected error has occured")
            print("P.A.N.D.A : Please check the values again")
        else:
            r27=cur.fetchall()
            print(tabulate(r27,headers=inp10,tablefmt="grid"))
        print()
    #Main Block
    print("Welcome to the Panda Vault. ")
    print("Here, you can view, edit or delete records from your databases.")
    print()
    print("CREATOR MODE : Create and access your own tables ")
    print("DEVELOPER MODE : Developer-exclusive tools to work on the Vault ")
    print()
    #The headers required to print the tables in a user-friendly format
    header_emergency=["Patient_ID","Name","Age","Blood_Group","Chronic_Disease","Doctor_Name","Doctor_Phone","Allergic_Medications"]
    header_medicine=["Disease","Medicine_Name","Manufacturer","Duration","Quantity","Amount","Remark"]
    header_exam=["Exam Name","Physics","Chemistry","Mathematics","English","Computer Science","Total","Average"]
    header_dictionary={"Emergency":header_emergency,"Medicine":header_medicine,"Student_Marks":header_exam}
    #Prints the table based on input
    while True:
        Choice=input("What do you want to access ( DATABASES | EDIT | MODE | SHOW | SEARCH | HELP )?")
        if "PANDA CARE" in Choice.upper():
            Emergency()
            print()
        elif "PANDA PHARMACY" in Choice.upper():
            Medicine()
            print()
        elif "PANDA MARKSHEET" in Choice.upper():
            MARKSHEET()
            print()
        elif "EDIT" in Choice.upper():
            #Executes series of functions to edit the tables
            n=0
            while n<3:
                p = input("Enter the password : ")
                if check_password(p):
                    Choice1=input("Which Table do you want to edit?")
                    if "PANDA CARE" in Choice1.upper():
                        EDIT_EMERGENCY()
                        print()
                        break
                    elif "PANDA PHARMACY" in Choice1.upper():
                        EDIT_MEDICINE()
                        print()
                        break
                    elif "PANDA MARKSHEET" in Choice1.upper():
                        EDIT_MARKSHEET()
                        print()
                        break
                    else:
                        print("P.A.N.D.A : Incorrect Passcode.")
                        print("P.A.N.D.A : Try again.")
                        n+=1
                    if n==3:
                        print("P.A.N.D.A : You are out of attempts. ACCESS DENIED. ")
            print()
        elif "DEVELOPER MODE" in Choice.upper():
            #Executes functions to enable developer mode where developer can directly type in code
            n=0
            while n<3:
                #Uses passcode authentication to ensure security
                passcode=input("Please enter the passcode : ")
                if passcode.upper()=="ILUVPANDAS":
                    USER()
                    break
                else:
                    print("P.A.N.D.A : Incorrect Passcode.")
                    print("P.A.N.D.A : Try Again.")
                    n+=1
            if n==3:
                print("P.A.N.D.A : You are out of attempts. ACCESS DENIED. ")
            print()
        elif "CREATOR MODE" in Choice.upper():
            #The creator mode asks for input from user, then accordingly calls functions to
            #create a new table, add a record to existing table, view tables or quit.
            while True:
                inp2=input("Do you want to ( VIEW | ADD | CREATE | QUIT ) ? ")
                if inp2.upper()=="CREATE":
                    panda_create()
                elif inp2.upper()=="ADD":
                    panda_add()
                elif inp2.upper()=="VIEW":
                    inp3=input("Is it a pre-determined table?")
                    if inp3.upper()=="YES":
                        print("Please use the designated commands to view those tables")
                        break
                    elif inp3.upper()=="NO":
                        SHOW()
                elif inp2.upper()=="QUIT":
                    print("P.A.N.D.A : Exiting CREATOR MODE...")
                    break
                else:
                    print("P.A.N.D.A : Wrong input.")
                    print("P.A.N.D.A : Try again.")
            print()
        elif "SHOW" in Choice.upper():
            SHOW_TABLES()
            print()
        elif "HELP" in Choice.upper():
            HELP()
            print()
        elif "SEARCH" in Choice.upper():
            while True:
                inp3=input("Is it a user-defined table ? ")
                if inp3.upper()=="NO":
                    PRE_SEARCH()
                    break
                elif inp3.upper()=="YES":
                    SEARCH()
                    break
                else:
                    print("P.A.N.D.A : Invalid choice.")
                    print("P.A.N.D.A : Try again.")
            print()
        elif Choice.upper()=="QUIT":
            print("Exiting the PandaVault ...")
            break

