from flask import Flask,flash, render_template, request,redirect,url_for,session
import datetime
import database as DB




def looger(usr,msg,timestamp):
    
    with open("looger.txt",'a+') as f:
        f.writelines(f"{usr} : {msg} : {timestamp}\n")
        
def logviewer():
    with open("looger.txt",'r+') as f:
        data=f.readlines()
        return data 
    
def id_creater(comp):
                
    id=comp.err.execute(f"SELECT rowid FROM COMPLETED{year}{month} ORDER BY rowid DESC LIMIT 1;")
    l_sno=id.fetchall()
    
    # print("l_sno=",l_sno)
    if(len(l_sno)==0):
        
        l_sno.append([0])
    l_sno=int(l_sno[0][0]+1)
    sno={1:"AA",2:"AB",3:"BB",4:"BC",5:"CC",6:"CD",7:"DD",8:"DE",9:"EE",0:"ZY"}
    enc={1:"Z",2:"X",3:"Y",4:"A",5:"E",6:"G",7:"O",8:"Q",9:"I",10:"J",11:"M",12:"L"}
    nsno=""
    while l_sno>=1:
        temp=l_sno%10
        nsno+=sno.get(temp)
        l_sno//=10
    # print(nsno)
    mon=f"{enc.get(month)}{year}{nsno}"
    return mon
    
def creater(name,email,joined_date,domain,phone,comp):

    comp.err.execute(f"CREATE TABLE IF NOT EXISTS COMPLETED{year}{month} (Email VARCHAR(50) NOT NULL,Name VARCHAR(20) NOT NULL,Phone INTEGER(12) NOT NULL,Domain VARCHAR(20) NOT NULL,JOINED VARCHAR(10) NOT NULL,COMPLETED VARCHAR(10) NOT NULL,CERTIFICATEID  VARCHAR(20) PRIMARY KEY)")
    data=[f"{email}",f"{name}",f"{phone}",f"{domain}",f"{joined_date.replace(')','')}",f"'{date.strftime('%d-%m-%Y')}'",f"'{id_creater(comp)}'"]
    # print(data)
    comp.insert(f"COMPLETED{year}{month}",*data,parameters="(Email VARCHAR(50) NOT NULL,Name VARCHAR(20) NOT NULL,Phone INTEGER(12) NOT NULL,Domain VARCHAR(20) NOT NULL,JOINED VARCHAR(10) NOT NULL,COMPLETED VARCHAR(10) NOT NULL,CERTIFICATEID  VARCHAR(20) PRIMARY KEY)")
    return "Data Inserted Successfully"
            


date=datetime.datetime.now()
year=date.year
month=date.month
# print(month)
app = Flask(__name__)
app.secret_key="ajksdhjasgduiqwdgsui"

@app.route('/',methods=['POST','GET'])
def home():
    session.pop("uname",None)
    session.pop("pass",None)
    if request.method=="POST":
        
        uname=request.form.get('username')
        upass=request.form.get('pass')
        
        if uname=="" and upass=="":
            return render_template("index.html")
        elif (uname=="Admin" and upass=="admin"):
            session["uname"]=uname
            session["pass"]=upass
            timestap=date.strftime("%d-%m-%Y %H:%M:%S")
            looger(uname,"Looged in",timestap)
            flash("Login Successfully")
            return redirect(url_for('main'))
        else:
            
            return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/month_data/<DATE>',methods=["GET","POST"])
def month_DATA(DATE):
    if ("uname" and "pass") in session:
        db=DB.database(f"database{DATE[0:4]}")
        if request.method=="POST":
            phone=request.form.get("entered_data")
            
            if phone=="":
                data1=db.show(f"registered{DATE}")
                
               
                
                return render_template('registration.html',data=data1)
                
            else:
                data1=db.get_data(f"registered{DATE}","phone",phone) 
                
                return render_template('registration.html',data=data1)
                
        
        data1=db.show(f"registered{DATE}")   
        
        
        return render_template('registration.html',data=data1)
    return redirect(url_for("home"))


@app.route('/home',methods=["POST",'GET'])
def main():
    if ("uname" and "pass") in session:
        
        if request.method=="POST":
            DATE=request.form.get("date")
            DATE=DATE.replace("-","")
           
            
            return redirect(url_for("month_DATA",DATE=DATE ))
        else: 
            data=logviewer()   
            return render_template("home.html",data=data)
    return redirect(url_for("home"))

@app.route(f"/registerd/month={month}",methods=["POST","GET"])
def registrations():
    db=DB.database('database')
    if ("uname" and "pass") in session:
        
        if request.method=="POST":
            phone=request.form.get("entered_data")
            
            if phone=="":
                data1=db.show(f"registered{year}{month}")
                
                return render_template('registration.html',data=data1)
                
            else:
                data1=db.get_data(f"registered{year}{month}","phone",phone) 
                
                return render_template('registration.html',data=data1)
                
        
        data1=db.show(f"registered{year}{month}")   
        
        
        return render_template('registration.html',data=data1)
    
        
    return redirect(url_for("home"))




@app.route('/new registration',methods=["POST","GET"])
def add_data():
    if ("uname" and "pass") in session:
        if request.method == 'POST':
            file=request.form.get('file')
            date=request.form.get('date')
            # print(date)
            DB.insert_many(file,date)
            Date=datetime.datetime.now()
            timestap=Date.strftime("%d-%m-%Y %H:%M:%S")
            looger(session.get('uname'),"Added new data",timestap)
            

            return redirect(url_for('month_DATA',DATE=date.replace('-','')))

        return render_template('new_registration.html')
    return redirect(url_for("home"))

@app.route(f'/completed/{year}{month}',methods=["POST","GET"])
def create():
    if ("uname" and "pass") in session:
        if request.method == 'POST':
            comp=DB.database(f'CERTIFICATES{year}')
            # creater(name,email,joined_date,domain,phone):
            table=request.form.getlist('done')
            data1=comp.show(f"COMPLETED{year}{month}") 
            print(data1)
            
            for ele in table:
                ele=ele.split(',')
                creater(ele[2],ele[1],ele[9],ele[8],ele[4],comp)
            return render_template('Completed.html',data=data1)
            

    return redirect(url_for("home"))

@app.route('/error')
def error_page():
    return render_template("error_page.html")

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)