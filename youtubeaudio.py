import tkinter as tk 
from tkinter import filedialog, font, IntVar, Toplevel
import re, os, sys
import subprocess
import webbrowser 

class AudioManager(tk.Tk):
    
    # data structure (queue) properties
    URLLIST = []
    YOUTUBE_URL_LENGTH = 43
    FSEXITLIST = []
    FSEXITMAX = 3
    
    # temporary, source directory on download
    ORIGIN_DIRECTORY_WINDOWS = "C:/Users/shull/youtube-audio-downloader"
    ORIGIN_DIRECTORY_LINUX = "/mnt/c/Users/shull/youtube-audio-downloader"
    
    # regex properties
    REGEX_CHANNEL = '(&ab_)\w+=[\w\d\_\-]+'
    REGEX_INDEX = '^[()]\d+[()]\s'
    
    # dimensions of Tkinter window + text styles
    tkHeight = 480
    tkWidth = 660
    tkScale = 1.5
    cutHeight = 1.5
    cutWidth = 2
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
        self.pick_top_buttons()
        self.pick_youtube_url()
        self.pick_directory()
        self.pick_queue()
        self.pick_result_msg()
        
        # and on exit, if enabling file system on close is allowed
        self.protocol("WM_DELETE_WINDOW", self.call_file_system_on_close)
        
    # labels for GUI
    def make_label(self, readable, src=None, bold=False, italic=False, bg=None, fg=None):
        label = tk.Label((src if src != None else self), text=readable, font=self.textProperties)
        if bold:
            label.configure(font=self.textBoldProperties)
        elif italic:
            label.configure(font=self.textTidbitProperties)
        if bg != None or fg != None:
            label.configure(bg=bg, fg=fg)
        return label
        
    # and buttons for GUI
    def make_button(self, readable, e, src=None, bg='white', fg='black'):
        return tk.Button((src if src != None else self), text=readable, command=e, bg=bg, fg=fg)
        
    # the two buttons on top of GUI
    def pick_top_buttons(self):
        self.creditsButton = self.make_button("FAQ", self.credits_and_help)
        self.creditsButton.grid(row=0, column=1, padx=2, pady=5)  
        
        self.favoriteButton = self.make_button("Favorites", self.open_favorites, bg='gold')
        self.favoriteButton.grid(row=0, column=2, padx=2, pady=5)
    
    # all components of: YouTube text entry
    def pick_youtube_url(self):
        inputlabel = self.make_label("::: YouTube Audio Downloader :::\nInsert YouTube link...", bold=True)
        inputlabel.grid(row=0, column=0, padx=2, pady=5)
        
        self.inputtxt = tk.Text(self, height=2, width=40)
        self.inputtxt.configure(font=self.textProperties)
        self.inputtxt.grid(row=1, column=0, padx=5, pady=10)   
        
        downloadNowButton = self.make_button("Download", self.download_now, bg='lightblue')
        downloadNowButton.grid(row=1, column=1, padx=2, pady=5)
        addToQueueButton = self.make_button("Add to Queue", self.post_to_queue, bg='orchid1')
        addToQueueButton.grid(row=1, column=2, padx=2, pady=5) 
    
        # enable file system on closing window (exit)
        self.enableFileSystemOnClose = IntVar()
        self.fsCloseCheckbox = tk.Checkbutton(
            self, 
            text='Open file systems after closing?', 
            variable=self.enableFileSystemOnClose,
            onvalue=1,
            offvalue=0
        )
        self.fsCloseCheckbox.grid(row=2, column=0)
            
    # create directory path
    def create_directory_path(self):
        self.savetofolder = os.getcwd()
        self.savetofolder = self.savetofolder.replace("\\", "/")
        current_directory_text = f"Currently saved in: {self.savetofolder}"
        self.cwdlabel = self.make_label(current_directory_text, bg='beige', fg='black')
        self.cwdlabel.grid(row=4, column=0, padx=2, pady=5)
    
    # function to edit directory path
    def edit_directory_path(self):
        self.savetofolder = filedialog.askdirectory(
            initialdir=os.path.normpath("/mnt/c/"), 
            title="Save to Folder"
        )
        self.cwdlabel.configure(
            text=f"Currently saved in {self.savetofolder}", 
            bg='beige', 
            fg='black'
        )
    
    # all components of: directory
    def pick_directory(self):
        self.create_directory_path()
        outputdirlabel = self.make_label("Where to save the audio?", bold=True)
        outputdirlabel.grid(row=3, column=0, padx=2, pady=5)
        outputbtn = self.make_button("Save to", self.edit_directory_path, bg='green', fg='white')
        outputbtn.grid(row=3, column=1, padx=2, pady=5)
        
    # convert and run Bash script to execute youtube-dl
    def bash_pipe(self, link):
        if self.savetofolder.startswith("C:/"):
            self.savetofolder = self.savetofolder.replace("C:/", "/mnt/c/")
        self.savetofolder = f"{self.savetofolder}/"
        
        youtubeURL = re.sub(self.REGEX_CHANNEL, '', link)
        bash_file = "./youtubeaudioconvert.sh"
        if (os.getcwd() != self.ORIGIN_DIRECTORY_LINUX or os.getcwd() != self.ORIGIN_DIRECTORY_WINDOWS):
            bash_file = f"{self.ORIGIN_DIRECTORY_LINUX}/youtubeaudioconvert.sh"
        process = subprocess.Popen(
            ["bash", bash_file, self.savetofolder, youtubeURL],
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
        listcanvaslabel = self.make_label("Queue", bold=True)
        listcanvaslabel.grid(row=6, column=0, padx=5, pady=5)
        
        self.listcanvas = tk.Listbox(self, height=8, width=50, bg='grey', activestyle='dotbox', fg='white')
        self.listcanvas.grid(row=7, column=0, rowspan=3, padx=2, pady=5)
        
        delFromQueueButton = self.make_button('Delete selection', self.delete_one_from_queue, bg='red')
        delFromQueueButton.grid(row=8, column=1, padx=2, pady=5)
        
        delFrame = tk.Frame(self)
        delFromLabel = self.make_label("Type index number:", src=delFrame, italic=True)
        delFromLabel.pack()
        self.delFromSelection = tk.Text(delFrame, width=3, height=1)
        self.delFromSelection.pack()
        delFrame.grid(row=8, column=2, padx=2, pady=5)
        
        downloadAllButton = self.make_button("Download All", self.download_queue, bg='cyan')
        downloadAllButton.grid(row=7, column=1, padx=2, pady=5)
    
        deleteAllButton = self.make_button("Delete Queue", self.delete_all_from_queue, bg='red')
        deleteAllButton.grid(row=9, column=1, padx=2, pady=5)
    
    # add into queue
    def post_to_queue(self):
        inp = self.inputtxt.get("1.0", "end-1c")
        if len(inp) < self.YOUTUBE_URL_LENGTH:
            return 
        if inp in self.URLLIST:
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
        self.msglabel = self.make_label("Window freezes when downloading, wait until you see 'Complete!'")
        self.msglabel.grid(row=10, column=0, padx=2, pady=5)
        
        # dynamic labels (change based on actions of user)
        self.donelabel = self.make_label("Complete!", bg='green', fg='white')
        self.exceptionlabel = self.make_label("Error: could not be performed!", bg='red', fg='white')
        
        # NEW, print audio title and author from json file
        self.authorlabel = self.make_label("")
        self.authorlabel.grid(row=11, column=0, padx=2, pady=5)    
    
    # save favorite directories for next time
    def save_favorite_directories(self):
        pass
    
    # and save favorite files just in case
    def save_favorite_files(self):
        pass
    
    # open favorite directories from previous sessions
    def open_favorite_directories(self):
        pass
    
    # open favorite files from previous sessions 
    def open_favorite_files(self):
        pass 
    
    # when opening favorites window, show elements here
    def open_favorites(self):
        self.favWindow = Toplevel(self)
        self.favWindow.title("Favorites")
        self.favWindow.geometry(f"{int(self.tkHeight / self.cutHeight)}x{int(self.tkWidth / self.cutWidth)}")
        
        favorites_label = self.make_label("Show favorites", src=self.favWindow, bold=True)
        favorites_label.grid(row=0, column=0, padx=5, pady=5)
        
        fav_button_frame = tk.Frame(self.favWindow)
        fav_dir_btn = self.make_button("Folders", self.open_favorite_directories, src=fav_button_frame, bg='yellow')
        fav_file_btn = self.make_button("Files", self.open_favorite_files, src=fav_button_frame, bg='beige')
        fav_dir_btn.pack()
        fav_file_btn.pack()
        fav_button_frame.grid(row=0, column=1, padx=5, pady=5)
    
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
        sys.exit(0)

    # get URL
    def retrieveURL(self, link):
        webbrowser.open_new_tab(link)

    # credits and help
    def credits_and_help(self):
        self.askWindow = Toplevel(self)
        self.askWindow.title("FAQ - YouTube Audio Downloader")
        self.askWindow.geometry(f"{int(self.tkHeight / self.cutHeight)}x{int(self.tkWidth / self.cutWidth)}")
        
        mainAskLabel = self.make_label("Credits", src=self.askWindow, bold=True)
        mainAskLabel.pack()
        
        creditsFrame = tk.Frame(self.askWindow)
        hyperlinkText = self.make_label("Link to GitHub", src=creditsFrame, fg='blue')
        hyperlinkText.bind(
            '<Button-1>', 
            lambda e: self.retrieveURL("https://www.github.com/stephull/youtube-audio-downloader/")
        )
        hyperlinkText.configure(font=font.Font(
            hyperlinkText, 
            hyperlinkText.cget('font'), 
            underline=True
        ))
        hyperlinkText.pack()
        creditsFrame.pack()
        
        secondAskLabel = self.make_label("FAQ", src=self.askWindow, bold=True)
        secondAskLabel.pack()
        
        faqFrame = tk.Frame(self.askWindow)
        faqFrame.pack()

# main application run
if __name__ == "__main__":
    root = AudioManager()
    root.mainloop()