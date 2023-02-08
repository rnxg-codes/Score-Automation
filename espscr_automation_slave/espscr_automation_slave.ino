#include "painlessMesh.h"
#include <Arduino_JSON.h>
#define   MESH_PREFIX     "RNTMESH" 
#define   MESH_PASSWORD   "MESHpassword" 
#define   MESH_PORT       5555 

#define D4 
int nodeNumber = 2;
String readings;
int first,second,third;

Scheduler userScheduler;
painlessMesh  mesh;
void sendMessage() ;
String getReadings(); 
Task taskSendMessage(TASK_SECOND * 5 , TASK_FOREVER, &sendMessage);

String getReadings () {
  JSONVar jsonReadings;
  jsonReadings["1"] = first;
  jsonReadings["2"] = second;
  jsonReadings["3"] = third;
  readings = JSON.stringify(jsonReadings);
  return readings;
}

void sendMessage () {
  first = second = third = 0;
 if(digitalRead(4)==HIGH)
 first = 10 ;
 if(digitalRead(5)==HIGH)
 second = 10; 
 if(digitalRead(21)==LOW)
third = 10 ; 
   String msg = getReadings();
  mesh.sendBroadcast(msg);  
}
void receivedCallback( uint32_t from, String &msg ) {

  JSONVar myObject = JSON.parse(msg.c_str());
  String rst = myObject["rst"]; 
  Serial.print("rst");
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
  pinMode(4,INPUT);
  pinMode(5,INPUT);
  pinMode(21,INPUT);
  

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