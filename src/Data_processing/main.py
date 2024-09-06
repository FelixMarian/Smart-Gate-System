from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
import time
import os

import GetLicencePlate
import dataBase
import serialCommunication

# Delete the previously processed image to make room for a new one
def delete_photo():
    filenameToDelete = GetLicencePlate.find_png_file()
    try:
        os.remove(filenameToDelete)
    except Exception as e:
        return None

def updatePhoto_n_Plate(carPhotoLabel, labelActualLicence):
    newCarArrived = serialCommunication.getArduinoData()

    # If we receive the 'K' signal (indicating a new car has arrived), update the display
    if newCarArrived == 'K':
        delete_photo()
        # Wait 10 seconds to allow the photo to be processed and saved
        time.sleep(10)
        filename = GetLicencePlate.find_png_file()
        # Update the car image
        carPixmap = QPixmap(filename)
        carPixmap = carPixmap.scaled(200, 150, 1)
        carPhotoLabel.setPixmap(carPixmap)
  
        # Update the license plate number
        extractedLicencePlate = GetLicencePlate.getLicencePlate()
        labelActualLicence.setText(extractedLicencePlate)
        dataBase.processLicencePlate(extractedLicencePlate)

        # Send a message to Arduino indicating the process is complete
        serialCommunication.sendMessage()

def main():
    # Initialize the application and main window
    app = QApplication([])
    mainWindow = QWidget()
    mainWindow.setGeometry(100, 100, 350, 150)
    mainWindow.setWindowTitle("GateProject")
 
    # Create a horizontal layout
    mainLayout = QHBoxLayout()
 
    # Load and scale the car image
    carPhotoLabel = QLabel()
    carPhotoLabel.setFixedSize(200, 150)

    # Create a vertical layout for displaying the license plate number
    carPlateLayout = QVBoxLayout()

    # Add spacers at the top and bottom to center the license plate label
    upperSpacer = QSpacerItem(50, 50)
    carPlateLayout.addItem(upperSpacer)
  
    # Label that shows "License plate" and below it, the actual extracted plate number
    labelLicPlate = QLabel()
    labelLicPlate.setText("License plate:")
    labelLicPlate.setFont(QFont("Arial", 12))
 
    labelActualLicence = QLabel()
    labelActualLicence.setFont(QFont("Arial", 16))

    carPlateLayout.addWidget(labelLicPlate)
    carPlateLayout.addWidget(labelActualLicence)
 
    downSpacer = QSpacerItem(50, 50)
    carPlateLayout.addItem(downSpacer)
 
    # Call the function to update the license plate number and photo
    updatePhoto_n_Plate(carPhotoLabel, labelActualLicence)

    # Re-call the update function every 3 seconds to check if there's a new image or not
    timer = QTimer()
    timer.timeout.connect(lambda: updatePhoto_n_Plate(carPhotoLabel, labelActualLicence))
    timer.start(3000)

    mainLayout.addWidget(carPhotoLabel)
    mainLayout.addLayout(carPlateLayout)
    mainWindow.setLayout(mainLayout)
 
    mainWindow.show()
    app.exec_()

if __name__ == "__main__":
    main()
