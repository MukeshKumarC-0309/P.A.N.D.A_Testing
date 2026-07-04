"""
PandaVault: the database-backed record management system.

This module is kept as one large DATABASE() function with nested
sub-functions per table, preserved from the original implementation.
It works correctly as-is; splitting it into a proper class-based
structure (one method per table, a shared connection object passed
in rather than relying on module-level globals) is a natural next
refactor once the rest of the project is stable. See README.md for
notes on that.

The only functional change here is credential handling: the database
connection now comes from config.py (environment variables) instead
of a hardcoded username/password in source.
"""
from tabulate import tabulate
import mysql.connector as mc

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

conobj = mc.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
cur = conobj.cursor()


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
            execute="insert into emergency values(%s,%s,%s,%s,%s,%s,%s,%s)"
            try:   
                cur.execute(execute,t)
            except:
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
            execute1="delete from Emergency where Patient_ID=%s"
            try:
                cur.execute(execute1,a)
            except:
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
                    execute2="Update Emergency set Name=%s where Patient_ID=%s"
                    try:    
                        cur.execute(execute2,t1)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="AGE":
                    execute2="Update Emergency set Age=%s where Patient_ID=%s"
                    try:    
                        cur.execute(execute2,t1)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="BLOOD GROUP":
                    execute2="Update Emergency set Blood_Group=%s where Patient_ID=%s"
                    try:    
                        cur.execute(execute2,t1)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="CHRONIC DISEASE":
                    execute2="Update Emergency set Chronic_Disease=%s where Patient_ID=%s"
                    try:    
                        cur.execute(execute2,t1)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="DOCTOR NAME":
                    execute2="Update Emergency set Doctor_Name=%s where Patient_ID=%s"
                    try:    
                        cur.execute(execute2,t1)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="DOCTOR PHONE":
                    execute2="Update Emergency set Doctor_Phone=%s where Patient_ID=%s"
                    try:    
                        cur.execute(execute2,t1)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field.upper()=="ALLERGIC MEDICATIONS":
                    execute2="Update Emergency set Allergic_Medications=%s where Patient_ID=%s"
                    try:    
                        cur.execute(execute2,t1)
                    except:
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
            execute="insert into Medicine values(%s,%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(execute,tup)
            except:
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
            execute2="delete from Medicine where Disease=%s"
            try:    
                cur.execute(execute2,a1)
            except:
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
                    execute3="update Medicine set Medicine_Name=%s where Disease=%s"
                    try:    
                        cur.execute(execute3,t3)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="MANUFACTURER":
                    execute3="update Medicine set Manufacturer=%s where Disease=%s"
                    try:    
                        cur.execute(execute3,t3)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="DURATION":
                    execute3="update Medicine set Duration=%s where Disease=%s"
                    try:    
                        cur.execute(execute3,t3)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="QUANTITY":
                    execute3="update Medicine set Quantity=%s where Disease=%s"
                    try:    
                        cur.execute(execute3,t3)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="AMOUNT":
                    execute3="update Medicine set Amount=%s where Disease=%s"
                    try:    
                        cur.execute(execute3,t3)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field1.upper()=="REMARK":
                    execute3="update Medicine set Remark=%s where Disease=%s"
                    try:    
                        cur.execute(execute3,t3)
                    except:
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
        cur.execute("select Exam_Name,Physics,Chemistry,Mathematics,English,Computer_Science,(Physics+Chemistry+Mathematics+English+Computer_Science)as Total,(Physics+Chemistry+Mathematics+English+Computer_Science)/5 as Average from Student_Marks")
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
            execute4="insert into Student_Marks values(%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(execute4,tup1)
            except:
                print("An unexpected error has occured")
                print("Please check the values again")
            else:    
                conobj.commit()
                cur.execute("select Exam_Name,Physics,Chemistry,Mathematics,English,Computer_Science,(Physics+Chemistry+Mathematics+English+Computer_Science)as Total,(Physics+Chemistry+Mathematics+English+Computer_Science)/5 as Average from Student_Marks")
                r10=cur.fetchall()
                print(tabulate(r10,headers=header3,tablefmt="grid"))
        elif Choice2.upper()=="DELETE":
            a2=()
            exam=input("Enter name of the exam whose record you want to remove : ")
            a2+=(exam,)
            execute5="delete from Student_Marks where Exam_Name=%s"
            try:    
                cur.execute(execute5,a2)
            except:
                print("P.A.N.D.A : An unexpected error has occured")
                print("P.A.N.D.A : Please check the values again")
            else:    
                conobj.commit()
                header3=["Exam Name","Physics","Chemistry","Mathematics","English","Computer Science","Total","Average"]
                cur.execute("select Exam_Name,Physics,Chemistry,Mathematics,English,Computer_Science,(Physics+Chemistry+Mathematics+English+Computer_Science)as Total,(Physics+Chemistry+Mathematics+English+Computer_Science)/5 as Average from Student_Marks")
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
                    execute6="update Student_Marks set Physics=%s where Exam_Name=%s"
                    try:    
                        cur.execute(execute6,t3)
                    except:
                        print("An unexpected error has occured")
                        print("Please check the values again") 
                    else:    
                        break
                elif field2.upper()=="CHEMISTRY":
                    execute6="update Student_Marks set Chemistry=%s where Exam_Name=%s"
                    try:    
                        cur.execute(execute6,t3)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field2.upper()=="MATHEMATICS":
                    execute6="update Student_Marks set Mathematics=%s where Exam_Name=%s"
                    try:    
                        cur.execute(execute6,t3)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field2.upper()=="ENGLISH":
                    execute6="update Student_Marks set English=%s where Exam_Name=%s"
                    try:    
                        cur.execute(execute6,t3)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field2.upper()=="COMPUTER SCIENCE":
                    execute6="update Student_Marks set Computer_Science=%s where Exam_Name=%s"
                    try:    
                        cur.execute(execute6,t3)
                    except:
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
            cur.execute("select Exam_Name,Physics,Chemistry,Mathematics,English,Computer_Science,(Physics+Chemistry+Mathematics+English+Computer_Science)as Total,(Physics+Chemistry+Mathematics+English+Computer_Science)/5 as Average from Student_Marks")
            r12=cur.fetchall()
            print(tabulate(r12,headers=header3,tablefmt="grid"))
        print()
    def PANDA_Mart():
        cur.execute("select* from PANDA_Mart")
        r2=cur.fetchall()
        header2=["Items","Quantity","Price"]
        conobj.commit()
        print(tabulate(r2,headers=header2,tablefmt="grid"))
        print()
    def EDIT_MART():
        #To edit the PandaMart table
        Choice3=input("What do you want to do ? ( Add | Edit | Delete ) : ")
        if Choice3.upper()=="ADD":
            l3=[]
            items1=input("Enter Item Name : ")
            l3.append(items1)
            quantity1=input("Enter Quantity : ")
            l3.append(quantity1)
            price1=input("Enter Price : ")
            l3.append(price1)
            t4=tuple(l3)
            header4=["Items","Quantity","Price"]
            execute7="insert into PANDA_Mart values(%s,%s,%s)"
            try:    
                cur.execute(execute7,t4)
            except:
                print("P.A.N.D.A : An unexpected error has occured")
                print("P.A.N.D.A : Please check the values again") 
            else:    
                conobj.commit()
                print("No.of records added:",cur.rowcount)
                cur.execute("select* from PANDA_Mart")
                r13=cur.fetchall()
                print(tabulate(r13,headers=header4,tablefmt="grid"))
        elif Choice3.upper()=="DELETE":
            a3=()
            item2=input("Enter item whose record you want to delete : ")
            a3+=(item2,)
            execute8="delete from PANDA_Mart where Items=%s"
            try:    
                cur.execute(execute8,a3)
            except:
                print("P.A.N.D.A : An unexpected error has occured")
                print("P.A.N.D.A : Please check the values again")
            else:
                conobj.commit()
                header4=["Items","Quantity","Price"]
                cur.execute("select* from PANDA_Mart")
                r14=cur.fetchall()
                print(tabulate(r14,headers=header4,tablefmt="grid"))
        elif Choice3.upper()=="EDIT":
            t4=()
            field3=input("Enter field whose record you want to change : ")
            item3=input("Enter item name of the record : ")
            new3=input("Enter new value : ")
            t4+=(new3,item3,)
            count4=0
            while True:
                if field3.upper()=="QUANTITY":
                    execute9="update PANDA_Mart set Quantity=%s where Items=%s"
                    try:    
                        cur.execute(execute9,t4)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif field3.upper()=="PRICE":
                    execute9="update PANDA_Mart set Price=%s where Items=%s"
                    try:    
                        cur.execute(execute9,t4)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                    else:    
                        break
                elif count4==3:
                    print("P.A.N.D.A : Please try using 'Help' command.")
                else:
                    print("P.A.N.D.A : Error !")
                    count4+=1
            conobj.commit()
            header4=["Items","Quantity","Price"]
            cur.execute("select* from PANDA_Mart")
            r15=cur.fetchall()
            print(tabulate(r15,headers=header4,tablefmt="grid"))
        print()
    def SHOPPING_LIST():
        cur.execute("select* from Shopping_List order by Serial_No")
        r16=cur.fetchall()
        header5=["Serial No.","Items","Price","Remark"]
        conobj.commit()
        print(tabulate(r16,headers=header5,tablefmt="grid"))
        print()
    def EDIT_LIST():
        #To edit the shopping list table
        Choice4=input("What do you want to do ? ( Add | Edit | Delete ) : ")
        if Choice4.upper()=="ADD":
            t5=()
            a1=input("Enter Serial No. : ")
            a2=input('What do you want to buy ? : ')
            a3=float(input('Enter price : '))
            cur.execute("Select Items from PANDA_Mart")
            r12=cur.fetchall()
            for i in r12:
                if a2.upper()==i[0].upper():
                    a4='Not Bought'
                    t5+=(a1,a2,a3,a4,)
                    execute10="insert into Shopping_List values(%s,%s,%s,%s)"
                    try:
                        cur.execute(execute10,t5)
                    except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : The value",i[1],"is invalid.") 
                    else:
                        conobj.commit()
                        cur.execute("Select * from Shopping_List order by Serial_No")
                        r17=cur.fetchall()
                        header5=["Serial No.","Items","Price","Remark"]
                        print(tabulate(r17,headers=header5,tablefmt="grid"))
        elif Choice4.upper()=='EDIT':
            t2=()
            a5=input("Enter the name of the item you want to update : ")
            field=input("Enter the field : ")
            new=input('Enter new value : ')
            t2+=(new,a5,)
            if field.upper()=='PRICE':
                execute11="update Shopping_List set Price=%s where Items=%s"
                try:
                    cur.execute(execute11,t2)
                except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again") 
                else:
                    conobj.commit()
                    cur.execute('Select * from Shopping_List order by Serial_No')
                    r18=cur.fetchall()
                    header5=["Serial No.","Items","Price","Remark"]
                    print(tabulate(r18,headers=header5,tablefmt="grid"))
            elif field.upper()=='REMARK':
                execute11="update Shopping_List set remark=%s where Items=%s"
                try:
                    cur.execute(execute11,t2)
                except:
                        print("P.A.N.D.A : An unexpected error has occured")
                        print("P.A.N.D.A : Please check the values again")
                else:
                    conobj.commit()
                    cur.execute('Select * from Shopping_List order by Serial_No')
                    r18=cur.fetchall()
                    header5=["Serial No.","Items","Price","Remark"]
                    print(tabulate(r18,headers=header5,tablefmt="grid"))
        elif Choice4.upper()=="DELETE":
            a5=()
            sno=input("Enter Serial no. whose record is to be deleted : ")
            a5+=(sno,)
            execute12="delete from Shopping_List where Serial_No=%s"
            try:    
                cur.execute(execute12,a5)
            except:
                print("P.A.N.D.A : An unexpected error has occured")
                print("P.A.N.D.A : Please check the values again")
            else:
                conobj.commit()
                cur.execute('Select * from Shopping_List order by Serial_No')
                r19=cur.fetchall()
                header5=["Serial No.","Items","Price","Remark"]
                print(tabulate(r19,headers=header5,tablefmt="grid"))
        print()
    def TRANSACTION_HISTORY():
        #To view the Transaction History table
        Choice5=input("Do you want to ( View | Delete ) your Transaction History ? ")
        if Choice5.upper()=="VIEW":
            cur.execute("select Serial_No,Items,Price from Shopping_List where Remark='Bought'")
            r20=cur.fetchall()
            for i in r20:
                execute13="insert ignore into Transaction_History values(%s,%s,%s)"
                try:
                    cur.execute(execute13,i)
                except:
                    print("An unexpected error has occured")
                    print("The value",i[1],"is invalid.")
                else:
                    conobj.commit()
                    cur.execute("select* from Transaction_History order by Serial_No")
                    r21=cur.fetchall()
                    header6=["Serial No.","Items","Price"]
                    conobj.commit()
            try:
                print(tabulate(r21,headers=header6,tablefmt="grid"))
            except UnboundLocalError:
                print("Shopping list is empty.")
        elif Choice5.upper()=="DELETE":
            a6=()
            sno1=input("Enter serial no. of record to be deleted : ")
            a6+=(sno1,)
            execute14="delete from Transaction_History where Serial_No=%s"
            try:
                cur.execute(execute14,a6)
            except:
                print("P.A.N.D.A : An unexpected error has occured.")
                print("P.A.N.D.A : Please check the values again.")
            else:
                conobj.commit()
                cur.execute("select* from Transaction_History order by Serial_No")
                r22=cur.fetchall()
                header6=["Serial No.","Items","Price"]
                print(tabulate(r22,headers=header6,tablefmt="grid"))
        print()
    def PANDA_COUNTER():
        #To display records from PandaCounter table based on input from user
        cur.execute("select* from Panda_Counter")
        r28=cur.fetchall()
        header7=["Serial No","Flight Number","Airline Name","Origin","Destination","Departure","Arrival"]
        conobj.commit()
        print(tabulate(r28,headers=header7,tablefmt="grid"))
        Choice6=input("Do you want to search for a specific flight ? ")
        if Choice6.upper()=="YES":
            origin=input("Enter origin country : ")
            destination=input("Enter destination country : ")
            execute22="select* from Panda_Counter where Origin='{}' and Destination='{}'".format(origin,destination)
            try:
                cur.execute(execute22)
            except:
                print("P.A.N.D.A : An unexpected error has occured")
                print("P.A.N.D.A : Please check the values again")
            else:
                r29=cur.fetchall()
                conobj.commit()
                header8=["Serial No","Flight Number","Airline Name","Origin","Destination","Departure","Arrival"]
                print(tabulate(r29,headers=header8,tablefmt="grid"))
        print()
    def EDIT_COUNTER():
        #To edit the PandaCounter table
        Choice7=input("What do you want to do ? ( Add | Edit | Delete ) : ")
        if Choice7.upper()=="ADD":
            serialno=int(input("Enter Serial No :"))
            flightno=input("Enter Flight Number :")
            airline=input("Enter Airline Name :")
            origin1=input("Enter Origin Country :")
            dest=input("Enter Destination Country :")
            departure=input("Enter Departure time :")
            arrival=input("Enter Arrival Time :")
            execute23="insert into Panda_Counter values({},'{}','{}','{}','{}','{}','{}')".format(serialno,flightno,airline,origin1,dest,departure,arrival)
            try:
                cur.execute(execute23)
            except:
                print("P.A.N.D.A : An unexpected error has occured")
                print("P.A.N.D.A : Please check the values again")
            else:
                conobj.commit()
                cur.execute("select* from Panda_Counter")
                r30=cur.fetchall()
                header9=["Serial No","Flight Number","Airline Name","Origin","Destination","Departure","Arrival"]
                print(tabulate(r30,headers=header9,tablefmt="grid"))
        elif Choice7.upper()=="DELETE":
            fieldname=input("Enter field name whose record is to be deleted :")
            val=input("Enter value of that field :")
            ch=input("Is your value a time ?")
            if ch.upper()=="YES":
                execute24="delete from Panda_Counter where {}='{}'".format(fieldname,val)
                try:
                    cur.execute(execute24)
                except:
                    print("P.A.N.D.A : An unexpected error has occured")
                    print("P.A.N.D.A : Please check the values again")
                else:
                    conobj.commit()
                    cur.execute("select* from Panda_Counter")
                    r31=cur.fetchall()
                    header10=["Serial No","FLight Number","Airline Name","Origin","Destination","Departure","Arrival"]
                    print(tabulate(r31,headers=header10,tablefmt="grid"))
            else:
                execute25="delete from Panda_Counter where {}={}".format(fieldname,val)
                try:
                    cur.execute(execute25)
                except:
                    print("P.A.N.D.A : An unexpected error has occured")
                    print("P.A.N.D.A : Please check the values again")
                else:
                    conobj.commit()
                    cur.execute("select* from Panda_Counter")
                    r32=cur.fetchall()
                    header11=["Serial No","Flight Number","Airline Name","Origin","Destination","Departure","Arrival"]
                    print(tabulate(r32,headers=header11,tablefmt="grid"))
        elif Choice7.upper()=="EDIT":
            sno1=int(input("Enter serial no. of flight whose value you want to change :"))
            fieldname1=input("Enter field name whose value you want to change :")
            newval=input("Enter new value : ")
            ch1=input("Is your value a time ? ")
            if ch1.upper()=="YES":
                execute26="update Panda_Counter set {}='{}' where Serial_No={}".format(fieldname1,newval,sno1)
                try:
                    cur.execute(execute26)
                except:
                    print("P.A.N.D.A : An unexpected error has occured")
                    print("P.A.N.D.A : Please check the values again")
                else:
                    conobj.commit()
                    cur.execute("select* from Panda_Counter")
                    r33=cur.fetchall()
                    header12=["Serial No","Flight Number","Airline Name","Origin","Destination","Departure","Arrival"]
                    print(tabulate(r33,headers=header12,tablefmt="grid"))
            else:
                execute27="update Panda_Counter set {}='{}' where Serial_No={}".format(fieldname1,newval,sno1)
                try:
                    cur.execute(execute27)
                except:
                    print("P.A.N.D.A : An unexpected error has occured")
                    print("P.A.N.D.A : Please check the values again")
                else:
                    conobj.commit()
                    cur.execute("select* from Panda_Counter")
                    r34=cur.fetchall()
                    header13=["Serial No","Flight Number","Airline Name","Origin","Destination","Departure","Arrival"]
                    print(tabulate(r34,headers=header13,tablefmt="grid"))
        print()
    def SHOW_TABLES():
        #To display all the tables stored in the vault
        cur.execute("show tables")
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
        print("P.A.N.D.A MART : P.A.N.D.A becomes a window into the world of online shopping with its extenisve list of items")
        print("P.A.N.D.A LIST : P.A.N.D.A acts as your personal shopping assistant by creating shopping lists that help you with your everyday shopping ")
        print("P.A.N.D.A REGISTER : P.A.N.D.A tracks your transaction history to keep you updated on your financial activity")
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
            except:
                print("P.A.N.D.A : An unexpected error has occurred.")
                print("P.A.N.D.A : Please try again.")
            finally:
                inp5=input("Do you want to continue using DEVELOPER MODE ? ")
                if inp5.upper()=="YES":
                    continue
                else:
                    print("Exiting DEVELOPER MODE...")
                    return
        print()
    def panda_create():
        ch=input("Enter table name : ")
        execute15="create table if not exists {}(Serial_No varchar(5))".format(ch)
        cur.execute(execute15)
        while True:
            inp1=input("Enter field name (enter 'exit' to exit) : ")
            if inp1.upper()=="EXIT":
                break
            else:
                execute16="alter table {} add({} varchar(50))".format(ch,inp1)
                try:
                    cur.execute(execute16)
                except:
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
                execute17="insert ignore into {} values{}".format(ch,a)
                try:
                    cur.execute(execute17)
                except:
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
        execute19="select* from {} where {}='{}'".format(inp7,field1,val)
        try:
            cur.execute(execute19)
        except:
            print("P.A.N.D.A : An unexpected error has occured")
            print("P.A.N.D.A : Please check the values again")
        else:
            r25=cur.fetchall()
            for i in r25:
                print(i)
        print()
    def SHOW():
        inp8=input("Enter table name")
        execute20="select* from {}".format(inp8)
        try:
            cur.execute(execute20)
        except:
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
        inp10=header_dictionary[inp9]
        try:
            execute21="select* from {} where {}='{}'".format(inp9,field2,val1)
        except:
            print("P.A.N.D.A : An unexpected error has occured")
            print("P.A.N.D.A : Please check the values again")
        else:
            cur.execute(execute21)
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
    header_mart=["Items","Quantity","Price"]
    header_list=["Serial No.","Items","Price","Remark"]
    header_register=["Serial No.","Items","Price"]
    header_counter=["Serial No","Flight Number","Airline Name","Origin","Destination","Departure","Arrival"]
    header_dictionary={"Emergency":header_emergency,"Medicine":header_medicine,"Panda_Mart":header_mart,"Student_Marks":header_exam,"Shopping_List":header_list,"Transaction_History":header_register,"Panda_Counter":header_counter}
    #Prints the table based on input
    while True:
        Choice=input("What do you want to access ( DATABASES | EDIT | MODE | SHOW | SEARCH | HELP )?")
        if "PANDA CARE" in Choice.upper():
            Emergency()
            print()
        elif "PANDA PHARMACY" in Choice.upper():
            Medicine()
            print()
        elif "PANDA MART" in Choice.upper():
            PANDA_Mart()
            print()
        elif "PANDA MARKSHEET" in Choice.upper():
            MARKSHEET()
            print()
        elif "PANDA LIST" in Choice.upper():
            SHOPPING_LIST()
            print()
        elif "PANDA REGISTER" in Choice.upper():
            TRANSACTION_HISTORY()
            print()
        elif "PANDA COUNTER" in Choice.upper():
            PANDA_COUNTER()
            print()
        elif "EDIT" in Choice.upper():
            #Executes series of functions to edit the tables
            n=0
            while n<3:
                p = input("Enter the password : ")
                f = open('password.txt', 'r')
                s = f.read()
                if s == p :
                    Choice1=input("Which Table do you want to edit?")
                    if "PANDA CARE" in Choice1.upper():
                        EDIT_EMERGENCY()
                        print()
                        break
                    elif "PANDA PHARMACY" in Choice1.upper():
                        EDIT_MEDICINE()
                        print()
                        break
                    elif "PANDA MART" in Choice1.upper():
                        EDIT_MART()
                        print()
                        break
                    elif "PANDA MARKSHEET" in Choice1.upper():
                        EDIT_MARKSHEET()
                        print()
                        break
                    elif "PANDA LIST" in Choice1.upper():
                        EDIT_LIST()
                        print()
                        break
                    elif "PANDA COUNTER" in Choice1.upper():
                        EDIT_COUNTER()
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

