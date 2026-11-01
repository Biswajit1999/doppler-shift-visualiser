"""Reproduce synthetic wavelength/RV uncertainty and correlation checks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.rv_covariance_audit import (  # noqa: E402
    C_KMS, compose_los_velocities, multi_line_gls,
    velocity_from_wavelength, velocity_uncertainty,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--figure", type=Path)
    args = parser.parse_args()
    rest = np.array([500., 600., 700., 800.])
    velocity = 30.0
    factor = np.sqrt((1 + velocity / C_KMS) / (1 - velocity / C_KMS))
    observed = rest * factor
    independent = multi_line_gls(observed, rest, 0.001)
    correlated = multi_line_gls(observed, rest, 0.001, common_zero_point_nm=0.002)
    rng = np.random.default_rng(20261101)
    draws = observed[0] + rng.normal(0, 0.001, 20000)
    empirical_sigma = float(np.std(velocity_from_wavelength(draws, rest[0]), ddof=1))
    analytic_sigma = float(velocity_uncertainty(observed[0], rest[0], 0.001))
    composition = float(compose_los_velocities(30000, 30000))
    result = {
        "kind": "synthetic line-centroid and shared wavelength-zero-point sensitivity",
        "seed": 20261101,
        "injected_velocity_kms": velocity,
        "independent_gls": independent,
        "shared_zero_point_gls": correlated,
        "single_line_analytic_sigma_kms": analytic_sigma,
        "single_line_mc_sigma_kms": empirical_sigma,
        "single_line_mc_draws": len(draws),
        "relativistic_composition_30000_plus_30000_kms": composition,
        "classical_sum_kms": 60000,
        "limitations": "No measured line centroids, laboratory calibration covariance, barycentric ephemeris or empirical RV precision",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    if args.figure:
        import matplotlib.pyplot as plt
        zero_points = np.linspace(0, 0.005, 31)
        sigmas = [multi_line_gls(observed, rest, 0.001,
                  common_zero_point_nm=float(z))["sigma_kms"] for z in zero_points]
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(zero_points * 1000, sigmas)
        ax.set(xlabel="Assumed shared wavelength zero point (pm)",
               ylabel="Formal multi-line RV uncertainty (km/s)",
               title="Correlated wavelength calibration sensitivity")
        fig.tight_layout()
        args.figure.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.figure, dpi=150)
        plt.close(fig)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
