#Version 0.8.5

try:
    from tkinter import *
    from tkinter import ttk
    from tkinter.ttk import *
    from tkinter import filedialog
    from tkinter import messagebox
    import configparser
    import threading
    from multiprocessing import Process
    import os

except:
    from Tkinter import *
    from Tkinter import filedialog
    from Tkinter import messagebox
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

### Design Vars ###


#####################################################################


### Threads ###

lighthouse_thread = threading.Thread(daemon=True)

#####################################################################


### Defs ###



def CheckInOut():
    global CheckIn
    global CheckOut

    if CheckIn and CheckOut == True:
        Start_Ligthouse.config(state= NORMAL)


    elif CheckIn and CheckOut == False:
        if has_started == False:
            Start_Ligthouse.config(state= DISABLED)
        else:
            pass

    root.after(100, CheckInOut)

#def InputCheck():
#    global CheckIn
#    global text
#    global file
#    global textEdit
#
#    textEdit = text.edit_modified()
#
#    if textEdit == 1:
#        CheckIn = True
#
#    elif textEdit == 0:
#        CheckIn = False
#    root.after(100, InputCheck)

def remember_location():
    global OldCheck
    global config


    if OldCheck != RememberLocationVar.get() or config["LIGHTHOUSE"]["output_path"]  != reportlocation:

        if RememberLocationVar.get() == 1:

            config.set("LIGHTHOUSE", "output_path", "{}".format(reportlocation))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            print(" Output was set ")
            OldCheck = 1


        elif OldCheck == 1 and RememberLocationVar.get() == 0:
            config.set("LIGHTHOUSE", "output_path", "{}".format("no path"))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            print(" Output was emptied ")
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
        print("1")
        CheckIn = False
        return

    elif linkfile is not None:
        print("2")
        print(linkfile.name)
        file = open(linkfile.name, mode="r")
        num_lines = sum(1 for line in file)
        file = open(linkfile.name, mode="r")

        CheckIn = True




    print(num_lines)

    links = linkfile.read()
    text.delete(0.0,END)
    text.insert(END,links)



def start_lighthouse():                                                                                                                                         # Function to send google lighthouse command to cmd (works but doesnt get the right input)
    global filenumber
    global linkfile
    global reportlocation
    global instantkill
    global file
    global CheckIn
    global CheckOut
    global text

    Start_Ligthouse.config(state= DISABLED)
    for url in file:

        url = url.rstrip("\n")
        print(url)
        import time
        time.sleep(0.1)
        filename = url.replace("https","").replace("/","-").replace("\n","").replace(":","").replace("--","")

        if os.path.isfile(reportlocation + "/" + filename + ".html"):
            print("EXISTS!")
            filenumber = 2
            while Keepfilesvar == 1:                                                                                                                                         # True muss durch Keepfiles ersetzt werden!
                newfilename = filename + "{}".format(filenumber)
                if not os.path.isfile(reportlocation + "/" + newfilename + ".html"):
                    filename = newfilename
                    break
                filenumber += 1
        if instantkill:
            break


        os.system("lighthouse --disable-device-emulation --throttling-method=provided --preset=perf --quiet --output-path={}/{}.html {}".format(reportlocation,filename,url))
    has_started = True
    file = open(linkfile.name, mode="r")
    CheckInOut()





def quit_all():                                                                                                                                                 # Explains itself
    global instantkill

    root.destroy() #and DesingPicker.destroy()
    instantkill = True
    SystemExit(0)


def report_location():
    global CheckOut
    global reportlocation
    reportlocation = filedialog.askdirectory()

    if len(reportlocation) > 0:
        print(reportlocation)
        Remember_Location.config(state=NORMAL)
        root.after(100,remember_location)
        CheckOut = True
    else:
        return

def create_thread():
    print("Thread Created")
    lighthouse_thread = threading.Thread(target=start_lighthouse)
    lighthouse_thread.start()
#####################################################################


### Window ###

root = Tk()
root.withdraw()
root.geometry("900x340")
root.config(background="snow")
root.title("SEO Helper")
#root.resizable(width=False, height=False)
root.grid_propagate(False)


#DesingPicker = Tk()
#DesingPicker.withdraw()
#DesingPicker.geometry("200x200")
#DesingPicker.config(background="gold")
#DesingPicker.resizable(width=False, height=False)
#DesingPicker.title("Design Picker")

#####################################################################


### Threads ###




#####################################################################

style = ttk.Style()

### Frames ###



entry_frame=Frame(root)
entry_frame.config(width=415, height=340)
entry_frame.grid(in_=root, row=1, column=1)
entry_frame.grid_propagate(False)

settings=Frame(root)
settings.config(width=355, height=340)
settings.grid(in_=root, row=1, column=2)
settings.grid_propagate(False)

right_frame=Frame(root)
right_frame.config(width=130, height=340)
right_frame.grid(in_=root, row=1, column=3)
right_frame.grid_propagate(False)

lighthouse_frame=LabelFrame(settings, text="Google Lighthouse Settings")
lighthouse_frame.config(width=350, height=260)
lighthouse_frame.grid(in_=settings, row = 1, column = 1)

file_options_frame=ttk.LabelFrame(settings, text="File Options")
file_options_frame.config(width=250, height=200)
file_options_frame.grid(in_=settings, row = 2, column = 1)
file_options_frame.grid_propagate(False)


#####################################################################


### Widgets ###

text=Text(root)
text.config(wrap="none", width=50, height=21, background="gray64", foreground="black")
text.place(in_=entry_frame)
#root.after(100, InputCheck)

status=Text(right_frame)
status.config(wrap="word", width=15, height=13, background="gray64", foreground="black")
status.grid(in_=right_frame, row = 3, column = 1)

status_text=Label(right_frame, text="Status", foreground="black")
status_text.grid(in_=right_frame, row=2, column=1)


#####################################################################






###Buttons###

OpenLink = Button(text, text="Linkdatei öffnen", command=file_open)
OpenLink.place(in_=text, x=305, y=312)

ReportLocation = Button(file_options_frame, text="Select Savelocation", command=report_location)
ReportLocation.grid(in_=file_options_frame, row = 1, column = 1)

Start_Ligthouse = Button(right_frame, text="Starten", command=create_thread, width = 19)
Start_Ligthouse.grid(in_=right_frame, row = 4, column = 1, pady=30)
Start_Ligthouse.config(state=DISABLED)
root.after(100, CheckInOut)

Quit_All = Button(right_frame, text="Beenden", command=quit_all)
Quit_All.grid(in_=right_frame, row = 1, column = 1, pady=10)

#####################################################################


### Google Lighthouse Vars ###

Keepfilesvar = IntVar()
RememberLocationVar = IntVar()
device_emulation = IntVar()

#####################################################################

def LighthouseSettings():
    global DeviceEmulationVar





### Google Lighthouse Settings ###                                                                                                                              # Everything for Google Lighthouse

Keepfiles_Check = Checkbutton(settings, text="Keep duplicate files", variable=Keepfilesvar)
Keepfiles_Check.grid(in_=file_options_frame, row = 1, column = 2)

Remember_Location = Checkbutton(settings, text="Remember Location?", variable=RememberLocationVar)
Remember_Location.grid(in_=file_options_frame, row = 2, column = 1)
Remember_Location.config(state=DISABLED)

Device_Emulation = Checkbutton()



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
                    print("installed")
                    root.deiconify()

                    DesingPicker.deiconify()


                elif answer == False:
                    messagebox.showwarning("Warning","This tool won't work unless the Google Lighthouse Package is installed, please install it yourself!")

                    print("quit")
                    root.deiconify()
                    quit_all()

            break

        except OSError:
            messagebox.showwarning("Warning","It seems like you don't have NPM installed. Please install it and restart the Program!")
            quit_all()
    elif config["DEFAULT"].getboolean("FirstRun") == False:
        root.deiconify()
        #DesingPicker.deiconify()
        #DesingPicker.lift()
        #DesingPicker.attributes('-topmost',True)
        #DesingPicker.attributes('-toolwindow',True)
        break

# Check for saved Path #
if config["LIGHTHOUSE"]["output_path"] != "no path":
    RememberLocationVar.set(1)
    OldCheck = 1
    reportlocation = config["LIGHTHOUSE"]["output_path"]
    print("reportlocation was set to saved path")
    CheckOut = True
    Remember_Location.config(state=NORMAL)
else:
    RememberLocationVar.set(0)
    OldCheck = 0
    print("No saved report location was found")
    CheckOut = False
    Remember_Location.config(state=DISABLED)


#####################################################################
root.mainloop()


#DesingPicker.mainloop()
