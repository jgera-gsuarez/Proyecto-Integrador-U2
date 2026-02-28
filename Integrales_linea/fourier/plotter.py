# Integrales_linea/fourier/plotter.py
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np


def plot_fourier_basic(plot_data: dict, title: str = "Serie de Fourier"):
    """
    plot_data esperado:
      x, f, S, err
    """
    x = plot_data["x"]
    f = plot_data["f"]
    S = plot_data["S"]
    err = plot_data["err"]

    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    axs[0].plot(x, f, label="f(x)")
    axs[0].plot(x, S, label="S_N(x)")
    axs[0].set_title(title)
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(x, err, label="error f(x)-S_N(x)")
    axs[1].legend()
    axs[1].grid(True)
    axs[1].set_xlabel("x")

    plt.tight_layout()
    plt.show()


def plot_coefficients(an, bn, title: str = "Coeficientes Fourier"):
    """
    an, bn: listas numéricas o arrays (n=1..N)
    """
    an = np.array(an, dtype=float)
    bn = np.array(bn, dtype=float)
    N = len(an)
    n = np.arange(1, N + 1)

    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    axs[0].bar(n, np.abs(an))
    axs[0].set_title(title + " |a_n|")
    axs[0].grid(True)

    axs[1].bar(n, np.abs(bn))
    axs[1].set_title(title + " |b_n|")
    axs[1].grid(True)
    axs[1].set_xlabel("n")

    plt.tight_layout()
    plt.show()