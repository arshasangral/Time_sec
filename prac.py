from flask import Flask
from flask import render_template,request
import mysql.connector
import datetime
import random



mydb = mysql.connector.connect(user="arsha", passwd="1234", host="localhost",auth_plugin='mysql_native_password',database ='timdatabase')

cursor = mydb.cursor()

cursor.execute("select Days_at_work from entry where email='ar@gmail.com' and pass_word='arsha3     '")

lst = [1,2,3,4] 
new_lst = ['null']*7
for i in range(len(lst)):
    new_lst[i]=lst[i]

print(new_lst)    
