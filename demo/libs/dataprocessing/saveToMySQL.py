import mysql.connector
from mysql.connector import Error
import os
import urlparse
from sys import argv

dbName = None
conn = None
cursor = None

def connect():
    """ Connect to MySQL database """
    global dbName
    global conn
    global cursor

    #Get MySQL Auth from Heroku ClearDB url
    urlparse.uses_netloc.append('mysql')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])

    dbName = url.path[1:]
    try:
        conn = mysql.connector.connect(host=url.hostname,
                                       port='3306',
                                       database=url.path[1:],
                                       user=url.username,
                                       password=url.password)
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()
            #getAllLoginAccounts()
            createRecordsTable()
            saveRecordsIntoTable(1001, 100) #maxNuRecords=1001, batchSize=100
    except Error as e:
        print(e)
    finally:
        conn.close()

def getAllLoginAccounts():
    queryStr = "SELECT * FROM " + dbName + ".demo_account"
    cursor.execute(queryStr)
    for row in cursor.fetchall() :
        print str(row[0])+" : "+str(row[1])+" : "+str(row[2])

def createRecordsTable():
    cursor.execute("DROP TABLE IF EXISTS " + dbName + ".demo_record")
    creatTableQueryStr = "CREATE TABLE IF NOT EXISTS " + dbName + ".demo_record(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
            +"hack_license VARCHAR(255),"\
            +"pickup_datetime DATETIME,"\
            +"dropoff_datetime DATETIME,"\
            +"passenger_count INT,"\
            +"trip_distance FLOAT,"\
            +"pickup_longitude FLOAT,"\
            +"pickup_latitude FLOAT,"\
            +"dropoff_longitude FLOAT,"\
            +"dropoff_latitude FLOAT"\
            +")"
    cursor.execute(creatTableQueryStr)
    print "created records table: " + dbName + ".demo_record"

def saveRecordsIntoTable(maxNuRecords, batchSize):
    tripDataFilePath = argv
    lineNum = 0
    batchRecords = []

    f = open(tripDataFilePath[1])

    for line in iter(f):
        #print line
        lineNum += 1
        if (lineNum == 1):
            continue
        if (lineNum >maxNuRecords):
            break
        lineAry = line.replace("\r\n","").split(",")
        #print lineAry
        batchRecords.append((lineAry[1],lineAry[5],lineAry[6],lineAry[7],lineAry[9],lineAry[10],lineAry[11],lineAry[12],lineAry[13]))
        if (lineNum % batchSize ==1):
            cursor.executemany("INSERT INTO "+ dbName + ".demo_record"\
                               +"(hack_license,pickup_datetime,dropoff_datetime,passenger_count,trip_distance,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude)"\
                               +"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                               ,batchRecords)
            print ">Sub: saved "+ str(batchSize) +" records into MySQL"
            batchRecords = []

    conn.commit()
    print ">>All: totally saved "+ str(maxNuRecords-1) +" records into MySQL"
    f.close()

if __name__ == '__main__':
    connect()
    cursor.close()
    conn.close()

