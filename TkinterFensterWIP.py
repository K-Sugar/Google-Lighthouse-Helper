try:
    from tkinter import *
    from tkinter import filedialog
except:
    from Tkinter import *
    from Tkinter import filedialog

import os



CWD = os.getcwd()
def donothing():
    print("a")

def file_open():
    global text
    linkfile = filedialog.askopenfile(initialdir = CWD,title = "Links.txt auswaehlen", filetypes=(("Textfile","*.txt"),("Alle Dateien","*.*")))
    links = linkfile.read()
    text.config(state="normal")
    text.delete(0.0,END)
    text.insert(END,links)
    text.config(state="disable")

    
 

root = Tk()
root.geometry("900x340")
root.config(background="gray26")
menubar=Menu(root)


text=Text(root)
text.config(state='disable', wrap="none", width=50, height=21, background="gray64")
text.grid(row=1, column=1)


OpenLink = Button(text, text="Linkdatei öffnen", command=file_open)
OpenLink.place(in_=text, x=305, y=312)


settings = LabelFrame(root, text="Einstellungen")
settings.config(width=495, height=340)
settings.grid(row=1, column=2)


root.mainloop()  
