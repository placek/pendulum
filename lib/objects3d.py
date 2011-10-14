import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from lib.vector3 import *


class Rod(object):
  """This class allows to render a basic Pendulum object - Rod.
     A Rods can be at different place, has a different length and
     color."""

  thickness = 0.1
  scale = 0.3

  def __init__(self, start, end, color = (255.0, 0.0, 0.0)):
    """sets a position and length"""
    self.position = start
    self.tip = end
    self.thickness *= self.scale
    self.color = color

  def length(self):
    """returns a length of rod"""
    return self.to_vector3().length

  def to_vector3(self):
    """returns a Vector3 representing rod"""
    return Vector3(self.tip).__sub__(Vector3(self.position))

  def angle(self):
    """returns angle, of which the rod is rotated from a vertical direction around Z-axis"""
    return math.acos(-(self.to_vector3()._get_1() / self.length()))

  def render(self):
    """renders an object"""
    glColor(self.color)
    glTranslate(self.position[0], self.position[1], self.position[2])
    glRotate(math.degrees(self.angle()), 0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex(-self.thickness, 0.0,  self.thickness)
    glVertex( self.thickness, 0.0,  self.thickness)
    glVertex( self.thickness, -self.length(),  self.thickness)
    glVertex(-self.thickness, -self.length(),  self.thickness)
    glEnd()
    glBegin(GL_QUADS)
    glVertex( self.thickness, 0.0,  self.thickness)
    glVertex( self.thickness, 0.0, -self.thickness)
    glVertex( self.thickness, -self.length(), -self.thickness)
    glVertex( self.thickness, -self.length(),  self.thickness)
    glEnd()
    glBegin(GL_QUADS)
    glVertex( self.thickness, 0.0, -self.thickness)
    glVertex(-self.thickness, 0.0, -self.thickness)
    glVertex(-self.thickness, -self.length(), -self.thickness)
    glVertex( self.thickness, -self.length(), -self.thickness)
    glEnd()
    glBegin(GL_QUADS)
    glVertex(-self.thickness, 0.0, -self.thickness)
    glVertex(-self.thickness, 0.0, self.thickness)
    glVertex(-self.thickness, -self.length(),  self.thickness)
    glVertex(-self.thickness, -self.length(), -self.thickness)
    glEnd()
    glRotate(-math.degrees(self.angle()), 0.0, 0.0, 1.0)
    glTranslate(-self.position[0], -self.position[1], -self.position[2])
