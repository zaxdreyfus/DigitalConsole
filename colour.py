from tkinter import *
import colorsys


class ApplicationWindow(Frame):

    def __init__(self, master=None):

        # Properties for the current colour in 3 forms
        self.hsl = {"hue": 0.75, "saturation": 0.5, "lightness": 0.5}
        self.rgb = {"red": 0, "green": 0, "blue": 0}
        self.hexcolor = "#000000"

        self.window = Tk()
        self.window.resizable(width=False, height=False)
        self.window.title("CodeDrome HSL GUI")
        self.window.geometry("800x600")

        self.createWidgets()

        # Set the slider positions to the hard-coded defaults.
        # This forces the sliders to call onchange and shoe the colour.
        self.hueslider.set(self.hsl["hue"] * 360)
        self.saturationslider.set(self.hsl["saturation"] * 100)
        self.lightnessslider.set(self.hsl["lightness"] * 100)

        self.window.mainloop()

    def createWidgets(self):

        # A few common values to use in all widgets.
        # A rough analogy with CSS!
        styles = \
            {
                "borderwidth": 0,
                "bg": "#282C34",
                "fg": "#FFFFFF",
                "troughcolor": "#FFFFFF",
                "sliderlength": 16,
                "highlightthickness": 0
            }

        # Hue
        self.hueslider = Scale(self.window, width=24, from_=0, to=360, orient=HORIZONTAL, command=self.onchange, borderwidth=styles["borderwidth"], bg=styles["bg"], fg=styles["fg"], sliderlength=styles["sliderlength"], troughcolor=styles["troughcolor"], highlightthickness=styles["highlightthickness"], label="Hue")
        self.hueslider.grid(sticky="NSEW")

        # Saturation
        self.saturationslider = Scale(self.window, width=24, from_=0, to=100, orient=HORIZONTAL, command=self.onchange, borderwidth=styles["borderwidth"], bg=styles["bg"], fg=styles["fg"], sliderlength=styles["sliderlength"], troughcolor=styles["troughcolor"], highlightthickness=styles["highlightthickness"], label="Saturation")
        self.saturationslider.grid(sticky="NSEW")

        # Lightness
        self.lightnessslider = Scale(self.window, width=24, from_=0, to=100, orient=HORIZONTAL, command=self.onchange, borderwidth=styles["borderwidth"], bg=styles["bg"], fg=styles["fg"], sliderlength=styles["sliderlength"], troughcolor=styles["troughcolor"], highlightthickness=styles["highlightthickness"], label="Lightness")
        self.lightnessslider.grid(sticky="NSEW")

        # RGB
        self.rvalue = Label(self.window, width=48, height=3, text="0", bg="#FF0000", fg="#FFFFFF", borderwidth=styles["borderwidth"])
        self.rvalue.grid(sticky="NSEW")

        self.gvalue = Label(self.window, height=3, text="0", bg="#00FF00", fg="#FFFFFF", borderwidth=styles["borderwidth"])
        self.gvalue.grid(sticky="NSEW")

        self.bvalue = Label(self.window, height=3, text="0", bg="#0000FF", fg="#FFFFFF", borderwidth=styles["borderwidth"])
        self.bvalue.grid(sticky="NSEW")

    def onchange(self, event):

        # Called when any of the sliders are changed.
        # Sets and shows the current colour.
        self.set_hsl()
        self.set_rgb()
        self.show_rgb()
        self.set_hexcolor()
        self.show_color()

    def set_hsl(self):

        # Pick up the user-set HSL values

        self.hsl["hue"] = self.hueslider.get() / 360
        self.hsl["saturation"] = self.saturationslider.get() / 100
        self.hsl["lightness"] = self.lightnessslider.get() / 100

    def set_rgb(self):

        # Set the RGB values from the HSL values.

        rgb = colorsys.hls_to_rgb(self.hsl["hue"], self.hsl["lightness"], self.hsl["saturation"])

        self.rgb["red"] = int(rgb[0]*255)
        self.rgb["green"] = int(rgb[1]*255)
        self.rgb["blue"] = int(rgb[2]*255)

    def show_rgb(self):

        # Show the RGB values in their respective Label widgets.

        self.rvalue.config(text="{}".format(self.rgb["red"]))
        self.gvalue.config(text="{}".format(self.rgb["green"]))
        self.bvalue.config(text="{}".format(self.rgb["blue"]))

    def set_hexcolor(self):

        # Set the hexadecimal colour from RGB values.

        self.hexcol = "#{}{}{}".format(hex(self.rgb["red"])[2:].zfill(2), hex(self.rgb["green"])[2:].zfill(2), hex(self.rgb["blue"])[2:].zfill(2))

    def show_color(self):

        # Set the main window background to the current colour.

        self.window.config(bg=self.hexcol)


def main():

    appwin = ApplicationWindow()


main()

