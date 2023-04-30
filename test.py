import unittest
from main import Bird, Pipe, Base

class TestBird(unittest.TestCase):
    def test_bird_initialization(self):
        bird = Bird(230, 350)
        self.assertEqual(bird.x, 230)
        self.assertEqual(bird.y, 350)
        self.assertEqual(bird.tilt, 0)

class TestPipe(unittest.TestCase):
    def test_pipe_initialization(self):
        pipe = Pipe(600)
        self.assertEqual(pipe.x, 600)
        self.assertIsInstance(pipe.height, int)

    def test_pipe_move(self):
        pipe = Pipe(600)
        pipe.move()
        self.assertEqual(pipe.x, 595)

class TestBase(unittest.TestCase):
    def test_base_initialization(self):
        base = Base(730)
        self.assertEqual(base.y, 730)

    def test_base_move(self):
        base = Base(730)
        base.move()
        self.assertEqual(base.x1, -5)
        self.assertEqual(base.x2, base.WIDTH - 5)

if __name__ == '__main__':
    unittest.main()
