from typing import Optional, Tuple, Union
from PIL import Image
from os import listdir
from os.path import isfile, join
from customtkinter import *
import time
import pygame
from tkinter import Menu



class App(CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.toplevel_window_setting = None

        self.title("ASCII ANIMATED")
        self.geometry("1800x1000")

        self.new_width = 200
        self.pixel_block = 65
        self.path = "Try1"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.ASCII_CHARS = ["$", "#", "&", "%", "?",
               "µ", "£", "¿", "€", "©", "¥"]
        
        self.menu = Menu(self)
        self.menu.add_command(label="Настройки", command=self.SettingFrameCheak)
        self.config(menu=self.menu)

        self.labelGraph = CTkLabel(self, text="", font=("Courier", 6))
        self.labelGraph.grid(row=0, column=0, sticky="ew")

    def SettingFrameCheak(self):
        if self.toplevel_window_setting is None or not self.toplevel_window_setting.winfo_exists():
            self.toplevel_window_setting = Setting(self)
            self.toplevel_window_setting.focus()
        else:
            self.toplevel_window_setting.focus()

    def LoadGif(self, path):
        return [f for f in listdir(path) if isfile(join(path, f))]

    def split_animated_gif(gif_file_path):
        ret = []
        gif = Image.open(gif_file_path)
        for frame_index in range(gif.n_frames):
            gif.seek(frame_index)
            frame_rgba = gif.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
            )
            ret.append(pygame_image)
        return ret

    def resize_image(self, image, new_width):
        width, height = image.size
        ratio = height / width
        new_height = int(new_width * ratio)
        resize_image = image.resize((new_width, new_height))
        return(resize_image)

    def grayify(self, image):
        grayscale_image = image.convert("L")
        return (grayscale_image)

    def pixels_to_ascii(self, image):
        pixels = image.getdata()
        characters = "".join([self.ASCII_CHARS[pixel//self.pixel_block] for pixel in pixels])
        return characters

    def label_update(self, label, text):
        label.config(text = text)
    
    def UpdateLabel(self):
        self.onlyfiles = self.LoadGif("Try1")
        while True:
            for i in self.onlyfiles:
                try:
                    image=  Image.open(f"{self.path}\{i}")
                except:
                    print(f"{self.path}, is not a valid pathname to an image.")
                
                new_image_data = self.pixels_to_ascii(self.grayify(self.resize_image(image, self.new_width)))

                pixel_count = len(new_image_data)
                ascii_image = "\n".join(new_image_data[i:(i+self.new_width)] for i in range(0, pixel_count, self.new_width))
                
                self.labelGraph.after(50, self.labelGraph.configure(text = ascii_image))
                self.update()
                # root.update()
        
class Setting(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("250x150")
        self.title("Настройки")

        self.scaling_label = CTkLabel(self, text="UI Scaling:", anchor="w", font=("Times", 20))
        self.scaling_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = CTkOptionMenu(self, values=["50%","60%","70%","80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event, width = 200)
        self.scaling_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 20))
        # self.new_width = 200
        # self.pixel_block = 65
        # self.New_WidthSlider = CTkSlider(self, from_=0, to=400, command=self.slider_change_value_width)
        # self.New_WidthSlider.grid(row=3, column=0, padx=20, pady=(10, 0))
        # self.New_WidthSlider.set(self.new_width)
        # self.Pixel_BlockSlider = CTkSlider(self, from_=0, to=100, command=self.slider_change_value_PixelBlock)
        # self.Pixel_BlockSlider.grid(row=5, column=0, padx=20, pady=(10, 0))
        # self.Pixel_BlockSlider.set(App.pixel_block)
    
    def slider_change_value_width(self, value):
        # App.new_width = value
        pass

    def slider_change_value_PixelBlock(self, value):
        # App.pixel_block = value
        pass
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(new_scaling_float)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)

app = App()
app.UpdateLabel()
app.mainloop()
# root = Tk()
# new_width = 200
# pixel_block = 65
# root.title("ASCII ANIMATED")
# root.geometry("1800x1000")

# lbl = Label(root, text="", font="Courier 6")  
# lbl.pack(anchor=CENTER, expand=1)
# # canvas = Canvas(bg="white", width=1555, height=1000)
# # canvas.pack(anchor=CENTER, expand=1)

# # path = input("Enter a valid pathname to an folder:\n")
# path = "Try1"
# onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]





# root.mainloop()


