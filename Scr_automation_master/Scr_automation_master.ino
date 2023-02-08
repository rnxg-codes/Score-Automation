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
Task taskSendMessage(TASK_SECOND * 5 , TASK_FOREVER, &sendMessage);

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
  // Serial.printf("Received from %u msg=%s\n", from, msg.c_str());
  JSONVar myObject = JSON.parse(msg.c_str());
  int E1a = myObject["Checkpoint1"];
  int E1b = myObject["Checkpoint2"];
  int E1c = myObject["Checkpoint3"];
  int E2a = myObject["Checkpoint4"];
  int E2b = myObject["Checkpoint5"];
  int E2c = myObject["Checkpoint6"];
  int E3a = myObject["Checkpoint7"];
  int E3b = myObject["Checkpoint8"];
  int E3c = myObject["Checkpoint9"];
  int E4a = myObject["Checkpoint10"];
  int E4b = myObject["Checkpoint11"];
  int E4c = myObject["Checkpoint12"];
  Serial.println(myObject);
/*  Serial.print(E1b);
  Serial.print(E1c);
  Serial.print(E2a);
  Serial.print(E2b);
  Serial.print(E2c);
  Serial.print(E3a);
  Serial.print(E3b);
  Serial.print(E3c);
  Serial.print(E4a);
  Serial.print(E4b);
  Serial.print(E4c);
  Serial.println();
 std::string to_string(E1a);
  String str2 = to_string(E1b);
  String str3 = to_string(E1c);
  String str4 = to_string(E2a);
  String str5 = to_string(E2b);
  String str6 = to_string(E2c);
  String str7 = to_string(E3a);
  String str8 = to_string(E3b);
  String str9 = to_string(E3c);
  String str10 = to_string(E4a);
  String str11= to_string(E4b);
  String str12 = to_string(E4c);
  String str111 = ("Checkpoint 1:");
   String str112 = (" Checkpoint 2:");
    String str113 = (" Checkpoint 3:");
     String str114 = (" Checkpoint 4:");
      String str115 = (" Checkpoint 5:");
       String str116 = (" Checkpoint 6:");
        String str117 = (" Checkpoint 7:");
         String str118 = (" Checkpoint 8:");
          String str119 = (" Checkpoint 9:");
           String str120 = (" Checkpoint 10:");
            String str121 = (" Checkpoint 11:");
 String str122 = (" Checkpoint 12:");
 String data ;
 String data.append(str111);
 data.append(str1);
 data.append(str112);
 data.append(str2);
 data.append(str113);
 data.append(str3);
 data.append(str114);
 data.append(str4);
 data.append(str115);
 data.append(str5);
 data.append(str116);
 data.append(str6);
 data.append(str117);
 data.append(str7);
 data.append(str118);
 data.append(str8);
 data.append(str119);
 data.append(str9);
 data.append(str120);
 data.append(str10);
 data.append(str121);
 data.append(str11);
 data.append(str122);
 data.append(str12);
 Serial.println(data);
       */     
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