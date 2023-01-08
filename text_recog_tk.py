import tkinter as tk
from tkinter import ttk
from PIL import Image
from pytesseract import pytesseract
import pyautogui as ag
import time

pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

x_start = 0
x_end = 0
x_final = 0
y_start = 0
y_end = 0
y_final = 0
width = 0
height = 0
capturing = False
capture_area = 0

window = tk.Tk()
window.title("Text Recognition Screen Capture Tool")

frame = tk.Frame(master = window)
frame.grid(row = 3, column = 1, padx=5, pady=5)

label_text = "Click \"Capture\" then drag your mouse over an area on the screen to capture a screenshot and analyze the text in that area. "
label = tk.Label(master = frame, text = label_text)
label.pack()

text_area = tk.Text(master = frame)
text_area.pack()

def button_action():

    global capturing
    global capture_area
    global window
    capture_area = tk.Tk()
    capture_area.attributes('-alpha',0.075)
    window.attributes('-alpha',0)
    capture_area.attributes('-fullscreen', True)
    capture_area.bind('<Button-1>', on_mouse_click)
    capture_area.bind('<ButtonRelease-1>', on_mouse_release)
    capturing = True

capture_btn = tk.Button(master = frame, text = "Capture", command = button_action)
capture_btn.pack()

def on_mouse_click(event):
    global capturing
    global x_start 
    global y_start
    if capturing:
        x_start, y_start = ag.position()

def on_mouse_release(event):
    global capturing
    global x_end 
    global y_end 
    global capture_area
    global window

    if capturing: 
        x_end, y_end = ag.position()
        set_w_h()
        #print("X: {0} Y: {1} W: {2} H: {3}".format(x_final, y_final, width, height))
        do_text_recog()
        capturing = False
        capture_area.destroy()
        window.attributes('-alpha',1)
    
def set_w_h():
    global x_start
    global x_end 
    global x_final 
    global y_start 
    global y_end 
    global y_final 
    global width
    global height 

    if x_start < x_end:
        width = x_end - x_start
        x_final = x_start
    else:
        width = x_start - x_end
        x_final = x_end
    if y_start < y_end:
        height = y_end - y_start
        y_final = y_start
    else:
        height = y_start - y_end
        y_final = y_end

def do_text_recog():
    global x_final
    global y_final
    global width
    global height
    image = ag.screenshot(region = (x_final, y_final, width, height))
    result = pytesseract.image_to_string(image)
    global text_area
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", result)

window.mainloop()


