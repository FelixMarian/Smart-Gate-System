#ifndef SONICSENSOR_H
#define SONICSENSOR_H

// PORTB pins configuration for ultrasonic sensor
// PB3 is used for trigger signal
// PB1 is used for echo signal

void set_pin_OUTPUT_pB(int pin) {
  if (pin == 50) DDRB |= (1 << PB3);  // Set PB3 (pin 50) as output
}

void set_pin_INPUT_pB(int pin) {
  if (pin == 52) DDRB &= ~(1 << PB1);  // Set PB1 (pin 52) as input
}

void write_HIGH_pB(int pin) {
  if (pin == 50) PORTB |= (1 << PB3);  // Set PB3 (pin 50) to HIGH
}

void write_LOW_pB(int pin) {
  if (pin == 50) PORTB &= ~(1 << PB3);  // Set PB3 (pin 50) to LOW
}

int read_INPUT_value_pB(int pin) {
  if (pin == 52) return PINB & (1 << PB1);  // Return the value of PB1 (pin 52)
}

// SonicSensor class for managing ultrasonic sensor functionality
class SonicSensor {
private:
  int triggerPin;  
  int echoPin;   

public:
  // Constructor to initialize pins
  SonicSensor(int trig, int ech) {
    triggerPin = trig;
    echoPin = ech;
    set_pin_OUTPUT_pB(triggerPin);  
    set_pin_INPUT_pB(echoPin);      
    write_LOW_pB(triggerPin);      
  }

  int getDistance() {
    // Send a pulse on the trigger pin
    write_LOW_pB(triggerPin);
    delayMicroseconds(2);
    write_HIGH_pB(triggerPin);
    delayMicroseconds(10);
    write_LOW_pB(triggerPin);

    // Measure the pulse duration on the echo pin
    long duration = pulseIn(echoPin, HIGH);

    // Calculate and return distance in centimeters
    int distance = (duration / 2.0) * 0.0343;  // Speed of sound is 0.0343 cm/µs

    // Check if the distance is within the valid range
    if (distance >= 2 && distance <= 450) {
      return distance;
    } else {
      return -1;  // Return -1 if distance is out of range
    }
  }
};
#endif
