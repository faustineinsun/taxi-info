import mysql.connector
from mysql.connector import Error
import os
import urlparse
import redis

dbName = None
conn = None
cursor = None
passengerCountByHour = [None] * 24 

url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

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
        # initialization
        lines = "{\"type\":\"MultiLineString\",\"coordinates\":[" 
        startpoints = "{\"type\":\"MultiPoint\",\"coordinates\":[" 
        endpoints = "{\"type\":\"MultiPoint\",\"coordinates\":[" 
        # query MySQL
        queryStr = "SELECT * FROM " + dbName + ".demo_record WHERE HOUR(pickup_datetime) IN(" + str(hour) +")"
        cursor.execute(queryStr)
        passengerCount = 0
        for row in cursor.fetchall() :
            passengerCount += 1
            #print str(row[4])+" : "+str(row[6])+" : "+str(row[7])+" : "+str(row[8])+" : "+str(row[9])
            lines += "[["+str(row[6])+","+str(row[7])+"],["+str(row[8])+","+str(row[9])+"]],"
            startpoints += "["+str(row[6])+","+str(row[7])+"],"
            endpoints += "["+str(row[8])+","+str(row[9])+"],"
        # save GeoJson to Redis
        lines = lines[:-1] # remove last charater ","
        lines +="]}"
        startpoints = startpoints[:-1]
        startpoints +="]}"
        endpoints = endpoints[:-1]
        endpoints +="]}"
        r.set("geojson:lines:"+str(hour),lines)
        r.set("geojson:startpoints:"+str(hour),startpoints)
        r.set("geojson:endpoints:"+str(hour),endpoints)
        # accumulate passenger count by hour
        passengerCountByHour[hour] = passengerCount
    print r.get("geojson:lines:2")
    print r.get("geojson:startpoints:2")
    print r.get("geojson:endpoints:2")
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

