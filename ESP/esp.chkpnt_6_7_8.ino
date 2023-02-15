#include "painlessMesh.h"
#include <Arduino_JSON.h>
#define MESH_PREFIX "RNTMESH"
#define MESH_PASSWORD "MESHpassword"
#define MESH_PORT 5555
#define p1 23
#define p2 22
#define p3 21

int rst;
String readings;
int third, second;
int first;

Scheduler userScheduler;
painlessMesh mesh;
void sendMessage();
String getReadings();
Task taskSendMessage(TASK_SECOND * 0.1, TASK_FOREVER, &sendMessage);

String getReadings() {
  JSONVar jsonReadings;
  jsonReadings["Checkpoint 5"] = first;
  jsonReadings["Checkpoint 6"] = second;
jsonReadings["Checkpoint 7"] = third;
  readings = JSON.stringify(jsonReadings);
  return readings;
}

void sendMessage() {


  String msg = getReadings();
  mesh.sendBroadcast(msg);
     Serial.println(msg);
}
void receivedCallback(uint32_t from, String &msg) {

  JSONVar myObject = JSON.parse(msg.c_str());
  int rst = myObject["rst"];
  Serial.print("rst :");
  Serial.println(rst);
  if (rst == 10)
    ESP.restart();
}

void newConnectionCallback(uint32_t nodeId) {
  Serial.printf("New Connection, nodeId = %u\n", nodeId);
}

void changedConnectionCallback() {
  Serial.printf("Changed connections\n");
}

void nodeTimeAdjustedCallback(int32_t offset) {
  Serial.printf("Adjusted time %u. Offset = %d\n", mesh.getNodeTime(), offset);
}

void setup() {
  Serial.begin(115200);
  pinMode(p1, INPUT_PULLUP);
  pinMode(p2, INPUT_PULLUP);
  pinMode(p3, INPUT_PULLUP);
  first = second = third = 0;

  mesh.setDebugMsgTypes(ERROR | STARTUP);
  mesh.init(MESH_PREFIX, MESH_PASSWORD, &userScheduler, MESH_PORT);
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);
  userScheduler.addTask(taskSendMessage);
  taskSendMessage.enable();
}

void loop() {
  if (digitalRead(p1) == LOW)
    first = 1;
  if (digitalRead(p2) == LOW)
    second = 1;
    if (digitalRead(p3) == LOW)
    third = 1;
  mesh.update();
}