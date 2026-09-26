"""Command-line Doppler-shift demonstration.

Positive velocity is receding. The default calculation uses the longitudinal
special-relativistic wavelength factor and reports the first-order residual.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

C_KMS = 299_792.458


def _validate(wavelength_nm: np.ndarray | float, velocity_kms: float) -> None:
    if np.any(np.asarray(wavelength_nm) <= 0) or not np.all(np.isfinite(wavelength_nm)):
        raise ValueError("wavelength must be positive and finite")
    if not np.isfinite(velocity_kms) or abs(velocity_kms) >= C_KMS:
        raise ValueError("velocity must be finite and satisfy |v| < c")


def classical_doppler_shift(wavelength_nm: np.ndarray | float, velocity_kms: float):
    _validate(wavelength_nm, velocity_kms)
    return np.asarray(wavelength_nm) * (1.0 + velocity_kms / C_KMS)


def relativistic_doppler_shift(wavelength_nm: np.ndarray | float, velocity_kms: float):
    _validate(wavelength_nm, velocity_kms)
    beta = velocity_kms / C_KMS
    factor = np.sqrt((1.0 + beta) / (1.0 - beta))
    return np.asarray(wavelength_nm) * factor


def gaussian_line(wavelength_nm: np.ndarray, centre_nm: float, width_nm: float) -> np.ndarray:
    return 1.0 - 0.8 * np.exp(-0.5 * ((wavelength_nm - centre_nm) / width_nm) ** 2)


def render_demo(velocity_kms: float, output_path: Path) -> Path:
    wavelength = np.linspace(580.0, 600.0, 4000)
    original_flux = gaussian_line(wavelength, centre_nm=589.592, width_nm=0.12)
    shifted_wavelength = relativistic_doppler_shift(wavelength, velocity_kms)
    first_order = classical_doppler_shift(589.592, velocity_kms)
    exact = float(relativistic_doppler_shift(589.592, velocity_kms))

    direction = "redshift" if velocity_kms > 0 else "blueshift" if velocity_kms < 0 else "no shift"
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(wavelength, original_flux, label="Rest-frame illustrative Na D1 line")
    ax.plot(shifted_wavelength, original_flux, "--", label=f"Exact shifted line ({direction})")
    ax.set(xlabel="Wavelength [nm]", ylabel="Relative flux", title=f"v = {velocity_kms:.3f} km s$^{{-1}}$")
    ax.text(
        0.02,
        0.04,
        f"exact λ = {exact:.9f} nm\nexact − first order = {(exact - first_order) * 1e3:.6g} pm",
        transform=ax.transAxes,
        fontsize=9,
    )
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return output_path


def main() -> None:
    print("Doppler Shift Visualiser")
    velocity = float(input("Radial velocity in km/s (+ receding, - approaching): "))
    output = render_demo(velocity, Path("outputs/doppler_shift_plot.png"))
    exact = float(relativistic_doppler_shift(589.592, velocity))
    print(f"Exact observed Na D1 wavelength: {exact:.9f} nm")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
