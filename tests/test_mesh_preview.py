import unittest

from tools.mesh_preview import rasterize_faces


class MeshPreviewTests(unittest.TestCase):
    def test_nearest_surface_wins_independent_of_draw_order(self):
        far = ([(0, 0, 1), (10, 0, 1), (0, 10, 1)], (255, 0, 0))
        near = ([(0, 0, 2), (10, 0, 2), (0, 10, 2)], (0, 0, 255))
        forward = rasterize_faces([far, near], 10, 10)
        backward = rasterize_faces([near, far], 10, 10)
        self.assertEqual(forward, backward)
        self.assertEqual(forward[(2 * 10 + 2) * 4:(2 * 10 + 2) * 4 + 4], bytes((0, 0, 255, 255)))
        self.assertEqual(forward[(9 * 10 + 9) * 4 + 3], 0)


if __name__ == "__main__":
    unittest.main()
