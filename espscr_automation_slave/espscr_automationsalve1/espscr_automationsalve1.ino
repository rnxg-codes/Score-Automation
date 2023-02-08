#include "painlessMesh.h"
#include <Arduino_JSON.h>
#define   MESH_PREFIX     "RNTMESH" 
#define   MESH_PASSWORD   "MESHpassword" 
#define   MESH_PORT       5555 
#define p1 2
#define p2 4
#define p3 7
int rst;
String readings;
int first,second,third;

Scheduler userScheduler;
painlessMesh  mesh;
void sendMessage() ;
String getReadings(); 
Task taskSendMessage(TASK_SECOND * 5 , TASK_FOREVER, &sendMessage);

String getReadings () {
  JSONVar jsonReadings;
  jsonReadings["Checkpoint1"] = first;
  jsonReadings["Checkpoint2"] = second;
  jsonReadings["Checkpoint3"] = third;
  readings = JSON.stringify(jsonReadings);
  return readings;
}

void sendMessage () {
  
 if(digitalRead(p1)==LOW)
 first = 1 ;
 if(digitalRead(p2)==LOW)
 second = 1; 
 if(digitalRead(p3)==LOW)
third = 1 ; 
   String msg = getReadings();
  mesh.sendBroadcast(msg);  
}
void receivedCallback( uint32_t from, String &msg ) {

  JSONVar myObject = JSON.parse(msg.c_str());
  int rst = myObject["rst"]; 
  Serial.print("rst :");
  Serial.println(rst);
}

void newConnectionCallback(uint32_t nodeId) {
  Serial.printf("New Connection, nodeId = %u\n", nodeId);

}

void changedConnectionCallback() {
  Serial.printf("Changed connections\n");
}

void nodeTimeAdjustedCallback(int32_t offset) {
  Serial.printf("Adjusted time %u. Offset = %d\n", mesh.getNodeTime(),offset);
}

void setup() {
  Serial.begin(115200);
  pinMode(p1,INPUT_PULLUP);
  pinMode(p2,INPUT_PULLUP);
  pinMode(p3,INPUT_PULLUP);
  

  //mesh.setDebugMsgTypes( ERROR | MESH_STATUS | CONNECTION | SYNC | COMMUNICATION | GENERAL | MSG_TYPES | REMOTE ); // all types on
  mesh.setDebugMsgTypes( ERROR | STARTUP );  // set before init() so that you can see startup messages

  mesh.init( MESH_PREFIX, MESH_PASSWORD, &userScheduler, MESH_PORT );
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);

  userScheduler.addTask(taskSendMessage);
  taskSendMessage.enable();
}

void loop() {
  // it will run the user scheduler as well
  mesh.update();
}