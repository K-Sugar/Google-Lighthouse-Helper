#Version 0.7

try:
    from tkinter import *
    from tkinter import filedialog
except:
    from Tkinter import *
    from Tkinter import filedialog

import os

CWD = os.getcwd()




def file_open():                                                                                                                                                # Function to call the Filedialog to then set the Var. for Lighthouse (DOESNT WORK FFS)
    global text
    global file

    linkfile = filedialog.askopenfile(initialdir = CWD,title = "Links.txt auswaehlen", filetypes=(("Textfile","*.txt"),("Alle Dateien","*.*")))
    if linkfile is None:
        return
    file = open(linkfile.name, mode="r")

    links = linkfile.read()
    text.config(state="normal")
    text.delete(0.0,END)
    text.insert(END,links)
    text.config(state="disable")

def start_lighthouse():                                                                                                                                         # Function to send google lighthouse command to cmd (works but doesnt get the right input)
    global file
    global reportlocation
    for url in file:
        print(url)
        os.system("lighthouse --disable-device-emulation --throttling-method=provided --preset=perf --quiet --output-path={}/Report.html {}".format(reportlocation,url))

def quit_all():                                                                                                                                                 # Explains itself
    root.destroy()
    raise SystemExit(1)

def report_location():
    global reportlocation
    reportlocation = filedialog.askdirectory()
    print(reportlocation)


root = Tk()
root.geometry("900x340")
root.config(background="gray26")
root.resizable(width=False, height=False)


text=Text(root)
text.config(state='disable', wrap="none", width=50, height=21, background="gray64", foreground="black")
text.grid(row=1, column=1)


settings=LabelFrame(root, text="Einstellungen")
settings.config(width=495, height=340)
settings.grid(row=1, column=2)

###Buttons###

OpenLink = Button(text, text="Linkdatei öffnen", command=file_open)
OpenLink.place(in_=text, x=305, y=312)

ReportLocation = Button(root, text="Select Savelocation", command=report_location)
ReportLocation.place(x=750, y=150)

Start_Ligthouse = Button(root, text="Starten", command=start_lighthouse)
Start_Ligthouse.place(x=850, y=312)

Quit_All = Button(root, text="Beenden", command=quit_all)
Quit_All.place(x=850, y=0)

root.mainloop()
