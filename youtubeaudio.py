import tkinter as tk 
from tkinter import filedialog
import subprocess, os

root = tk.Tk()
savetofolder = filedialog.askdirectory(initialdir=os.path.normpath("/mnt/c/"), title="Save to Folder")
savetofolder = savetofolder.replace("C:/", "/mnt/c/")
canvas1 = tk.Canvas(root, width=240, height=240)
ready = False

def convert(link):
    bashCmd = f"bash ./convert.sh {link} {savetofolder}"
    process = subprocess.Popen(bashCmd.split(), stdout=subprocess.PIPE)
    output, err = process.communicate()
    if (err != None):
        print(err)

def hello():
    label1 = tk.Label(root, text="Complete!", fg='black')
    canvas1.create_window(120, 150, window=label1)
    ready = True
    inp = inputtxt.get(1.0, "end-1c")
    if ready and len(inp) > 0:
        convert(inp)

def saveto():
    root

inputlabel = tk.Label(root, text="Insert YouTube link...")
inputlabel.pack()
inputtxt = tk.Text(root, height=2, width=60)
inputtxt.pack()

outputdirlabel = tk.Label(root, text='Where do you want to save the audio?')
outputdirlabel.pack()
outputbtn = tk.Button(root, text='Save to...', command=saveto, bg='blue', fg='white')
outputbtn.pack()

msglabel = tk.Label(root, text="Window will freeze when downloading, wait until you see 'Complete'")
msglabel.pack()
button1 = tk.Button(root, text="Download", command=hello, bg='blue', fg='white')

canvas1.create_window(120, 120, window=button1)
canvas1.pack()

root.mainloop()