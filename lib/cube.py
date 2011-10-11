import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from lib.vector3 import *


# instance of this object renders a cube
# will disapear in future
class Cube(object):

  def __init__(self, position, color):
    """sets a position and color"""
    self.position = position
    self.color = color

  num_faces = 6
  vertices = [ (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 1.0), (0.0, 1.0, 1.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0) ]
  normals = [ (0.0, 0.0, +1.0), (0.0, 0.0, -1.0), (+1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, +1.0, 0.0), (0.0, -1.0, 0.0) ]
  vertex_indices = [ (0, 1, 2, 3), (4, 5, 6, 7), (1, 5, 6, 2), (0, 4, 7, 3), (3, 2, 6, 7), (0, 1, 5, 4) ]

  def render(self):
    """renders a cube"""
    glColor(self.color)
    vertices = [tuple(Vector3(v) + self.position) for v in self.vertices]
    glBegin(GL_QUADS)
    for face_no in xrange(self.num_faces):
      glNormal3dv( self.normals[face_no] )
      v1, v2, v3, v4 = self.vertex_indices[face_no]
      glVertex( vertices[v1] )
      glVertex( vertices[v2] )
      glVertex( vertices[v3] )
      glVertex( vertices[v4] )
    glEnd()
