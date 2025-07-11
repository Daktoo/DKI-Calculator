import math
import webbrowser
import tkinter as tk
from fractions import Fraction
import os
from PIL import Image, ImageTk

# Tooltip class for displaying tooltips :p
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwin = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwin or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tipwin = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(tw, text=self.text, bg="black", fg="white",
                 relief="solid", borderwidth=1, font=("Arial", 9)).pack(ipadx=4, ipady=2)

    def hide(self, event=None):
        if self.tipwin:
            self.tipwin.destroy()
            self.tipwin = None


# State
expr = ""     
mem = None   
history = []  

# GUI handles
root = None
display = None
entry_box = None
imgRef = None

def press(val):
    global expr
    expr += str(val)
    display.set(expr)

def equal():
    global expr, imgRef, entry_box

    # easter egg o.o
    if expr.strip().replace(" ", "") in ["28/08", "28/8"]:
        display.set("It's me!")
        if entry_box: entry_box.grid_forget()
        if imgRef: imgRef.destroy()
        if os.path.exists("dak.png"):
            img = Image.open("dak.png")
            w, h = 250, 40
            if entry_box:
                w = max(entry_box.winfo_width(), w)
                h = max(entry_box.winfo_height(), h)
            img.thumbnail((w, h), Image.Resampling.LANCZOS)
            thumb = ImageTk.PhotoImage(img)
            imgRef = tk.Label(root, image=thumb)
            imgRef.image = thumb
            imgRef.grid(row=0, column=0, columnspan=6, pady=10, sticky="nsew")
        else:
            display.set("dak.png not found.")
        expr = ""
        return

    try:
        scope = {**vars(math), "Fraction": Fraction}
        temp_result = eval(expr, {"__builtins__": None}, scope)
        display.set(str(temp_result))
        history.append(f"{expr} = {temp_result}")
        expr = str(temp_result)
        if imgRef: 
            imgRef.destroy()
            imgRef = None
        if entry_box and not entry_box.winfo_ismapped():
            entry_box.grid(row=0, column=0, columnspan=6, ipadx=8, ipady=10, pady=10, padx=10, sticky="nsew")
    except Exception as boo:
        display.set(f"Error: {boo}")
        expr = ""

def clear():
    global expr, imgRef
    expr = ""
    display.set("")
    if imgRef:
        imgRef.destroy()
        imgRef = None
    if entry_box:
        entry_box.grid(row=0, column=0, columnspan=0, ipadx=8, ipady=10, pady=10, padx=10, sticky="nsew")

def dec_to_frac():
    global expr
    if not expr:
        display.set("Nothing to convert")
        return
    try:
        fenv = {**vars(math), "Fraction": Fraction}
        val = eval(expr, {"__builtins__": None}, fenv)
        f = Fraction(str(val)).limit_denominator()
        display.set(str(f))
        expr = str(f)
    except:
        display.set("An error occurred")
        expr = ""

def memory_save():
    global mem, expr
    try:
        mem = eval(expr, {"__builtins__": None}, {**vars(math), "Fraction": Fraction})
        display.set("Saved")
        expr = ""
    except:
        display.set("Error")
        expr = ""

def memory_recall():
    global expr
    if mem is not None:
        expr += str(mem)
        display.set(expr)
    else:
        display.set("Empty")

def memory_clear():
    global mem
    mem = None
    display.set("Memory Cleared")

def show_history():
    if history:
        display.set("\n".join(history))
    else:
        display.set("No history")

def open_website(event=None):
    webbrowser.open_new("https://www.daktoinc.co.uk")

resize_timer = None

def resize_background(event):
    global resize_timer
    if resize_timer:
        root.after_cancel(resize_timer)
    resize_timer = root.after(150, lambda: do_resize(event.width, event.height))

def do_resize(w, h):
    global bg_img_ref, bg_original
    new_bg = bg_original.resize((w, h), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(new_bg)
    bg_img_ref.config(image=bg)
    bg_img_ref.image = bg

# MAIN GUI RUNNER
def run_gui():
    global root, display, entry_box, imgRef
    root = tk.Tk()
    root.title("Dakto INC Calculator")
    root.configure(bg="black")
    root.geometry("430x570")

    display = tk.StringVar()
    imgRef = None

    # load background if exists
    if os.path.exists("background.png"):
        global bg_original, bg_img_ref
        bg_original = Image.open("background.png")
        initial = bg_original.resize((430, 570), Image.Resampling.LANCZOS)
        init_img = ImageTk.PhotoImage(initial)
        bg_img_ref = tk.Label(root, image=init_img)
        bg_img_ref.image = init_img
        bg_img_ref.place(x=0, y=0, relwidth=1, relheight=1)
        root.bind("<Configure>", resize_background)

    entry_box = tk.Entry(root, textvariable=display, font=('Arial', 14))
    entry_box.grid(columnspan=4, ipadx=70, ipady=10, pady=10)

    # button definitions
    btns = [
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

    for text, row, col in btns:
        if text == '=':
            fn = equal
        elif text == 'C':
            fn = clear
        elif text == 'Frac-Dec':
            fn = dec_to_frac
        elif text == 'M+':
            fn = memory_save
        elif text == 'MR':
            fn = memory_recall
        elif text == 'MC':
            fn = memory_clear
        elif text == 'History':
            fn = show_history
        elif text == '^':
            fn = lambda: press('**')
        elif text == 'Fraction':
            fn = lambda: press('Fraction(')
        else:
            fn = lambda t=text: press(t)

        tk.Button(root, text=text, command=fn, height=2, width=9).grid(
            row=row, column=col, padx=2, pady=2, sticky="nsew")

    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    for j in range(6):
        root.grid_columnconfigure(j, weight=1)

    # show icon if available
    if os.path.exists("dki-icon.png"):
        icon = Image.open("dki-icon.png").resize((38, 38), Image.Resampling.LANCZOS)
        icon_img = ImageTk.PhotoImage(icon)
        icon_btn = tk.Label(root, image=icon_img, bg="black", cursor="hand2")
        icon_btn.image = icon_img
        icon_btn.grid(row=99, column=5, sticky="e", padx=5, pady=5)
        icon_btn.bind("<Button-1>", open_website)
        Tooltip(icon_btn, "Go to Dakto INC website")

    root.mainloop()

run_gui()
