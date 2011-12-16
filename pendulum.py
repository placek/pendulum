#!/usr/bin/env python
#
# Simulation of complex pendulum.
#
# by placek@ragnarson.com
#
import sys
import itertools
from lib.simulation import SimulationRunner
from lib.objects3d import *
from Tkinter import *

class PendulumApp(Frame):

  def __init__(self, master = None):
    """initialize an application main window"""
    Frame.__init__(self, master)
    self.grid()
    self.chain = RodsChain()
    self.create_widgets()
    self.left_color = (255.0, 0.0, 0.0)
    self.right_color = (0.0, 0.0, 255.0)

  def create_widgets(self):
    """initialize applications main window components"""
    top = self.winfo_toplevel()
    top.rowconfigure(0, weight = 1)
    top.rowconfigure(1, weight = 1)
    top.columnconfigure(0, weight = 1)
    self.columnconfigure(1, weight = 1)
    self.left_frame = LabelFrame(self, text = "first pendulum", labelanchor = "nw", width = 200)
    self.left_frame.grid(row = 0, rowspan = 1, column = 0, columnspan = 1)
    self.right_frame = LabelFrame(self, text = "second pendulum", labelanchor = "nw", width = 200)
    self.right_frame.grid(row = 0, rowspan = 1, column = 1, columnspan = 1)
    # inputs on left side
    self.left_angle_label = Label(self.left_frame, text = "angle", anchor = W)
    self.left_angle_label.grid()
    self.left_angle = Spinbox(self.left_frame, from_ = -179.5, to = 180, increment = 0.5, width = 5, wrap = True)
    for _ in itertools.repeat(None, 359):
      self.left_angle.invoke("buttonup")
    self.left_angle.grid()
    self.left_length_label = Label(self.left_frame, text = "lenght", anchor = W)
    self.left_length_label.grid()
    self.left_length = Spinbox(self.left_frame, from_ = 0.1, to = 4, increment = 0.1, width = 5)
    for _ in itertools.repeat(None, 9):
      self.left_length.invoke("buttonup")
    self.left_length.grid()
    self.left_mass_label = Label(self.left_frame, text = "mass", anchor = W)
    self.left_mass_label.grid()
    self.left_mass = Spinbox(self.left_frame, from_ = 0.1, to = 4, increment = 0.1, width = 5)
    for _ in itertools.repeat(None, 9):
      self.left_mass.invoke("buttonup")
    self.left_mass.grid()
    # inputs on right side
    self.right_angle_label = Label(self.right_frame, text = "angle", anchor = W)
    self.right_angle_label.grid()
    self.right_angle = Spinbox(self.right_frame, from_ = -179.5, to = 180, increment = 0.5, width = 5, wrap = True)
    for _ in itertools.repeat(None, 359):
      self.right_angle.invoke("buttonup")
    self.right_angle.grid()
    self.right_length_label = Label(self.right_frame, text = "lenght", anchor = W)
    self.right_length_label.grid()
    self.right_length = Spinbox(self.right_frame, from_ = 0.1, to = 4, increment = 0.1, width = 5)
    for _ in itertools.repeat(None, 9):
      self.right_length.invoke("buttonup")
    self.right_length.grid()
    self.right_mass_label = Label(self.right_frame, text = "mass", anchor = W)
    self.right_mass_label.grid()
    self.right_mass = Spinbox(self.right_frame, from_ = 0.1, to = 4, increment = 0.1, width = 5)
    for _ in itertools.repeat(None, 9):
      self.right_mass.invoke("buttonup")
    self.right_mass.grid()
    # sumulation_button
    self.simulation_button = Button(self, text = "start", command = self.simulation)
    self.simulation_button.grid(row = 1, rowspan = 1, column = 0, columnspan = 1)
    # quit_button
    self.quit_button = Button(self, text = "quit", command = self.quit)
    self.quit_button.grid(row = 1, rowspan = 1, column = 1, columnspan = 1)

  def quit(self):
    """terminate the simulation thread and exit"""
    try:
      self.simulation_thread.kill()
      sys.exit()
    except:
      sys.exit()

  def simulation(self):
    """start simulation thread"""
    self.chain.push(float(self.left_length.get()), math.radians(float(self.left_angle.get())), float(self.left_mass.get()), self.left_color)
    self.chain.push(float(self.right_length.get()), math.radians(float(self.right_angle.get())), float(self.right_mass.get()), self.right_color)
    self.simulation_thread = SimulationRunner(self.chain)
    self.simulation_thread.start()
    self.simulation_button.configure(state=DISABLED)


app = PendulumApp()
app.mainloop()
