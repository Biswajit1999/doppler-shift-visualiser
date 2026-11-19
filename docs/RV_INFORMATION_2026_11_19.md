# Spectral RV information (19 November 2026)

Two new complementary diagnostics: (1) a finite-difference Fisher-information estimate of photon-noise-limited radial-velocity uncertainty for a fixed, sampled flux template with independent known Gaussian flux uncertainties; (2) wavelength-mask sensitivity using gradients calculated on the full wavelength grid before masking. The module also includes a stable longitudinal relativistic wavelength-to-velocity inversion as a regression reference; this inversion overlaps earlier PRs and is not counted as a novel research analysis.

The local derivative is `dF/dv = (lambda/c) dF/dlambda` at zero velocity, so `sigma_v = [sum((lambda dF/dlambda/(c sigma_F))^2)]^-1/2`. Assumptions: no correlated detector noise, no continuum nuisance parameters, no spectral resampling covariance, no telluric uncertainty, and no instrumental line-spread-function calibration. It is not a measured EPRV precision, and finite-difference gradients at the edges may be less accurate.

Run: `python -m unittest discover -s tests -p "test_*.py"` (requires numpy). Eight combined local development tests passed before upload; remote CI and exact branch-head testing remain unverified.

Code and tests were prepared with AI assistance for scientific review. No observational RV detection or instrument performance claim is made.
