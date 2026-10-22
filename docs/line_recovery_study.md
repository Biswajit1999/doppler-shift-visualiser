# Controlled Doppler line recovery and telluric-bias experiment

This is an **optional Python synthetic analysis** separate from the existing browser Doppler visualiser. It does not imply a spectrograph reduction, telluric correction pipeline, stellar RV measurement, or planet detection.

## Three independent diagnostics

1. **Weighted line-centroid recovery.** A Gaussian absorption profile is shifted by the existing exact longitudinal SR Doppler factor. A profiled least-squares likelihood fits continuum and line depth analytically at each trial velocity; a coarse scan and golden-section search fit velocity. The formal local 1-sigma curvature uncertainty assumes independent Gaussian flux errors and an exactly known line width/rest wavelength.
2. **Nuisance-marginalized Fisher information.** An analytic derivative of the shifted Gaussian is projected orthogonally to the continuum and depth nuisance directions. The resulting `1/sqrt(F)` is compared with independent finite-difference profile curvature in tests. It is a conditional toy lower bound, **not** an observed spectrograph `Q` or real RV precision forecast.
3. **Seeded injection recovery and fixed telluric blend.** Repeated independent-noise realizations compare clean, blended and masked spectra. The telluric line is fixed in the observer frame while the stellar line shifts. Masking trades information for bias control. Detection completeness and instrument noise correlations are outside this experiment.

## Reproduce

```bash
python -m unittest discover -s tests -p 'test_line_recovery.py' -v
python -m research.run_line_recovery --trials 60 --output outputs/line_recovery_synthetic.json
```

Only NumPy is required for this optional module (already listed in requirements.txt). Tests cover exact red/blue-shift recovery, Fisher/curvature consistency, scaling with flux uncertainty, telluric negative control, reproducible injections and failure on absent lines. These results are *synthetic only*; do not attach them to real targets or use them to infer stellar activity, barycentric corrections or detector performance.
