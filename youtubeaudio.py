import tkinter as tk 
from tkinter import filedialog
import subprocess, os, re

# stack for queueing multiple items
URLLIST = ["Song 1", "Song 2", "Song 3"]

# essential Tkinter window items
root = tk.Tk()
root.title("YouTube Audio Downloader")
root.tk.call('tk', 'scaling', 1.5)
canvas1 = tk.Canvas(root, width=250, height=150)
ready = False

# variable for directory 
savetofolder = os.getcwd()
savetofolder = savetofolder.replace("\\", "/")

# dynamic labels (change based on actions of user)
cwdlabel = tk.Label(root, text=f"Currently saved in: {savetofolder}", bg='yellow', fg='black')
donelabel = tk.Label(root, text="Complete!", fg='black', bg='green2')

# input Youtube URL 
inputlabel = tk.Label(root, text="Insert YouTube link...")
inputlabel.pack()
inputtxt = tk.Text(root, height=2, width=60)
inputtxt.pack()

# FUNCTION: save to chosen directory if user wants specific directory
def saveto():
    global savetofolder
    savetofolder = filedialog.askdirectory(initialdir=os.path.normpath("/mnt/c/"), title="Save to Folder")
    cwdlabel.configure(text=f"Currently saved in {savetofolder}", bg='yellow', fg='black')

# instruct user to choose directory and display directory
outputdirlabel = tk.Label(root, text='Where do you want to save the audio?')
outputdirlabel.pack()
outputbtn = tk.Button(root, text='Save to...', command=saveto, bg='blue', fg='white')
outputbtn.pack()
cwdlabel.pack()

# FUNCTION: save link and refine using regex, ensures link is readable in Bash
youtubeURL = None
def convert(link):
    global savetofolder, youtubeURL
    if savetofolder.startswith("C:/"):
        savetofolder = savetofolder.replace("C:/", "/mnt/c/")
    savetofolder = f"{savetofolder}/"
    
    channelURI = "&ab_"
    youtubeURL = re.sub(f'({channelURI})\w+=[\w\d\$\_\-]+', '', link)
    print(youtubeURL)
    
    bashCmd = f"bash ./convert.sh {savetofolder} {youtubeURL}"
    process = subprocess.Popen(bashCmd.split(), stdout=subprocess.PIPE)
    
    output, err = process.communicate()
    if (err != None):
        print(f"::: ERROR :::\n{err}")
    print(f"::: OUTPUT :::\n{output}")
    donelabel.pack()

# ready to download audio from link, triggered when user clicks 'Download'
def download():
    ready = True
    inp = inputtxt.get(1.0, "end-1c")
    if ready and len(inp) > 0:
        convert(inp)

# download all from list of links prepared
def downloadAll():
    pass

# components of tkinter window
button1 = tk.Button(root, text="Download", command=download, bg='blue', fg='white')
canvas1.create_window(120, 60, window=button1)
msglabel = tk.Label(root, text="Window will freeze when downloading, wait until you see 'Complete'")
msglabel.pack()

button2 = tk.Button(root, text="Download All", command=downloadAll, bg='purple', fg='white')
canvas1.create_window(120, 90, window=button2)

# show list from URLLIST
listcanvas = tk.Listbox(root, height=5, width=50, bg='grey', activestyle='dotbox', fg='white')
for i in range(len(URLLIST)):
    listcanvas.insert(i+1, URLLIST[i])
listcanvas.pack()

# finalize everything :-)
canvas1.pack()
root.mainloop()