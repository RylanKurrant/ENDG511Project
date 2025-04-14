import time
import cv2  
import torch
from fastai.vision.all import *
import pandas as pd

# Load the model once
learn = load_learner('v2pruned_plant_classifier.pkl')
# Load the DataLoaders
with open('v2pruned_dls.pkl', 'rb') as f:
    learn.dls = pickle.load(f)


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
    df = pd.read_csv("ENDG511 Project Temps and Humidity.csv")
    # Find matching row
    matching_row = df[df.iloc[:, 0] == predicted_value]

    # Select specific columns (e.g., column 2 and 3)
    selected_columns = matching_row.iloc[:, [3, 6]]

    # Extracting temperature and humidty values
    temp = selected_columns.iloc[0, 0]
    hum = selected_columns.iloc[0, 1]

    return temp, hum

def arduino_function():
    
    ## Insert Code ###


    return 

i = 1
while i < 5:
    if i == 1:
        # Plant is identified once every 10 seconds
        print("Analyzing Plant...")
        pred_class, img = capture_and_predict()
        temp, hum = ideal_values(pred_class)
        i = i+1
        start_time = time.time()
        timer = time.time()- start_time
    else:
        # Once the plant is identified, conditions are continously monitored with the Arduino. Once the timer hits 10 seconds, the loop is restarted and the plant is identified again. 
        print("Gathering Live Data...")
        while timer < 10:
            timer = time.time()- start_time
            print(timer)
            # Display image with predicted class
            # plt.imshow(img)
            # plt.axis('off')  # Hide axis
            # plt.title(f'Predicted: {pred_class}', fontsize=14, color='blue')  # Show prediction
            # plt.text(0.5, -0.04, f'The Ideal Temperature is: {temp} degrees Celsius', ha='center', va='center', fontsize=12, color='black', transform=plt.gca().transAxes)
            # plt.text(0.5, -0.1, f'The Ideal Humidity is: {hum} %', ha='center', va='center', fontsize=12, color='black', transform=plt.gca().transAxes)
            # plt.text(0.01, -0.1, f'timer: {timer}', ha='center', va='center', fontsize=12, color='red', transform=plt.gca().transAxes)
            # plt.show()
        i = 1

