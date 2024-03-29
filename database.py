import sqlite3 as sq
import os
import datetime
import firebase_admin
from firebase_admin import credentials,db

date=datetime.datetime.now()
year=date.year
month=date.month
day=date.day

class database:
    
    def __init__(self,database_name):
        cwd=os.getcwd()
        self.conn = sq.connect(f'{cwd}/database/{database_name}.db')
        self.err = self.conn.cursor()
        
    def create(self,table_name):
        try:
            self.err.execute('CREATE TABLE IF NOT EXISTS '+table_name+" (Email VARCHAR(50) NOT NULL,Name VARCHAR(20) NOT NULL,Age INTEGER(3) NOT NULL,Phone INTEGER(12) NOT NULL,Year INTEGER(4) ,BRANCH VARCHAR(10) ,College VARCHAR(40) ,DOMAIN VARCHAR(20) NOT NULL,JOINED VARCHAR(10))")
            self.conn.commit()
            return table_name
        except Exception as e:
            return e
        
  
           
    def insert(self,table_name,*value,parameters="(Email VARCHAR(50) NOT NULL,Name VARCHAR(20) NOT NULL,Age INTEGER(3) NOT NULL,Phone INTEGER(12) NOT NULL,Year INTEGER(4) ,BRANCH VARCHAR(10) ,College VARCHAR(40) ,DOMAIN VARCHAR(20) NOT NULL,JOINED VARCHAR(10)"):
        try:
            self.err.execute('CREATE TABLE IF NOT EXISTS '+table_name+parameters)
            self.err.execute(f"INSERT INTO {table_name} VALUES({','.join(value)})")
            self.conn.commit()
            return "Data Inserted Successfully"
        except Exception as e:
            return e
    
    # TODO: Cretae a delete function 

    def get_data(self,table_name,value,column):
        try:
            data=self.err.execute(f"SELECT rowid,* FROM {table_name} where {column} = {value}")
            return data.fetchall()
        except Exception as e:
            return e
        
    #TODO: No update function required
    def update(self,table_name,value,column):
        try:
            data=self.err.execute(f"UPDATE {table_name} SET {column} = {value}")
            return data.fetchall()
        except Exception as e:
            return e
    
       
    def show(self,table_name):
        
        try:
            table=self.create(f"{table_name}")
            # print(table)
            if table:
                table_name=table
            
            data=self.err.execute(f"SELECT rowid,* FROM {table_name}")
            return data.fetchall()
        except Exception as e:
            return e

class insert_many:
    
    def __init__(self,file,DATE):
        try:
        
            DB=database(f"database{DATE.split('-')[0]}")

            bdb=database(f"warehouse/database{DATE.split('-')[0]}")
            temp=[]   
            with open(f"{file}",'r+') as file:
            
                for line in file.readlines():
                    temp.append(line.split(','))

            for ele in temp:
                temp1=[]
                for el in ele:
                    string1=f"'{el}'"
                    temp1.append(string1)
                datej=f"{str(day)}/{str(month)}/{str(year)}"
                print(datej)
                temp1.append(datej)
                # print(f"{day}/{month}/{year}")
                print(DB.insert(f"registered{DATE.replace('-', '')}",*temp1))
                bdb.insert(f"registered{DATE.replace('-', '')}",*temp1)
                # print(temp1)
        except Exception as e:
            print(e)

class online_db:
    def __init__(self,year):
        # add a cred.json file in folder to connect to your firebase
        #  modify this data as required
        cred = credentials.Certificate("cred.json")
        app=firebase_admin.initialize_app(cred,{'databaseURL':'https://interno-404-default-rtdb.asia-southeast1.firebasedatabase.app/',})
        self.ref=db.reference(f'{year}')
        
    
    def insert(self,month,**data):
        try:
            self.ref=self.ref.child(f'{month}')
            user_ref=self.ref.child(data.get('id'))
            u_data={
                'name':data.get('name'),
                'domain':data.get('domain'),
                'email':data.get('email'),
                'joined_date':data.get('joined_date'),
                'complted_date':data.get('complted_date')
            }
            user_ref.set(u_data)
            return "Data Inserted Successfully"
        except Exception as e:
            return e
        
    def search(self,year,month,id):
        try:
            ref=db.reference(f'{year}/{month}')
            user_ref=ref.child(id)
            return user_ref.get()
        except Exception as e:
            return e


