import mysql.connector
from mysql.connector import Error
import os
import urlparse
import redis

dbName = None
conn = None
cursor = None
passengerCountByHour = [None] * 24 

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
            queryMySQLByHourAndGenerateGeoJSON()
    except Error as e:
        print(e)
    finally:
        conn.close()

def queryMySQLByHourAndGenerateGeoJSON():
    for hour in range(0,24):
        queryStr = "SELECT * FROM " + dbName + ".demo_record WHERE HOUR(pickup_datetime) IN(" + str(hour) +")"
        cursor.execute(queryStr)
        passengerCount = 0
        for row in cursor.fetchall() :
            passengerCount += 1
            #print str(row[4])+" : "+str(row[6])+" : "+str(row[7])+" : "+str(row[8])+" : "+str(row[9])
        passengerCountByHour[hour] = passengerCount
    #print passengerCountByHour
    savePassengerCountInfoToRedis()

def savePassengerCountInfoToRedis():
    night = [None]*6
    morning = [None]*6
    afternoon = [None]*6
    evening = [None]*6
    for hour in range(0,24):
        if hour < 6:
            night[hour] = passengerCountByHour[hour]
        elif hour<12 and hour>=6:
            morning[hour-6] = passengerCountByHour[hour]
        elif hour<18 and hour>=12:
            afternoon[hour-12] = passengerCountByHour[hour]
        else:
            evening[hour-18] = passengerCountByHour[hour]
    print passengerCountByHour
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    r = redis.from_url(redis_url)
    r.set("passengercount:night", generateChartData(0,6,night))
    r.set("passengercount:morning", generateChartData(6,6,morning))
    r.set("passengercount:afternoon", generateChartData(12,6,afternoon))
    r.set("passengercount:evening", generateChartData(18,6,evening))
    r.set("passengercount:all", generateChartData(0,24,passengerCountByHour))
    print r.get("passengercount:night")
    print r.get("passengercount:morning")
    print r.get("passengercount:afternoon")
    print r.get("passengercount:evening")
    print r.get("passengercount:all")

def generateChartData(offset,size,ary):
    chartAry = [None]*size*2
    for i in range(0,size*2):
        tuple = [None]*2
        chartIdx = offset 
        if i%2 == 0:
            chartIdx += int(i/2)
        else:
            chartIdx += int(i/2)+1
        tuple[0] = chartIdx 
        tuple[1] = ary[int(i/2)] 
        chartAry[i] = tuple
    return chartAry

if __name__ == '__main__':
    connect()
    cursor.close()
    conn.close()

