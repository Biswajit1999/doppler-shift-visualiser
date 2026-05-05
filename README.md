# Doppler Shift Visualiser

A simple Python and web-based tool for visualising Doppler shift in astronomical spectra.

## What this project does

This project shows how spectral lines move when an astronomical object has radial motion relative to the observer.

- Positive velocity means the object is moving away: redshift
- Negative velocity means the object is moving towards us: blueshift

## Physics background

For small velocities compared with the speed of light, the Doppler shift can be approximated as:

Δλ / λ = v / c

where:

- Δλ is the change in wavelength
- λ is the original wavelength
- v is radial velocity
- c is the speed of light

## Why this matters

Doppler shift is central to observational astronomy. It is used to study:

- radial velocity of stars
- exoplanet detection
- binary stars
- galaxy motion
- spectroscopy

## Live Demo

[Try the interactive tool](https://biswajit1999.github.io/doppler-shift-visualiser/web/)

## Python version

Run:

```bash
pip install -r requirements.txt
python main.py
