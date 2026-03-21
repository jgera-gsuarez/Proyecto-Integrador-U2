import matplotlib.pyplot as plt
from ..core.types import FourierResult
from ..core.plotting import setup_standard_figure
import numpy as np


def plot_fourier_result(result: FourierResult, periods: int=2, show: bool=True):
    if result.status != "ok":
        return print(f"Error al graficar: {result.message}")

    # 1. Usamos la configuración estándar de core
    title = f"Aproximación de Serie de Fourier (N={result.n_harmonics})"
    fig, ax = setup_standard_figure(title, "x", "f(x)")

    # 2. Preparar datos
    a_val, b_val, t_val = float(result.a), float(result.b), float(result.T)
    x_min = a_val - (periods - 1) * t_val / 2
    x_max = b_val + (periods - 1) * t_val / 2
    x_pts = np.linspace(x_min, x_max, 1000)

    y_orig = np.array([result.f_callable(val) for val in x_pts])
    y_approx = np.array([result.s_callable(val) for val in x_pts])

    # 3. Dibujar en el 'ax' que nos dio core
    ax.plot(x_pts, y_orig, 'k--', alpha=0.5, label="Original (periódica)")
    ax.plot(x_pts, y_approx, 'r-', linewidth=1.5, label="Serie de Fourier")
    ax.axvspan(a_val, b_val, color='yellow', alpha=0.1, label="Intervalo Base")
    ax.legend()

    if show:
        plt.show()

    return fig  # Devolvemos la figura para la GUI

'''
   # 1. Definir el rango de visualización(por defecto 2 periodos)
    a_val = float(result.a)
    b_val = float(result.b)
    _T_val = float(result.T)

    x_min = a_val - (periods - 1) * _T_val / 2
    x_max = b_val + (periods - 1) * _T_val / 2

    x_pts = np.linspace(x_min, x_max, 1000)

    # 2. Evaluar las funciones usando los callables del motor
    # f_base es la original periódica, s_math es la serie truncada
    y_orig = np.array([result.f_callable(val) for val in x_pts])
    y_approx = np.array([result.s_callable(val) for val in x_pts])

    # 3. Configuración de la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(x_pts, y_orig, 'k--', alpha=0.5, label="Función Original (periódica)")
    plt.plot(x_pts, y_approx, 'r-', linewidth=1.5, label=f"Serie de Fourier (N={result.n_harmonics})")

    # Resaltar el intervalo fundamental [a, b]
    plt.axvspan(a_val, b_val, color='yellow', alpha=0.1, label="Intervalo Base")

    plt.title(f"Aproximación de Serie de Fourier\n$N = {result.n_harmonics}$ armónicos")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.legend()

    print("Mostrando gráfica... Cierra la ventana para continuar.")
    plt.show()
'''

def plot_coefficients(an, bn, title: str = "Coeficientes Fourier"):
    """
    an, bn: listas numéricas o arrays (n=1..N)
    """
    an = np.array(an, dtype=float)
    bn = np.array(bn, dtype=float)
    _N = len(an)
    n = np.arange(1, _N + 1)

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