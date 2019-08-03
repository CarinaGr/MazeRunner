"""
This class is the template class for the MQTT client which receives MQTT messages 
and sends MQTT messages
"""
import paho.mqtt.client as mqtt
import time
import array as arr
import os
from MazeSolverAlgoTeamCarina import MazeSolverAlgoTeamCarina

if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1" #lokaler Server

# HINT: it might be a good idea to copy this file into your team folder, e.g. TeamA
# HINT: it might be good idea to rename both the file and the class name
class MazeSolverClient:

    # initialize the MQTT client
    def __init__(self,master):
        
        print("Constructor Team Carina MQTT Client")
        self.master=master

        # HINT: here you should register the onConnect and onMessage callback functions
        #       it might be a good idea to look into file Framework\Test\test_mqtt_publisher.py
        self.master.on_connect=self.onConnect
        self.master.on_message=self.onMessage
        self.master.connect(mqtt_server,1883,60)
        
        # This MQTT client forwards the requests, so you need a link to the solver
        # HINT: don't forget to create your algorithm class here, e.g.
        self.solver = MazeSolverAlgoTeamCarina()

    # Implement MQTT publishing function
    def publish(self, topic, message=None, qos=0, retain=False):
        print("Published message: " , topic , " --> " , message)
        self.master.publish(topic,message,qos,retain)
        # HINT: it might be a good idea to look into file Framework\Test\test_mqtt_publisher.py


    # Implement MQTT receive message function
    def onMessage(self, master, obj, msg):
        # HINT: it might be a good idea to look into file Framework\Test\test_mqtt_subscriber.py
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        print("TeamCarina: Received message:", topic , " --> " , payload)

        if topic=="/maze":
            if payload == "clear":
                self.solver.clearMaze()
            elif payload == "start":
                self.solver.startMaze(0,0)
            elif payload == "solve":
                self.solveMaze()          
            elif payload == "end":
                self.solver.endMaze()
                print("folgende Maze wurde über MQTT empfangen\n")
                self.solver.printMaze()
                
            else:
                pass
        elif topic=="/maze/dimRow":
            self.solver.setDimRows(int(payload))
            self.solver.startMaze(self.solver.dimRows, self.solver.dimColumns)
            
        elif topic=="/maze/dimCol":
            self.solver.setDimCols(int(payload))
            self.solver.startMaze(self.solver.dimRows, self.solver.dimColumns)
            
        elif topic=="/maze/startCol":
            self.solver.setStartCol(int(payload))
            
        elif topic=="/maze/startRow":
            self.solver.setStartRow(int(payload))
        
        elif topic=="/maze/endCol":
            self.solver.setEndCol(int(payload))
            
        elif topic=="/maze/endRow":
            self.solver.setEndRow(int(payload))
            
        elif topic=="/maze/blocked":
            cell = payload.split(",")
            self.solver.setBlocked(int(cell[0]),int(cell[1]))
           
        else:
            pass

    # Implement MQTT onConnecr function
    def onConnect(self, master, obj, flags, rc):
        # HINT: it might be a good idea to look into file Framework\Test\test_mqtt_subscriber.py
        self.master.subscribe("/maze" )
        self.master.subscribe("/maze/dimRow" )
        self.master.subscribe("/maze/dimCol" )
        self.master.subscribe("/maze/startCol" )
        self.master.subscribe("/maze/startRow" )
        self.master.subscribe("/maze/endCol" )
        self.master.subscribe("/maze/endRow" )
        self.master.subscribe("/maze/blocked" )
        print("Connnect to mqtt-broker")
    
    # Initiate the solving process of the maze solver
    def solveMaze(self):
        for step in self.solver.solveMaze():
            step_str = '{},{}'.format(step[0],step[1])
           
            self.publish("/maze/go" , step_str)
        #HINT:  don't forget to publish the results, e.g. 
        #self.publish("/maze/go" , resultString)
     

    
if __name__ == '__main__':
    mqttclient=mqtt.Client()
    #HINT: maybe you rename the MazeSolverAlgoTemplate class ?
    solverClient = MazeSolverClient(mqttclient)
    solverClient.master.loop_forever()
