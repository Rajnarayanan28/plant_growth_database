import mysql.connector
import datetime
from datetime import datetime, timedelta
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

def display_details():
    mycursor.execute("select * from plant_detail A,plant_progress B where A.plant_id = B.plant_id")
    print(Fore.RED+"plant_id |",Fore.BLUE+" plant_name |",Fore.RED+" plant_type |",Fore.BLUE+" watering_schedule |",Fore.RED+" Special_consideration |",Fore.BLUE+" planted_on |",Fore.RED+" plant_id |",Fore.BLUE+" plant_name |",Fore.RED+" current_watering_status |")
    list=[8,16,14,26,31,12,10,12,12]
    l=0
    for rec in mycursor:
        start_date = rec[-1]
        days_to_add = rec[3]
        delta = timedelta(days=days_to_add)
        result_date = start_date + delta  
        #print("Result date after adding days:", result_date)

        # Convert result_date to datetime.datetime object
        result_date = datetime.combine(result_date, datetime.min.time())

        current_date = datetime.now()
        difference = current_date - result_date

        # Access the 'days' attribute of the timedelta object to get the number of days
        number_of_days = difference.days

        #print("Number of days between the two dates:", number_of_days)
        print("|",end="")
        if number_of_days<=0:
            print(Fore.GREEN+"")
        elif number_of_days>0:
            print(Fore.YELLOW+"")
        else:
            pass
        for i in rec:
            lenn=len(str(i))
            if lenn<list[l]:
                if l%2==0:
                    res=list[l]-lenn
                    print("",i," "*res,"|",end='')
                    print(end="")
                    l=l+1
                else:
                    res=list[l]-lenn
                    print("",i," "*res,"|",end='')
                    print(end="")
                    l=l+1  
            else:
                print(i)
                l=l+1
        print()
        l=0
'''
def display_details():
    mycursor.execute("select * from plant_detail A,plant_progress B where A.plant_id = B.plant_id")
    print(Fore.RED + "plant_id |", Fore.BLUE + " plant_name |", Fore.RED + " plant_type |", Fore.BLUE + " watering_schedule |", Fore.RED + " Special_consideration |", Fore.BLUE + " planted_on |", Fore.RED + " plant_id |", Fore.BLUE + " plant_name |", Fore.RED + " current_watering_status |")
    list = [8, 16, 14, 26, 31, 12, 10, 12, 12]
    l = 0
    for rec in mycursor:
        start_date = rec[-1]
        days_to_add = rec[3]
        delta = timedelta(days=days_to_add)
        result_date = start_date + delta  
        print("Result date after adding days:", result_date)

        # Convert result_date to datetime.datetime object
        result_date = datetime.combine(result_date, datetime.min.time())

        current_date = datetime.now()
        difference = current_date - result_date

        # Access the 'days' attribute of the timedelta object to get the number of days
        number_of_days = difference.days

        print("Number of days between the two dates:", number_of_days)        
'''
# Define a starting date
start_date = datetime(2024, 2, 22)

# Define the number of days to add
days_to_add = 5

# Create a timedelta object with the number of days to add
delta = timedelta(days=days_to_add)

# Add the timedelta to the starting date
result_date = start_date + delta

print("Original date:", start_date.date())
print("Result date after adding days:", result_date.date())


display_details()
display_specific_details()