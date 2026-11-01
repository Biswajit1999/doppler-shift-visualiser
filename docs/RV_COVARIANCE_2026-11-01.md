# Spectroscopic RV covariance audit (1 November 2026)

This research module is independent of the educational browser's plotted stellar lines. It tests three numerical assumptions for one-dimensional longitudinal special-relativistic Doppler shifts.

1. **Stable inverse and delta-method uncertainty.** For positive rest/observed wavelengths, beta = tanh(log(lambda_obs/lambda_rest)). The first-order derivative is dv/dlog(lambda_obs/lambda_rest) = c(1-beta²). Independent wavelength uncertainties and an explicitly supplied within-line correlation propagate into the variance of the log ratio. This is local linearization, not an empirical error bar.
2. **Collinear frame composition.** The Einstein rule is evaluated via the sum of rapidities, which is stable and subluminal. It is **not** a barycentric correction: no observing time, sky direction, observatory, or ephemeris is provided.
3. **Multi-line GLS.** Convert each line's wavelength ratio to an RV and propagate independent centroid/rest-wavelength errors plus a single additive common wavelength-zero-point uncertainty in nm. Solve the full covariance-weighted constant-RV model; report formal uncertainty and chi-square. A common zero point does not average down like independent photon noise.

The synthetic reproducibility experiment uses four rest wavelengths (500, 600, 700, 800 nm), a common injected recession velocity of 30 km/s, 0.001 nm independent centroid errors, and an illustrative 0.002 nm shared zero point. A 20,000-draw Gaussian Monte Carlo checks the single-line first-order uncertainty. These are assumed parameters, **not** measured spectrograph performance. No air/vacuum convention, line blending, stellar activity, non-linear wavelength solution, barycentric ephemeris, or instrument-specific covariance is inferred.

Run python scripts/run_rv_covariance_audit.py --output /tmp/rv.json --figure /tmp/rv.png and python -m unittest discover -s tests -p test_rv_covariance_audit.py.

AI assistance was used in preparing this research code; Git authorship is attributed only to the authenticated repository owner.
