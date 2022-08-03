import tkinter as tk 
from tkinter import filedialog
import subprocess, os, re

root = tk.Tk()
root.title("YouTube Audio Downloader")
root.tk.call('tk', 'scaling', 1.5)
canvas1 = tk.Canvas(root, width=250, height=150)
ready = False

savetofolder = os.getcwd()
savetofolder = savetofolder.replace("\\", "/")

cwdlabel = tk.Label(root, text=f"Currently saved in: {savetofolder}", bg='yellow', fg='black')
donelabel = tk.Label(root, text="Complete!", fg='black')

inputlabel = tk.Label(root, text="Insert YouTube link...")
inputlabel.pack()
inputtxt = tk.Text(root, height=2, width=60)
inputtxt.pack()

def saveto():
    global savetofolder
    savetofolder = filedialog.askdirectory(initialdir=os.path.normpath("/mnt/c/"), title="Save to Folder")
    cwdlabel.configure(text=f"Currently saved in {savetofolder}", bg='yellow', fg='black')

outputdirlabel = tk.Label(root, text='Where do you want to save the audio?')
outputdirlabel.pack()
outputbtn = tk.Button(root, text='Save to...', command=saveto, bg='blue', fg='white')
outputbtn.pack()
cwdlabel.pack()

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

def download():
    ready = True
    inp = inputtxt.get(1.0, "end-1c")
    if ready and len(inp) > 0:
        convert(inp)

button1 = tk.Button(root, text="Download", command=download, bg='blue', fg='white')
canvas1.create_window(120, 60, window=button1)
msglabel = tk.Label(root, text="Window will freeze when downloading, wait until you see 'Complete'")
msglabel.pack()
canvas1.pack()

root.mainloop()