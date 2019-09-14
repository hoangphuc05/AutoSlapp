import csv
import pyodbc
from checkID import checkID
from func import getYear

cre = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=SLDatabase;UID='put the UID here';PWD='put the password here'!'
conn = pyodbc.connect(cre)
cursor = conn.cursor()

f = open("new.csv", "r")
csv_reader = csv.reader(f,delimiter=",")

nf = open("new1.csv", "w")
new_writer = csv.writer(nf, delimiter=",")

for row in csv_reader:
    #print(row)
    if getYear(row[2]):
        if not row[3].isdigit():
            cursor.execute("SELECT * FROM dbo.Student where Email='"+str(row[2]+"'"))
            result = cursor.fetchall()
            if len(result) == 0:
                cursor.execute("SELECT * FROM dbo.Student where FirstName='"+str(row[0])+"' and LastName='"+str(row[1])+"'")
                result = cursor.fetchall()
            if len(result) == 0:
                row[3] = checkID(row[0],row[1]," ")
                print(row[3])
                #print(row[0]," ",row[1])
            else:
                row[3] = result[0][0]
                
            new_writer.writerow(row)

        else:
            new_writer.writerow(row)
    else:
        print(row[2])
print("finished")