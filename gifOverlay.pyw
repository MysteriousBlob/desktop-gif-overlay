import tkinter as tk 
from tkinter import filedialog  
from PIL import Image, ImageTk

def Image_Seek(Image, Index):
    Image.seek(Index)
    return Image

class configWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        self.title("Gif Configure")
        self.geometry("400x200")
        self.wm_resizable(False, False)
        self.minsize(400, 200)
        self.maxsize(400, 200)

        self.wm_attributes("-topmost", True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.bind("]", lambda event: self.master.destroy())

    def place_widgets(self):
        self.width_label = tk.Label(self, text="Width:")
        self.width_label.grid(row=0, column=0, ipady=3)

        self.width_entry = tk.Entry(self, textvariable=self.master.gif_width)
        self.width_entry.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=20, ipady=3)

        self.height_label = tk.Label(self, text="Height:")
        self.height_label.grid(row=1, column=0, ipady=3)

        self.width_entry = tk.Entry(self, textvariable=self.master.gif_height)
        self.width_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=20, ipady=3)

        self.path_label = tk.Label(self, text="Path:")
        self.path_label.grid(row=2, column=0, ipady=3)

        self.path_selection = tk.Entry(self, textvariable=self.master.gif_path)
        self.path_selection.grid(row=2, column=1, sticky=tk.EW, padx=20, ipady=3)

        self.choose_path = tk.Button(self, text="Select Path", command=self.select_path)
        self.choose_path.grid(row=2, column=2, sticky=tk.EW, padx=20, ipady=3)

        self.submit_button = tk.Button(self, text="Submit", command=self.master.Submit)
        self.submit_button.grid(row=3, column=1, sticky=tk.EW, padx=5)

        self.display_button = tk.Button(self, text="Display", command=self.master.Display)
        self.display_button.grid(row=3, column=2, sticky=tk.EW, padx=5)

    def select_path(self):
        self.master.gif_path.set(filedialog.askopenfilename())

class IgifOverlay():
    def __init__(self):
        self.title("Gif Viewer")
        self.geometry("400x400-0-0")
        self.wm_attributes("-topmost", True)
        self.wm_resizable(False, False)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "white")
        self.configure(bg="white")


        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.config_window_called = False
        self.cycle_working = False
        self.width = 0
        self.height = 0
        self.filepath = ""
        self.gif_width = tk.IntVar()
        self.gif_height = tk.IntVar()
        self.gif_path = tk.StringVar()

        self.place_widgets()

        self.bind("'", func=lambda event: self.create_config_window())
        self.bind("]", func=lambda event: self.destroy())


    def place_widgets(self):
        self.button = tk.Button(self, text="Select/Configure the gif", font="90", command=self.create_config_window)
        self.button.grid(row=0, column=0, sticky=tk.NSEW)

    def create_config_window(self):
        if not self.config_window_called:
            self.config_window = configWindow(self)
            self.config_window_called = True
            
            self.config_window.place_widgets()

            self.config_window.protocol("WM_DELETE_WINDOW", self.destroy_config_window)

            self.wm_attributes("-disabled", True)

    def destroy_config_window(self):
        self.config_window_called = False
        self.config_window.destroy()
        self.wm_attributes("-disabled", False)
    
    def display_gif(self):
        if self.filepath != "":
            self.construct_gif()


            if self.width == 0 or self.height == 0:
                self.geometry(f"{self.gif.width}x{self.gif.height}-0-0")
            else:
                self.geometry(f"{self.width}x{self.height}-0-0")

            if self.cycle_working:
                self.label.destroy()

            self.button.destroy()
            self.label = tk.Label(self, image=self.images[0])
            self.label.grid(row=0, column=0, sticky=tk.NSEW)
            self.label.configure(bg="white")
            self.label.bind("<B1-Motion>", lambda event: self.moveGif())

            if not self.cycle_working:
                self.after(self.frame_delay, self.cycle_gif)

            self.cycle_working = True

    def cycle_gif(self):
        self.label.configure(image=self.images[self.current_frame%self.frames])
        self.current_frame += 1
        self.after(self.frame_delay, self.cycle_gif)

    def construct_gif(self):
        self.gif = Image.open(self.filepath)
        self.frames = self.gif.n_frames
        self.frame_delay = self.gif.info['duration']
        self.current_frame = 1
        if self.width == 0 or self.height == 0:
            self.images = tuple([tk.PhotoImage(file=self.filepath, format=f"gif -index {i}") for i in range(self.frames)])
        else:
            self.images = tuple([ImageTk.PhotoImage(Image_Seek(self.gif, i).resize((self.width, self.height), Image.Resampling.NEAREST)) for i in range(self.frames)])
    
    def Submit(self):
        if self.gif_width.get() >= 0:
            self.width = self.gif_width.get()

        if self.gif_height.get() >= 0:
            self.height = self.gif_height.get()

        self.filepath = self.gif_path.get()

    def Display(self):
        self.display_gif()

    def moveGif(self):
        x = self.winfo_pointerx()
        y = self.winfo_pointery()

        geo = self.winfo_geometry().replace("+", "x").split("x")
        self.geometry(f"{geo[0]}x{geo[1]}+{x-int(geo[0])//2}+{y-int(geo[1])//2}")

class gifOverlayMaster(tk.Tk, IgifOverlay):
    def __init__(self):
        tk.Tk.__init__(self)
        IgifOverlay.__init__(self)

        self.subWindows = []
        self.bind_all("\\", lambda event: self.create_subwindow())
        self.bind_all("r", lambda event: self.reset_frames())

    def create_subwindow(self):
        self.subWindows.append(gifOverlayChild(self))
    
    def reset_frames(self):
        self.current_frame = 0
        for i in self.subWindows:
            i.current_frame = 0

class gifOverlayChild(tk.Toplevel, IgifOverlay):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        IgifOverlay.__init__(self)

app = gifOverlayMaster()

app.mainloop()
