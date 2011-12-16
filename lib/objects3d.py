# vim: set fe=utf8
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
  """This class allows to render a basic Pendulum object - Rod."""

  thickness = 0.1
  scale = 0.3

  def __init__(self, position, length, angle, mass, color):
    """sets a position and length"""
    self.position = position
    self.mass = mass
    self.length = length
    self.angle = angle
    self.angular_speed = 0.0
    self.angular_acceleration = 0.0
    self.thickness *= self.scale
    self.color = color

  def start(self):
    """start position as tuple"""
    return self.position

  def tip(self):
    """tip position as tuple"""
    return (self.start()[0] + self.length * math.sin(self.angle), self.start()[1] - self.length * math.cos(self.angle), self.start()[2])

  def render(self):
    """renders an object"""
    glColor(self.color)
    glTranslate(self.start()[0], self.start()[1], self.start()[2])
    glRotate(math.degrees(self.angle), 0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex(-self.thickness, 0.0,  self.thickness)
    glVertex( self.thickness, 0.0,  self.thickness)
    glVertex( self.thickness, -self.length,  self.thickness)
    glVertex(-self.thickness, -self.length,  self.thickness)
    glEnd()
    glBegin(GL_QUADS)
    glVertex( self.thickness, 0.0,  self.thickness)
    glVertex( self.thickness, 0.0, -self.thickness)
    glVertex( self.thickness, -self.length, -self.thickness)
    glVertex( self.thickness, -self.length,  self.thickness)
    glEnd()
    glBegin(GL_QUADS)
    glVertex( self.thickness, 0.0, -self.thickness)
    glVertex(-self.thickness, 0.0, -self.thickness)
    glVertex(-self.thickness, -self.length, -self.thickness)
    glVertex( self.thickness, -self.length, -self.thickness)
    glEnd()
    glBegin(GL_QUADS)
    glVertex(-self.thickness, 0.0, -self.thickness)
    glVertex(-self.thickness, 0.0, self.thickness)
    glVertex(-self.thickness, -self.length,  self.thickness)
    glVertex(-self.thickness, -self.length, -self.thickness)
    glEnd()
    glRotate(-math.degrees(self.angle), 0.0, 0.0, 1.0)
    glTranslate(-self.start()[0], -self.start()[1], -self.start()[2])


class RodsChain(object):
  """This class provides possibility of managing a pair of Rods."""

  def __init__(self, position = (0.0, 0.0, 0.0)):
    """initializes a new rods chain"""
    self.position = position
    self.rods = []
    self.gravity = 9.80665

  def push(self, length, angle, mass, color):
    """appends a new rod with specific length and rotated by angle"""
    if len(self.rods) == 0:
      self.rods.append(Rod(self.position, length, angle, mass, color))
    elif len(self.rods) == 1:
      self.rods.append(Rod(self.rods[0].tip, length, angle, mass, color))

  def pop(self):
    """remove a last rod"""
    return self.rods.pop()

  def update(self, delta_t):
    """updates rods attributes due to euler calculation"""
    # variables
    m1, m2 = self.rods[0].mass, self.rods[1].mass
    a1, a2 = self.rods[0].angle, self.rods[1].angle
    as1, as2 = self.rods[0].angular_speed, self.rods[1].angular_speed
    l1, l2 = self.rods[0].length, self.rods[1].length
    g = self.gravity
    # equations of movement
    self.rods[0].angular_acceleration = (-g * (2.0 * m1 + m2) * math.sin(a1) - g * m2 * math.sin(a1 - 2.0 * a2) - 2.0 * math.sin(a1 - a2) * m2 * (math.pow(as2, 2.0) * l2 + math.pow(as1, 2.0) * l1 * math.cos(a1 - a2))) / (l1 * (2.0 * m1 + m2 - m2 * math.cos(2.0 * a1 - 2.0 * a2)))
    self.rods[1].angular_acceleration = (2.0 * math.sin(a1 - a2) * (math.pow(as1, 2.0) * l1 * (m1 + m2) + g * (m1 + m2) * math.cos(a1) + math.pow(as2, 2.0) * l2 * m2 * math.cos(a1 - a2))) / (l2 * (2.0 * m1 + m2 - m2 * math.cos(2.0 * a1 - 2.0 * a2)))
    self.rods[0].angular_speed += delta_t * self.rods[0].angular_acceleration
    self.rods[1].angular_speed += delta_t * self.rods[1].angular_acceleration
    self.rods[0].angle += delta_t * self.rods[0].angular_speed
    self.rods[1].angle += delta_t * self.rods[1].angular_speed
    self.rods[1].position = self.rods[0].tip()

  def render(self):
    """draws a rods chain"""
    self.rods[0].render()
    self.rods[1].render()
