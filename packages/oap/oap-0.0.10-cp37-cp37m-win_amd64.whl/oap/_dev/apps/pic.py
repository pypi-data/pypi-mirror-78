"""
Optical Array Probe Particle Image Classifier (PIC)
Author: Lucas Tim Grulich
Date:   28. May 2018
"""

import os
import oap
import errno
# ToDo: Antialiasing Monoscale? Define Export Directory? Truncated / Centered / XSIZES und YSIZES -> POISSON anzeigen
# Name of Imagefile in the Top / Monochromatic anstatt Antialiasing
# Delete Button -> evtl auch UNKNOWN?!?

# --- Python 2.7 and 3.7 Compatible ------------------------------------------------------------------------------------
try:
    import Tkinter as tk
    from tkFileDialog import askopenfilename as askopenfile
except ImportError:
    import tkinter as tk
    from tkinter.filedialog import askopenfile

from PIL import Image, ImageTk


class PIC:

    def __init__(self, master):

        master.title("PIC - OAP Particle Image Classifier")
        master.geometry("1000x440")
        master.lift()   # Lift app to the toplevel
        master.bind("<Key>", self.key_events)

        # --- GLOBALS --------------------------------------------------------------------------------------------------
        self.imagefile = ""
        self.images = []
        self.output = []

        self.buffer_idx = 0
        self.particle_idx = 0
        self.number_of_buffers = 0
        self.number_of_particles = 0

        self.monoscale = False
        self.antialias = False

        self.scale = 3
        self.scale_stripe = 2

        # --- OPTIONS --------------------------------------------------------------------------------------------------
        self.y_sizes = [(5, 125)]
        self.x_sizes = [(5, 64)]

        self.fg_color = 'grey'
        self.bg_color_1 = "#%02x%02x%02x" % (15, 15, 15)
        self.bg_color_2 = "#%02x%02x%02x" % (15, 15, 15)
        self.bg_color_3 = "#%02x%02x%02x" % (2, 39, 55)

        self.step = 10
        self.header_size = 1
        self.export_folder = "PIC_Export"
        self.slice_size = oap.SLICE_SIZE

        # --- GUI Variables --------------------------------------------------------------------------------------------
        self.buffer_idx_label = tk.StringVar()
        self.particle_idx_label = tk.StringVar()
        self.sec_of_day = tk.StringVar()

        self.particles = tk.StringVar()
        self.particle_type = tk.StringVar()

        # --- Image Stripe ---------------------------------------------------------------------------------------------
        self.stripe_1 = None
        self.stripe_2 = None
        self.stripe_3 = None
        self.stripe_4 = None
        self.optical_array = None

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
            else:
                output = "Corrupted"
            return output

    def check_if_file_already_exists(self, filename, delete=False):
        if not os.path.isdir(self.export_folder):
            return False
        for dir_path, _, file_names in os.walk(self.export_folder):
            if filename in file_names:
                file_path = os.path.abspath(os.path.join(dir_path, filename))
                if delete:
                    os.remove(file_path)
                    return True
                with open(file_path, "rb") as f:
                    header = f.read(self.header_size)
                    f.close()
                    return header
        return False

    def update_image_stripe(self):

        dummy = ImageTk.PhotoImage(Image.new('RGB', size=(self.scale_stripe * self.slice_size,
                                                          self.scale_stripe * self.slice_size), color=self.bg_color_2))
        if not self.number_of_particles:
            image_1 = dummy
            image_2 = dummy
            image_3 = dummy
            image_4 = dummy

        else:
            if self.particle_idx-2 >= 0:
                image_1 = ImageTk.PhotoImage(oap.array_as_png(self.images[self.particle_idx-2],
                                                              scale=self.scale_stripe))
            else:
                image_1 = dummy
            if self.particle_idx-1 >= 0:
                image_2 = ImageTk.PhotoImage(oap.array_as_png(self.images[self.particle_idx-1],
                                                              scale=self.scale_stripe))
            else:
                image_2 = dummy
            if self.particle_idx+1 <= self.number_of_particles-1:
                image_3 = ImageTk.PhotoImage(oap.array_as_png(self.images[self.particle_idx+1],
                                                              scale=self.scale_stripe))
            else:
                image_3 = dummy
            if self.particle_idx+2 <= self.number_of_particles-1:
                image_4 = ImageTk.PhotoImage(oap.array_as_png(self.images[self.particle_idx+2],
                                                              scale=self.scale_stripe))
            else:
                image_4 = dummy

        self.stripe_1.configure(image=image_1)
        self.stripe_1.image = image_1
        self.stripe_2.configure(image=image_2)
        self.stripe_2.image = image_2
        self.stripe_3.configure(image=image_3)
        self.stripe_3.image = image_3
        self.stripe_4.configure(image=image_4)
        self.stripe_4.image = image_4

    def update_image(self):

        self.update_image_stripe()

        if not self.number_of_particles:
            image = ImageTk.PhotoImage(Image.new('RGB', size=(self.scale * self.slice_size,
                                                              self.scale * self.slice_size), color=self.bg_color_2))
        else:
            fname = os.path.basename(os.path.normpath(self.imagefile)) + "_"
            fname += str(self.output[self.particle_idx][0]) + "_"
            fname += str(self.output[self.particle_idx][1]) + oap.OAP_FILE_EXTENSION

            p_type = self.check_if_file_already_exists(fname)
            if p_type:
                self.particle_type.set(self.decode_header(p_type))
            else:
                self.particle_type.set("-")

            self.sec_of_day.set(str(self.output[self.particle_idx][0]))

            image = ImageTk.PhotoImage(oap.array_as_png(self.images[self.particle_idx], scale=self.scale))

        if self.number_of_particles:
            self.particle_idx_label.set(str(self.particle_idx + 1) + " / " + str(self.number_of_particles))
        else:
            self.particle_idx_label.set("0 / 0")
            self.particle_type.set("-")
        self.optical_array.configure(image=image)
        self.optical_array.image = image

    def update_buffer(self, direction):
        self.images = []
        self.output = []

        buffers = list(range(self.buffer_idx, self.buffer_idx + self.step))
        self.number_of_particles = oap.imagefile(self.imagefile,
                                                 includebuffers=buffers,
                                                 poisson=False,
                                                 centerparticle=False,
                                                 truncated=False,
                                                 ysizes=self.y_sizes,
                                                 xsizes=self.x_sizes,
                                                 images=self.images,
                                                 output=self.output)
        print(len(self.images))
        if direction == "forward" or direction == "down":
            self.particle_idx = 0
        elif direction == "previous":
            self.particle_idx = self.number_of_particles - 1

        self.buffer_idx_label.set(str(self.buffer_idx) + " - "
                                  + str(min(self.buffer_idx + self.step - 1, self.number_of_buffers))
                                  + " of " + str(self.number_of_buffers))
        self.particles.set(str(self.number_of_particles))

    def next_buffer(self, direction, step_size):
        if direction == "forward" \
                and self.buffer_idx + step_size - 1 < self.number_of_buffers:
            self.buffer_idx += step_size
        elif direction == "previous" \
                and self.buffer_idx > step_size:
            self.buffer_idx -= step_size
        elif direction == "down" \
                and self.buffer_idx > step_size \
                and self.particle_idx == 0:
            self.buffer_idx -= step_size

        self.update_buffer(direction)
        self.update_image()

    def next_image(self, direction, switch=False):
        if not self.imagefile:
            return
        if direction == "forward" \
                and self.particle_idx < self.number_of_particles - 1:
            self.particle_idx += 1
        elif direction == "previous" \
                and self.particle_idx > 0:
            self.particle_idx -= 1
        else:
            if switch:
                self.next_buffer(direction, self.step)
                return
        self.update_image()

    def open_imagefile(self):
        imagefile = tk.filedialog.askopenfilename()
        if imagefile:
            self.imagefile = imagefile
            self.buffer_idx = 1
            self.number_of_buffers = oap.number_of_buffers(imagefile)
            self.update_buffer("forward")
            self.update_image()

    def export_binary(self, p_type):

        folder = self.decode_header(p_type, folder=True)
        imagefile = os.path.basename(os.path.normpath(self.imagefile))

        try:
            os.makedirs(os.path.join(self.export_folder, imagefile, folder))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        fname = imagefile + "_"
        fname += str(self.output[self.particle_idx][0]) + "_"
        fname += str(self.output[self.particle_idx][1])

        self.check_if_file_already_exists(fname + oap.OAP_FILE_EXTENSION, delete=True)

        fpath = os.path.join(self.export_folder, imagefile, folder, fname)
        oap.array_as_oap_file(self.images[self.particle_idx], filename=fpath, header=p_type)

        self.update_image()

    def change_scale(self, change):
        if 1 <= (self.scale + change) <= 20:
            self.scale += change
            self.update_image()

    def change_monoscale(self):
        if self.monoscale:
            self.monoscale = False
        else:
            self.monoscale = True
        if self.number_of_particles:
            self.update_image()

    def change_antialias(self):
        if self.antialias:
            self.antialias = False
        else:
            self.antialias = True
        if self.number_of_particles:
            self.update_image()

    def key_events(self, event):
        if event.char == 'a' or repr(event.char) == "u'\uf702'":
            self.next_image("previous")
        elif event.char == 'd' or repr(event.char) == "u'\uf703'":
            self.next_image("forward")
        elif event.char == 'w' or repr(event.char) == "u'\uf700'":
            self.next_buffer("forward", self.step)
        elif event.char == 's' or repr(event.char) == "u'\uf701'":
            self.next_buffer("down", self.step)
        elif event.char == 'u':
            self.next_buffer("forward", 100)
        elif event.char == 'j':
            self.next_buffer("down", 100)
        elif event.char == 'i':
            self.next_buffer("forward", 500)
        elif event.char == 'k':
            self.next_buffer("down", 500)
        elif event.char == 'o':
            self.open_imagefile()
        elif event.char == '+':
            self.change_scale(1)
        elif event.char == '-':
            self.change_scale(-1)
        elif event.char == 'n':
            self.change_antialias()
        elif event.char == 'm':
            self.change_monoscale()

        # Export classified binary image.
        elif event.char == '1':
            self.export_binary(oap.SPHERE)
        elif event.char == '2':
            self.export_binary(oap.COLUMN)
        elif event.char == '3':
            self.export_binary(oap.ROSETTE)
        elif event.char == '4':
            self.export_binary(oap.DENDRITE)
        elif event.char == '5':
            self.export_binary(oap.PLATE)

        elif event.char == '9':
            self.export_binary(oap.INDEFINABLE)
        elif event.char == '0':
            self.export_binary(oap.ERRONEOUS)

    def build_gui(self):
        label_width = 9
        manual_l_width = 22
        manual_r_width = 16

        # --- Header ---------------------------------------------------------------------------------------------------
        frame_head_1 = tk.Frame(bg=self.bg_color_1)
        tk.Label(frame_head_1, width=manual_l_width, bg=self.bg_color_1, fg="grey", anchor='w',
                 text="O - Open imagefile").pack(side=tk.LEFT)
        tk.Label(frame_head_1,  width=label_width, bg=self.bg_color_1, fg="white", anchor='w',
                 text="Buffer IDs:").pack(side=tk.LEFT)
        tk.Label(frame_head_1, bg=self.bg_color_1, fg="white", anchor='w',
                 textvariable=self.buffer_idx_label).pack(side=tk.LEFT)
        tk.Label(frame_head_1, width=manual_r_width, bg=self.bg_color_1, fg="grey", anchor='w',
                 text="N - Antialising").pack(side=tk.RIGHT)

        frame_head_2 = tk.Frame(bg=self.bg_color_1)
        tk.Label(frame_head_2, width=manual_l_width, bg=self.bg_color_1, fg="grey", anchor='w',
                 text="W - Next " + str(self.step) + " buffers").pack(side=tk.LEFT)
        tk.Label(frame_head_2, width=label_width, bg=self.bg_color_1, fg="white", anchor='w',
                 text="Sec of Day:").pack(side=tk.LEFT)
        tk.Label(frame_head_2, bg=self.bg_color_1, fg="white", anchor='w',
                 textvariable=self.sec_of_day).pack(side=tk.LEFT)
        tk.Label(frame_head_2, width=manual_r_width, bg=self.bg_color_1, fg="grey", anchor='w',
                 text="M - Monoscale").pack(side=tk.RIGHT)

        frame_head_3 = tk.Frame(bg=self.bg_color_1)
        tk.Label(frame_head_3, width=manual_l_width, bg=self.bg_color_1, fg="grey", anchor='w',
                 text="S - Previous " + str(self.step) + " buffers").pack(side=tk.LEFT)
        tk.Label(frame_head_3, width=label_width, bg=self.bg_color_1, fg="white", anchor='w',
                 text="Particles:").pack(side=tk.LEFT)
        tk.Label(frame_head_3, bg=self.bg_color_1, fg="white", anchor='w',
                 textvariable=self.particles).pack(side=tk.LEFT)
        tk.Label(frame_head_3, width=manual_r_width, bg=self.bg_color_1, fg="grey", anchor='w',
                 text="+/- Scale image").pack(side=tk.RIGHT)

        frame_head_4 = tk.Frame(bg=self.bg_color_1)
        tk.Label(frame_head_4, bg=self.bg_color_1, fg="white", textvariable=self.particle_type).pack(side=tk.BOTTOM)

        frame_head_1.pack(fill=tk.X)
        frame_head_2.pack(fill=tk.X)
        frame_head_3.pack(fill=tk.X)
        frame_head_4.pack(fill=tk.X)

        # --- Image Stripe ---------------------------------------------------------------------------------------------
        frame_image_stripe_border = tk.Frame(bg=self.bg_color_3)
        frame_image_stripe = tk.Frame(frame_image_stripe_border, bg=self.bg_color_3)

        stripe_height = self.slice_size * self.scale_stripe
        self.stripe_1 = tk.Label(frame_image_stripe, bg=self.bg_color_2, height=stripe_height, image=None)
        self.stripe_2 = tk.Label(frame_image_stripe, bg=self.bg_color_2, height=stripe_height, image=None)
        self.stripe_3 = tk.Label(frame_image_stripe, bg=self.bg_color_2, height=stripe_height, image=None)
        self.stripe_4 = tk.Label(frame_image_stripe, bg=self.bg_color_2, height=stripe_height, image=None)
        self.optical_array = tk.Label(frame_image_stripe, bg=self.bg_color_2)

        # --- Pack Image Stripe ----------------------------------------------------------------------------------------
        self.stripe_1.pack(side=tk.LEFT)
        tk.Label(frame_image_stripe, fg="grey", bg=self.bg_color_3, text="  <  ").pack(side=tk.LEFT)
        self.stripe_2.pack(side=tk.LEFT)
        tk.Label(frame_image_stripe, fg="grey", bg=self.bg_color_3, text="    <<   A   ").pack(side=tk.LEFT)
        self.optical_array.pack(side=tk.LEFT, expand=True, fill=tk.Y)
        tk.Label(frame_image_stripe, fg="grey", bg=self.bg_color_3, text="   D   >>    ").pack(side=tk.LEFT)
        self.stripe_3.pack(side=tk.LEFT)
        tk.Label(frame_image_stripe, fg="grey", bg=self.bg_color_3, text="  >  ").pack(side=tk.LEFT)
        self.stripe_4.pack(side=tk.LEFT)

        frame_image_stripe.pack(expand=True, fill=tk.Y)
        frame_image_stripe_border.pack(fill=tk.BOTH, expand=True)

        # -- Footer ----------------------------------------------------------------------------------------------------
        frame_foot = tk.Frame(bg=self.bg_color_1)
        tk.Label(frame_foot, bg=self.bg_color_1, fg="white", textvariable=self.particle_idx_label).pack()
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
        PIC(root)
        root.mainloop()


if __name__ == "__main__":
    PIC.start()
