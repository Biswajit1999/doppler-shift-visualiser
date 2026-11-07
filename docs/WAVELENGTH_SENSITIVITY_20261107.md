# Wavelength uncertainty sensitivity (2026-11-07)

Two analytic diagnostics: stable relativistic Doppler wavelength Jacobian and first-order correlated rest/observed wavelength uncertainty. Positive velocity is redshift. The two-wavelength correlation is not a multi-line calibration covariance. First-order propagation may fail for broad or non-Gaussian uncertainties. Reproduce: `python -m unittest discover -s tests -p 'test_wavelength_sensitivity_20261107.py'`. All tests use synthetic/analytic cases, not instrument data. AI-assisted implementation; review before scientific use.
