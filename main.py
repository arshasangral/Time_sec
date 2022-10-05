from flask import Flask
from flask import render_template,request
import mysql.connector
import datetime
import random



mydb = mysql.connector.connect(user="arsha", passwd="1234", host="localhost",auth_plugin='mysql_native_password',database ='timdatabase')

cursor = mydb.cursor()

  

app = Flask(__name__)


@app.route('/')
def home():
  return render_template('form.html') 


@app.route('/open',methods = ["POST","GET"])
def open():
    if request.method =="POST":
        name = request.form['uname']
        surname= request.form['psw']

        cursor.execute(f"select Days_at_work , Num_of_hours from entry where employee_name = '{name}' and sur_name = '{surname}'")

                    
        for i in cursor:
                hours = i[1]//i[0]
                add = i[1]%i[0]
                total_hours = [hours]*i[0]
                count = 1
                if add!=0:
                    for j in range(len(total_hours)):
                        if count <=add:
                            total_hours[j]+=1
                            count+=1

        timeList = [datetime.timedelta(hours=7),
                        datetime.timedelta(hours=10),
                        datetime.timedelta(hours=14)]
        lst = []

        for hour in total_hours:
                time = random.choice(timeList)
                deltatime = datetime.timedelta(hours=hour)
                d = datetime.datetime.strptime(str(time),"%H:%M:%S")
                new_time = d.strftime("%I:%M %p")
                sum = time + deltatime
                dd = datetime.datetime.strptime(str(sum),"%H:%M:%S")
                new_sum = dd.strftime("%I:%M %p")
                
                lst.append((new_time +" "+ "-" +" "+ new_sum))

    return lst




if __name__ == "__main__":
    app.run()