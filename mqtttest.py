import paho.mqtt.client as mqtt
import json
import psycopg2


                # Define event callbacks
def on_connect(client, userdata, rc):
    if rc == 0:
          print("Connected successfully.")
    else:
         print("Connection failed. rc= "+str(rc))

def on_publish(client, userdata, mid):
    print("Message "+str(mid)+" published.")
    
def on_subscribe(client, userdata, mid, granted_qos):
     print("Subscribe with mid "+str(mid)+" received.")

def on_message(client, userdata, msg):
    print("Topic: ", msg.topic)
    if (msg.topic)==("/larteyjoshua@gmail.com/test"):
        print(" Pump is ",str(msg.payload.decode("utf-8")))

    if (msg.topic)==("/larteyjoshua@gmail.com/SensorData"):
        print("Sensor Reading update")
        print(str(msg.payload.decode("utf-8")))
        data= json.loads(msg.payload.decode("utf-8"))
        print(data)
       
        print("connecting to DB")
        # con = sqlite3.connect(':memory:') # when db locks
        con = psycopg2.connect("dbname='IotIrrigation' user='postgres' host='localhost' password='12345678'")
        cursor = con.cursor()
        print("connect to DB")   
        
        # print("creating  DB")
        # cursor.execute("CREATE TABLE SensorRecords(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, time TIMESdTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,temperature REAL,water_used REAL,ph REAL,moisture REAL);")
        # cursor.commit()
                                
        # print('...inside create db fxn') 

        # # if not included, creates only DB without any table    
        cursor = con.cursor()

        print('before try...')
        try:
            cursor.execute(""" INSERT INTO SensorRecords( temperature, water_used, ph, moisture) 
                            VALUES (%s, %s, %s, %s) """,
                    (data["temperature"], data["waterused"], data["ph"], data["moisture"]))
            con.commit()
            print("Data posted SUCCESSFULLY")
        except Exception as err:
            print('...posting data FAILED')
            print(err)
            
    
   
mqttclient = mqtt.Client()

                # Assign event callbacks
mqttclient.on_connect = on_connect
mqttclient.on_publish = on_publish
mqttclient.on_subscribe = on_subscribe
mqttclient.on_message = on_message

                # Connect
mqttclient.username_pw_set("larteyjoshua@gmail.com", "7f8a9110")
mqttclient.connect("mqtt.dioty.co", 1883)

                # Start subscription
mqttclient.subscribe("/larteyjoshua@gmail.com/test")
mqttclient.subscribe("/larteyjoshua@gmail.com/SensorData")

mqttclient.subscribe("/larteyjoshua@gmail.com/boardstatus")

           # Publish a message
mqttclient.publish("/larteyjoshua@gmail.com/test", "on")

rc = 0
while rc == 0:
    rc = mqttclient.loop()
print("rc: " + str(rc))

