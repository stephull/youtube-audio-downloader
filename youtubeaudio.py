import tkinter as tk 
from tkinter import filedialog, font, IntVar
import re
import os
import subprocess

class AudioManager(tk.Tk):
    
    # data structure (queue) properties
    URLLIST = []
    YOUTUBE_URL_LENGTH = 43
    FSEXITLIST = []
    FSEXITMAX = 3
    
    # regex properties
    REGEX_CHANNEL = '(&ab_)\w+=[\w\d\_\-]+'
    REGEX_INDEX = '^[()]\d+[()]\s'
    
    # dimensions of Tkinter window + text styles
    tkHeight = 480
    tkWidth = 630
    tkScale = 1.5
    textProperties = ("Helvetica", 10)
    textBoldProperties = ("Helvetica", 10, font.BOLD)
    textTidbitProperties = ("Helvetica", 7, font.ITALIC)

    # start program
    def __init__(self):
        super().__init__()
        self.title("YouTube Audio Downloader")
        self.tk.call('tk', 'scaling', self.tkScale)
        self.geometry(f"{self.tkWidth}x{self.tkHeight}")
        
        # place components in order of appearence
        self.pick_youtube_url()
        self.pick_directory()
        self.pick_queue()
        self.pick_result_msg()
        
        # and on exit, if enabling file system on close is allowed
        self.protocol("WM_DELETE_WINDOW", self.call_file_system_on_close)
        
    # all components of: YouTube text entry
    def pick_youtube_url(self):
        inputlabel = tk.Label(
            self, 
            text="::: YouTube Audio Downloader :::\nInsert YouTube link...",
            font=self.textBoldProperties
        )
        inputlabel.grid(row=0, column=0, padx=2, pady=5)
        
        self.inputtxt = tk.Text(self, height=2, width=40)
        self.inputtxt.configure(font=self.textProperties)
        self.inputtxt.grid(row=1, column=0, padx=5, pady=10)   
        
        downloadNowButton = tk.Button(self, command=self.download_now, text='Download', bg='blue', fg='white')
        downloadNowButton.grid(row=1, column=1, padx=2, pady=5)
        addToQueueButton = tk.Button(self, command=self.post_to_queue, text='Add To Queue', bg='purple', fg='white')
        addToQueueButton.grid(row=1, column=2, padx=2, pady=5) 
    
        # enable file system on closing window (exit)
        self.enableFileSystemOnClose = IntVar()
        self.fsCloseCheckbox = tk.Checkbutton(
            self, 
            text='Open file systems after closing?', variable=self.enableFileSystemOnClose,
            onvalue=1,
            offvalue=0
        )
        self.fsCloseCheckbox.grid(row=2, column=0)
            
    # create directory path
    def create_directory_path(self):
        self.savetofolder = os.getcwd()
        self.savetofolder = self.savetofolder.replace("\\", "/")
        self.cwdlabel = tk.Label(self, text=f"Currently saved in: {self.savetofolder}", bg='yellow', fg='black')
        self.cwdlabel.grid(row=4, column=0, padx=2, pady=5)
    
    # function to edit directory path
    def edit_directory_path(self):
        self.savetofolder = filedialog.askdirectory(initialdir=os.path.normpath("/mnt/c/"), title="Save to Folder")
        self.cwdlabel.configure(text=f"Currently saved in {self.savetofolder}", bg='yellow', fg='black')
    
    # all components of: directory
    def pick_directory(self):
        self.create_directory_path()
        outputdirlabel = tk.Label(self, text='Where do you want to save the audio?', font=self.textBoldProperties)
        outputdirlabel.grid(row=3, column=0, padx=2, pady=5)
        outputbtn = tk.Button(self, text='Save to...', command=self.edit_directory_path, bg='green', fg='white')
        outputbtn.grid(row=3, column=1, padx=2, pady=5)
        
    # convert and run Bash script to execute youtube-dl
    def bash_pipe(self, link):
        if self.savetofolder.startswith("C:/"):
            self.savetofolder = self.savetofolder.replace("C:/", "/mnt/c/")
        self.savetofolder = f"{self.savetofolder}/"
        
        youtubeURL = re.sub(self.REGEX_CHANNEL, '', link)
        process = subprocess.Popen(
            ["bash", "./convert.sh", self.savetofolder, youtubeURL],
            stdout=subprocess.PIPE        
        )
        
        output, err = process.communicate()
        ec = (err != None)
        print(f"::: ERROR :::\n{err}" if ec else f"::: OUTPUT :::\n{output}")
        new_label = self.exceptionlabel if ec else self.donelabel
        new_label.grid(row=10, column=1, padx=2, pady=5)
        self.inputtxt.delete(1.0, "end-1c")
        
    # check for file system queue if user allows it
    def wait_for_closing(self):
        if self.enableFileSystemOnClose.get() > 0:
            if len(self.FSEXITLIST) == self.FSEXITMAX:
                self.FSEXITLIST.pop(0)
            self.FSEXITLIST.append(self.savetofolder)
            print(self.FSEXITLIST)
        
    # download one song immediately from text entry
    def download_now(self):
        inp = self.inputtxt.get(1.0, "end-1c")
        if len(inp) >= self.YOUTUBE_URL_LENGTH:
            self.bash_pipe(inp) 
            self.wait_for_closing()
    
    # all components for: queue area
    def pick_queue(self):
        listcanvaslabel = tk.Label(self, text='Queue', font=self.textBoldProperties)
        listcanvaslabel.grid(row=6, column=0, padx=5, pady=5)
        
        self.listcanvas = tk.Listbox(self, height=8, width=50, bg='grey', activestyle='dotbox', fg='white')
        self.listcanvas.grid(row=7, column=0, rowspan=3, padx=2, pady=5)
        
        delFromQueueButton = tk.Button(self, command=self.delete_one_from_queue, text='Delete Selection', bg='red', fg='white')
        delFromQueueButton.grid(row=8, column=1, padx=2, pady=5)
        
        delFrame = tk.Frame(self)
        delFromLabel = tk.Label(delFrame, text='Type index number:', font=('Helvetica', 7, font.ITALIC))
        delFromLabel.pack()
        self.delFromSelection = tk.Text(delFrame, width=3, height=1)
        self.delFromSelection.pack()
        delFrame.grid(row=8, column=2, padx=2, pady=5)
        
        downloadAllButton = tk.Button(self, command=self.download_queue, text='Download All', bg='blue', fg='white')
        downloadAllButton.grid(row=7, column=1, padx=2, pady=5)
    
        deleteAllButton = tk.Button(self, command=self.delete_all_from_queue ,text='Delete All', bg='red', fg='white')
        deleteAllButton.grid(row=9, column=1, padx=2, pady=5)
    
    # add into queue
    def post_to_queue(self):
        inp = self.inputtxt.get("1.0", "end-1c")
        if len(inp) < self.YOUTUBE_URL_LENGTH:
            return 
        tmp_index = len(self.URLLIST)
        self.URLLIST.append(inp)
        self.listcanvas.insert(tmp_index, f"({tmp_index}) {self.URLLIST[tmp_index]}")
        self.inputtxt.delete(1.0, "end-1c")
    
    # download all audio from queue
    def download_queue(self):
        for i in range(len(self.URLLIST)):
            downloading = self.listcanvas.get(0)
            downloading = re.sub(self.REGEX_INDEX, '', downloading)
            self.bash_pipe(downloading)
            self.listcanvas.delete(0)
        self.URLLIST.clear()
        self.wait_for_closing()
    
    # delete selection from queue
    def delete_one_from_queue(self):
        try:
            index = int(self.delFromSelection.get(1.0, "end-1c"))
            self.delFromSelection.delete(1.0, "end-1c")
        except ValueError:
            return 
        self.listcanvas.delete(index)
        self.URLLIST.pop(index)
        for i in range(index, len(self.URLLIST)):
            list_value = self.listcanvas.get(i)
            list_value = re.sub(self.REGEX_INDEX, '', list_value)
            self.listcanvas.delete(i)
            self.listcanvas.insert(i, f"({i}) {list_value}")
            
    # and delete all items from queue
    def delete_all_from_queue(self):
        for url in self.URLLIST:
            self.listcanvas.delete(0)
        self.URLLIST.clear()
    
    # all components for results (messages)
    def pick_result_msg(self):
        self.msglabel = tk.Label(self, text="Window freezes when downloading, wait until you see 'Complete!'")
        self.msglabel.grid(row=10, column=0, padx=2, pady=5)
        
        # dynamic labels (change based on actions of user)
        self.donelabel = tk.Label(self, text="Complete!", fg='black', bg='green2')
        self.exceptionlabel = tk.Label(self, text="Error, link could not be completed!", bg='red', fg='white')
        
        # NEW, print audio title and author from json file
        self.authorlabel = tk.Label(self, text="")
        self.authorlabel.grid(row=11, column=0, padx=2, pady=5)    
    
    # last method: on closing, open file system(s) to open downloads
    # and allows up to 3 most recent directories open at once.
    def call_file_system_on_close(self):
        if (self.enableFileSystemOnClose.get() == 1):
            for i in range(len(self.FSEXITLIST)):
                element = self.FSEXITLIST[i]
                filedialog.askopenfilename(
                    initialdir=element, 
                    title=f"({i+1}/{len(self.FSEXITLIST)}) View Downloads in: {element}"
                )
        self.FSEXITLIST.clear()
        self.destroy()
        print("Exiting YouTube Audio Downloader...")

# main application run
if __name__ == "__main__":
    root = AudioManager()
    root.mainloop()