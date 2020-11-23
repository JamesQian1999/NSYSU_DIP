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


def forget_smooth_shape(): # remove the forget_smooth_shape label
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

def forget_HSI(): # remove the HSI label
    try:
        global HSI_h, HSI_s, HSI_i, HSI_h_label, HSI_s_label ,HSI_i_label
        HSI_h.destroy()
        HSI_s.destroy()
        HSI_i.destroy()
        HSI_h_label.destroy()
        HSI_s_label.destroy()
        HSI_i_label.destroy()
    except:
        pass

def forget_feather(): #remove the feather label
    try:
        global STEP1 ,STEP2, STEP3,STEP1_label,STEP2_label,STEP3_label
        STEP1.destroy()
        STEP2.destroy()
        STEP3.destroy()
        STEP1_label.destroy()
        STEP2_label.destroy()
        STEP3_label.destroy()
    except:
        pass

def reset(): # reset the image
    global image2, input_image_cv2, input_image_cv2_tmp
    # refresh image
    forget_smooth_shape()
    forget_HSI()
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(input_image_cv2, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    input_image_cv2_tmp = input_image_cv2



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
    forget_smooth_shape()
    forget_HSI()
    forget_feather()


def green():
    global input_image_cv2_tmp, input_image_cv2, image2
    g = input_image_cv2.copy()
    # set blue and green channels to 0
    g[:, :, 0] = 0
    g[:, :, 2] = 0
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(g, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    forget_smooth_shape()
    forget_HSI()
    forget_feather()


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
    forget_smooth_shape()
    forget_HSI()
    forget_feather()


tk.Button(window, text="Red component",  width=12, height=3, command=red).place(x=85, y=330)
tk.Button(window, text="Green component",  width=12, height=3, command=green).place(x=215, y=330)
tk.Button(window, text="Blue component",  width=12, height=3, command=blue).place(x=345, y=330)


def HSI(): # used the HSI formula
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

            # let HSI image visible
            hsi[i, j, 0] = H * 255
            hsi[i, j, 1] = S * 255
            hsi[i, j, 2] = I * 255

    # refresh the image
    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(hsi, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    forget_smooth_shape()

    # show the HSI component
    global hsi_h ,HSI_h, hsi_s, HSI_s, hsi_i, HSI_i, HSI_h_label,  HSI_s_label ,HSI_i_label
    hsi_h = cv2.resize(hsi[:,:,0], (150, 150), interpolation = cv2.INTER_CUBIC)
    hsi_h = ImageTk.PhotoImage(image=Image.fromarray(hsi_h))
    HSI_h = tk.Label(window, image=hsi_h, width=150, height=150)
    HSI_h.place(x=460, y=500)
    HSI_h_label = tk.Label(window, text="H",width=10, height=1)
    HSI_h_label.place(x=460, y=655)
    
    hsi_s = cv2.resize(hsi[:,:,1], (150, 150), interpolation = cv2.INTER_CUBIC)
    hsi_s = ImageTk.PhotoImage(image=Image.fromarray(hsi_s))
    HSI_s = tk.Label(window, image=hsi_s, width=150, height=150)
    HSI_s.place(x=620, y=500)
    HSI_s_label = tk.Label(window, text="S",width=10, height=1)
    HSI_s_label.place(x=620, y=655)

    hsi_i = cv2.resize(hsi[:,:,2], (150, 150), interpolation = cv2.INTER_CUBIC)
    hsi_i = ImageTk.PhotoImage(image=Image.fromarray(hsi_i))
    HSI_i = tk.Label(window, image=hsi_i, width=150, height=150)
    HSI_i.place(x=780, y=500)
    HSI_i_label = tk.Label(window, text="I",width=10, height=1)
    HSI_i_label.place(x=780, y=655)

    forget_feather()
    
    return hsi


tk.Button(window, text="HSI",  width=12, height=3, command=HSI).place(x=540, y=330)


def Enhance():
    enhance = input_image_cv2.copy()

    # used 
    enhance = 255 - enhance

    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(enhance, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    forget_smooth_shape()
    forget_HSI()
    forget_feather()

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
    rgb_smooth = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(rgb_smooth, cv2.COLOR_BGR2RGB)))
    RGB_SMOOTH = tk.Label(window, image=rgb_smooth, width=150, height=150)
    RGB_SMOOTH.place(x=300, y=500)
    RGB_SMOOTH_label = tk.Label(window, text="RGB Smooth",width=10, height=1)
    RGB_SMOOTH_label.place(x=300, y=655)

    hsi_smooth = cv2.resize(hsi_smooth, (150, 150), interpolation = cv2.INTER_CUBIC)
    hsi_smooth = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(hsi_smooth, cv2.COLOR_BGR2RGB)))
    HSI_SMOOTH = tk.Label(window, image=hsi_smooth, width=150, height=150)
    HSI_SMOOTH.place(x=460, y=500)
    HSI_SMOOTH_label = tk.Label(window, text="HSI Smooth",width=10, height=1)
    HSI_SMOOTH_label.place(x=460, y=655)

    rgb_shape = cv2.resize(rgb_shape, (150, 150), interpolation = cv2.INTER_CUBIC)
    rgb_shape = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(rgb_shape, cv2.COLOR_BGR2RGB)))
    RGB_SHAPE = tk.Label(window, image=rgb_shape, width=150, height=150)
    RGB_SHAPE.place(x=620, y=500)
    RGB_SHAPE_label = tk.Label(window, text="RGB SHAPE",width=10, height=1)
    RGB_SHAPE_label.place(x=620, y=655)

    hsi_shape = cv2.resize(hsi_shape, (150, 150), interpolation = cv2.INTER_CUBIC)
    hsi_shape = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(hsi_shape, cv2.COLOR_BGR2RGB)))
    HSI_SHAPE = tk.Label(window, image=hsi_shape, width=150, height=150)
    HSI_SHAPE.place(x=780, y=500)
    HSI_SHAPE_label = tk.Label(window, text="HSI SHAPE",width=10, height=1)
    HSI_SHAPE_label.place(x=780, y=655)

    forget_HSI()
    forget_feather()


tk.Button(window, text="Smoothing and Sharping",  width=18, height=3, command=smoothing_and_sharping).place(x=705, y=430)


def feather():
    global input_image_cv2
    finalload = input_image_cv2.copy()
    global step1, step2, step3, STEP1 ,STEP2, STEP3, STEP1_label,STEP2_label,STEP3_label

    rows = int(finalload.shape[0])
    cols = int(finalload.shape[1])

    for i in range(rows):
        for j in range(cols):
            B,G,R=finalload[i,j]
            B=int(B)
            G=int(G)
            R=int(R)
            up=0.5*((R-G)+(R-B))
            down=math.sqrt(pow((R-G),2)+(R-B)*(G-B))
            sita=((math.acos(up/down))*180)/(math.pi)
            sita=(sita/360)*255
            if B>G:	sita=255-sita
            Hue=sita
            if Hue<120 or Hue>220:	finalload[i,j]=[0,0,0]
    step1 = cv2.resize(finalload, (150, 150), interpolation = cv2.INTER_CUBIC)
    step1 = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(step1, cv2.COLOR_BGR2RGB)))
    STEP1 = tk.Label(window, image=step1, width=150, height=150)
    STEP1.place(x=460, y=500)
    STEP1_label = tk.Label(window, text="Step 1",width=10, height=1)
    STEP1_label.place(x=460, y=655)


    for i in range(rows):
        for j in range(cols):
            B,G,R=finalload[i,j]
            B=int(B)
            G=int(G)
            R=int(R)
            if R+G+B:Satu = 255*(1-(3/(R+G+B))*min(R,G,B))
            else: Satu = 0 
            if (Satu<50 or Satu>120):	finalload[i,j]=[0,0,0]
    step2 = cv2.resize(finalload, (150, 150), interpolation = cv2.INTER_CUBIC)
    step2 = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(step2, cv2.COLOR_BGR2RGB)))
    STEP2 = tk.Label(window, image=step2, width=150, height=150)
    STEP2.place(x=620, y=500)
    STEP2_label = tk.Label(window, text="Step 2",width=10, height=1)
    STEP2_label.place(x=620, y=655)


    for i in range(rows):
        for j in range(cols):
            B,G,R=finalload[i,j]
            B=int(B)
            G=int(G)
            R=int(R)
            up=0.5*((R-G)+(R-B))
            down=math.sqrt(pow((R-G),2)+(R-B)*(G-B))
            if down :sita=((math.acos(up/down))*180)/(math.pi)
            else: sita=0
            sita=(sita/360)*255
            if B>G:	sita=255-sita
            Hue=sita
            if R+G+B:Satu = 255*(1-(3/(R+G+B))*min(R,G,B))
            else: Satu = 0 
            if (Hue<120 or Hue>220) or (Satu<50 or Satu>120):	finalload[i,j]=[0,0,0]
    step3 = cv2.resize(finalload, (150, 150), interpolation = cv2.INTER_CUBIC)
    step3 = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(step3, cv2.COLOR_BGR2RGB)))
    STEP3 = tk.Label(window, image=step3, width=150, height=150)
    STEP3.place(x=780, y=500)
    STEP3_label = tk.Label(window, text="Step 3",width=10, height=1)
    STEP3_label.place(x=780, y=655)


    adjust_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(finalload, cv2.COLOR_BGR2RGB)))
    image2.config(image=adjust_image, width=300, height=300)
    image2.Image = adjust_image
    forget_smooth_shape()
    forget_HSI()

tk.Button(window, text="Segment the feather",  width=18, height=3, command=feather).place(x=505, y=430)

window.mainloop()
