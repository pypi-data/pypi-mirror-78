"""
CCR - Correct Classification Rate - Tool

Graphical User Interface for manually measuring the correct classification rate of the developed
cloud particle classifier.

Author: Lucas Tim Grulich
Date:   23. January 2019
"""

import os
import oap
import errno
import shutil

# --- Python 2.7 and 3.7 Compatible ------------------------------------------------------------------------------------
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from PIL import Image, ImageTk


class CCR:

    def __init__(self, master):

        master.title("CCR - Correct Classification Rate Tool")
        master.geometry("800x600")
        master.lift()  # Lift app to the toplevel
        master.bind("<Key>", self.key_events)

        # --- GLOBALS --------------------------------------------------------------------------------------------------
        self.files = []
        self.backup = ""

        self.scale = 3
        self.center = True
        self.antialias = False
        self.monoscale = False
        self.rgb = (23, 69, 51)

        # --- OPTIONS --------------------------------------------------------------------------------------------------
        self.slice_size = oap.SLICE_SIZE
        self.main_directory = "CCR"

        # --- GUI Variables --------------------------------------------------------------------------------------------
        self.particle_class = tk.StringVar()
        self.no_of_imgs = tk.StringVar()
        self.oap_img = None

        self.files = oap.filepaths(self.main_directory)
        self.no_of_imgs.set("Images left: " + str(len(self.files)))

        # --- Call Functions -------------------------------------------------------------------------------------------
        self.build_gui()
        self.update_image()

    def classify_image(self, state):

        if len(self.files):
            file = self.files.pop(0)

            # --- Create Folders ---------------------------------------------------------------------------------------
            try:
                os.makedirs(os.path.join(self.main_directory, "correct"))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            try:
                os.makedirs(os.path.join(self.main_directory, "false"))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            if state:
                if not os.path.basename(os.path.normpath(file)) \
                       in os.listdir(os.path.join(self.main_directory, "correct")):
                    shutil.move(file, os.path.join(self.main_directory, "correct"))
                    self.backup = os.path.join(self.main_directory, "correct", os.path.basename(os.path.normpath(file)))
            else:
                if not os.path.basename(os.path.normpath(file)) \
                       in os.listdir(os.path.join(self.main_directory, "false")):
                    shutil.move(file, os.path.join(self.main_directory, "false"))
                    self.backup = os.path.join(self.main_directory, "false", os.path.basename(os.path.normpath(file)))
        self.update_image()

    def backup_image(self):
        if self.backup == "":
            return
        if len(self.files) and self.files[0] != self.backup:
            self.files = [self.backup] + self.files
            self.update_image()
        elif not len(self.files):
            self.files = [self.backup]
            self.update_image()

    def update_image(self):

        if len(self.files):

            array, header = oap.read_oap_file(self.files[0])

            if self.center:
                array = oap.center_particle(array)

            particle_class = header
            image = ImageTk.PhotoImage(oap.array_as_png(array, scale=self.scale))
        else:
            particle_class = "THE END"
            image = ImageTk.PhotoImage(Image.new('RGB', size=(self.scale * self.slice_size,
                                                              self.scale * self.slice_size), color=self.rgb))

        self.no_of_imgs.set("Images left: " + str(len(self.files)))

        # ToDo: Colors for other particle types
        if particle_class == oap.SPHERE:
            particle_header = "Spherical Object"
            self.rgb = (23, 46, 69)
        elif particle_class == oap.COLUMN:
            particle_header = "Column or Needle"
            self.rgb = (23, 69, 51)
        elif particle_class == oap.ROSETTE:
            particle_header = "Rosette"
            self.rgb = (15, 75, 77)
        elif particle_class == oap.ERRONEOUS:
            particle_header = "Erroneous Image"
        elif particle_class == "THE END":
            particle_header = "THE END"
        else:
            # ToDo: Header is corrupted
            particle_header = "File is corrupted"
        self.particle_class.set(particle_header)

        self.oap_img.configure(image=image, bg='#%02x%02x%02x' % self.rgb)
        self.oap_img.image = image

    def change_scale(self, change):
        if 1 <= self.scale + change <= 20:
            self.scale += change
            self.update_image()

    def key_events(self, event):
        if event.char == '+':
            self.change_scale(1)
        elif event.char == '-':
            self.change_scale(-1)
        elif event.char == 'y':
            self.classify_image(True)
        elif event.char == 'n':
            self.classify_image(False)
        elif event.char == 'r':
            self.backup_image()

    def build_gui(self):
        # --- Header ---------------------------------------------------------------------------------------------------
        frame_head = tk.Frame(bg="black")
        tk.Label(frame_head, font=("Helvetica", 20), bg="black", fg="white", textvariable=self.particle_class).pack()
        frame_head.pack(fill=tk.X)

        self.oap_img = tk.Label(bg='#%02x%02x%02x' % self.rgb)
        self.oap_img.pack(fill=tk.BOTH, expand=True)

        # --- Footer ---------------------------------------------------------------------------------------------------
        frame_foot = tk.Frame(bg="black")
        tk.Label(frame_foot, font=("Helvetica", 14), bg="black", fg="white", textvariable=self.no_of_imgs).pack()
        frame_foot.pack(fill=tk.X)

        # --- Manual ---------------------------------------------------------------------------------------------------
        frame_manual = tk.Frame(bg="black")
        tk.Label(frame_manual, fg="grey", bg="black", text="Y - Correct classified").pack(side=tk.TOP, anchor=tk.W)
        tk.Label(frame_manual, fg="grey", bg="black", text="N - Falsely classified").pack(side=tk.TOP, anchor=tk.W)
        tk.Label(frame_manual, fg="grey", bg="black", text="R - Back to the last image").pack(side=tk.TOP, anchor=tk.W)
        frame_manual.pack(fill=tk.X)

    @staticmethod
    def start():
        root = tk.Tk()
        CCR(root)
        root.mainloop()


if __name__ == "__main__":
    CCR.start()
