import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from ..core.plotting import setup_standard_figure
from ..core.exporter import get_output_path


def plot_transform_result(expr_sympy, f_range=(-5, 5), points=1000, show=True):
    """
    Grafica la Magnitud y Fase de una Transformada de Fourier compleja.
    """
    # 1. Preparar símbolos y funciones numéricas
    f = sp.symbols('f')
    # Lambdify convierte la expresión de SymPy a una función de NumPy (vectorizada)
    # Usamos "modules='numpy'" para que entienda funciones como sinc, exp, etc.
    f_callable = sp.lambdify(f, expr_sympy, modules=['numpy', {'sinc': lambda x: np.sinc(x / np.pi)}])

    # 2. Generar datos numéricos
    f_pts = np.linspace(f_range[0], f_range[1], points)
    complex_vals = f_callable(f_pts)

    magnitude = np.abs(complex_vals)
    phase = np.angle(complex_vals)  # Fase en radianes

    # 3. Crear la figura con dos subplots
    fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # --- Subplot 1: Magnitud ---
    # Usamos la estética de tu core
    setup_standard_figure("Espectro de Magnitud |X(f)|", "f (Hz)", "|X(f)|", ax=ax_mag)
    ax_mag.plot(f_pts, magnitude, color='blue', linewidth=2, label="Magnitud")
    ax_mag.fill_between(f_pts, magnitude, color='blue', alpha=0.1)
    ax_mag.legend()

    # --- Subplot 2: Fase ---
    setup_standard_figure("Espectro de Fase ∠X(f)", "f (Hz)", "Fase (rad)", ax=ax_phase)
    ax_phase.plot(f_pts, phase, color='red', linewidth=1.5, label="Fase")
    ax_phase.set_ylim(-np.pi - 0.5, np.pi + 0.5)  # Limitar de -pi a pi
    ax_phase.legend()

    plt.tight_layout()

    # 4. Exportación
    path = get_output_path("transformada_fourier.png")
    plt.savefig(path, dpi=300)

    if show:
        plt.show()

    return fig