import tkinter as tk
from tkinter import ttk, filedialog
from gtts import gTTS
from datetime import datetime
import io
import pygame

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                text = file.read()
                text_entry.delete("1.0", "end")
                text_entry.insert("1.0", text)
        except Exception as ex:
            result_label.config(text=str(ex))

def save_as_audio(file_name):
    input_text = text_entry.get("1.0", "end-1c") 
    if input_text:
        tts = gTTS(input_text, slow=speed_var.get() == 1)
        tts.save(str(file_name) + str(datetime.now().strftime("H%M%S")) + ".mp3")

def convert_text():
    try:
        input_text = text_entry.get("1.0", "end-1c")
        save_option = save_var.get()

        if save_option == "yes":
            filename = filename_entry.get()
            save_as_audio(filename)
            result_label.config(text=f'Saved as {filename}')
        else:
            tts = gTTS(input_text, slow=speed_var.get() == 1) 
            audio_file = io.BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
            result_label.config(text="Speech Played successfully")
    except Exception as ex:
        result_label.config(text=str(ex))

# Create the main window
root = tk.Tk()
root.title("Text-to-Speech Converter")

# Text Entry
text_label = ttk.Label(root, text="Enter the text you want to convert:")
text_label.pack()

text_entry = tk.Text(root, height=5, width=40)
text_entry.pack()

# Open Text File Button
open_file_button = ttk.Button(root, text="Open Text File", command=open_file_dialog)
open_file_button.pack()

# Save as Audio Option
save_var = tk.StringVar()
save_label = ttk.Label(root, text="Save as audio file?")
save_label.pack()

save_yes = ttk.Radiobutton(root, text="Yes", variable=save_var, value="yes")
save_yes.pack()

save_no = ttk.Radiobutton(root, text="No (Play immediately)", variable=save_var, value="no")
save_no.pack()

# Speed Controller
speed_label = ttk.Label(root, text="Speed Control:")
speed_label.pack()

speed_var = tk.IntVar()
speed_var.set(1)  # Set default speed to Slow (1)
speed_slider = ttk.Scale(root, from_=0, to=1, orient="horizontal", variable=speed_var)
speed_slider.pack()

speed_label_fast = ttk.Label(root, text="Fast")
speed_label_slow = ttk.Label(root, text="Slow")
speed_label_fast.pack()
speed_label_slow.pack()

# File Name Entry (if saving as audio)
filename_label = ttk.Label(root, text="If you choose yes, enter the filename (e.g., output.mp3):")
filename_label.pack()

filename_entry = ttk.Entry(root)
filename_entry.pack()

# Convert Button
convert_button = ttk.Button(root, text="Convert/Play", command=convert_text)
convert_button.pack()

note_label = ttk.Label(root, text="Note: please wait for few seconds it may take couple of seconds")
note_label.pack()

# Result Label
result_label = ttk.Label(root, text="")
result_label.pack()

root.mainloop()
