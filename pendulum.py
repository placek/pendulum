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
    Frame.__init__(self, master)
    self.grid()
    self.chain = RodsChain()
    self.create_widgets()

  def create_widgets(self):
    self.chain = RodsChain()
    top = self.winfo_toplevel()
    top.rowconfigure(0, weight = 1)
    top.columnconfigure(0, weight = 1)
    self.columnconfigure(1, weight = 1)
    self.left_frame = LabelFrame(self, text = "settings", labelanchor = "nw")
    self.left_frame.grid(row = 0, rowspan = 1, column = 0, columnspan = 1)
    self.right_frame = Frame(self)
    self.right_frame.grid(row = 0, rowspan = 1, column = 1, columnspan = 1)
    # list of objects with scrolling
    self.yScroll = Scrollbar(self.left_frame, orient = VERTICAL)
    self.yScroll.grid(row = 0, column = 1, sticky = N + S)
    self.xScroll = Scrollbar(self.left_frame, orient = HORIZONTAL)
    self.xScroll.grid(row = 1, column = 0, sticky = E + W)
    self.list_values = StringVar()
    self.listbox = Listbox(self.left_frame, xscrollcommand = self.xScroll.set,
                                            yscrollcommand = self.yScroll.set,
                                            listvariable = self.list_values,
                                            state = DISABLED)
    self.listbox.grid(row = 0, column = 0, sticky = N + S + E + W)
    self.xScroll["command"] = self.listbox.xview
    self.yScroll["command"] = self.listbox.yview
    # inputs
    self.angle_label = Label(self.left_frame, text = "angle", anchor = W)
    self.angle_label.grid()
    self.angle = Spinbox(self.left_frame, from_ = -179.5, to = 180, increment = 0.5, width = 5, wrap = True)
    for _ in itertools.repeat(None, 359):
      self.angle.invoke("buttonup")
    self.angle.grid()
    self.length_label = Label(self.left_frame, text = "lenght", anchor = W)
    self.length_label.grid()
    self.length = Spinbox(self.left_frame, from_ = 0.1, to = 4, increment = 0.1, width = 5)
    for _ in itertools.repeat(None, 9):
      self.length.invoke("buttonup")
    self.length.grid()
    # add_rod_button
    self.add_rod_button = Button(self.left_frame, text = "add rod", command = self.add_rod)
    self.add_rod_button.grid()
    # remove_rod_button
    self.remove_rod_button = Button(self.left_frame, text = "remove rod", command = self.remove_rod)
    self.remove_rod_button.grid()
    # sumulation_button
    self.simulation_started = False
    self.simulation_button = Button(self.right_frame, text = "start", command = self.simulation)
    self.simulation_button.grid()
    # quit_button
    self.quit_button = Button(self.right_frame, text = "quit", command = self.quit)
    self.quit_button.grid()

  def quit(self):
    try:
      self.simulation_thread.kill()
      sys.exit()
    except:
      sys.exit()

  def simulation(self):
    if self.simulation_started == False:
      self.simulation_thread = SimulationRunner(self.chain)
      self.simulation_thread.start()
      self.simulation_button.configure(text = "stop")
      self.simulation_started = True
    else:
      self.simulation_thread.kill()
      self.simulation_button.configure(text = "start")
      self.simulation_started = False

  def add_rod(self):
    self.chain.push(float(self.length.get()), float(self.angle.get()))
    self.list_values.set(" ".join([n.to_string() for n in self.chain.rods]))

  def remove_rod(self):
    self.chain.pop()
    self.list_values.set(" ".join([n.to_string() for n in self.chain.rods]))

app = PendulumApp()
app.mainloop()
