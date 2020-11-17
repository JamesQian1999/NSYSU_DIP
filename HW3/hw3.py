# Student ID: B073021024
import cv2
import tkinter as tk
from tkinter import filedialog as fd
# sudo apt-get install python3-tk
from PIL import Image, ImageTk, ImageOps, ImageEnhance
# sudo apt-get install python3-pil python3-pil.imagetk
import numpy as np
# sudo apt-get install python3-numpy
import matplotlib.pyplot as plt
# sudo apt-get install python3-matplotlib
import math

# main window
window = tk.Tk()
window.title("Digital Image HW2")  # Whindow title
window.geometry('1000x800')  # Window size
window.configure(background='white')   # window color


def reset():
    global image2, input_image_cv2, input_image_cv2_tmp
    # refresh image
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(input_image_cv2, cv2.COLOR_BGR2RGB)))  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    input_image_cv2_tmp = input_image_cv2


tk.Button(window, text="Reset",  height=5, width=20,command=reset).place(x=90, y=640)  # Creat the reset button

def open_file():
    try:
        global openfile
        #openfile = tk.filedialog.askopenfilename(title="Select file", filetypes=(("Image files", "*.*"), ("all files", "*.*")))
        openfile = "/home/jamesqian/Documents/DIP/HW3/Lenna_512_color.tif" #temp
        # Choose the file
        print(openfile)  # Print the file name
        # Open image in gray scale
        global input_image_cv2, input_image_cv2_tmp
        input_image_cv2 = cv2.imread(openfile,1)
        # Resize image to fit the label
        input_image_cv2 = cv2.resize(input_image_cv2, (300, 300), interpolation=cv2.INTER_CUBIC)
        # Resize image to fit the label
        global photo
        # Transform image into ImageTk form
        photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(input_image_cv2, cv2.COLOR_BGR2RGB)))
        # show
        global image1, image2
        # creat label for original image
        image1 = tk.Label(window, image=photo, width=300, height=300)
        image1.place(x=220, y=20)
        # creat label for adjusted image
        image2 = tk.Label(window, image=photo, width=300, height=300)
        image2.place(x=580, y=20)

        input_image_cv2_tmp = input_image_cv2
    except:
        print("Error!")

tk.Button(window, text="Open",  height=5, width=10, command=open_file).place(x=90, y=50)  # Creat the open button


def red():
    global input_image_cv2_tmp, input_image_cv2, image2
    r = input_image_cv2.copy()
    # set blue and green channels to 0
    r[:, :, 0] = 0
    r[:, :, 1] = 0
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(r, cv2.COLOR_BGR2RGB)))  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
def green():
    global input_image_cv2_tmp, input_image_cv2, image2
    g = input_image_cv2.copy()
    # set blue and green channels to 0
    g[:, :, 0] = 0
    g[:, :, 2] = 0
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(g, cv2.COLOR_BGR2RGB)))  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
def blue():
    global input_image_cv2_tmp, input_image_cv2, image2
    b = input_image_cv2.copy()
    # set blue and green channels to 0
    b[:, :, 1] = 0
    b[:, :, 2] = 0
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(b, cv2.COLOR_BGR2RGB)))  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image

tk.Button(window, text="Red component",  width=12, height=3, command=red).place(x=85, y=330)
tk.Button(window, text="Green component",  width=12, height=3, command=green).place(x=215, y=330)
tk.Button(window, text="Blue component",  width=12, height=3, command=blue).place(x=345, y=330)

window.mainloop()