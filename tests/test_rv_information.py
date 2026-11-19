import unittest
import numpy as np
from research.doppler_diagnostics import rv_information, relativistic_velocity_from_wavelength, rv_information_mask_sensitivity, C_M_S


class RVInformationTests(unittest.TestCase):
    def test_uncertainty_scaling(self):
        w = np.linspace(500, 501, 101)
        f = 1 - .5*np.exp(-((w-500.5)/.07)**2)
        a = rv_information(w, f, np.full(101, .01))
        b = rv_information(w, f, np.full(101, .02))
        self.assertAlmostEqual(b/a, 2)

    def test_relativistic_inverse(self):
        beta = .1
        factor = np.sqrt((1+beta)/(1-beta))
        self.assertAlmostEqual(float(relativistic_velocity_from_wavelength(500, 500*factor))/C_M_S, beta)

    def test_mask_reduces_information(self):
        w = np.linspace(500, 501, 101)
        f = np.sin(w*20)
        s = np.ones(101)*.01
        full, half = rv_information_mask_sensitivity(w, f, s, [np.ones(101, bool), np.arange(101)<50])
        self.assertGreaterEqual(half, full)
