from func import getYear,addStudent,getClassName,getNumber

import re
import pyodbc
import csv
from collections import defaultdict
profile = defaultdict(list)
notFound = defaultdict(list)

cre = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE='database here';UID='uid here';PWD='password here''
conn = pyodbc.connect(cre)
cursor = conn.cursor()

csv_file = open("new1.csv","r")
csv_reader = csv.reader(csv_file, delimiter=',')

for row in csv_reader:
    if row[2] in profile:
        pass
    else:
        for col in row:
            profile[row[2]].append(col)

for row in profile.values():
    #print(row[2])
    cursor.execute("SELECT * FROM dbo.Student where Email='"+str(row[2]+"'"))
    result = cursor.fetchall()
    if len(result) == 0:
        #print(row[0]," ",row[1]," ", row[2])
        #print(row[3])
        if row[3]:
            cursor.execute("SELECT * FROM dbo.Student where Student_ID="+str(row[3]))
            result2 = cursor.fetchall()
            if len(result2) != 0:
                #print(row[0]," is matched to ", result2)
                pass
            if len(result2) == 0:
                cursor.execute("SELECT * FROM dbo.Student where FirstName='"+str(row[0])+"' and LastName='"+str(row[1])+"'")
                result3 = cursor.fetchall()
                if len(result3) != 0:
                    #print(row[0]," is matched to ", result3)
                    pass
                if len(result3)==0:
                    for data in row:
                        notFound[row[2]].append(data)
                    print("No match found: ",row[0]," ",row[1]," ", row[2]," ",row[3]) 
    else:
        #print(row[0]," ",row[1]," is matched to ", result)
        pass


#addStudent(StudentID, FirstName, LastName, Email):
for student in notFound.values():
    addStudent(cursor, student[3],student[0],student[1],student[2])

#cursor.close()

#add student id to csv file:


    


#All missing profile are added before this, next is to add their hour and class
entries = defaultdict(list)

#this step: Add hour of same entries
#dictionary term:class + need title

#loop through the csv file again
csv_file.seek(0)
for row in csv_reader:
    #check if the dict existed
    #DO NOT ROUND THE NUMBER YET
    term = row[0]+row[1]+row[7]+row[8]
    if term not in entries:
        reResult = re.search("Field.Experience",row[7])
        if reResult:
            entries[term]=[row[3], getClassName(row[7]), getNumber(row[7]), 1,"NULL","Spring",2019,float(row[12]),"NULL",1,0,0,0,'Educational Field Placement']
        else:
            entries[term]=[row[3], getClassName(row[7]), getNumber(row[7]), 1,"NULL","Spring",2019,float(row[12]),"NULL",1,0,0,0,'Pure Service']
    else:
        entries[term][7] += float(row[12])
    if not row[7]:
        #print("No class name found: ", row[0]," ",row[1])
        pass

#round all the number at this step
for keys,data in entries.items():
    data[7] = round(data[7])

uwuu = open("debug.txt","w")
#INSERT [dbo].[Learning_Experience] ([Student_ID], [CourseName], [CourseNumber], [Section], [Professor], [Semester], [Year], [TotalHours], [TypeofLearning], [ConfirmedHours], [LiabilityWaiver], [ProjectAgreement], [TimeLog], [ID]) VALUES (1353269, N'Software Engineering', N'CS 472', N'1', N'Tucker', N'Spring', 2013, 50, N'Problem-Based', 0, 1, 1, 1, 50)
for keys,data in entries.items():
    print(data[7])
    if data[1] and data[2]:
        #print("|",data[1],"|:|",data[2],"|")
        print(data[1])
        if len(data[1]) > 50:
            data[1] = data[1][:49]
        cursor.execute("INSERT [dbo].[Learning_Experience] ([Student_ID], [CourseName], [CourseNumber], [Section], [Professor], [Semester], [Year], [TotalHours], [TypeofLearning], [ConfirmedHours], [LiabilityWaiver], [ProjectAgreement], [TimeLog]) VALUES ("+str(data[0])+", N'"+data[1]+"', N'"+data[2]+"', N'1', N'', N'Spring', 2019, "+str(data[7])+", N'"+data[13]+"', 1, 0, 0, 1)")
        #print("INSERT [dbo].[Learning_Experience] ([Student_ID], [CourseName], [CourseNumber], [Section], [Professor], [Semester], [Year], [TotalHours], [TypeofLearning], [ConfirmedHours], [LiabilityWaiver], [ProjectAgreement], [TimeLog]) VALUES ("+str(data[0])+", N'"+data[1]+"', N'"+data[2]+"', N'1', N'', N'Spring', 2019, "+str(data[7])+", N'', 1, 0, 0, 1)")
        uwuu.write("INSERT [dbo].[Learning_Experience] ([Student_ID], [CourseName], [CourseNumber], [Section], [Professor], [Semester], [Year], [TotalHours], [TypeofLearning], [ConfirmedHours], [LiabilityWaiver], [ProjectAgreement], [TimeLog]) VALUES ("+str(data[0])+", N'"+data[1]+"', N'"+data[2]+"', N'1', N'', N'Spring', 2019, "+str(data[7])+", N'"+data[13]+"', 1, 0, 0, 1)"+"\n")
        cursor.commit()
        #cursor.execute
        pass
    else:
        cursor.execute("INSERT [dbo].[Learning_Experience] ([Student_ID], [CourseName], [CourseNumber], [Section], [Professor], [Semester], [Year], [TotalHours], [TypeofLearning], [ConfirmedHours], [LiabilityWaiver], [ProjectAgreement], [TimeLog]) VALUES ("+str(data[0])+", N'"+data[1]+"', N'"+data[2]+"', N'1', N'', N'Spring', 2019, "+str(data[7])+", N'"+data[13]+"', 1, 0, 0, 1)")
        uwuu.write("INSERT [dbo].[Learning_Experience] ([Student_ID], [CourseName], [CourseNumber], [Section], [Professor], [Semester], [Year], [TotalHours], [TypeofLearning], [ConfirmedHours], [LiabilityWaiver], [ProjectAgreement], [TimeLog]) VALUES ("+str(data[0])+", N'"+data[1]+"', N'"+data[2]+"', N'1', N'', N'Spring', 2019, "+str(data[7])+", N'"+data[13]+"', 1, 0, 0, 1)"+"\n")
        cursor.commit()
        print("added anyway: ",data[0],"|",data[1],"|:|",data[2],"|",data[7])