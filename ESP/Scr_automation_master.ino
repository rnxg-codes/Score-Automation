#include "painlessMesh.h"
#include <Arduino_JSON.h>
#include <string>
#define   MESH_PREFIX     "RNTMESH" 
#define   MESH_PASSWORD   "MESHpassword" 
#define   MESH_PORT       5555 


String readings;
int rst ;
Scheduler userScheduler;
painlessMesh  mesh;

void sendMessage() ;
String getReadings();
Task taskSendMessage(TASK_SECOND * 1 , TASK_FOREVER, &sendMessage);

String getReadings () {
  JSONVar jsonReadings;
  jsonReadings["rst"] = rst;
  readings = JSON.stringify(jsonReadings);
  return readings;
}

void sendMessage () {
while(Serial.available())
{
rst = Serial.read();
}
  String msg = getReadings();
  mesh.sendBroadcast(msg);
  rst = 0 ;
}

void receivedCallback( uint32_t from, String &msg ) {
  
  JSONVar myObject = JSON.parse(msg.c_str());
 
  Serial.println(myObject);

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
  mesh.update();
}