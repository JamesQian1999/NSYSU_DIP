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
window.title("Digital Image HW1")  # Whindow title
window.geometry('1000x800')  # Window size
window.configure(background='white')   # window color


def reset():
    global image2, input_image_cv2, input_image_cv2_tmp
    # refresh image
    tmp = Image.fromarray(input_image_cv2)
    adjust_image = ImageTk.PhotoImage(tmp)  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    input_image_cv2_tmp = input_image_cv2


tk.Button(window, text="Reset",  height=5, width=20,command=reset).place(x=90, y=640)  # Creat the reset button


def open_file():
    try:
        global openfile
        openfile = tk.filedialog.askopenfilename(title="Select file", filetypes=(("Image files", "*.*"), ("all files", "*.*")))
        # Choose the file
        print(openfile)  # Print the file name
        # Open image in gray scale
        global input_image_cv2, input_image_cv2_tmp
        input_image_cv2 = cv2.imread(openfile, 0)
        # Resize image to fit the label
        input_image_cv2 = cv2.resize(
            input_image_cv2, (300, 300), interpolation=cv2.INTER_CUBIC)
        # Resize image to fit the label
        global photo
        # Transform image into ImageTk form
        input_image_tk = Image.fromarray(input_image_cv2)
        photo = ImageTk.PhotoImage(image=input_image_tk)
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

def save_file():
    global openfile ,input_image_cv2_tmp
    print("Adjusted_"+openfile) # Print the file name
    output = Image.fromarray(input_image_cv2_tmp)
    output.save("Adjusted_"+openfile) # save image


tk.Button(window, text="Open",  height=5, width=10,
          command=open_file).place(x=90, y=50)  # Creat the open button
tk.Button(window , text = "Save",  height = 5, width = 10, command = save_file).place(x=90,y=160) # Creat the ssave button


def gray_level():
    a = entry_output_low.get()
    b = entry_output_up.get()
    print("before:", a, b)
    if a and b:
        a = int(entry_output_low.get())
        b = int(entry_output_up.get())
    if not a:
        a = 0
    if not b:
        b = 255
    if a > b:
        print("ERROR")
        return
    print("after:", a, b)

    global input_image_cv2_tmp ,input_image_cv2
    tmp = input_image_cv2

    print("tmp:", tmp.shape)
    print("input_image_cv2:", input_image_cv2_tmp.shape)
    # set range
    x, y = tmp.shape
    z = np.zeros((x, y))
    for i in range(0, x):
        for j in range(0, y):
            if(tmp[i][j] > a and tmp[i][j] < b):
                z[i][j] = 255
            else:
                z[i][j] = 0

    # refresh image
    input_image_cv2_tmp = Image.fromarray(np.uint8(z))
    global adjust_image, image2
    adjust_image = ImageTk.PhotoImage(input_image_cv2_tmp)  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    input_image_cv2_tmp = np.asarray(input_image_cv2_tmp)
    print("input_image_cv2_tmp:", input_image_cv2_tmp.shape)

#creat entery to Lower bound and upper bound
entry_output_low = tk.StringVar()
tk.Entry(window, textvariable=entry_output_low, width=4).place(x=450, y=360)
tk.Label(window, text="Lower bound", width=11, height=1).place(x=355, y=360)
entry_output_up = tk.StringVar()
tk.Entry(window, textvariable=entry_output_up, width=4).place(x=450, y=385)
tk.Label(window, text="Upper bound", width=11, height=1).place(x=355, y=385)

#creat OK button
tk.Label(window, text="Range should be \nbetween 0 and 255.", width=16, height=2).place(x=219, y=365)
tk.Label(window, text="Gray-level Slicing",  width=15, height=3).place(x=85, y=360)
tk.Button(window, text="OK",  height=2, width=5, command=gray_level).place(x=500, y=360)


def Bit_Plane(value):
    global input_image_cv2, input_image_cv2_tmp, adjust_image, image2
    tmp = input_image_cv2
    value = int(value) # transform string into integer
    print("value =", value)
    lst = []
    # find bit in image
    for i in range(tmp.shape[0]):
        for j in range(tmp.shape[1]):
            # width = no. of bits
            lst.append(np.binary_repr(tmp[i][j], width=8))
    input_image_cv2_tmp = (np.array([int(i[value]) for i in lst], dtype=np.uint8) * 255).reshape(tmp.shape[0], tmp.shape[1])

    # refresh image
    input_image_cv2_tmp = Image.fromarray(input_image_cv2_tmp)
    adjust_image = ImageTk.PhotoImage(input_image_cv2_tmp)  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    input_image_cv2_tmp = np.asarray(input_image_cv2_tmp)

#creat Bit-Plane images scale
tk.Scale(label=' ', orient=tk.HORIZONTAL, from_=0, to=7, showvalue=False, bg='light blue', fg='black', tickinterval=1, length=750, width=5, troughcolor='blue', command=Bit_Plane).place(x=219, y=410)
tk.Label(window, text="Bit-Plane images",  width=15, height=3).place(x=85, y=410)


smooth_value = 0
sharpe_value = 0


def Sharpe(value):
    global input_image_cv2, input_image_cv2_tmp, image2, sharpe_value, smooth_value
    tmp = input_image_cv2
    value = int(value) # transform string into integer
    sharpe_value = value
    print(value)
    #creat the sharpe kernel
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    for i in range(0, value):
        tmp = cv2.filter2D(tmp, -1, kernel)
    if smooth_value:
        #creat the smooth kernel
        kernel = np.array([[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]])
        for i in range(0, smooth_value):
            tmp = cv2.filter2D(tmp, -1, kernel)
            
     # refresh image
    input_image_cv2_tmp = tmp
    tmp = Image.fromarray(input_image_cv2_tmp)
    adjust_image = ImageTk.PhotoImage(tmp) 
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image


def Smooth(value):
    global input_image_cv2, input_image_cv2_tmp, image2, smooth_value, sharpe_value
    tmp = input_image_cv2
    value = int(value) # transform string into integer
    smooth_value = value
    print(value)
    #creat the smooth kernel
    kernel = np.array([[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]])
    for i in range(0, value):
        tmp = cv2.filter2D(tmp, -1, kernel)
    if sharpe_value:
        #creat the sharpe kernel
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        for i in range(0, sharpe_value):
            tmp = cv2.filter2D(tmp, -1, kernel)

    # refresh image
    input_image_cv2_tmp = tmp
    tmp = Image.fromarray(input_image_cv2_tmp)
    adjust_image = ImageTk.PhotoImage(tmp) 
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image

#creat the smooth and sharpe scale
tk.Scale(label='Smoothing', orient=tk.HORIZONTAL, showvalue=False, bg='light blue', fg='black', from_=0, to=20, resolution=1, tickinterval=2, length=400, width=5, troughcolor='blue', command=Smooth).place(x=170, y=465)
tk.Scale(label='sharpening', orient=tk.HORIZONTAL, showvalue=False, bg='light blue', fg='black', from_=0, to=5,  resolution=1, tickinterval=1, length=400, width=5, troughcolor='blue', command=Sharpe).place(x=570, y=465)
tk.Label(window, text="Smooth and\nsharpe", width=10, height=3).place(x=85, y=465)


def FFT():
    global input_image_cv2, input_image_cv2_tmp, image2, FFT_image
    tmp = input_image_cv2 #Inport the image
    tmp = np.fft.fft2(tmp) # Transform
    tmp = np.fft.fftshift(tmp) # Shift
    tmp = np.abs(tmp)
    tmp = np.log(tmp)
    input_image_cv2_tmp = 15*np.asarray(tmp, dtype=np.uint8) 
    FFT_image = input_image_cv2_tmp # save image
    print(type(input_image_cv2_tmp))

    # refresh image
    tmp = Image.fromarray(input_image_cv2_tmp)
    adjust_image = ImageTk.PhotoImage(tmp)  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image

#creat FFT button
tk.Button(window, text="FFT",  width=8, height=3, command=FFT).place(x=170, y=550)

def Amplitude():
    global input_image_cv2, input_image_cv2_tmp, image2
    tmp = np.fft.fft2(input_image_cv2)
    tmp = np.fft.fftshift(tmp)  # get fft and shift image
    tmp = np.fft.ifftshift(np.abs(tmp))  # Amplitude
    tmp = np.fft.ifft2(tmp)  # invrse transform
    tmp = np.abs(tmp)
    input_image_cv2_tmp = tmp
    # refresh image
    tmp = Image.fromarray(tmp)
    adjust_image = ImageTk.PhotoImage(tmp)  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image

#creat Amplitude button
tk.Button(window, text="Amplitude",  width=8, height=3, command=Amplitude).place(x=270, y=550)

def phase():
    global input_image_cv2, input_image_cv2_tmp, image2
    tmp = np.fft.fft2(input_image_cv2)
    tmp = np.fft.fftshift(tmp)  # get fft and shift image
    #Phase
    tmp=np.fft.ifftshift(np.angle(tmp))	
    tmp=np.fft.ifft2(tmp)			
    tmp=5000*np.abs(tmp)
    input_image_cv2_tmp = tmp

    # refresh image
    tmp = Image.fromarray(tmp)
    adjust_image = ImageTk.PhotoImage(tmp)  
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image

#creat phase button
tk.Button(window, text=" Phase",  width=8, height=3, command=phase).place(x=370, y=550)

def Homomorphic_filter():
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~open Fig0460a~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    global openfile
    # Choose the file
    openfile = ("Fig0460a.tif")  # tmp
    print(openfile)  # Print the file name
    # Open image in gray scale
    global input_image_cv2, input_image_cv2_tmp
    input_image_cv2 = cv2.imread(openfile, 0)
    # Resize image to fit the label
    input_image_cv2 = cv2.resize(input_image_cv2, (300, 300), interpolation=cv2.INTER_CUBIC)
    # Resize image to fit the label
    global photo
    # Transform image into ImageTk form
    input_image_tk = Image.fromarray(input_image_cv2)
    photo = ImageTk.PhotoImage(image=input_image_tk)
    # show
    global image1, image2
    # creat label for original image
    image1 = tk.Label(window, image=photo, width=300, height=300)
    image1.place(x=220, y=20)
    # creat label for adjusted image
    image2 = tk.Label(window, image=photo, width=300, height=300)
    image2.place(x=580, y=20)
    input_image_cv2_tmp = input_image_cv2
    d0 = 20; r1 = 0.4; rh = 3.0; c = 5; h = 2.0; l = 0.5
    gray = tmp = input_image_cv2_tmp
    if len(tmp.shape) > 2:
        gray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
    gray = np.float64(gray)
    rows, cols = gray.shape

    #Implement Homomorphic filter
    gray_dft = np.fft.fft2(gray)
    gray_dftshift = np.fft.fftshift(gray_dft)
    dst_dftshift = np.zeros_like(gray_dftshift)
    M, N = np.meshgrid(np.arange(-cols // 2, cols // 2), np.arange(-rows//2, rows//2))
    D = np.sqrt(M ** 2 + N ** 2)
    Z = (rh - r1) * (1 - np.exp(-c * (D ** 2 / d0 ** 2))) + r1
    dst_dftshift = Z * gray_dftshift
    dst_dftshift = (h - l) * dst_dftshift + l
    dst_idftshift = np.fft.ifftshift(dst_dftshift)
    dst_idft = np.fft.ifft2(dst_idftshift)
    dst = np.real(dst_idft)
    dst = np.uint8(np.clip(dst, 0, 255))
    input_image_cv2_tmp = dst

    # refresh image
    tmp = Image.fromarray(dst)
    adjust_image = ImageTk.PhotoImage(tmp) 
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image

#creat Homomorphic filter button
tk.Button(window, text="Homomorphic filter",  width=15, height=3, command=Homomorphic_filter).place(x=470, y=550)


window.mainloop()
