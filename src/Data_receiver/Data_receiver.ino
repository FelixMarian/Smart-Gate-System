#include "SonicSensor.h"
#include "ServoM.h"

bool carArrived = false, photoProcessed = false;  //We save here if the car arrived
unsigned int lastLoopExecution = 0;
SonicSensor sensorCarCame(50, 52);  //Checks if the car has arrived at the gate
ServoM servoGate(8);

void setup() {
  Serial.begin(9600);
  Serial2.begin(19200);
  servoGate.begin();
}

void loop() {
  unsigned int currentMillis = millis();

  // Execute everything at intervals of 500 ms
  if (hasTimePassed(currentMillis, lastLoopExecution, 500)) {
    
    // Check for messages from Serial
    if (Serial.available()) {
      char receivedMessage = Serial.read();
      if (receivedMessage == 'L')
        servoGate.openGate();
    }

    // Check if the car has arrived
    if (!carArrived) {
      int measuredValue = sensorCarCame.getDistance();
      if (measuredValue <= 10 && measuredValue != -1) {
        Serial2.println("K");  // We send 'K' when a car has approached
        Serial.println("K");
        carArrived = true;
      }
    }

    // If the car has arrived, check if it's still there
    if (carArrived) {
      int measuredValue = sensorCarCame.getDistance();

      // If the car has left, close the gate
      if (measuredValue > 10 && measuredValue != -1) {
        carArrived = false;
        servoGate.closeGate();  // Close the gate after the car leaves
      }
    }
  }
}

// Function to check if the specified time has passed
int hasTimePassed(unsigned int currentMillis, unsigned int &lastCheck, int time) {
  if (currentMillis - lastCheck >= time) {
    lastCheck = currentMillis;
    return 1;
  }
  return 0;
}
