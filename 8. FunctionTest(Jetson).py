import time
import cv2  
import numpy
import numpy as np
np.bool = np.bool_
import torch
import fastai
from fastai.vision.all import *
import pandas as pd

#Code fixes NotImplementedError: cannot instantiate 'WindowsPath' on your system when load .pkl file in prod environtment
from pathlib import Path
import pathlib
temp = pathlib.PosixPath
pathlib.WindowsPath = pathlib.PosixPath

# Load the model once
learn = load_learner('/home/chidiebere/Documents/ENDG511_Project/v2pruned_plant_classifier.pkl')
# Load the DataLoaders
with open('/home/chidiebere/Documents/ENDG511_Project/v2pruned_dls.pkl', 'rb') as f:
    learn.dls = pickle.load(f)

from fastai.torch_core import default_device

# Set device on the dataloaders
learn.dls.device = default_device()

# Also force the dataloaders to rebuild and assign the correct device to subcomponents
for dl in [learn.dls.train, learn.dls.valid]:
    dl.device = default_device()
    if hasattr(dl.dataset, 'device'):
        dl.dataset.device = default_device()

def capture_and_predict():
    # Initialize webcam (use index 0 for default camera)
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        exit()

    # Capture a single frame from the webcam
    ret, frame = cap.read()

    if ret:
        # Save the captured image
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        img = Image.open(image_path)
        # Close the webcam
        cap.release()

        # Use your model to make a prediction
        pred_class, pred_idx, outputs = learn.predict(image_path)

        print(f"Predicted plant: {pred_class}")

    else:
        print("Error: Failed to capture an image.")
    
    return pred_class, img


def ideal_values(predicted_value):
    # Load the CSV file
    df = pd.read_csv("/home/chidiebere/Documents/ENDG511_Project/ENDG511 Project Temps and Humidity.csv")
    # Find matching row
    matching_row = df[df.iloc[:, 0] == predicted_value]

    if matching_row.empty:
        print(f"[ERROR] No match found for predicted value: {predicted_value}")
        return None, None  # Return something safe

    # Select specific columns (e.g., column 2 and 3)
    selected_columns = matching_row.iloc[:, [3, 6]]

    # Extracting temperature and humidty values
    temp = selected_columns.iloc[0, 0]
    hum = selected_columns.iloc[0, 1]

    return temp, hum

def arduino_function():
    
    ## Insert Code ###
    # Returns current temperature and current humidity

    return 

i = 1
while i < 5:
    if i == 1:
        print("Analyzing Plant...")
        pred_class, img = capture_and_predict()
        temp, hum = ideal_values(pred_class)
        i = i+1
        start_time = time.time()
        timer = time.time()- start_time
    else:
        print("Gathering Live Data...")
        while timer < 10:
            timer = time.time()- start_time
            # Display image with predicted class
            plt.imshow(img)
            plt.axis('off')  # Hide axis
            plt.title(f'Predicted: {pred_class}', fontsize=14, color='blue')  # Show prediction
            plt.text(0.5, -0.04, f'The Ideal Temperature is: {temp} degrees Celsius', ha='center', va='center', fontsize=12, color='black', transform=plt.gca().transAxes)
            plt.text(0.5, -0.1, f'The Ideal Humidity is: {hum} %', ha='center', va='center', fontsize=12, color='black', transform=plt.gca().transAxes)
            plt.text(0.01, -0.1, f'timer: {timer}', ha='center', va='center', fontsize=12, color='red', transform=plt.gca().transAxes)
            plt.show()
            #Python to arduino
            import serial
            import time

            arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
            time.sleep(2)  

            def send_data(tempVal, humVal):
                data_string = f"{tempVal:.3f},{humVal:.3f}\n"  # Format as CSV
                arduino.write(data_string.encode()) 
                time.sleep(0.5)  

            temp = temp
            hum = hum
            send_data(temp, hum) # Change to values from ML model
            print("Data sent successfully.")

            # Check for Arduino response
            response = arduino.readline()  # Read the response from Arduino
            if response:
                print(f"{response.decode(errors='replace').strip()}")
                #print(temp,hum)
            else:
                print("No response from Arduino.")

            # Close the serial connection
            arduino.close()
        i = 1

