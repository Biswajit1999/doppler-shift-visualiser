"""Non-relativistic RV information and relativistic wavelength diagnostics."""
import numpy as np

C_M_S = 299792458.0


def _spectrum(wavelength, flux, sigma):
    w, f, s = (np.asarray(v, dtype=float) for v in (wavelength, flux, sigma))
    if w.ndim != 1 or len(w) < 4 or f.shape != w.shape or s.shape != w.shape or not all(np.all(np.isfinite(v)) for v in (w, f, s)) or np.any(w <= 0) or np.any(np.diff(w) <= 0) or np.any(s <= 0):
        raise ValueError('wavelength must increase; arrays finite and sigma positive')
    return w, f, s


def rv_information(wavelength, flux, sigma):
    """Fisher-limited RV sigma for fixed continuum and independent Gaussian flux errors."""
    w, f, s = _spectrum(wavelength, flux, sigma)
    derivative = np.gradient(f, w, edge_order=2)
    info = np.sum((w * derivative / (C_M_S * s))**2)
    if not np.isfinite(info) or info <= 0:
        raise ValueError('spectrum contains no RV information')
    return float(1 / np.sqrt(info))


def relativistic_velocity_from_wavelength(rest, observed):
    """Signed radial velocity for the longitudinal SR Doppler factor (receding positive)."""
    a = np.asarray(rest, float)
    b = np.asarray(observed, float)
    if np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)) or np.any(a <= 0) or np.any(b <= 0):
        raise ValueError('wavelengths must be positive finite')
    log_d = np.log(b/a)
    return C_M_S * np.tanh(log_d)


def rv_information_mask_sensitivity(wavelength, flux, sigma, masks):
    """RV precision for masks; gradients computed on full spectrum before masking."""
    w, f, s = _spectrum(wavelength, flux, sigma)
    d = np.gradient(f, w, edge_order=2)
    contributions = (w*d/(C_M_S*s))**2
    result = []
    for mask in masks:
        m = np.asarray(mask)
        if m.shape != w.shape or m.dtype != np.dtype(bool) or not np.any(m):
            raise ValueError('mask must be nonempty boolean vector')
        information = np.sum(contributions[m])
        result.append(float(1/np.sqrt(information)) if information > 0 else float('inf'))
    return np.asarray(result)
