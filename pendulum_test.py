import unittest
import pygame
import math
from lib.objects3d import *

class TestCamera(unittest.TestCase):

  def setUp(self):
    clock = pygame.time.Clock()
    self.camera = Camera(clock, 5.0)

  def test_instance_variables(self):
    self.assertEqual(self.camera.distance, 5.0)
    self.assertIsInstance(self.camera.camera_matrix, Matrix44)
    self.assertEqual(self.camera.rotation_speed, radians(90.0))
    self.assertEqual(self.camera.move_speed, 3.0)


class TestRod(unittest.TestCase):

  def setUp(self):
    self.rod = Rod((0.0, 0.0, 0.0), (1.0, 2.0, 3.0))

  def test_instance_variables(self):
    self.assertEqual(self.rod.color, (255.0, 0.0, 0.0))
    self.assertEqual(self.rod.position, (0.0, 0.0, 0.0))
    self.assertEqual(self.rod.tip, (1.0, 2.0, 3.0))
    self.assertEqual(self.rod.thickness, 0.03)

  def test_instance_length_method(self):
    self.assertEqual(self.rod.length(), math.sqrt(1.0*1.0 + 2.0*2.0 + 3.0*3.0))

  def test_instance_to_vector3_method(self):
    self.assertIsInstance(self.rod.to_vector3(), Vector3)
    self.assertEqual(self.rod.to_vector3()._get_0(), 1.0)
    self.assertEqual(self.rod.to_vector3()._get_1(), 2.0)
    self.assertEqual(self.rod.to_vector3()._get_2(), 3.0)

  def test_instance_angle_method(self):
    self.assertEqual(self.rod.angle(), 2.1347389681555256)


class TestRodsChain(unittest.TestCase):

  def setUp(self):
    self.chain = RodsChain()
    self.chain.push(math.sqrt(2), 45.0)
    self.chain.push(1.0, 180.0)
    self.chain.push(2.0, 90.0)

  def test_positions_and_tips_of_rods_in_chain(self):
    self.assertAlmostEqual(self.chain.rods[0].length(), math.sqrt(2))
    self.assertAlmostEqual(self.chain.rods[0].angle(), math.radians(45.0))
    self.assertEqual(self.chain.position, (0.0, 0.0, 0.0))
    self.assertEqual(self.chain.rods[0].position, (0.0, 0.0, 0.0))
    self.assertAlmostEqual(self.chain.rods[0].tip[0], 1.0)
    self.assertAlmostEqual(self.chain.rods[0].tip[1], -1.0)
    self.assertAlmostEqual(self.chain.rods[1].position[0], 1.0)
    self.assertAlmostEqual(self.chain.rods[1].position[1], -1.0)
    self.assertAlmostEqual(self.chain.rods[1].tip[0], 1.0)
    self.assertAlmostEqual(self.chain.rods[1].tip[1], 0.0)
    self.assertAlmostEqual(self.chain.rods[2].position[0], 1.0)
    self.assertAlmostEqual(self.chain.rods[2].position[1], 0.0)
    self.assertAlmostEqual(self.chain.rods[2].tip[0], 3.0)
    self.assertAlmostEqual(self.chain.rods[2].tip[1], 0.0)


if __name__ == '__main__':
  unittest.main()
