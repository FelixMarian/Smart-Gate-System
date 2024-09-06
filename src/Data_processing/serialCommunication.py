import serial
import time

# Set the port and baud rate
arduino_port = 'COM8'
baud_rate = 9600 

serial_conn = serial.Serial(arduino_port, baud_rate, timeout=1)

def sendMessage():
    messageToSend = 'L'
    serial_conn.write(messageToSend.encode()) # Send 'L' to indicate "left" to trigger gate opening

def getArduinoData():
    try:
        # Check if there is any data waiting on the serial connection
        if serial_conn.in_waiting > 0:
            # Read the incoming message
            message = serial_conn.read().decode('utf-8').rstrip()
            if message == 'K':
                return 'K'
    except Exception as e:
        print("None")
        return None
