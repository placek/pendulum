#!/usr/bin/env python
#
# Simulation of complex pendulum.
#
# by placek@ragnarson.com
#
import sys
from lib.simulation import SimulationRunner
from Tkinter import *

class PendulumApp:

  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    # run_sumulation_button
    self.run_simulation_button = Button(frame, text = "Simulation", command = self.run_simulation)
    self.run_simulation_button.pack(side = LEFT)
    # quit_button
    self.quit_button = Button(frame, text = "Quit", command = self.quit)
    self.quit_button.pack(side=LEFT)

  def quit(self):
    sys.exit()

  def run_simulation(self):
    SimulationRunner().start()

root = Tk()
app = PendulumApp(root)
root.mainloop()
