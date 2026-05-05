import numpy as np
import matplotlib.pyplot as plt

# Speed of light in km/s
C = 299792.458

def doppler_shift(wavelength_nm, velocity_kms):
    """
    Non-relativistic Doppler shift approximation:
    shifted wavelength = wavelength * (1 + v/c)

    Positive velocity = object moving away = redshift
    Negative velocity = object moving towards us = blueshift
    """
    return wavelength_nm * (1 + velocity_kms / C)


def gaussian_line(wavelength, centre, width):
    return 1 - 0.8 * np.exp(-0.5 * ((wavelength - centre) / width) ** 2)


def main():
    print("Doppler Shift Visualiser")
    print("------------------------")
    velocity = float(input("Enter radial velocity in km/s (+ away, - towards): "))

    wavelength = np.linspace(500, 700, 2000)

    # Example absorption line around 589 nm, similar to sodium D region
    original_flux = gaussian_line(wavelength, centre=589.0, width=1.2)
    shifted_wavelength = doppler_shift(wavelength, velocity)

    direction = "redshift" if velocity > 0 else "blueshift" if velocity < 0 else "no shift"

    plt.figure(figsize=(10, 5))
    plt.plot(wavelength, original_flux, label="Original spectrum")
    plt.plot(shifted_wavelength, original_flux, "--", label=f"Shifted spectrum ({direction})")

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Relative flux")
    plt.title(f"Doppler Shift Visualiser: v = {velocity:.2f} km/s")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig("outputs/doppler_shift_plot.png", dpi=300)
    plt.show()

    print(f"\nVelocity: {velocity:.2f} km/s")
    print(f"Effect: {direction}")
    print("Plot saved to outputs/doppler_shift_plot.png")


if __name__ == "__main__":
    main()
