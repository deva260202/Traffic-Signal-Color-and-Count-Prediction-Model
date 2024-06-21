import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

def predict(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    predictions = model.predict(img_array)
    car_color, car_count, male_count, female_count, other_vehicle_count = predictions

    # Car color mapping
    color_mapping = ['red', 'blue', 'other']  # Adjust this list based on your actual color labels

    # Swap red and blue if people are present
    if male_count[0] + female_count[0] > 0:
        if np.argmax(car_color[0]) == 0:  # Red
            car_color[0][0], car_color[0][1] = car_color[0][1], car_color[0][0]  # Swap red and blue
        elif np.argmax(car_color[0]) == 1:  # Blue
            car_color[0][1], car_color[0][0] = car_color[0][0], car_color[0][1]  # Swap blue and red

    car_color_label = color_mapping[np.argmax(car_color[0])]
    car_count_label = int(round(car_count[0][0]))
    male_count_label = int(round(male_count[0][0]))
    female_count_label = int(round(female_count[0][0]))
    other_vehicle_count_label = int(round(other_vehicle_count[0][0]))

    return {
        'car_color': car_color_label,
        'car_count': car_count_label,
        'male_count': male_count_label,
        'female_count': female_count_label,
        'other_vehicle_count': other_vehicle_count_label
    }

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        
        panel.config(image=img)
        panel.image = img

        result = predict(file_path)
        result_text = (f"Car Color: {result['car_color']}\n"
                       f"Car Count: {result['car_count']}\n"
                       f"Male Count: {result['male_count']}\n"
                       f"Female Count: {result['female_count']}\n"
                       f"Other Vehicle Count: {result['other_vehicle_count']}")
        result_label.config(text=result_text)

# Load the trained model
model_path = 'C:/Users/admin/Desktop/Python Prog/Age gender detector/Traffic_model.keras'
model = tf.keras.models.load_model(model_path)

# Create the GUI window
root = tk.Tk()
root.title("Traffic Image Predictor")
root.geometry("400x400") 

heading=Label(root, text="Traffic Image Predictor", pady=20, font=("arial",20, "bold")) 
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

# Create a button to open images
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

# Create a panel to display the image
panel = Label(root)
panel.pack()

# Create a label to display the results
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack()

# Run the GUI
root.mainloop()
