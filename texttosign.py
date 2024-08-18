import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import time

root = tk.Toplevel()
root.title("Text To Sign Conversion")
root.geometry("850x650")
root.configure(bg="#f0f0f0")

# Dictionary mapping characters to corresponding hand gesture images
gesture_map = {chr(i): f'text_to_sign_data//{chr(i).lower()}.jpg' for i in range(97, 123)}

# Lists to keep references to images
image_refs = []
gesture_labels = []
char_labels = []

# Function to display hand gesture images for a given word
def display_gestures(word):
    global image_refs, gesture_labels, char_labels
    # Remove any existing labels from the root window
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()

    # Clear previous references
    image_refs = []
    gesture_labels = []
    char_labels = []

    # Calculate the total width and starting x position to center the images
    total_width = len(word) * 130 
    start_x = (root.winfo_width() - total_width) // 2
    y = 150

    for char in word:
        if char in gesture_map:
            # Load the hand gesture image for the character
            gesture_image = Image.open(gesture_map[char])
            gesture_image = gesture_image.resize((100, 100), resample=Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(gesture_image)
            image_refs.append(tk_image)  # Keep a reference to the image
            
            # Create label for each character
            gesture_label = tk.Label(root, image=tk_image, bg="#f0f0f0")
            gesture_label.place(x=start_x, y=y)
            gesture_labels.append(gesture_label)
            char_label = tk.Label(root, text=char.upper(), font=("Arial", 16), bg="#f0f0f0")
            char_label.place(x=start_x + 30, y=y + 110)  # Centered under the image
            char_labels.append(char_label)
            start_x += 130

    # Spell out the characters one by one
    for i, char in enumerate(word):
        if char in gesture_map:
            engine = pyttsx3.init()
            engine.say(char)
            engine.runAndWait()
            gesture_labels[i].lift()
            char_labels[i].lift()
            root.update()
            time.sleep(1)

# Function to get the input text and display the corresponding hand gesture images
def submit_text():
    word = input_text.get().lower()  # Convert input to lowercase
    display_gestures(word)

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=(20, 10))  # Add some padding around the frame

# Text box to get the input text
input_text = tk.Entry(frame, width=50, font=("Arial", 14))
input_text.pack(padx=10, pady=10)

# Button to display the hand gesture images
submit_button = tk.Button(frame, text="Display Gesture", command=submit_text, 
                          font=("Arial", 14), bg="#4CAF50", fg="white")
submit_button.pack(pady=(0, 20))  # Add space below the button

root.mainloop()
