import tkinter as tk 
from tkinter import filedialog, font
import customytaudioconfigs as config
import subprocess, re, os, sys

# stack for queueing multiple items
URLLIST = []

# dimensions
windowHeight = 480
windowWidth = 630
windowScaling = 1.5
textData = ("Helvetica", 10)
textDataBold = ("Helvetica", 10, font.BOLD)
YOUTUBE_URL_LENGTH = 42

# regex
clearChannel = '(&ab_)\w+=[\w\d\_\-]+'
clearIndices = '^[()]\d+[()]\s'

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
inputlabel = tk.Label(
    root, 
    text="::: YouTube Audio Downloader :::\nInsert YouTube link...",
    font=textDataBold    
)
inputlabel.grid(row=0, column=0, padx=2, pady=5)
inputtxt = tk.Text(root, height=2, width=40)
inputtxt.configure(font=textData)
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

outputdirlabel = tk.Label(root, text='Where do you want to save the audio?', font=textDataBold)
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
    
    youtubeURL = re.sub(clearChannel, '', link)
    
    process = subprocess.Popen(
        ["bash", "./convert.sh", savetofolder, youtubeURL],
        stdout=subprocess.PIPE
    )
    
    output, err = process.communicate()
    print(f"::: ERROR :::\n{err}" if err != None else f"::: OUTPUT :::\n{output}")
    new_label = exceptionlabel if err != None else donelabel
    new_label.grid(row=9, column=0, padx=2, pady=5)
    inputtxt.delete(1.0, "end-1c")
    
def download():
    inp = inputtxt.get(1.0, "end-1c")
    if len(inp) >= YOUTUBE_URL_LENGTH:
        convert(inp) 
downloadNowButton = tk.Button(root, command=download, text='Download', bg='blue', fg='white')
downloadNowButton.grid(row=1, column=1, padx=2, pady=5)

# button and command to add to queue
def addtoqueue():
    inp = inputtxt.get("1.0", "end-1c")
    if len(inp) < YOUTUBE_URL_LENGTH:
        return 
    tmp_index = len(URLLIST)
    URLLIST.append(inp)
    listcanvas.insert(tmp_index, f"({tmp_index}) {URLLIST[tmp_index]}")
    inputtxt.delete(1.0, "end-1c")
addToQueueButton = tk.Button(root, command=addtoqueue, text='Add To Queue', bg='purple', fg='white')
addToQueueButton.grid(row=1, column=2, padx=2, pady=5)

# delete selection from queue (needs index number)
def deletefromqueue():
    try:
        index = int(delFromSelection.get(1.0, "end-1c"))
        delFromSelection.delete(1.0, "end-1c")
    except ValueError:
        return 
    listcanvas.delete(index)
    URLLIST.pop(index)
    for i in range(index, len(URLLIST)):
        list_value = listcanvas.get(i)
        list_value = re.sub(clearIndices, '', list_value)
        listcanvas.delete(i)
        listcanvas.insert(i, f"({i}) {list_value}")
delFromQueueButton = tk.Button(root, command=deletefromqueue, text='Delete Selection', bg='red', fg='white')
delFromQueueButton.grid(row=7, column=1, padx=2, pady=5)

delFrame = tk.Frame(root)
delFromLabel = tk.Label(delFrame, text='Type index number:', font=('Helvetica', 7, font.ITALIC))
delFromLabel.pack()
delFromSelection = tk.Text(delFrame, width=3, height=1)
delFromSelection.pack()
delFrame.grid(row=7, column=2, padx=2, pady=5)

# button and commmand for downloading all links
def downloadAll():
    for i in range(len(URLLIST)):
        print(URLLIST[i])
        downloading = listcanvas.get(0)
        downloading = re.sub(clearIndices, '', downloading)
        convert(downloading)
        listcanvas.delete(0)
    URLLIST.clear()
downloadAllButton = tk.Button(root, command=downloadAll, text='Download All', bg='blue', fg='white')
downloadAllButton.grid(row=6, column=1, padx=2, pady=5)

#
#
#

# components of tkinter window
msglabel = tk.Label(root, text="Window freezes when downloading, wait until you see 'Complete!'")
msglabel.grid(row=8, column=0, padx=2, pady=5)

# show list from URLLIST
listcanvaslabel = tk.Label(root, text='Queue', font=textDataBold)
listcanvaslabel.grid(row=5, column=0, padx=5, pady=5)
listcanvas = tk.Listbox(root, height=8, width=50, bg='grey', activestyle='dotbox', fg='white')
listcanvas.grid(row=6, column=0, rowspan=2, padx=2, pady=5)

root.mainloop()