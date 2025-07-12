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

class Calculator:
    def __init__(self, root):
        self.expr = ""
        self.mem = None
        self.history = []
        self.root = root
        self.display = tk.StringVar()
        self.entry_box = None
        self.imgRef = None
        self.bg_img_ref = None
        self.bg_original = None
        self.resize_timer = None
        self.setup_gui()

    def safe_eval(self, expr):
        scope = {**vars(math), "Fraction": Fraction}
        return eval(expr, {"__builtins__": None}, scope)

    def press(self, val):
        self.expr += str(val)
        self.display.set(self.expr)

    def equal(self):
        # easter egg o.o
        if self.expr.strip().replace(" ", "") in ["28/08", "28/8"]:
            self.display.set("It's me!")
            if self.entry_box: self.entry_box.grid_forget()
            if self.imgRef: self.imgRef.destroy()
            if os.path.exists("dak.png"):
                img = Image.open("dak.png")
                w, h = 250, 40
                if self.entry_box:
                    w = max(self.entry_box.winfo_width(), w)
                    h = max(self.entry_box.winfo_height(), h)
                img.thumbnail((w, h), Image.Resampling.LANCZOS)
                thumb = ImageTk.PhotoImage(img)
                self.imgRef = tk.Label(self.root, image=thumb)
                self.imgRef.image = thumb
                self.imgRef.grid(row=0, column=0, columnspan=6, pady=10, sticky="nsew")
            else:
                self.display.set("dak.png not found.")
            self.expr = ""
            return
        try:
            temp_result = self.safe_eval(self.expr)
            self.display.set(str(temp_result))
            self.history.append(f"{self.expr} = {temp_result}")
            self.expr = str(temp_result)
            if self.imgRef:
                self.imgRef.destroy()
                self.imgRef = None
            if self.entry_box and not self.entry_box.winfo_ismapped():
                self.entry_box.grid(row=0, column=0, columnspan=6, ipadx=8, ipady=10, pady=10, padx=10, sticky="nsew")
        except Exception as boo:
            self.display.set(f"Error: {boo}")
            self.expr = ""

    def clear(self):
        self.expr = ""
        self.display.set("")
        if self.imgRef:
            self.imgRef.destroy()
            self.imgRef = None
        if self.entry_box:
            self.entry_box.grid(row=0, column=0, columnspan=0, ipadx=8, ipady=10, pady=10, padx=10, sticky="nsew")

    def dec_to_frac(self):
        if not self.expr:
            self.display.set("Nothing to convert")
            return
        try:
            val = self.safe_eval(self.expr)
            f = Fraction(str(val)).limit_denominator()
            self.display.set(str(f))
            self.expr = str(f)
        except:
            self.display.set("An error occurred")
            self.expr = ""

    def memory_save(self):
        try:
            self.mem = self.safe_eval(self.expr)
            self.display.set("Saved")
            self.expr = ""
        except:
            self.display.set("Error")
            self.expr = ""

    def memory_recall(self):
        if self.mem is not None:
            self.expr += str(self.mem)
            self.display.set(self.expr)
        else:
            self.display.set("Empty")

    def memory_clear(self):
        self.mem = None
        self.display.set("Memory Cleared")

    def show_history(self):
        if self.history:
            self.display.set("\n".join(self.history))
        else:
            self.display.set("No history")

    def open_website(self, event=None):
        webbrowser.open_new("https://www.daktoinc.co.uk")

    def resize_background(self, event):
        if self.resize_timer:
            self.root.after_cancel(self.resize_timer)
        self.resize_timer = self.root.after(150, lambda: self.do_resize(event.width, event.height))

    def do_resize(self, w, h):
        if self.bg_original and self.bg_img_ref:
            new_bg = self.bg_original.resize((w, h), Image.Resampling.LANCZOS)
            bg = ImageTk.PhotoImage(new_bg)
            self.bg_img_ref.config(image=bg)
            self.bg_img_ref.image = bg

    def setup_gui(self):
        self.root.title("Dakto INC Calculator")
        self.root.configure(bg="black")
        self.root.geometry("430x570")
        self.imgRef = None
        # load background if exists
        if os.path.exists("background.png"):
            self.bg_original = Image.open("background.png")
            initial = self.bg_original.resize((430, 570), Image.Resampling.LANCZOS)
            init_img = ImageTk.PhotoImage(initial)
            self.bg_img_ref = tk.Label(self.root, image=init_img)
            self.bg_img_ref.image = init_img
            self.bg_img_ref.place(x=0, y=0, relwidth=1, relheight=1)
            self.root.bind("<Configure>", self.resize_background)
        self.entry_box = tk.Entry(self.root, textvariable=self.display, font=('Arial', 14))
        self.entry_box.grid(columnspan=4, ipadx=70, ipady=10, pady=10)
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
        actions = {
            '=': self.equal,
            'C': self.clear,
            'Frac-Dec': self.dec_to_frac,
            'M+': self.memory_save,
            'MR': self.memory_recall,
            'MC': self.memory_clear,
            'History': self.show_history,
            '^': lambda: self.press('**'),
            'Fraction(': lambda: self.press('Fraction(')
        }
        for text, row, col in btns:
            fn = actions.get(text, lambda t=text: self.press(t))
            tk.Button(self.root, text=text, command=fn, height=2, width=9).grid(
                row=row, column=col, padx=2, pady=2, sticky="nsew")
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(6):
            self.root.grid_columnconfigure(j, weight=1)
        # show icon if available
        if os.path.exists("dki-icon.png"):
            icon = Image.open("dki-icon.png").resize((38, 38), Image.Resampling.LANCZOS)
            icon_img = ImageTk.PhotoImage(icon)
            icon_btn = tk.Label(self.root, image=icon_img, bg="black", cursor="hand2")
            icon_btn.image = icon_img
            icon_btn.grid(row=99, column=5, sticky="e", padx=5, pady=5)
            icon_btn.bind("<Button-1>", self.open_website)
            Tooltip(icon_btn, "Go to Dakto INC website")

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
