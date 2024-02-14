import mysql.connector
import datetime
now=datetime.datetime.now()
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
    print("hello")

import mysql.connector
db = mysql.connector.connect(host='localhost', user='root', password='3372', database='plant')
mycursor = db.cursor()


def create():
    try:
        mycursor.execute("create table plant_detail (plant_id varchar(10) Primary key ,plant_name varchar(20),plant_type varchar(20),watering_schedule int,Special_consideration varchar(30),planted_on date)")
        mycursor.execute("create table plant_progress (plant_id varchar(10) Primary key,plant_name varchar(20),current_watering_status date,Days_without_water int)")
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
        mycursor.execute("insert into plant_progress (plant_id,plant_name,current_watering_status,Days_without_water) values ('{}','{}','{}',{})".format(plant_id,plant_name,current_watering_status,Days_without_water))
        db.commit()
    except:
        print("Error: details not entered")
def display_details():
    mycursor.execute("select * from plant_detail A,plant_progress B where A.plant_id = B.plant_id")
    print(Fore.RED+"plant_id |",Fore.BLUE+" plant_name |",Fore.RED+" plant_type |",Fore.BLUE+" watering_schedule |",Fore.RED+" Special_consideration |",Fore.BLUE+" planted_on |",Fore.RED+" plant_id |",Fore.BLUE+" plant_name |",Fore.RED+" current_watering_status |",Fore.BLUE+" Days_without_water")
    list=[9,11,12,19,23,12,10,12,25,19]
    l=0
    for rec in mycursor:
        print("|",end="")
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
    i=input("enter choice to check specific")
    mycursor.execute("select * from plant_detail A,plant_progress B where A.plant_id = {}".format(i))
    print(Fore.RED+"plant_id |",Fore.BLUE+" plant_name |",Fore.RED+" plant_type |",Fore.BLUE+" watering_schedule |",Fore.RED+" Special_consideration |",Fore.BLUE+" planted_on |",Fore.RED+" plant_id |",Fore.BLUE+" plant_name |",Fore.RED+" current_watering_status |",Fore.BLUE+" Days_without_water")
    list=[9,11,12,19,23,12,10,12,25,19]
    l=0
    for rec in mycursor:
        if rec[0]==i:
            print("|",end="")
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




create()
#add_dtl()
display_details()
display_specific_details()




