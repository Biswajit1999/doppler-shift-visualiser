from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from main import C_KMS, relativistic_doppler_shift

def _inputs(wavelength_nm, flux, sigma_flux, mask=None):
    w = np.asarray(wavelength_nm, dtype=float)
    y = np.asarray(flux, dtype=float)
    s = np.asarray(sigma_flux, dtype=float)
    if s.ndim == 0:
        s = np.full_like(w, float(s))
    if w.ndim != 1 or w.size < 12 or w.shape != y.shape or (s.shape != w.shape):
        raise ValueError('need >=12 aligned wavelength, flux and sigma samples')
    if not np.all(np.isfinite(w)) or not np.all(np.isfinite(y)) or (not np.all(np.isfinite(s))):
        raise ValueError('arrays must be finite')
    if np.any(w <= 0) or np.any(np.diff(w) <= 0) or np.any(s <= 0):
        raise ValueError('wavelengths must increase and sigmas must be positive')
    if mask is not None:
        keep = np.asarray(mask, dtype=bool)
        if keep.shape != w.shape or keep.sum() < 12:
            raise ValueError('mask must retain at least 12 pixels')
        w, y, s = (w[keep], y[keep], s[keep])
    return (w, y, s)

def _template(w: np.ndarray, rest_nm: float, width_nm: float, velocity_kms: float):
    mu = float(relativistic_doppler_shift(rest_nm, velocity_kms))
    return (np.exp(-0.5 * ((w - mu) / width_nm) ** 2), mu)

def _profile(w, y, s, rest, width, v):
    g, _ = _template(w, rest, width, v)
    weight = 1 / s ** 2
    sw = weight.sum()
    sg = np.dot(weight, g)
    sgg = np.dot(weight, g * g)
    det = sw * sgg - sg * sg
    if det <= 1e-12 * sw * sgg:
        return (np.inf, np.nan, np.nan)
    sy = np.dot(weight, y)
    sgy = np.dot(weight * g, y)
    continuum = (sy * sgg - sg * sgy) / det
    amplitude = (sw * sgy - sg * sy) / det
    chi2 = np.dot(weight, (y - continuum - amplitude * g) ** 2)
    return (float(chi2), float(continuum), float(-amplitude))

@dataclass(frozen=True)
class LineFit:
    velocity_kms: float
    sigma_velocity_kms: float
    continuum: float
    depth: float
    chi_square: float
    degrees_of_freedom: int
    at_search_boundary: bool

def fit_line_velocity(wavelength_nm, flux, sigma_flux, *, rest_nm=589.592, width_nm=0.06, velocity_bounds_kms=(-40.0, 40.0), mask=None) -> LineFit:
    w, y, s = _inputs(wavelength_nm, flux, sigma_flux, mask)
    lo, hi = map(float, velocity_bounds_kms)
    if not np.isfinite([rest_nm, width_nm, lo, hi]).all() or rest_nm <= 0 or width_nm <= 0 or (not -C_KMS < lo < hi < C_KMS):
        raise ValueError('invalid line or search parameters')
    grid = np.linspace(lo, hi, 201)
    costs = np.array([_profile(w, y, s, rest_nm, width_nm, v)[0] for v in grid])
    best = int(np.argmin(costs))
    if best == 0 or best == grid.size - 1 or (not np.isfinite(costs[best])):
        raise ValueError('no interior identifiable line minimum; widen bounds/check wavelength coverage')
    a, b = (float(grid[best - 1]), float(grid[best + 1]))
    ratio = (np.sqrt(5.0) - 1.0) / 2.0
    x1, x2 = (b - ratio * (b - a), a + ratio * (b - a))
    f1 = _profile(w, y, s, rest_nm, width_nm, x1)[0]
    f2 = _profile(w, y, s, rest_nm, width_nm, x2)[0]
    for _ in range(70):
        if f1 > f2:
            a, x1, f1 = (x1, x2, f2)
            x2 = a + ratio * (b - a)
            f2 = _profile(w, y, s, rest_nm, width_nm, x2)[0]
        else:
            b, x2, f2 = (x2, x1, f1)
            x1 = b - ratio * (b - a)
            f1 = _profile(w, y, s, rest_nm, width_nm, x1)[0]
    v = (a + b) / 2
    chi2, continuum, depth = _profile(w, y, s, rest_nm, width_nm, v)
    h = max(0.002, 0.001 * (hi - lo))
    curvature = (_profile(w, y, s, rest_nm, width_nm, v + h)[0] - 2 * chi2 + _profile(w, y, s, rest_nm, width_nm, v - h)[0]) / h ** 2
    if not np.isfinite(curvature) or curvature <= 0 or depth <= 0:
        raise ValueError('no physical absorption-line solution or nonpositive curvature')
    return LineFit(float(v), float(np.sqrt(2 / curvature)), continuum, depth, chi2, int(w.size - 3), bool(abs(v - lo) < 1e-05 or abs(v - hi) < 1e-05))

def fisher_velocity_sigma(wavelength_nm, sigma_flux, *, rest_nm=589.592, width_nm=0.06, depth=0.3, velocity_kms=0.0, mask=None) -> float:
    w = np.asarray(wavelength_nm, dtype=float)
    dummy = np.ones_like(w)
    w, _, s = _inputs(w, dummy, sigma_flux, mask)
    if not np.isfinite([rest_nm, width_nm, depth, velocity_kms]).all() or rest_nm <= 0 or width_nm <= 0 or (depth <= 0):
        raise ValueError('invalid line parameters')
    g, mu = _template(w, rest_nm, width_nm, velocity_kms)
    beta = velocity_kms / C_KMS
    dmu_dv = mu / (C_KMS * (1 - beta ** 2))
    dflux_dv = -depth * g * (w - mu) / width_nm ** 2 * dmu_dv
    x = np.column_stack((np.ones_like(g), g))
    weighted_x = x / s[:, None]
    weighted_d = dflux_dv / s
    try:
        coefficients = np.linalg.solve(weighted_x.T @ weighted_x, weighted_x.T @ weighted_d)
    except np.linalg.LinAlgError as exc:
        raise ValueError('unidentifiable continuum/line depth') from exc
    projected = weighted_d - weighted_x @ coefficients
    information = float(projected @ projected)
    if not np.isfinite(information) or information <= 1e-15:
        raise ValueError('no measurable Doppler information in the specified sampling')
    return float(1 / np.sqrt(information))

@dataclass(frozen=True)
class InjectionResult:
    truth_velocity_kms: float
    n_trials: int
    median_velocity_kms: float
    bias_kms: float
    scatter_kms: float
    median_formal_sigma_kms: float
    fraction_within_two_sigma: float
    seed: int

def injection_recovery(wavelength_nm, *, truth_velocity_kms=12.0, rest_nm=589.592, width_nm=0.06, depth=0.3, sigma_flux=0.01, n_trials=60, telluric_centre_nm=None, telluric_depth=0.0, telluric_width_nm=0.015, mask_telluric=False, velocity_bounds_kms=(-40, 40), seed=20261022) -> InjectionResult:
    w = np.asarray(wavelength_nm, dtype=float)
    if w.ndim != 1 or w.size < 12 or (not np.all(np.isfinite(w))) or np.any(np.diff(w) <= 0):
        raise ValueError('invalid wavelength sampling')
    if not isinstance(n_trials, int) or n_trials < 2 or sigma_flux <= 0 or (not np.isfinite(sigma_flux)):
        raise ValueError('invalid trial count or noise')
    if not np.isfinite([depth, telluric_depth, telluric_width_nm]).all() or depth <= 0 or (not 0 <= telluric_depth < 1) or (telluric_width_nm <= 0):
        raise ValueError('invalid absorption parameters')
    star, _ = _template(w, rest_nm, width_nm, truth_velocity_kms)
    flux = 1 - depth * star
    mask = np.ones(w.size, dtype=bool)
    if telluric_centre_nm is not None:
        if not np.isfinite(telluric_centre_nm):
            raise ValueError('invalid telluric centre')
        atmospheric = np.exp(-0.5 * ((w - telluric_centre_nm) / telluric_width_nm) ** 2)
        flux *= 1 - telluric_depth * atmospheric
        if mask_telluric:
            mask = abs(w - telluric_centre_nm) > 3 * telluric_width_nm
    rng = np.random.default_rng(seed)
    estimates, formal = ([], [])
    for _ in range(n_trials):
        simulated = flux + rng.normal(0, sigma_flux, size=w.size)
        fit = fit_line_velocity(w, simulated, sigma_flux, rest_nm=rest_nm, width_nm=width_nm, velocity_bounds_kms=velocity_bounds_kms, mask=mask)
        estimates.append(fit.velocity_kms)
        formal.append(fit.sigma_velocity_kms)
    est, unc = (np.asarray(estimates), np.asarray(formal))
    return InjectionResult(truth_velocity_kms, n_trials, float(np.median(est)), float(np.mean(est - truth_velocity_kms)), float(np.std(est, ddof=1)), float(np.median(unc)), float(np.mean(abs(est - truth_velocity_kms) <= 2 * unc)), seed)
