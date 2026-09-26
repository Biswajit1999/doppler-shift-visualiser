from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np

from main import C_KMS, classical_doppler_shift, relativistic_doppler_shift, render_demo


class DopplerPhysicsTests(unittest.TestCase):
    def test_zero_velocity(self):
        self.assertEqual(float(relativistic_doppler_shift(589.592, 0)), 589.592)

    def test_low_velocity_limit(self):
        exact = float(relativistic_doppler_shift(589.592, 0.03))
        classical = float(classical_doppler_shift(589.592, 0.03))
        self.assertLess(abs(exact - classical), 1e-10)

    def test_reciprocal_factors(self):
        positive = float(relativistic_doppler_shift(1.0, 30_000))
        negative = float(relativistic_doppler_shift(1.0, -30_000))
        self.assertAlmostEqual(positive * negative, 1.0, places=14)

    def test_invalid_velocity(self):
        with self.assertRaises(ValueError):
            relativistic_doppler_shift(500.0, C_KMS)

    def test_render_creates_parent_directory(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "figure.png"
            self.assertEqual(render_demo(30.0, output), output)
            self.assertGreater(output.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
