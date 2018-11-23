#Version 0.8

try:
    from tkinter import *
    from tkinter import filedialog
    from tkinter import messagebox
    import configparser 
    from threading import *
    import os

except:
    from Tkinter import *
    from Tkinter import filedialog
    from Tkinter import messagebox
    from threading import *
    import configparser
    import os


### Variables ###

CWD = os.getcwd()
keepfiles = 2
filenumber = 0
instantkill = False
config = configparser.ConfigParser()

#####################################################################


### Defs ###

def file_open():                                                                                                                                                # Function to call the Filedialog to then set the Var. for Lighthouse (DOESNT WORK FFS)
    global text
    global file

    linkfile = filedialog.askopenfile(initialdir = CWD,title = "Links.txt auswaehlen", filetypes=(("Textfile","*.txt"),("Alle Dateien","*.*")))
    if linkfile is None:
        return
    file = open(linkfile.name, mode="r")

    links = linkfile.read()
    #text.config(state="normal")
    text.delete(0.0,END)
    text.insert(END,links)
    #text.config(state="disable")


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

#####################################################################


### Window ###

root = Tk()
root.withdraw()
root.geometry("900x340")
root.config(background="gray26")
root.title("SEO Helper")
root.resizable(width=False, height=False)

#####################################################################


### Threads ###

lighthouse_thread = Thread(target=start_lighthouse, daemon=True)

#####################################################################


### Frames ###

settings=LabelFrame(root, text="Einstellungen")
settings.config(width=495, height=340)
settings.grid(row=1, column=2)
settings.grid_propagate(False)

Keepfile_Frame=LabelFrame(settings, text="Keep files if Duplicate?")
Keepfile_Frame.config(width=150, height=200)
Keepfile_Frame.grid(in_=settings, row = 1, column = 1)

#####################################################################


### Widgets ###

text=Text(root)
text.config(wrap="none", width=50, height=21, background="gray64", foreground="black")
text.grid(row=1, column=1)

#####################################################################


###Buttons###

OpenLink = Button(text, text="Linkdatei öffnen", command=file_open)
OpenLink.place(in_=text, x=305, y=312)

ReportLocation = Button(root, text="Select Savelocation", command=report_location)
ReportLocation.place(x=750, y=150)

Start_Ligthouse = Button(root, text="Starten", command=lighthouse_thread.start)
Start_Ligthouse.place(x=850, y=312)

Quit_All = Button(root, text="Beenden", command=quit_all)
Quit_All.place(x=835, y=15)

#####################################################################


### Google Lighthouse Settings ###                                                                                                                              # Everything for Google Lighthouse

Keepfiles_Check = Checkbutton(settings, text="Keep duplicate files")
Keepfiles_Check.grid(in_=Keepfile_Frame, row = 1, column = 1)

#####################################################################


### First run check ###
config.read("config.ini")
print(config["DEFAULT"].getboolean("FirstRun"))


while True:

    if config["DEFAULT"].getboolean("FirstRun") == True:

        try:
            os.system("npm -v")
            
            try:
                os.system("npm show lighthouse version")
                break
                

            
            except OSError:
                answer = messagebox.askyesno("Warning!","It seems like you don't have the Google lighthouse Package installed. Should the program install it for you?")

                if answer == True:
                    print("installed")
                    root.deiconify()

                elif answer == False:
                    print("quit")
                    root.deiconify()
                    quit_all()

            break
                
        except OSError:
            messagebox.showwarning("Warning","It seems like you don't have NPM installed. Please install it and restart the Program!")
            quit_all()
root.deiconify()



#####################################################################


root.mainloop()
