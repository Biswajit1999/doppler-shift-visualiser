import unittest
import numpy as np
from research.rv_covariance_audit import (
    C_KMS, compose_los_velocities, multi_line_gls,
    velocity_from_wavelength, velocity_uncertainty,
)


class RVCovarianceTests(unittest.TestCase):
    def test_inverse_roundtrip(self):
        beta = np.array([-0.9, -0.1, 0.0, 0.1, 0.9])
        factor = np.sqrt((1 + beta) / (1 - beta))
        np.testing.assert_allclose(velocity_from_wavelength(500 * factor, 500),
                                   C_KMS * beta, rtol=1e-14, atol=1e-9)

    def test_invalid_wavelength(self):
        with self.assertRaises(ValueError):
            velocity_from_wavelength(-1, 500)

    def test_uncertainty_matches_finite_difference(self):
        obs, rest, sigma = 500.1, 500, 0.001
        numeric = (velocity_from_wavelength(obs + sigma, rest) -
                   velocity_from_wavelength(obs - sigma, rest)) / 2
        analytic = velocity_uncertainty(obs, rest, sigma)
        self.assertAlmostEqual(float(numeric / analytic), 1.0, places=9)

    def test_correlation_cancels_equal_common_wavelength_errors(self):
        sigma = velocity_uncertainty(500, 500, 0.001, 0.001, correlation=1)
        self.assertEqual(float(sigma), 0)

    def test_einstein_inverse(self):
        self.assertAlmostEqual(float(compose_los_velocities(50000, -50000)), 0.0, places=8)
        self.assertAlmostEqual(float(compose_los_velocities(0, 123)), 123.0, places=10)

    def test_einstein_is_not_classical_at_high_speed(self):
        v = float(compose_los_velocities(0.5 * C_KMS, 0.5 * C_KMS))
        self.assertAlmostEqual(v / C_KMS, 0.8, places=14)

    def test_subluminal_guard(self):
        with self.assertRaises(ValueError):
            compose_los_velocities(C_KMS, 10)

    def test_gls_independent_improves_sqrt_n(self):
        rest = np.array([500., 600., 700., 800.])
        out = multi_line_gls(rest, rest, np.ones(4) * 0.001)
        self.assertAlmostEqual(out["velocity_kms"], 0.0)
        self.assertEqual(out["degrees_of_freedom"], 3)
        self.assertGreater(out["sigma_kms"], 0)
        self.assertLess(out["sigma_kms"], velocity_uncertainty(500, 500, 0.001))

    def test_common_zero_point_increases_uncertainty(self):
        rest = np.array([500., 510., 520.])
        independent = multi_line_gls(rest, rest, 0.001)
        correlated = multi_line_gls(rest, rest, 0.001, common_zero_point_nm=0.005)
        self.assertGreater(correlated["sigma_kms"], independent["sigma_kms"])
        self.assertGreater(correlated["covariance_kms2"][0][1], 0)

    def test_rest_error_increases_uncertainty(self):
        rest = np.array([500., 510., 520.])
        baseline = multi_line_gls(rest, rest, 0.001)
        uncertain = multi_line_gls(rest, rest, 0.001, sigma_rest_nm=0.002)
        self.assertGreater(uncertain["sigma_kms"], baseline["sigma_kms"])

    def test_invalid_gls(self):
        with self.assertRaises(ValueError):
            multi_line_gls([500], [500], [0.001])
        with self.assertRaises(ValueError):
            multi_line_gls([500, 600], [500, 600], [0, 0])


if __name__ == "__main__":
    unittest.main()
