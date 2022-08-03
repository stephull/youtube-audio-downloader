import tkinter as tk 
from tkinter import filedialog
import subprocess, os, re

# stack for queueing multiple items
URLLIST = []

# dimensions
windowHeight = 420
windowWidth = 625
windowScaling = 1.5

# essential Tkinter window items
root = tk.Tk()
root.title("YouTube Audio Downloader")
root.tk.call('tk', 'scaling', windowScaling)
root.geometry(f"{windowWidth}x{windowHeight}")

# variable for directory 
savetofolder = os.getcwd()
savetofolder = savetofolder.replace("\\", "/")

# dynamic labels (change based on actions of user)
cwdlabel = tk.Label(root, text=f"Currently saved in: {savetofolder}", bg='yellow', fg='black')
donelabel = tk.Label(root, text="Complete!", fg='black', bg='green2')
exceptionlabel = tk.Label(root, text="Error, link could not be completed!", bg='red', fg='white')

# input Youtube URL 
inputlabel = tk.Label(root, text="::: YouTube Audio Downloader :::\n\nInsert YouTube link...")
inputlabel.grid(row=0, column=0, padx=2, pady=5)
inputtxt = tk.Text(root, height=2, width=40)
inputtxt.configure(font=("Helvetica", 10))
inputtxt.grid(row=1, column=0, padx=5, pady=10)

#
#
#

# choose directory
# ... save to chosen directory if user wants specific directory
def saveto():
    global savetofolder
    savetofolder = filedialog.askdirectory(initialdir=os.path.normpath("/mnt/c/"), title="Save to Folder")
    cwdlabel.configure(text=f"Currently saved in {savetofolder}", bg='yellow', fg='black')

outputdirlabel = tk.Label(root, text='Where do you want to save the audio?')
outputdirlabel.grid(row=2, column=0, padx=2, pady=5)
outputbtn = tk.Button(root, text='Save to...', command=saveto, bg='green', fg='white')
outputbtn.grid(row=2, column=1, padx=2, pady=5)
cwdlabel.grid(row=3, column=0, padx=2, pady=5)

# button & command to download immediately
# ... save link and refine using regex, ensures link is readable in Bash
youtubeURL = None
def convert(link):
    global savetofolder, youtubeURL
    if savetofolder.startswith("C:/"):
        savetofolder = savetofolder.replace("C:/", "/mnt/c/")
    savetofolder = f"{savetofolder}/"
    
    channelURI = "&ab_"
    youtubeURL = re.sub(f'({channelURI})\w+=[\w\d\$\_\-]+', '', link)
    
    bashCmd = f"bash ./convert.sh {savetofolder} {youtubeURL}"
    process = subprocess.Popen(bashCmd.split(), stdout=subprocess.PIPE)
    
    output, err = process.communicate()
    if (err != None):
        print(f"::: ERROR :::\n{err}")
        exceptionlabel.grid(row=9, column=0, padx=2, pady=5)
    else:
        print(f"::: OUTPUT :::\n{output}")
        donelabel.grid(row=9, column=0, padx=2, pady=5)
    inputtxt.delete("1.0", "end-1c")
    
def download():
    inp = inputtxt.get(1.0, "end-1c")
    if len(inp) > 0:
        convert(inp)
downloadNowButton = tk.Button(root, command=download, text='Download', bg='blue', fg='white')
downloadNowButton.grid(row=1, column=1, padx=2, pady=5)

# button and command to add to queue
def addtoqueue():
    inp = inputtxt.get("1.0", "end-1c")
    tmp_index = len(URLLIST)
    URLLIST.append(inp)
    listcanvas.insert(tmp_index, URLLIST[tmp_index])
    inputtxt.delete("1.0", "end-1c")
addToQueueButton = tk.Button(root, command=addtoqueue, text='Add To Queue', bg='purple', fg='white')
addToQueueButton.grid(row=1, column=2, padx=2, pady=5)

# button and commmand for downloading all links
def downloadAll():
    for i in range(len(URLLIST)):
        print(URLLIST[i])
        tmp_download = listcanvas.get(0)
        convert(tmp_download)
        listcanvas.delete(0)
    URLLIST.clear()
downloadAllButton = tk.Button(root, command=downloadAll, text='Download All', bg='blue', fg='white')
downloadAllButton.grid(row=6, column=1, padx=2, pady=5)

#
#
#

# components of tkinter window
msglabel = tk.Label(root, text="Window freezes when downloading, wait until you see 'Complete!'")
msglabel.grid(row=7, column=0, padx=2, pady=5)

# show list from URLLIST
listcanvaslabel = tk.Label(root, text='Queue')
listcanvaslabel.grid(row=5, column=0, padx=5, pady=5)
listcanvas = tk.Listbox(root, height=5, width=50, bg='grey', activestyle='dotbox', fg='white')
for i in range(len(URLLIST)):
    listcanvas.insert(i, URLLIST[i])
listcanvas.grid(row=6, column=0, padx=2, pady=5)

root.mainloop()