import mysql.connector
import datetime
from datetime import datetime
now=datetime.now()
current_hour = now.hour
if current_hour < 12:
    print("Good morning!")
elif current_hour < 18:
    print("Good afternoon!")
else:
    print("Good evening!")
print(now.strftime("The Current Time is %Y-%m-%d"))
from colorama import Fore, Back, Style
db = mysql.connector.connect(host='localhost', user='root', password='3372')
mycursor = db.cursor()
try:
    mycursor.execute('create database plant')
except:
    print('...create...')
    print("..")

import mysql.connector
db = mysql.connector.connect(host='localhost', user='root', password='3372', database='plant')
mycursor = db.cursor()


def create():
    try:
        mycursor.execute("create table plant_detail (plant_id varchar(10) Primary key ,plant_name varchar(20),plant_type varchar(20),watering_schedule int,Special_consideration varchar(30),planted_on date)")
        mycursor.execute("create table plant_progress (plant_id varchar(10) Primary key,plant_name varchar(20),current_watering_status date)")
    except:
        print("File exists")
        

def add_dtl():
    plant_id=input()
    plant_name=input()
    plant_type=input()
    watering_schedule=int(input())
    special_consideration=input()
    planted_on=input("enter value in format yyyy-mm-dd")
    current_watering_status=planted_on
    Days_without_water=0

    try:
        mycursor.execute("insert into plant_detail (plant_id,plant_name,plant_type,watering_schedule,special_consideration,planted_on) values ('{}','{}','{}',{},'{}','{}')".format(plant_id,plant_name,plant_type,watering_schedule,special_consideration,planted_on))
        mycursor.execute("insert into plant_progress (plant_id,plant_name,current_watering_status) values ('{}','{}','{}')".format(plant_id,plant_name,current_watering_status))
        db.commit()
    except:
        print("Error: details not entered")
def display_details():
    mycursor.execute("select * from plant_detail A,plant_progress B where A.plant_id = B.plant_id")
    print(Fore.RED+"plant_id |",Fore.BLUE+" plant_name |",Fore.RED+" plant_type |",Fore.BLUE+" watering_schedule |",Fore.RED+" Special_consideration |",Fore.BLUE+" planted_on |",Fore.RED+" plant_id |",Fore.BLUE+" plant_name |",Fore.RED+" current_watering_status |")
    list=[8,16,14,26,31,12,10,12,12]
    l=0
    for rec in mycursor:
        print(Fore.RED+"|",end="")
        for i in rec:
            lenn=len(str(i))
            if lenn<list[l]:
                if l%2==0:
                    res=list[l]-lenn
                    print(Fore.RED+"",i," "*res,"|",end='')
                    print(Style.RESET_ALL,end="")
                    l=l+1
                else:
                    res=list[l]-lenn
                    print(Fore.BLUE+"",i," "*res,"|",end='')
                    print(Style.RESET_ALL,end="")
                    l=l+1  
            else:
                print(i)
                l=l+1
        print()
        l=0
                
def display_specific_details():
    try:
        i=input("enter choice to check specific")
        mycursor.execute("select * from plant_detail A,plant_progress B where A.plant_id=B.plant_id and A.plant_id = {}".format(i))
        i=mycursor.fetchone()
        print("plant id",i[0])
        print("plant_name",i[1])
        print("plant_type",i[2])
        print("watering_schedule",i[3])
        print("Special_consideration",i[4])
        print("planted_on",i[5])
        print("current_watering_status",i[8])
        print("Days_without_water:-",)
        current_watering_status = datetime.strptime(str(i[8]), "%Y-%m-%d")
        current_date = datetime.now()
        difference = current_date - current_watering_status
        # Extract the number of days from the difference
        result = difference.days
        print(result)
    except:
        print("No Data..")


def water():
    display_details()
    plant_id = input("Enter plant ID to check specific: ")

    mycursor.execute("SELECT * FROM plant_detail A, plant_progress B WHERE A.plant_id=B.plant_id AND A.plant_id = {}".format(plant_id))
    plant_details = mycursor.fetchone()
    print("Plant details:", plant_details)
    
    
    formatted_date = datetime.now().strftime("%Y-%m-%d")
    print("Formatted Date:", formatted_date)
    try:
        mycursor.execute("UPDATE plant_progress SET current_watering_status = %s WHERE plant_id = %s", (formatted_date, plant_id))
        db.commit()
        print("Plant has been watered")
    except Exception as e:
        print("Error has occurred:", e)

def delete_record():
    plant_id=input("enter plant_id")
    try:
        mycursor.execute("DELETE FROM plant_progress WHERE plant_id = %s", (plant_id,))
        db.commit()
        mycursor.execute("DELETE FROM plant_detail WHERE plant_id = %s", (plant_id,))
        db.commit()
        print("Record with plant ID {} deleted successfully.".format(plant_id))
    except Exception as e:
        print("Error occurred while deleting record:", e)


def edit_details():
    display_details()
    plant_id=input("enter plant_id")
    print("select choice : ")
    print("\n1.plant name\n2.plant_type \n3.watering_schedule \n4.special consideration\n")
    i=int(input(":-"))
    if i == 1:
        name=input("enter name")
        try:
            mycursor.execute("UPDATE plant_detail SET plant_name = %s WHERE plant_id = %s", (name, plant_id))
            db.commit()
        except:
            print("error occured")
    elif i == 2:
        plant_type=input("enter plant type")
        try:
            mycursor.execute("UPDATE plant_detail SET plant_type = %s WHERE plant_id = %s", (plant_type, plant_id))
            db.commit()
        except:
            print("error occured")
    elif i == 3:
        watering_schedule=int(input("enter watering schedule"))
        try:
            mycursor.execute("UPDATE plant_detail SET watering_schedule = %s WHERE plant_id = %s", (watering_schedule, plant_id))
            db.commit()
        except:
            print("error occured")
    elif i == 4:
        Special_consideration=input("enter special consideration")
        try:
            mycursor.execute("UPDATE plant_detail SET Special_consideration = %s WHERE plant_id = %s", (Special_consideration, plant_id))
            db.commit()
        except:
            print("error occured")
    else:
        pass
    
com=0
while com!=1:
    print("enter choice :\n1.add_dtl \n2.display_details \n3.display_specific_details \n4.water \n5.delete_record \n6.edit_details \n")
    i=int(input(":-"))
    if i==1:
        add_dtl()
        print()
    elif i==2:
        display_details()
        print()
    elif i==3:
        display_specific_details()
        print()
    elif i==4:
        water()
        print()
    elif i==5:
        delete_record()
        print()
    elif i==6:
        edit_details()
        print()
    else:
        com=1

    
