#Version 0.8

try:
    from tkinter import *
    from tkinter import filedialog
    from threading import *
    import os

except:
    from Tkinter import *
    from Tkinter import filedialog
    from threading import *
    import os

####### Variables #######

CWD = os.getcwd()
keepfiles = 2
filenumber = 0
instantkill = False

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
    global filenumber
    global file
    global reportlocation
    global instantkill
    for url in file:
        print(url)
        filename = url.replace("https","").replace("/","-").replace("\n","").replace(":","").replace("--","")
        
        if os.path.isfile(reportlocation + "/" + filename + ".html"):
            print("EXISTS!")
            filenumber = 2
            while True:                                                                                                                                         # True muss durch Keepfiles ersetzt werden! 
                newfilename = filename + "{}".format(filenumber)
                if not os.path.isfile(reportlocation + "/" + newfilename + ".html"):
                    filename = newfilename
                    break
                filenumber += 1
        if instantkill:
            break
        
        os.system("lighthouse --disable-device-emulation --throttling-method=provided --preset=perf --quiet --output-path={}/{}.html {}".format(reportlocation,filename,url))
        




def quit_all():                                                                                                                                                 # Explains itself
    global instantkill
    root.destroy()
    instantkill = True
    SystemExit(0)

def report_location():
    global reportlocation
    reportlocation = filedialog.askdirectory()
    print(reportlocation)

lighthouse_thread = Thread(target=start_lighthouse, daemon=True)

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

Start_Ligthouse = Button(root, text="Starten", command=lighthouse_thread.start)
Start_Ligthouse.place(x=850, y=312)

Quit_All = Button(root, text="Beenden", command=quit_all)
Quit_All.place(x=850, y=0)

Keepfiles_Check = Checkbutton(master = settings, text="Keep duplicate files")

root.mainloop()
