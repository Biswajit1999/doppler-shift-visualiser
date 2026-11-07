"""Analytic RV sensitivity to wavelength calibration, conditional on known rest wavelengths."""
from __future__ import annotations
import math
C_KMS=299792.458

def relativistic_velocity(rest_nm, observed_nm):
    """Relativistic longitudinal Doppler convention; positive is redshift."""
    if not all(math.isfinite(x) and x>0 for x in (rest_nm,observed_nm)):
        raise ValueError("positive finite wavelengths required")
    r=observed_nm/rest_nm
    return C_KMS*math.tanh(math.log(r))

def wavelength_jacobian(rest_nm, observed_nm):
    """dv/d(lambda_obs), dv/d(lambda_rest), km/s per nm."""
    v=relativistic_velocity(rest_nm,observed_nm)
    factor=C_KMS*(1-(v/C_KMS)**2)
    return (-factor/rest_nm, factor/observed_nm)

def velocity_variance(rest_nm, observed_nm, sigma_rest_nm, sigma_obs_nm, correlation=0.):
    """First-order variance including cross-covariance of rest and observed wavelength.
    
    This does not account for shared calibration errors across different lines.
    """
    if not all(math.isfinite(s) and s>=0 for s in (sigma_rest_nm,sigma_obs_nm)):
        raise ValueError("nonnegative finite uncertainties required")
    if not math.isfinite(correlation) or abs(correlation)>1:
        raise ValueError("correlation must be within [-1,1]")
    a,b=wavelength_jacobian(rest_nm,observed_nm)
    variance=(a*sigma_rest_nm)**2+(b*sigma_obs_nm)**2+2*correlation*a*b*sigma_rest_nm*sigma_obs_nm
    return max(0.,variance)
