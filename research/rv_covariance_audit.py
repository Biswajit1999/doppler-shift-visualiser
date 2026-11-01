"""Longitudinal SR Doppler inversion and conditional line-centroid covariance.

Positive velocity denotes recession. No barycentric ephemeris or calibration
solution is inferred: the common wavelength offset is an assumed nuisance.
"""

from __future__ import annotations

import numpy as np

C_KMS = 299_792.458


def _positive_finite(x, name):
    a = np.asarray(x, dtype=float)
    if not np.all(np.isfinite(a)) or np.any(a <= 0):
        raise ValueError(f"{name} must be finite and positive")
    return a


def velocity_from_wavelength(observed_nm, rest_nm):
    """Stable inversion beta=tanh(log(lambda_obs/lambda_rest))."""
    obs = _positive_finite(observed_nm, "observed wavelength")
    rest = _positive_finite(rest_nm, "rest wavelength")
    return C_KMS * np.tanh(np.log(obs) - np.log(rest))


def velocity_uncertainty(observed_nm, rest_nm, sigma_obs_nm, sigma_rest_nm=0.0,
                         correlation=0.0):
    """First-order standard deviation including within-line wavelength correlation."""
    obs = _positive_finite(observed_nm, "observed wavelength")
    rest = _positive_finite(rest_nm, "rest wavelength")
    so = np.asarray(sigma_obs_nm, dtype=float)
    sr = np.asarray(sigma_rest_nm, dtype=float)
    if not np.all(np.isfinite(so)) or not np.all(np.isfinite(sr)) or np.any(so < 0) or np.any(sr < 0):
        raise ValueError("uncertainties must be finite and nonnegative")
    if not np.isfinite(correlation) or abs(correlation) > 1:
        raise ValueError("correlation must lie in [-1,1]")
    beta = np.tanh(np.log(obs) - np.log(rest))
    g = C_KMS * (1 - beta**2)
    variance = g**2 * ((so / obs)**2 + (sr / rest)**2 -
                       2 * correlation * so * sr / (obs * rest))
    return np.sqrt(np.maximum(variance, 0.0))


def compose_los_velocities(first_kms, second_kms):
    """Einstein addition for collinear inertial velocities, not ephemeris correction."""
    a, b = np.asarray(first_kms, dtype=float), np.asarray(second_kms, dtype=float)
    if (not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)) or
            np.any(np.abs(a) >= C_KMS) or np.any(np.abs(b) >= C_KMS)):
        raise ValueError("velocities must be finite and subluminal")
    return C_KMS * np.tanh(np.arctanh(a / C_KMS) + np.arctanh(b / C_KMS))


def multi_line_gls(observed_nm, rest_nm, sigma_obs_nm, *,
                   sigma_rest_nm=0.0, common_zero_point_nm=0.0):
    """Common-RV GLS under independent centroid errors plus additive shared offset.

    Linearization assumes small wavelength errors relative to line centres.
    Common zero-point is perfectly correlated *in nm* across all lines.
    """
    obs = _positive_finite(observed_nm, "observed wavelength")
    rest = _positive_finite(rest_nm, "rest wavelength")
    if obs.ndim != 1 or rest.shape != obs.shape or len(obs) < 2:
        raise ValueError("at least two matched one-dimensional lines required")
    so = np.broadcast_to(np.asarray(sigma_obs_nm, dtype=float), obs.shape)
    sr = np.broadcast_to(np.asarray(sigma_rest_nm, dtype=float), obs.shape)
    zp = float(common_zero_point_nm)
    if (np.any(~np.isfinite(so)) or np.any(so <= 0) or
            np.any(~np.isfinite(sr)) or np.any(sr < 0) or
            not np.isfinite(zp) or zp < 0):
        raise ValueError("invalid wavelength uncertainties")
    v = velocity_from_wavelength(obs, rest)
    beta = v / C_KMS
    d_obs = C_KMS * (1 - beta**2) / obs
    d_rest = -C_KMS * (1 - beta**2) / rest
    diagonal = (d_obs * so)**2 + (d_rest * sr)**2
    covariance = np.diag(diagonal) + zp**2 * np.outer(d_obs, d_obs)
    ones = np.ones(len(v))
    weights = np.linalg.solve(covariance, ones)
    den = float(ones @ weights)
    if den <= 0:
        raise ValueError("nonpositive GLS information")
    estimate = float(weights @ v / den)
    uncertainty = float(np.sqrt(1 / den))
    residual = v - estimate
    chi2 = float(residual @ np.linalg.solve(covariance, residual))
    return {"velocity_kms": estimate, "sigma_kms": uncertainty,
            "chi2": chi2, "degrees_of_freedom": len(v) - 1,
            "line_velocities_kms": v.tolist(), "covariance_kms2": covariance.tolist(),
            "assumed_common_zero_point_nm": zp}
