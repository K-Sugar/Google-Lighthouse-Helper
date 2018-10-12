import os
import time
import sys



# IMPORTANT! #
                                                                                                                                # OS Definieren um OS bedingte commands zu aendern
if sys.platform == "win32" or "win64":
    FindOS = "Windows"
    clear = "cls"
elif sys.platform == "linux" or "linux2":
    FindOS = "Linux"
    clear = "cls"
elif sys.platform == "Darwin":
    FindOS = "Mac"
    clear = "clear"

#####################

try:                                                                                                                            # Versuchen die Link.txt zu oeffnen, falls nicht gefunden werden kann wird Fehler geworfen und beendet.
    file = open("Links.txt", mode="r")
    num_lines = sum(1 for line in open('Links.txt'))
except FileNotFoundError:
    print("Kann 'Links.txt' nicht in " + str(os.getcwd()) + " finden. Bitte stelle sicher das sie existiert!")
    raise SystemExit(0)


#Pfad zu den Reports#
path = "C:/Users/sugar/Desktop/Google_Lighthouse_TEST/reports/"
#####################
                                                                                                                                # Variablen die nicht veraendert werden sollten!
links_done = 0

filenumber = 2

keepfiles = 0

Ja = "ja", "j", "y", "yes"

Nein = "n", "nein", "no"

replacedfiles = 0

#####################








os.system(clear)
print("Reports werden in " + "'" +path + "'" + " gespeichert")
print("OS = " + FindOS)
print("Falls URLs in der Links.txt mehrmals vorkommen, sollen die Dateien ersetzt werden?")

while keepfiles == 0:                                                                                                           # Definierung des Verhalten bei doppelten Links in der Links.txt
    filechoice = input("Ja / Nein :")
    if filechoice.lower() in Ja:
        keepfiles = 1
        print("Doppelte Dateien werden Ueberschrieben!")
        for i in range(5):
            time.sleep(1)
            print(".")
        continue

    if filechoice.lower() in Nein:
        keepfiles = 2
        print("Dateien werden Nummeriert und doppelt behalten!")
        for i in range(5):
            time.sleep(1)
            print(".")
        continue

    elif filechoice.lower() != Ja or Nein:
        keepfiles = 0
        print("Bitte eingabe überprüfen!")


for url in file:
    if links_done != 0:
        s = 15
        for i in range(15):                                                                                                     # Cooldown um verfaelschung der Werte zu vermeiden
            s -= 1
            time.sleep(1)
            os.system(clear)
            print("Cooldown " + str(s) + "s")

    else:
        os.system(clear)
    
    os.system(clear)
    os.system("lighthouse --disable-device-emulation --throttling-method=provided --preset=perf --quiet --output-path=C:/Users/sugar/Desktop/Google_Lighthouse_TEST/Report.html {}".format(url))
    links_done += 1
    print("{} von {} fertig!".format(links_done , num_lines))
    filename = url.replace("https","").replace("/","-").replace("\n","").replace(":","").replace("--","")
    try:
        os.rename("Report.html" , str(path) + "Report_" + str(filename) + ".html")                                              # Umbennen der "Report.html"
    
    except OSError:
        if keepfiles == 1:
            os.remove(str(path) + "Report_" + str(filename) + ".html")                                                          # Falls Daten ueberschieben werden sollen wird hier die alte Datei geloescht
            os.rename("Report.html" , str(path) + "Report_" + str(filename) + ".html")
            print("Datei wurde ersetzt!")
            replacedfiles += 1
        
        elif keepfiles == 2:
            while True:                                                                                                         # Schleife um Daten eine Zahl am ende zu geben damit mehrere existieren koennen
                try:        
                    os.rename("Report.html" , str(path) + "Report_" + str(filename) + str(filenumber) + ".html")
                    break

                except OSError:
                    filenumber += 1

    if links_done == num_lines:
        print("Alle links fertig!")
        print("Es wurden insgesamt [" + str(replacedfiles) + "] Dateien ersetzt")
        break
    else:
        continue

