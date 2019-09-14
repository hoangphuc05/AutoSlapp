

def getYear(email):
    if email[-17:] == "@my.whitworth.edu" and email[-19:-17].isdigit():
        return str(20) + email[-19:-17]
    else:
        return 0


#INSERT [dbo].[Student] ([Student_ID], [FirstName], [LastName], [GraduationYear], [Email]) VALUES (146671, N'Brandi', N'Hayes', 2015, N'bhayes15@my.whitworth.edu')
def addStudent(cursor, StudentID, FirstName, LastName, Email):
    if getYear(Email) == -1:
        return 0
    if not StudentID.isdigit():
        return 0
    
   
    cursor.execute("INSERT [dbo].[Student] ([Student_ID], [FirstName], [LastName], [GraduationYear], [Email]) VALUES ("+str(StudentID)+", N'"+str(FirstName)+"', N'"+str(LastName)+"', "+str(getYear(Email))+", N'"+str(Email)+"')")
    cursor.commit()
    return 1

#\s[A-Z][A-Z]+.*[0-9][0-9][0-9]
#\(.+\)

import re
import string
def getNumber(original):
    #print(original)
    result = re.search("\s[A-Z][A-Z]+.*[0-9][0-9][0-9]"," "+original)
    if result:
        className = result.group(0)
        className = className.strip()
        return className
    else:
        return ""
    
def getClassName(original):
    
    result1 = re.sub("\(.+\)", ""," "+original)
    result = re.sub("\s[A-Z][A-Z]+.*[0-9][0-9][0-9]","",result1)
    result = result.strip()
    result= re.sub('^[^a-zA-z]*|[^a-zA-Z]*$','',result)
    result = re.sub(' +', ' ', result)
    if not result:
        return result1
    else:
        return result

#print(getNumber("(SP 19) PY-402 Senior Practicum "))
#print(getClassName("(SP 19) PY-402 Senior Practicum"))