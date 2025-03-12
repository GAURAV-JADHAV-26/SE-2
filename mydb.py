import mysql.connector

dataBase = mysql.connector.connect(

    host='localhost',
    user = 'root',
    passwd = 'SqL_root@123',
)

cursorObject = dataBase.cursor()

cursorObject.execute('CREATE DATABASE Job_Analyser')
print("DB Created !")

# admin : Admin
# sample : S@mple@143#


# Step1 : view : def something(request): #code      IN views.py
# Step2 : .html
# Step3 : Url : urls.py