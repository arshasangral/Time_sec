from flask import Flask, redirect,url_for
from flask import render_template,request
import mysql.connector
import datetime
import random



mydb = mysql.connector.connect(user="arsha", passwd="1234", host="localhost",auth_plugin='mysql_native_password',database ='timdatabase')

cursor = mydb.cursor()

timeList = [datetime.timedelta(hours=7),
                        datetime.timedelta(hours=10),
                        datetime.timedelta(hours=14)]

def get_total_hours(row):   
    hours = row[1]//row[0]
    add = row[1]%row[0]
    total_hours = [hours]*row[0]
    count = 1
    if add!=0:
        for j in range(len(total_hours)):
            if count <=add:
                total_hours[j]+=1
                count+=1

    return total_hours            

def get_authenticate(email,password):
    cursor.execute(f"select pass_word from entry where email ='{email}'")
    data = cursor.fetchall()
    if len(data)==0:
        return False
  
    # extract pasword from pass_wrd
    return password == data[0][0]



def get_name(email):
    cursor.execute(f"select Employee_name from entry where email = '{email}'")
    name = cursor.fetchall()
    return name[0][0]



def get_schedule_list(email):

    cursor.execute(f"select Days_at_work, Num_of_hours from entry where email = '{email}'")
                    
    for i in cursor:
        divided_hours = get_total_hours(i)
                    

    lst = [] 
            

    for hour in divided_hours:
                    time = random.choice(timeList)
                    deltatime = datetime.timedelta(hours=hour)
                    d = datetime.datetime.strptime(str(time),"%H:%M:%S")
                    new_time = d.strftime("%I:%M %p")
                    sum = time + deltatime
                    dd = datetime.datetime.strptime(str(sum),"%H:%M:%S")
                    new_sum = dd.strftime("%I:%M %p")
                    
                    lst.append((new_time +" "+ "-" +" "+ new_sum))

    new_lst = ['not scheduled']*7
    for i in range(len(lst)):
                new_lst[i]=lst[i] 


    return new_lst            


app = Flask(__name__)


@app.route('/')
def home():
  return render_template('form.html') 

@app.route('/redirected')
def redirected():
    return render_template('sec.html')

@app.route('/authenticate',methods = ["POST","GET"])
def open():
    if request.method =="POST":
        email = request.form['uname']
        password= request.form['psw']


        authenticate = get_authenticate(email,password)


        if authenticate==False:
            return redirect(url_for('redirected'))
        
        else:    

            sec_lst = get_schedule_list(email)
            name = get_name(email)      
            
            return render_template('display.html',value = name ,value1 =sec_lst [0],value2 = sec_lst [1],value3 = sec_lst [2],value4 =sec_lst [3],value5 =sec_lst [4],value6 =sec_lst [5],value7 =sec_lst [6])

@app.route('/signup', methods = ["POST","GET"])
def signup():
    if request.method =="POST":
        return render_template('signup.html')

@app.route('/add',methods =['POST','GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        sur_name = request.form['sname']
        user_email = request.form['uname']
        user_pass = request.form['psw']
        work_hours = request.form['hname']
        work_days = request.form['wname']


    sql = "INSERT into entry (Employee_name,sur_name,Email,Days_at_work,Num_of_hours,pass_word) values(%s,%s,%s,%s,%s,%s)"   
    cursor.execute(sql,(name,sur_name,user_email,work_days,work_hours,user_pass))  

    mydb.commit()   

    return('<h2> form submitted succesfully</h2>')




if __name__ == "__main__":
    app.run()