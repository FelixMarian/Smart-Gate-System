#ifndef SERVO_H
#define SERVO_H

#include <Servo.h>

class ServoM {
private:
  Servo myServo;  
  int pin;     

public:
  // Constructor to initialize pin
  ServoM(int pin_c) {
    pin = pin_c;
  }

  // Attach the servo to the specified pin
  void begin() {
    myServo.attach(pin);
  }

  // Open the gate by setting the servo to 0 degrees
  void openGate() {
    myServo.write(0); 
  }

  // Close the gate by setting the servo to 80 degrees
  void closeGate() {
    myServo.write(80); 
  }
};

#endif
