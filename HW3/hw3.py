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


def forget():
    try:
        global RGB_SMOOTH, HSI_SMOOTH, RGB_SHAPE, HSI_SHAPE, RGB_SMOOTH_label, HSI_SMOOTH_label, RGB_SHAPE_label, HSI_SHAPE_label
        RGB_SMOOTH.destroy()
        HSI_SMOOTH.destroy()
        RGB_SHAPE.destroy()
        HSI_SHAPE.destroy()
        RGB_SMOOTH_label.destroy()
        HSI_SMOOTH_label.destroy()
        RGB_SHAPE_label.destroy()
        HSI_SHAPE_label.destroy()
    except:
        pass

def reset():
    global image2, input_image_cv2, input_image_cv2_tmp
    # refresh image
    forget()
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(input_image_cv2, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    input_image_cv2_tmp = input_image_cv2
    try:
        hsi_label.destroy()
    except:
        pass


tk.Button(window, text="Reset",  height=5, width=20, command=reset).place(x=70, y=640)  # Creat the reset button


def open_file():
    try:
        global openfile
        #openfile = tk.filedialog.askopenfilename(title="Select file", filetypes=(("Image files", "*.*"), ("all files", "*.*")))
        openfile = "/home/jamesqian/Documents/DIP/HW3/Lenna_512_color.tif"  # temp
        # Choose the file
        print(openfile)  # Print the file name
        # Open image in gray scale
        global input_image_cv2, input_image_cv2_tmp
        input_image_cv2 = cv2.imread(openfile, 1)
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

        original_label = tk.Label(window,text="Original", width=7, height=2)
        original_label.place(x=220, y=20)
        adjust_label = tk.Label(window,text="Adjust", width=7, height=2)
        adjust_label.place(x=580, y=20)


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
    forget()
    try:
        hsi_label.destroy()
    except:
        pass


def green():
    global input_image_cv2_tmp, input_image_cv2, image2
    g = input_image_cv2.copy()
    # set blue and green channels to 0
    g[:, :, 0] = 0
    g[:, :, 2] = 0
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(g, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    forget()
    try:
        hsi_label.destroy()
    except:
        pass


def blue():
    global input_image_cv2_tmp, input_image_cv2, image2
    b = input_image_cv2.copy()
    # set blue and green channels to 0
    b[:, :, 1] = 0
    b[:, :, 2] = 0
    adjust_image = ImageTk.PhotoImage(
        Image.fromarray(cv2.cvtColor(b, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    forget()
    try:
        hsi_label.destroy()
    except:
        pass


tk.Button(window, text="Red component",  width=12, height=3, command=red).place(x=85, y=330)
tk.Button(window, text="Green component",  width=12, height=3, command=green).place(x=215, y=330)
tk.Button(window, text="Blue component",  width=12, height=3, command=blue).place(x=345, y=330)


def HSI():
    hsi = input_image_cv2.copy()

    rows = int(hsi.shape[0])
    cols = int(hsi.shape[1])
    B, G, R = cv2.split(hsi)
    B = B / 255.0
    G = G / 255.0
    R = R / 255.0
    H, S, I = cv2.split(hsi)
    for i in range(rows):
        for j in range(cols):
            num = 0.5 * ((R[i, j] - G[i, j]) + (R[i, j] - B[i, j]))
            den = np.sqrt((R[i, j] - G[i, j]) ** 2 +(R[i, j] - B[i, j]) * (G[i, j] - B[i, j]))
            theta = float(np.arccos(num / den))

            if den == 0:
                H = 0
            elif B[i, j] <= G[i, j]:
                H = theta
            else:
                H = 2 * 3.14169265 - theta

            min_RGB = min(min(B[i, j], G[i, j]), R[i, j])
            sum = B[i, j] + G[i, j] + R[i, j]
            if sum == 0:
                S = 0
            else:
                S = 1 - 3 * min_RGB / sum

            H = H / (2 * 3.14159265)
            I = sum / 3.0
            # 輸出HSI圖像，擴充到255以方便顯示，一般H分量在[0,2pi]之間，S和I在[0,1]之間
            hsi[i, j, 0] = H * 255
            hsi[i, j, 1] = S * 255
            hsi[i, j, 2] = I * 255

    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(hsi, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image

    global hsi_label
    hsi_label = tk.Label(window, width=10, height=10)
    hsi_label.place(x=890, y=20)
    hsi_label.config(text="Hue:\n"+str(H)[:7] + "\n\nSaturation:\n"+str(S)[:7]+"\n\nIntensity:\n"+str(I)[:7])

    return hsi


tk.Button(window, text="HSI",  width=12, height=3, command=HSI).place(x=540, y=330)


def Enhance():
    enhance = input_image_cv2.copy()

    enhance = 255 - enhance

    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(enhance, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    forget()
    try:
        hsi_label.destroy()
    except:
        pass

tk.Button(window, text="Enhance the detail",  width=14, height=3, command=Enhance).place(x=735, y=330)


def smoothing_and_sharping():
    global input_image_cv2, rgb_smooth, hsi_smooth, rgb_shape, hsi_shape, RGB_SMOOTH, HSI_SMOOTH, RGB_SHAPE, HSI_SHAPE, RGB_SMOOTH_label, HSI_SMOOTH_label, RGB_SHAPE_label, HSI_SHAPE_label
    rgb = input_image_cv2.copy()
    hsi = HSI()

    kernel = np.array([[1/25, 1/25, 1/25,1/25,1/25], [1/25, 1/25, 1/25,1/25,1/25], [1/25, 1/25, 1/25,1/25,1/25], [1/25, 1/25, 1/25,1/25,1/25], [1/25, 1/25, 1/25,1/25,1/25]])
    rgb_smooth = cv2.filter2D(rgb, -1, kernel)
    hsi_smooth = cv2.filter2D(hsi, -1, kernel)
    
    kernel = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    rgb_shape = cv2.filter2D(rgb, -1, kernel)
    hsi_shape = cv2.filter2D(hsi, -1, kernel)


    rgb_smooth = cv2.resize(rgb_smooth, (150, 150), interpolation = cv2.INTER_CUBIC)
    hsi_smooth = cv2.resize(hsi_smooth, (150, 150), interpolation = cv2.INTER_CUBIC)
    rgb_shape = cv2.resize(rgb_shape, (150, 150), interpolation = cv2.INTER_CUBIC)
    hsi_shape = cv2.resize(hsi_shape, (150, 150), interpolation = cv2.INTER_CUBIC)
    rgb_smooth = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(rgb_smooth, cv2.COLOR_BGR2RGB)))
    hsi_smooth = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(hsi_smooth, cv2.COLOR_BGR2RGB)))
    rgb_shape = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(rgb_shape, cv2.COLOR_BGR2RGB)))
    hsi_shape = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(hsi_shape, cv2.COLOR_BGR2RGB)))

    RGB_SMOOTH = tk.Label(window, image=rgb_smooth, width=150, height=150)
    RGB_SMOOTH.place(x=300, y=500)
    RGB_SMOOTH_label = tk.Label(window, text="RGB Smooth",width=10, height=1)
    RGB_SMOOTH_label.place(x=300, y=655)

    HSI_SMOOTH = tk.Label(window, image=hsi_smooth, width=150, height=150)
    HSI_SMOOTH.place(x=460, y=500)
    HSI_SMOOTH_label = tk.Label(window, text="HSI Smooth",width=10, height=1)
    HSI_SMOOTH_label.place(x=460, y=655)

    RGB_SHAPE = tk.Label(window, image=rgb_shape, width=150, height=150)
    RGB_SHAPE.place(x=620, y=500)
    RGB_SHAPE_label = tk.Label(window, text="RGB SHAPE",width=10, height=1)
    RGB_SHAPE_label.place(x=620, y=655)

    HSI_SHAPE = tk.Label(window, image=hsi_shape, width=150, height=150)
    HSI_SHAPE.place(x=780, y=500)
    HSI_SHAPE_label = tk.Label(window, text="HSI SHAPE",width=10, height=1)
    HSI_SHAPE_label.place(x=780, y=655)


tk.Button(window, text="Smoothing and Sharping",  width=18, height=3, command=smoothing_and_sharping).place(x=705, y=430)


window.mainloop()