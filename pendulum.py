#!/usr/bin/env/python
# complex pendulum simulation by placek

import sys

try:
  import pygame
  from math import radians
  from OpenGL.GL import *
  from OpenGL.GLU import *
  from pygame.locals import *
  from gameobjects.matrix44 import *
  from gameobjects.vector3 import *
except:
  print '''pendulum: error: loading pyOpenGL fails!'''
  sys.exit()

SCREEN_SIZE = (800, 600)

# on_resize event handling
def resize(width, height):
  glViewport(0, 0, width, height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(60.0, float(width)/height, .1, 1000.)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()


# gaphics initialization
def init():
  pygame.init()
  screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
  resize(*SCREEN_SIZE)
  glEnable(GL_DEPTH_TEST)
  glShadeModel(GL_FLAT)
  glClearColor(1.0, 1.0, 1.0, 0.0)
  glEnable(GL_COLOR_MATERIAL)
  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))


# instance of this object renders a cube
class Cube(object):

  def __init__(self, position, color):
    """sets a position and color"""
    self.position = position
    self.color = color

  num_faces = 6
  vertices =       [ (0.0, 0.0, 1.0),
                     (1.0, 0.0, 1.0),
                     (1.0, 1.0, 1.0),
                     (0.0, 1.0, 1.0),
                     (0.0, 0.0, 0.0),
                     (1.0, 0.0, 0.0),
                     (1.0, 1.0, 0.0),
                     (0.0, 1.0, 0.0) ]
  normals =        [ (0.0, 0.0, +1.0),  # front
                     (0.0, 0.0, -1.0),  # back
                     (+1.0, 0.0, 0.0),  # right
                     (-1.0, 0.0, 0.0),  # left
                     (0.0, +1.0, 0.0),  # top
                     (0.0, -1.0, 0.0) ] # bottom
  vertex_indices = [ (0, 1, 2, 3),  # front
                     (4, 5, 6, 7),  # back
                     (1, 5, 6, 2),  # right
                     (0, 4, 7, 3),  # left
                     (3, 2, 6, 7),  # top
                     (0, 1, 5, 4) ] # bottom

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



# instance of this class controlls OpenGL camera
class Camera(object):

  def __init__(self, clock, distance):
    """sets up the OpenGl camera looking at point (0.0, 0.0, 0.0) and being at some distance from this point"""
    self.clock = clock
    self.distance = distance
    self.camera_matrix = Matrix44()
    self.camera_matrix.translate = (0.0, 0.0, distance)
    self.rotation_speed = radians(90.0)
    self.move_speed = 3.0

  def rotate(self, rotation_direction):
    """rotates camera arount the point due to rotation direction"""
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



# application's main thread
def run():
  init()
  clock = pygame.time.Clock()
  glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
  glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

  # this object renders the cube
  cube = Cube((0.0, 0.0, 0.0), (255.0, 0.0, 0.0))
  # this object controlls camera
  camera = Camera(clock, 5.0)

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        return
      if event.type == KEYUP and event.key == K_ESCAPE:
        return

    # clear the screen, and z-buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    # modify direction vectors for key presses
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
      camera.rotate(Vector3(0.0, -1.0, 0.0))
    elif pressed[K_RIGHT]:
      camera.rotate(Vector3(0.0, +1.0, 0.0))
    if pressed[K_UP]:
      camera.rotate(Vector3(-1.0, 0.0, 0.0))
    elif pressed[K_DOWN]:
      camera.rotate(Vector3(+1.0, 0.0, 0.0))
    if pressed[K_q]:
      camera.move(-1.0)
    elif pressed[K_a]:
      camera.move(+1.0)
    camera.rotate(Vector3(0.0, 0.0, 0.0))

    # light must be transformed as well
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0))

    # render the cube
    cube.render()

    # show the screen
    pygame.display.flip()

run()
