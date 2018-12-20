#Version 0.8.5

try:
    from tkinter import *
    from tkinter import ttk
    from tkinter.ttk import *
    from tkinter import filedialog
    from tkinter import messagebox
    from datetime import date
    import configparser
    import threading
    import os

except:
    from Tkinter import *
    from Tkinter import filedialog
    from Tkinter import messagebox
    from datetime import date
    import threading
    import configparser
    import os


### Variables ###

CWD = os.getcwd()
keepfiles = 2
filenumber = 0
instantkill = False
config = configparser.ConfigParser()
CheckIn = False
CheckOut = False
config.read("config.ini")
has_started = False
OldCheck = 2
num_lines = 0
date = str(date.today())
### Design Vars ###


#####################################################################



#####################################################################


### Defs ###



def CheckInOut():
    global CheckIn
    global CheckOut

    if CheckIn and CheckOut == True and throttling_menu.current() != -1:
        Start_Ligthouse.config(state= NORMAL)

    elif CheckIn and CheckOut == False:
        if has_started == False:
            Start_Ligthouse.config(state= DISABLED)
        else:
            Start_Ligthouse.config(state= NORMAL)

    root.after(100, CheckInOut)


def remember_location():
    global OldCheck
    global config


    if OldCheck != RememberLocationVar.get() or config["LIGHTHOUSE"]["output_path"]  != reportlocation:

        if RememberLocationVar.get() == 1:

            config.set("LIGHTHOUSE", "output_path", "{}".format(reportlocation))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            OldCheck = 1


        elif OldCheck == 1 and RememberLocationVar.get() == 0:
            config.set("LIGHTHOUSE", "output_path", "{}".format("no path"))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            OldCheck = 0


    root.after(100,remember_location)



def file_open():                                                                                                                                                # Function to call the Filedialog to then set the Var. for Lighthouse (DOESNT WORK FFS)
    global text
    global file
    global CheckIn
    global textEdit
    global linkfile
    global num_lines

    linkfile = filedialog.askopenfile(initialdir = CWD,title = "Links.txt auswaehlen", filetypes=(("Textfile","*.txt"),("Alle Dateien","*.*")))
    if linkfile is None: # and textEdit == 0:
        CheckIn = False
        return

    elif linkfile is not None:
        file = open(linkfile.name, mode="r")
        num_lines = sum(1 for line in file)
        file = open(linkfile.name, mode="r")

        CheckIn = True





    links = linkfile.read()
    text.delete(0.0,END)
    text.insert(END,links)



def start_lighthouse():                                                                                                                                         # Function to send google lighthouse command to cmd (works but doesnt get the right input)
    global filenumber
    global Keepfilesvar
    global linkfile
    global reportlocation
    global instantkill
    global file
    global CheckIn
    global CheckOut
    global text
    global DevEmuStr
    global throttlingVar
    global presetVar
    global CacheStr

    LighthouseSettings()
    CheckIn = False
    CheckOut = False
    Quit_All.config(state= NORMAL)
    instantkill = False
    Start_Ligthouse.config(state= DISABLED)

    for url in file:

        if instantkill == True:
            file = open(linkfile.name, mode="r")
            CheckInOut()
            break



        url = url.rstrip("\n")
        print(url)
        import time
        time.sleep(0.1)
        filename = url.replace("https","").replace("/","-").replace("\n","").replace(":","").replace("--","")+date

        if os.path.isfile(reportlocation + "/" + filename + ".html"):

            if Keepfilesvar.get() == 1:
                print("File exists, will be kept!")
            elif Keepfilesvar.get() == 0:
                print("File exists, will be replaced!")
            filenumber = 2
            while Keepfilesvar.get() == 1:
                newfilename = filename + "{}".format(filenumber)
                if not os.path.isfile(reportlocation + "/" + newfilename + ".html"):
                    filename = newfilename
                    break
                filenumber += 1



        os.system("lighthouse --quiet {} {} {} {} {} --output-path={}/{}.html ".format(DevEmuStr,throttlingVar,CacheStr,presetVar,url,reportlocation,filename))


    has_started = True
    file = open(linkfile.name, mode="r")
    Start_Ligthouse.config(state=NORMAL)
    if instantkill == True:
        status.config(state=NORMAL)
        status.delete(0.0,END)
        status.config(state=DISABLED)
        print("################################")
        print("You can now safely exit the tool!")
        print("################################")

    Quit_All.config(state= DISABLED)




def quit_all():                                                                                                                                                 # Explains itself
    global instantkill
    instantkill = True
    print("################################")
    print("Stopping, please don't quit yet!")
    print("################################")

def report_location():
    global CheckOut
    global reportlocation
    reportlocation = filedialog.askdirectory()

    if len(reportlocation) > 0:
        print("Reportlocation was set to " + reportlocation)
        Remember_Location.config(state=NORMAL)
        root.after(100,remember_location)
        CheckOut = True
    else:
        return

def create_thread():
    lighthouse_thread = threading.Thread(target=start_lighthouse)
    lighthouse_thread.start()


def print(message):
    status.config(state=NORMAL)
    status.insert(END, message + "\n")
    status.config(state=DISABLED)
    status.see(END)
#####################################################################


### Window ###

root = Tk()
root.withdraw()
root.geometry("990x340")
root.config(background="white")
root.title("SEO Helper")
root.resizable(width=False, height=False)
root.grid_propagate(False)


#####################################################################


### Frames ###



entry_frame=Frame(root)
entry_frame.config(width=415, height=340)
entry_frame.grid(in_=root, row=1, column=1)
entry_frame.grid_propagate(False)

settings=Frame(root)
settings.config(width=575, height=340)
settings.grid(in_=root, row=1, column=2)
settings.grid_propagate(False)

lighthouse_frame=LabelFrame(settings, text="Google Lighthouse Settings")
lighthouse_frame.config(width=400, height=260)
lighthouse_frame.grid(in_=settings, row = 1, column = 1)
lighthouse_frame.grid_propagate(False)

right_frame=Frame(settings)
right_frame.config(width=175)
right_frame.grid(in_=settings, row = 1, column = 2)

file_options_frame=ttk.LabelFrame(right_frame, text="File Options")
file_options_frame.config(width=160, height=200)
file_options_frame.grid(in_=right_frame, row = 1, column = 2)
file_options_frame.grid_propagate(False)


#####################################################################


### Widgets ###

text=Text(entry_frame)
text.config(wrap="none", width=50, height=21, background="gray64", foreground="black")
text.grid(in_=entry_frame, row = 1, column = 1)

#root.after(100, InputCheck)

status=Text(settings)
status.config(wrap="word", width=50, height=4, background="gray64", foreground="black", state = DISABLED)
status.grid(in_=settings, row = 2, column = 1, sticky = W, padx = 2, pady = 5)
status.see(END)


status_text=Label(settings, text="Status", foreground="black")
status_text.grid(in_=settings, row=2, column=1, sticky = N+E)


#####################################################################






###Buttons###

OpenLink = Button(entry_frame, text="Select Linkfile", command=file_open)
OpenLink.grid(in_=entry_frame, row = 1, column = 1, sticky = S+E)

ReportLocation = Button(file_options_frame, text="Select Savelocation", command=report_location)
ReportLocation.grid(in_=file_options_frame, row = 1, column = 1, sticky = W, padx = 5)

Start_Ligthouse = Button(right_frame, text="Start", command=create_thread, width = 19)
Start_Ligthouse.grid(in_=right_frame, row = 2, column = 2)
Start_Ligthouse.config(state=DISABLED)
root.after(100, CheckInOut)

Quit_All = Button(right_frame, text="Stop", command=quit_all, width = 19)
Quit_All.grid(in_=right_frame, row = 3, column = 2)
Quit_All.config(state= DISABLED)
#####################################################################


### Google Lighthouse Vars ###

Keepfilesvar = IntVar()
RememberLocationVar = IntVar()
DeviceEmulationVar = IntVar()
CacheVar = IntVar()

#####################################################################

def LighthouseSettings():
    global DeviceEmulationVar
    global DevEmuStr
    global throttlingVar
    global presetVar
    global ChacheStr
    global CacheStr

    if DeviceEmulationVar.get() == 0:
        DevEmuStr = "--emulated-form-factor=desktop"
    elif DeviceEmulationVar.get() == 1:
        DevEmuStr = "--emulated-form-factor=mobile"

    if throttling_menu.current() == 0:
        throttlingVar = "--throttling-method=provided"

    elif throttling_menu.current() == 1:
        throttlingVar = "--throttling-method=devtools"

    elif throttling_menu.current() == 2:
        throttlingVar = "--throttling-method=simulate"

    if preset_menu.current() == 0:
        presetVar = "--preset=full"
    elif preset_menu.current() == 1:
        presetVar = "--preset=perf"

    if CacheVar.get() == 0:
        CacheStr = ""
    elif CacheVar.get() == 1:
        CacheStr = " --disable-storage-reset"


### Google Lighthouse Settings ###                                                                                                                              # Everything for Google Lighthouse

Keepfiles_Check = Checkbutton(settings, text="Keep duplicate files", variable=Keepfilesvar)
Keepfiles_Check.grid(in_=file_options_frame, row = 3, column = 1, sticky = W, padx = 5)

Remember_Location = Checkbutton(settings, text="Remember Location?", variable=RememberLocationVar)
Remember_Location.grid(in_=file_options_frame, row = 2, column = 1, sticky = W, padx = 5)
Remember_Location.config(state=DISABLED)

throttling_label=Label(lighthouse_frame, text="Throttling Preset:", foreground="black")
throttling_label.grid(in_=lighthouse_frame, row = 0, column = 1, sticky=W, padx=10)

throttling_menu = Combobox(lighthouse_frame, state="readonly", values=["No Throttling","Slow 4G","Fast 4G"])
throttling_menu.grid(in_=lighthouse_frame, row = 0, column = 2)

preset_label=Label(lighthouse_frame, text="Audit Preset:", foreground="black")
preset_label.grid(in_=lighthouse_frame, row = 1, column = 1, sticky=W, padx=10, pady = 5)

preset_menu = Combobox(lighthouse_frame, state="readonly", values=["Full","Performance"])
preset_menu.grid(in_=lighthouse_frame, row = 1, column = 2)

Device_Emulation = Checkbutton(lighthouse_frame, text=" Enable Device Emulation?", variable=DeviceEmulationVar)
Device_Emulation.grid(in_=lighthouse_frame, row = 2, column = 1, sticky = W, padx = (10,25), columnspan=2)

Cache = Checkbutton(lighthouse_frame, text="Keep Cache", variable=CacheVar)
Cache.grid(in_=lighthouse_frame, row = 3, column = 1, sticky = W, padx = (10,25), columnspan=2)

Cooldown_label = Label(right_frame, text="Cooldown (s)", foreground="black")
Cooldown_label.grid(in_=right_frame, row = 4, column = 2)

Cooldown_Entry = Text(right_frame, width = 3, height = 1)
Cooldown_Entry.grid(in_=right_frame, row = 4, column = 2)



#adv_seperator=Separator(lighthouse_frame, orient="horizontal")
#adv_seperator.grid(row=4, column=1, sticky="we")

#####################################################################



















### First run check ###



while True:

    if config["DEFAULT"].getboolean("FirstRun") == True:
        config.set("DEFAULT", "FirstRun", "False")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        try:
            os.system("npm -v")

            try:
                os.system("npm show lighthouse version")
                root.deiconify()
                break



            except OSError:
                answer = messagebox.askyesno("Warning!","It seems like you don't have the Google lighthouse Package installed. Should the program install it for you?")

                if answer == True:
                    os.system("npm install -g lighthouse")

                    root.deiconify()




                elif answer == False:
                    messagebox.showwarning("Warning","This tool won't work unless the Google Lighthouse Package is installed, please install it yourself!")

                    print("quit")
                    root.deiconify()
                    quit_all()

            break

        except OSError:
            messagebox.showwarning("Warning","It seems like you don't have NPM installed. Please install it and restart the Program!")
            SystemExit(0)
    elif config["DEFAULT"].getboolean("FirstRun") == False:
        root.deiconify()
        break

# Check for saved Path #
if config["LIGHTHOUSE"]["output_path"] != "no path":
    RememberLocationVar.set(1)
    OldCheck = 1
    reportlocation = config["LIGHTHOUSE"]["output_path"]
    print("Reportlocation was set to: "+reportlocation)
    print("Please select the Linkfile and Throttling Method")

    CheckOut = True
    Remember_Location.config(state=NORMAL)
else:
    RememberLocationVar.set(0)
    OldCheck = 0
    print("No saved report location was found")
    print("Please select the Linkfile and Throttling Method and select a Savelocation")
    CheckOut = False
    Remember_Location.config(state=DISABLED)


#####################################################################
root.mainloop()
