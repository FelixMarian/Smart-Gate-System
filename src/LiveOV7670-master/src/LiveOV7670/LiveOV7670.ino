




// change setup.h to switch between buffered and pixel-by-pixel processing
#include "setup.h"
#include <SoftwareSerial.h>

SoftwareSerial SerialUART(8, 9);

void setup() {
  // This is not necessary and has no effect for ATMEGA based Arduinos.
  // WAVGAT Nano has slower clock rate by default. We want to reset it to maximum speed
  CLKPR = 0x80;  // enter clock rate change mode
  CLKPR = 0;     // set prescaler to 0. WAVGAT MCU has it 3 by default.
  SerialUART.begin(19200);
  //Serial.begin(9600);
  initializeScreenAndCamera();
}


void loop() {
  if (SerialUART.available()) {
    char answer = SerialUART.read();
    if (answer == 'K')
      processFrame();
  }
}
