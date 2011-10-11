try:
  import sys
  import threading
  from math import radians
  import pygame
  from OpenGL.GL import *
  from OpenGL.GLU import *
  from pygame.locals import *
  from lib.camera import *
  from lib.cube import *
except:
  print '''pendulum: simulation error: failed to load libraries'''
  sys.exit()


class SimulationRunner(threading.Thread):

  screen_size = (800, 600)

  # OpenGL window on_resize event handling
  def __resize(self, width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


  # OpenGL gaphics initialization
  def __init(self):
    pygame.init()
    screen = pygame.display.set_mode(self.screen_size, HWSURFACE|OPENGL|DOUBLEBUF)
    self.__resize(*self.screen_size)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_FLAT)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))

  # thread body
  def run(self):
    self.__init()
    clock = pygame.time.Clock()
    glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    cube = Cube((0.0, 0.0, 0.0), (255.0, 0.0, 0.0))
    camera = Camera(clock, 5.0)

    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          sys.exit()
        if event.type == KEYUP and event.key == K_ESCAPE:
          sys.exit()

      # clear the screen, and z-buffer
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

      # modify camera view for key presses
      pressed = pygame.key.get_pressed()
      if pressed[K_LEFT]:
        camera.rotate((0.0, -1.0, 0.0))
      elif pressed[K_RIGHT]:
        camera.rotate((0.0, +1.0, 0.0))
      if pressed[K_UP]:
        camera.rotate((-1.0, 0.0, 0.0))
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
