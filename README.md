# Doppler Shift Visualiser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Biswajit1999/doppler-shift-visualiser/actions/workflows/ci.yml/badge.svg)](https://github.com/Biswajit1999/doppler-shift-visualiser/actions/workflows/ci.yml)

An interactive spectroscopy laboratory for comparing the first-order and longitudinal special-relativistic Doppler relations, following source-frame stellar lines, and separating them from an observer-frame telluric feature.

## Live laboratory

[Open the interactive visualiser](https://biswajit1999.github.io/doppler-shift-visualiser/web/)

The browser view provides:

- exact `1 + z = sqrt((1 + beta)/(1 - beta))` wavelength shifts over ±300 km/s;
- the first-order `z ≈ v/c` approximation and its residual from the exact result;
- a labelled Na I D doublet plus representative stellar features;
- an O₂ B telluric feature that remains fixed in the observer frame;
- a deliberately exaggerated wavefront animation, clearly separate from the numerical calculation; and
- a photon-noise precision relation stated in the Bouchy–Pepe–Queloz quality-factor form.

This is an educational forward model, not a wavelength-calibration pipeline, synthetic spectrograph, cross-correlation implementation, or exoplanet detection claim.

## Numerical model

For one-dimensional relative motion in flat spacetime,

```text
beta = v / c
lambda_obs / lambda_0 = 1 + z = sqrt((1 + beta) / (1 - beta))
```

For `|v| << c`, `z ≈ v/c` and `lambda_obs ≈ lambda_0(1 + v/c)`. The interface computes the exact relation and reports the first-order discrepancy. It does not use this special-relativistic relation to explain cosmological redshift.

The photon-limited RV uncertainty context is

```text
sigma_v = c / (Q sqrt(N_e))
```

where `Q` summarizes the Doppler information content of the sampled spectrum and `N_e` is the detected photoelectron count. This is a lower bound conditional on the spectrum and detector sampling; stellar activity, calibration, tellurics, and instrumental systematics are additional.

## Run locally

Serve the repository so browser modules load correctly:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/web/`.

The separate Python demonstration can be run with:

```bash
python -m pip install -r requirements.txt
python main.py
```

## Verification

```bash
npm test
npm run validate:research
python -m unittest discover -s tests -p "test_*.py"
```

The JavaScript tests cover zero shift, low-velocity agreement, relativistic reciprocal symmetry, sign conventions, invalid inputs, and the photon-noise quality-factor relation. The Python tests independently exercise the numerical shift functions and output-path handling.

## Evidence and boundaries

- [Methods](docs/METHODS.md)
- [Validation](docs/VALIDATION.md)
- [Data and references](docs/DATA_SOURCES.md)
- [Limitations](docs/LIMITATIONS.md)

## Citation

See `CITATION.cff`. Code is MIT licensed. The project is independent and is not affiliated with NIST, ESO, NASA, ESA, or any instrument consortium.
