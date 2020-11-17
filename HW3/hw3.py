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