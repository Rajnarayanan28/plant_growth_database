import mysql.connector
from colorama import Fore, Back, Style
db = mysql.connector.connect(host='localhost', user='root', password='3372', database='plant')
mycursor = db.cursor()
def print_table(nested_list, column_names):
    num_cols = len(column_names)
    header_row = (
        '| ' 
        + ' | '.join(column_names)
        + ' |'
    )
    nice_horizontal_rule = ('|'+'-' * (len(header_row)-2)+'|')
    print(nice_horizontal_rule)
    print(header_row)
    print(nice_horizontal_rule)
list="plant_id | plant_name | plant_type | watering_schedule | Special_consideration | planted_on | plant_id | plant_name | current_watering_status | Days_without_water"
def display_details():
    mycursor.execute("select * from plant_detail A,plant_progress B where A.plant_id = B.plant_id")
    l=[]
    for i in mycursor:
        l.append(list(i))
    print(l)
    print_table(l,list)

display_details()
#hell yaaaaa
