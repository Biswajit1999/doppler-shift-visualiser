"""Independent synthetic physics tests for the optional Doppler recovery lab."""
import unittest
import numpy as np
from main import relativistic_doppler_shift
from research.line_recovery import (
    _template, fisher_velocity_sigma, fit_line_velocity, injection_recovery,
)


class LineRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.w = np.linspace(589.25, 589.95, 240)

    def test_noiseless_exact_relativistic_recovery(self):
        g, _ = _template(self.w, 589.592, 0.06, 18.0)
        fit = fit_line_velocity(self.w, 1.02-0.4*g, 0.01)
        self.assertAlmostEqual(fit.velocity_kms, 18.0, delta=0.002)
        self.assertAlmostEqual(fit.depth, 0.4, delta=1e-5)
        self.assertAlmostEqual(fit.continuum, 1.02, delta=1e-5)

    def test_negative_velocity_sign(self):
        g, _ = _template(self.w, 589.592, 0.06, -21)
        fit = fit_line_velocity(self.w, 1-0.3*g, 0.01)
        self.assertAlmostEqual(fit.velocity_kms, -21, delta=0.002)

    def test_fisher_matches_profiled_curvature(self):
        g, _ = _template(self.w, 589.592, 0.06, 12)
        fit = fit_line_velocity(self.w, 1-0.3*g, 0.015)
        fisher = fisher_velocity_sigma(self.w, 0.015, velocity_kms=12)
        self.assertAlmostEqual(fit.sigma_velocity_kms, fisher, delta=0.01*fisher)

    def test_information_improves_with_noise(self):
        low = fisher_velocity_sigma(self.w, 0.02)
        high = fisher_velocity_sigma(self.w, 0.01)
        self.assertAlmostEqual(low / high, 2, places=9)

    def test_sampling_window_missing_line_rejected(self):
        w = np.linspace(590.5, 591.0, 120)
        with self.assertRaises(ValueError):
            fisher_velocity_sigma(w, 0.01)

    def test_reproducible_injections(self):
        a = injection_recovery(self.w, n_trials=24, seed=123)
        b = injection_recovery(self.w, n_trials=24, seed=123)
        self.assertEqual(a, b)
        self.assertLess(abs(a.bias_kms), 2.0)

    def test_stronger_telluric_blend_masking_reduces_bias(self):
        kwargs = dict(n_trials=25, seed=21, sigma_flux=0.005,
                      telluric_centre_nm=589.615, telluric_depth=0.25)
        unmasked = injection_recovery(self.w, mask_telluric=False, **kwargs)
        masked = injection_recovery(self.w, mask_telluric=True, **kwargs)
        self.assertLess(abs(masked.bias_kms), abs(unmasked.bias_kms))

    def test_invalid_inputs_rejected(self):
        g, _ = _template(self.w, 589.592, 0.06, 0)
        with self.assertRaises(ValueError):
            fit_line_velocity(self.w, 1-0.3*g, 0)
        with self.assertRaises(ValueError):
            fit_line_velocity(self.w[::-1], 1-0.3*g, 0.01)
        with self.assertRaises(ValueError):
            injection_recovery(self.w, n_trials=1)


if __name__ == "__main__":
    unittest.main()
