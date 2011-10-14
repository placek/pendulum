import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from lib.vector3 import *
from lib.matrix44 import *


class Camera(object):

  def __init__(self, clock, distance):
    """sets up the OpenGL camera looking at point (0.0, 0.0, 0.0) and being at some distance from this point"""
    self.clock = clock
    self.distance = distance
    self.camera_matrix = Matrix44()
    self.camera_matrix.translate = (0.0, 0.0, distance)
    self.rotation_speed = radians(90.0)
    self.move_speed = 3.0

  def rotate(self, direction):
    """rotates camera arount the point due to rotation direction"""
    rotation_direction = Vector3(direction)
    time_passed_seconds = self.clock.tick() / 1000.0
    rotation = rotation_direction * self.rotation_speed * time_passed_seconds
    rotation_matrix = Matrix44.xyz_rotation(*rotation)
    self.camera_matrix *= rotation_matrix
    new_position = Vector3(self.camera_matrix.forward).unit() * self.distance
    self.camera_matrix.translate = new_position
    glLoadMatrixd(self.camera_matrix.get_inverse().to_opengl())

  def move(self, direction):
    """changes a camera distance from the base point"""
    time_passed_seconds = self.clock.tick() / 1000.0
    self.distance += direction * time_passed_seconds * self.move_speed
    if self.distance < 2.0:
      self.distance = 2.0
    elif self.distance > 8.0:
      self.distance = 8.0
    new_position = Vector3(self.camera_matrix.forward).unit() * self.distance
    self.camera_matrix.translate = new_position
    glLoadMatrixd(self.camera_matrix.get_inverse().to_opengl())


class Rod(object):
  """This class allows to render a basic Pendulum object - Rod. A Rods can be at different place, has a different length and color."""

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


class RodsChain(object):
  """This class provides possibility of managing a chain of
     Rods."""

  def __init__(self, position = (0.0, 0.0, 0.0)):
    """initializes a new rods chain"""
    self.position = position
    self.rods = []

  def push(self, length, angle):
    """appends a new rod with specific length and rotated by angle"""
    if len(self.rods) == 0:
      new_position = (self.position[0] + length * math.sin(math.radians(angle)), self.position[1] - length * math.cos(math.radians(angle)) , 0.0)
      self.rods.append(Rod(self.position, new_position))
    else:
      last = self.rods[-1]
      new_position = (last.tip[0] + length * math.sin(math.radians(angle)), last.tip[1] - length * math.cos(math.radians(angle)) , 0.0)
      self.rods.append(Rod(last.tip, new_position))

  def pop(self):
    """remove a last rod"""
    return self.rods.pop()

  def render(self):
    """draws a rods chain"""
    for rod in self.rods:
      rod.render()
