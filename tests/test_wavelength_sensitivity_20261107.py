"""Independent finite-difference and limiting-case checks."""
import unittest
import math
from research.wavelength_sensitivity_20261107 import relativistic_velocity,wavelength_jacobian,velocity_variance,C_KMS

class WavelengthTests(unittest.TestCase):
    def test_zero(self):
        self.assertAlmostEqual(relativistic_velocity(500,500),0)
    def test_jacobian_finite_difference(self):
        h=1e-4
        a,b=wavelength_jacobian(500,501)
        self.assertAlmostEqual(a,(relativistic_velocity(500+h,501)-relativistic_velocity(500-h,501))/(2*h),places=5)
        self.assertAlmostEqual(b,(relativistic_velocity(500,501+h)-relativistic_velocity(500,501-h))/(2*h),places=5)
    def test_common_mode_cancel(self):
        self.assertAlmostEqual(velocity_variance(500,500,.001,.001,1),0,places=12)
    def test_independent(self):
        expected=2*(C_KMS*.001/500)**2
        self.assertAlmostEqual(velocity_variance(500,500,.001,.001),expected)
    def test_invalid(self):
        with self.assertRaises(ValueError): velocity_variance(500,501,.1,.1,1.1)
if __name__=="__main__": unittest.main()
