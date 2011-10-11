from math import radians
from OpenGL.GL import *
from lib.matrix44 import *
from lib.vector3 import *


# instance of this class controls OpenGL camera
class Camera(object):

  def __init__(self, clock, distance):
    """sets up the OpenGl camera looking at point (0.0, 0.0, 0.0) and being at some distance from this point"""
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
