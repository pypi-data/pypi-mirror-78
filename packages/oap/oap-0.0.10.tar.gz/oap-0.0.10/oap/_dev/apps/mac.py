"""
MAC - Manual Array Classifier
Author: Lucas Tim Grulich
Date:   01. September 2017
"""

import os
import oap
import errno
import shutil

# ToDO: Ueberpruefen was passiert, wenn wirklich mal eine Datei gelöscht wurde - Ist das überhaupt nötig?
# ToDo: Sortieren funktiniert nicht

# --- Python 2.7 and 3.7 Compatible ------------------------------------------------------------------------------------
try:
    import Tkinter as tk
    from tkFileDialog import askdirectory
except ImportError:
    import tkinter as tk
    from tkinter.filedialog import askdirectory

from PIL import Image, ImageTk

CLOSING_TEXT = """
Sort previous OAP Images
by Particle Type into
corresponding folders?
"""


class MAC:

    def __init__(self, master):
        master.title("MAC - Manual Array Classifier")
        master.geometry("800x600")
        master.lift()   # Lift app to the toplevel
        master.bind("<Key>", self.key_events)
        self.master = master

        # --- GLOBALS --------------------------------------------------------------------------------------------------
        self.files = []
        self.index = 0
        self.directory = "."
        self.main_directory = "."
        self.scale = 3
        self.imgy = 30
        self.antialias = False
        self.monoscale = False
        self.centering = False

        # --- OPTIONS --------------------------------------------------------------------------------------------------
        self.main_folder = "MAC_Export"
        self.slice_size = oap.SLICE_SIZE

        # --- GUI Variables --------------------------------------------------------------------------------------------
        self.filename = tk.StringVar()
        self.folder = tk.StringVar()
        self.particle_class = tk.StringVar()
        self.image_index = tk.StringVar()
        self.optical_array = None

        # --- OPTIONS --------------------------------------------------------------------------------------------------
        self.fg_color = 'grey'
        self.bg_color_1 = '#%02x%02x%02x' % (0, 0, 40)
        self.bg_color_2 = '#%02x%02x%02x' % (15, 15, 15)

        # --- Call Functions -------------------------------------------------------------------------------------------
        self.build_gui()
        self.update_image()

    @staticmethod
    def decode_header(header, folder=False):
        if folder:
            if header == oap.SPHERE:
                output = "1_SphericalObjects"
            elif header == oap.COLUMN:
                output = "2_ColumnsAndNeedles"
            elif header == oap.ROSETTE:
                output = "3_Rosettes"
            elif header == oap.DENDRITE:
                output = "4_Dendrites"
            elif header == oap.PLATE:
                output = "5_Plates"

            elif header == oap.INDEFINABLE:
                output = "9_IndefinableParticles"
            elif header == oap.ERRONEOUS:
                output = "0_ErroneousImages"
            else:
                output = "Corrupted"
            return output
        else:
            if header == oap.SPHERE:
                output = "1 - Spherical Object"
            elif header == oap.COLUMN:
                output = "2 - Column or Needle"
            elif header == oap.ROSETTE:
                output = "3 - Rosettes"
            elif header == oap.DENDRITE:
                output = "4 - Dendrite"
            elif header == oap.PLATE:
                output = "5 - Plate"

            elif header == oap.INDEFINABLE:
                output = "9 - Indefinable Particle"
            elif header == oap.ERRONEOUS:
                output = "0 - Erroneous Image"

            elif header == "IOError":
                output = "File does not exist anymore"
            else:
                output = "Corrupted"
            return output

    def update_image(self):

        if len(self.files):
            self.filename.set("Filename: " + self.files[self.index].split('/')[-1])
            file_root = self.files[self.index].split('/')[-3] + '/' + self.files[self.index].split('/')[-2]
            self.folder.set("Directory: " + file_root)

            try:
                self.image_index.set(str(self.index + 1) + " / " + str(len(self.files)))
                array, header = oap.read_oap_file(os.path.join(self.directory, self.files[self.index]))
                if self.centering:
                    array = oap.center_particle(array)
                image = ImageTk.PhotoImage(oap.array_as_png(array, scale=self.scale))

            except IOError:
                header = "IOError"
                image = ImageTk.PhotoImage(Image.new('RGB', size=(self.scale * self.slice_size,
                                                                  self.scale * self.slice_size), color=self.bg_color_1))
            self.particle_class.set(self.decode_header(header))
        else:
            self.particle_class.set("-")
            self.image_index.set("- / -")
            image = ImageTk.PhotoImage(Image.new('RGB', size=(self.scale * self.slice_size,
                                                              self.scale * self.slice_size), color=self.bg_color_1))

        self.optical_array.configure(image=image, bg=self.bg_color_1)
        self.optical_array.image = image

    def change_background(self):
        if len(self.files):
            if self.bg_color_1 == '#%02x%02x%02x' % (0, 0, 40):
                self.bg_color_1 = '#%02x%02x%02x' % (0, 0, 0)
            else:
                self.bg_color_1 = '#%02x%02x%02x' % (0, 0, 40)
            self.update_image()

    def change_monoscale(self):
        if self.monoscale:
            self.monoscale = False
        else:
            self.monoscale = True
        if len(self.files):
            self.update_image()

    def change_antialias(self):
        if self.antialias:
            self.antialias = False
        else:
            self.antialias = True
        if len(self.files):
            self.update_image()

    def change_scale(self, change):
        if len(self.files):
            if 1 <= self.scale + change <= 20:
                self.scale += change
                self.update_image()

    def open_directory(self):
        directory = askdirectory()
        if directory:
            self.directory = directory
            self.index = 0
            self.files = oap.filepaths(directory)
            self.files = sorted(self.files)
            self.update_image()

    def next_image(self, direction, step=1):
        if len(self.files):
            if direction == "forward" and self.index < len(self.files) - 1:
                self.index += step
            if direction == "previous" and self.index > 0:
                self.index -= step
            self.update_image()

    def key_events(self, event):
        if event.char == 'a' or repr(event.char) == "u'\uf702'":
            self.next_image("previous", 1)
        elif event.char == 'd' or repr(event.char) == "u'\uf703'":
            self.next_image("forward", 1)
        # elif event.char == 's' or repr(event.char) == "u'\uf702'":
        #    self.next_image("previous", 500)
        # elif event.char == 'w' or repr(event.char) == "u'\uf703'":
        #    self.next_image("forward", 500)
        elif event.char == 'o':
            self.open_directory()
        elif event.char == '+':
            self.change_scale(1)
        elif event.char == '-':
            self.change_scale(-1)
        elif event.char == 'n':
            self.change_antialias()
        elif event.char == 'm':
            self.change_monoscale()
        elif event.char == 'b':
            self.change_background()

        # Classify binary image.
        elif event.char == '1':
            self.classify(oap.SPHERE)
        elif event.char == '2':
            self.classify(oap.COLUMN)
        elif event.char == '3':
            self.classify(oap.ROSETTE)
        elif event.char == '4':
            self.classify(oap.DENDRITE)
        elif event.char == '5':
            self.classify(oap.PLATE)

        elif event.char == '9':
            self.classify(oap.INDEFINABLE)
        elif event.char == '0':
            self.classify(oap.ERRONEOUS)

    def classify(self, particle_type):
        if len(self.files):
            p_type = oap.read_bytes(os.path.join(self.directory,
                                                 self.files[self.index]), 0, 1)
            if p_type != particle_type:
                oap.modify_bytes(os.path.join(self.directory, self.files[self.index]), 0, particle_type)
                self.update_image()

    def move_files(self):
        for file in self.files[:self.index + 1]:
            p_type = oap.read_bytes(os.path.join(self.directory, file), 0, 1)
            folder = self.decode_header(p_type, folder=True)

            try:
                os.makedirs(os.path.join(self.main_directory, self.main_folder, folder))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            # move or copy
            shutil.move(os.path.join(file),
                        os.path.join(self.main_directory, self.main_folder, folder, file.split('/')[-1]))
        self.master.destroy()

    def key_pop_up(self, event):
        if event.char == 'y':
            self.move_files()
        elif event.char == 'n':
            self.master.destroy()

    def closing_pop_up(self):
        toplevel = tk.Toplevel()
        toplevel.title("")
        toplevel.geometry("300x200")
        toplevel.bind("<Key>", self.key_pop_up)

        tk.Label(toplevel, text=CLOSING_TEXT, font=("Helvetica", 12)).pack()
        frame_srt = tk.Frame(toplevel)
        tk.Button(frame_srt, text="YES", width=8, command=self.move_files).pack(side=tk.LEFT)
        tk.Label(frame_srt, width=5).pack(side=tk.LEFT)
        tk.Button(frame_srt, text="NO", width=8, command=self.master.destroy).pack(side=tk.RIGHT)
        frame_srt.pack(side=tk.BOTTOM)

    def close_window(self):
        if len(self.files) != 1 and self.index > 0 or len(self.files) == 1:
            self.closing_pop_up()
        else:
            self.master.destroy()

    def build_gui(self):

        # --- Header ---------------------------------------------------------------------------------------------------
        frame_head = tk.Frame(bg=self.bg_color_2, pady=20)
        tk.Label(frame_head, fg=self.fg_color, bg=self.bg_color_2, textvariable=self.folder).pack()
        tk.Label(frame_head, fg=self.fg_color, bg=self.bg_color_2, textvariable=self.filename).pack()
        frame_head.pack(fill=tk.X)

        # --- Optical Array --------------------------------------------------------------------------------------------
        tk.Label(font=("Helvetica", 20), bg="black", fg="white", textvariable=self.particle_class).pack(fill=tk.X)
        self.optical_array = tk.Label(bg=self.bg_color_1)
        self.optical_array.pack(fill=tk.BOTH, expand=True)

        # --- Footer ---------------------------------------------------------------------------------------------------
        frame_foot = tk.Frame(bg="black")
        tk.Label(frame_foot, font=("Helvetica", 10), bg="black", fg="white", textvariable=self.image_index).pack()
        frame_foot.pack(fill=tk.X)

        # --- Manual ---------------------------------------------------------------------------------------------------
        frame_manual = tk.Frame(bg=self.bg_color_2)
        tk.Label(frame_manual, fg=self.fg_color, bg=self.bg_color_2, text="1 - Spherical Object")\
            .pack(side=tk.TOP, anchor=tk.W)
        tk.Label(frame_manual, fg=self.fg_color, bg=self.bg_color_2, text="2 - Column or Needle")\
            .pack(side=tk.TOP, anchor=tk.W)
        tk.Label(frame_manual, fg=self.fg_color, bg=self.bg_color_2, text="3 - Rosette").pack(side=tk.TOP, anchor=tk.W)
        tk.Label(frame_manual, fg=self.fg_color, bg=self.bg_color_2, text="4 - Dendrite").pack(side=tk.TOP, anchor=tk.W)
        tk.Label(frame_manual, fg=self.fg_color, bg=self.bg_color_2, text="5 - Plate").pack(side=tk.TOP, anchor=tk.W)
        tk.Label(frame_manual, fg=self.fg_color, bg=self.bg_color_2, text="9 - Indefinable Particle")\
            .pack(side=tk.TOP, anchor=tk.W)
        tk.Label(frame_manual, fg=self.fg_color, bg=self.bg_color_2, text="0 - Erroneous Image")\
            .pack(side=tk.TOP, anchor=tk.W)
        frame_manual.pack(fill=tk.X)

    @staticmethod
    def start():
        root = tk.Tk()
        MAC(root)
        root.mainloop()


if __name__ == "__main__":
    MAC.start()
