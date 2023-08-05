#!/usr/bin/env python
# coding: utf-8

# In[29]:
# dev complete and tested. Update the password in dev database
# added the password in codebase in test environment
# test successful and now ready for deployment to Prod.
# production deployed. this is final version
# this is a module makes a connection to a database
import psycopg2 as pgs
import sys
import platform
from requests import get
import platform as os

uname = os.uname()
uname = uname[1]
#print(uname)
try:
    ip = get('https://api.ipify.org').text
except BaseException:
    ip = "127.0.0.1"
    print("couldnt reach internet")
#print ('My public IP address is:', ip)

# connection class - where all functions to connect to a DB are mentioned


class connect:
    # function to create connection
    def create():
        #host_prod = "lykkelle-prod-us-east.postgres.database.azure.com"
        if ip == '213.127.49.192':
            host_prod = "127.0.0.1"
            usr = "postgres"
            mydb = "lykkelledev_db"
            ssl ="disable"
            print("this is connected to main Dev Database")
        elif ip == '20.42.97.74':
            usr = "postgres"
            host_prod = "127.0.0.1"
            mydb = "lykkelle_db"
            ssl = "require"
            print("this is connected to Prod Database")
        elif '138.91.117.218' in ip:
            usr = "postgres"
            host_prod = "127.0.0.1"
            mydb = "lykkelletest_db"
            ssl = "require"
            print("This is connected to release database")
        elif '52.188.202.133' in ip:
            usr = "postgres"
            host_prod = "10.0.0.7"
            mydb = "lykkelletest_db"
            ssl = "require"
            print("This is connected to release database from Web server")
        elif 'LYK' in uname and 'local' in uname:
            host_prod = "127.0.0.1"
            usr = "postgres"
            print("Linking to Dev database as you are not connecting from authorized IPs. Your ip:", ip , "& machine name:",uname)
            mydb = "lykkelledev_db"
            ssl = "disable"
        elif 'LYK' not in uname:
            usr = "postgres"
            host_prod = "10.0.0.6"
            print("CI/CD Build commencing. Your ip:", ip)
            mydb = "lykkelleut_db"
            ssl = "require"
        else:
            host_prod = "127.0.0.1"
            usr = "postgres"
            print("Linking to Dev database as you are not connecting from authorized IPs. Your ip:", ip , "& machine name:",uname)
            mydb = "lykkelledev_db"
            ssl = "disable"
        try:
            conn = pgs.connect(database=mydb,
                               sslmode = ssl,
                               user=usr,
                               host=host_prod,
                               port="5432",
                               password="Debajyoti86")
        except pgs.Error as e:
            print("Unable to connect!")
            print(e.pgerror)
            sys.exit(1)
        conn.autocommit = True
        cursor = conn.cursor()
        set_path = "SET search_path = dbo"
        cursor.execute(set_path)
        # cursor.execute("select version()")
        # record=cursor.fetchone()
        # print("connection successful and you are connected to","\t",record)
        return conn
