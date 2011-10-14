import unittest
import pygame
from lib.camera import *

class TestCamera(unittest.TestCase):

  def setUp(self):
    clock = pygame.time.Clock()
    self.camera = Camera(clock, 5.0)

  def test_instance_variables(self):
    self.assertEqual(self.camera.distance, 5.0)
    self.assertIsInstance(self.camera.camera_matrix, Matrix44)
    self.assertEqual(self.camera.rotation_speed, radians(90.0))
    self.assertEqual(self.camera.move_speed, 3.0)


if __name__ == '__main__':
  unittest.main()
