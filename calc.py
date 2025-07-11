import math
import webbrowser
import tkinter as tk
from fractions import Fraction
import os
from PIL import Image, ImageTk

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x = y = 0
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="black", foreground="white", relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack(ipadx=4, ipady=2)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# Globals
expr = ""
memory = None
history = []
image_label = None
root = None
display = None
entry = None

expr = ""
memory = None
history = []

def press(key):  
    global expr
    expr += str(key)
    display.set(expr)

def equal():
    global expr, image_label, entry, root
    try:
        if expr.strip().replace(" ", "") in ["28/08", "28/8"]:
            display.set("It's me!")
            if entry is not None:
                entry.grid_forget()
            if image_label is not None:
                image_label.destroy()
            if os.path.exists("dak.png"):
                img = Image.open("dak.png")
                if entry is not None:
                    entry_width = entry.winfo_width()
                    entry_height = entry.winfo_height()
                    if entry_width <= 1 or entry_height <= 1:
                        entry_width, entry_height = 250, 40
                else:
                    entry_width, entry_height = 250, 40
                img.thumbnail((entry_width, entry_height), Image.Resampling.LANCZOS)

                img_tk = ImageTk.PhotoImage(img)
                image_label = tk.Label(root, image=img_tk)
                image_label.image = img_tk 
                image_label.grid(row=0, column=0, columnspan=6, pady=10, sticky="nsew")
            else:
                display.set("dak.png not found.")
            expr = ""
            return
        allowed = {**vars(math), "Fraction": Fraction}
        result = eval(expr, {"__builtins__": None}, allowed)
        display.set(str(result))
        history.append(f"{expr} = {result}")
        expr = str(result)
        if image_label is not None:
            image_label.destroy()
            image_label = None
        if entry is not None and not entry.winfo_ismapped():
            entry.grid(row=0, column=0, columnspan=6, ipadx=8, ipady=10, pady=10, padx=10, sticky="nsew")
    except Exception as e:
        display.set(f"Error: {e}")
        expr = ""

def clear():
    global expr, image_label, entry
    expr = ""
    display.set("")
    if image_label:
        image_label.destroy()
        image_label = None
    if entry:
        entry.grid(row=0, column=0, columnspan=0, ipadx=8, ipady=10, pady=10, padx=10, sticky="nsew")

def dec_to_frac():
    global expr
    try:
        if not expr:
            display.set("Nothing to convert")
            return
        allowed_names = {**vars(math), "Fraction": Fraction}
        value = eval(expr, {"__builtins__": None}, allowed_names)
        fraction = Fraction(str(value)).limit_denominator()
        display.set(str(fraction))
        expr = str(fraction)
    except Exception as e:
        display.set("An error occurred")
        expr = ""

def memory_save():
    global memory, expr
    try:
        memory = eval(expr, {"__builtins__": None}, {**vars(math), "Fraction": Fraction})
        display.set("Saved")
        expr = ""
    except:
        display.set("Error")
        expr = ""

def memory_recall():
    global expr
    if memory is not None:
        expr += str(memory)
        display.set(expr)
    else:
        display.set("Empty")

def memory_clear():
    global memory
    memory = None
    display.set("Memory Cleared")

def show_history():
    if history:
        display.set("\n".join(history))
    else:
        display.set("No history")

def open_website(event=None):
    webbrowser.open_new("https://www.daktoinc.co.uk")

resize_after_id = None

def resize_background(event):
    global resize_after_id
    if resize_after_id:
        root.after_cancel(resize_after_id)
    resize_after_id = root.after(150, lambda: do_resize(event.width, event.height))
        
def do_resize(new_width, new_height):
    global background_label, original_bg
    resized = original_bg.resize((new_width, new_height), Image.Resampling.LANCZOS)
    new_bg = ImageTk.PhotoImage(resized)
    background_label.config(image=new_bg)
    background_label.image = new_bg

def run_gui():
    global display, root
    root = tk.Tk()
    root.configure(bg="black")
    root.title("Dakto INC Calculator")
    root.geometry("430x570")

    display = tk.StringVar()
    image_label = None
   
    if os.path.exists("background.png"):
        global original_bg, background_label
        original_bg = Image.open("background.png")
        resized_bg = original_bg.resize((root.winfo_width(), root.winfo_height()), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(resized_bg)
        background_label = tk.Label(root, image=bg_image)
        background_label.image = bg_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        root.bind("<Configure>", resize_background)


        
    entry = tk.Entry(root, textvariable=display, font=('Arial', 14))
    entry.grid(columnspan=4, ipadx=70, ipady=10, pady=10)
    
    # Button rows
    button = [
        ('7',2,0), ('8',2,1), ('9',2,2), ('/',2,3),
        ('4',3,0), ('5',3,1), ('6',3,2), ('*',3,3),
        ('1',4,0), ('2',4,1), ('3',4,2), ('-',4,3),
        ('0',5,0), ('.',5,1), ('=',5,2), ('+',5,3),
        ('sin',6,0), ('cos',6,1), ('tan',6,2), ('sqrt(',6,3),
        ('log10(',7,0), ('ln',7,1), ('^',7,2), ('C',7,3),
        ('Fraction(',8,0), ('π',8,1), ('e',8,2), ('(',8,3),
        (')',9,0), ('Frac-Dec',9,1), ('M+',9,2), ('MR',9,3),
        ('MC',10,0), ('History',10,1)
    ]

    for (text, row, col) in button:
        if text == '=':
            action = equal
        elif text == 'C':
            action = clear
        elif text == 'Frac-Dec':
            action = dec_to_frac
        elif text == 'M+':
            action = memory_save
        elif text == 'MR':
            action = memory_recall
        elif text == 'MC':
            action = memory_clear
        elif text == 'History':
            action = show_history
        elif text == '^':
            action = lambda: press('**')
        elif text == 'Fraction':
            action = lambda: press('Fraction(')
        else:
            action = lambda t=text: press(t)

        Button = tk.Button(root, text=text, command=action, height=2, width=9).grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    for i in range(6):
        root.grid_columnconfigure(i, weight=1)
    
    if os.path.exists("dki-icon.png"):
        icon_img = Image.open("dki-icon.png")
        icon_img = icon_img.resize((38, 38), Image.Resampling.LANCZOS)
        icon_img = ImageTk.PhotoImage(icon_img)
        icon_button = tk.Label(root, image=icon_img, bg="black", cursor="hand2")
        icon_button.image = icon_img
        icon_button.grid(row=99, column=5, sticky="e", padx=5, pady=5)
        icon_button.bind("<Button-1>", open_website)
        Tooltip(icon_button, "Go to Dakto INC website")
    root.mainloop()

run_gui()



