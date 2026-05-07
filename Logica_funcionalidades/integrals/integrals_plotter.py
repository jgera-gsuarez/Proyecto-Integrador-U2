import sympy as sp
import matplotlib.pyplot as plt
from ..core.plotting import setup_standard_figure
from ..core.exporter import get_output_path

def plot_complex_contour(res_data: dict, show: bool = True):
    """
    Grafica el contorno complejo y las singularidades.
    res_data: El diccionario que devuelve tu motor de residuos.
    """
    if res_data.get("status") != "ok":
        print(f"Error en datos de gráfica: {res_data.get('reason')}")
        return None

    # 1. Configuración base desde core
    fig, ax = setup_standard_figure("Plano Complejo: Análisis de Residuos", "Re(z)", "Im(z)")

    # 2. Dibujar el Contorno
    # Suponiendo que el contorno devuelve puntos para graficar o es un objeto conocido
    contour = res_data.get("contour_obj")

    if contour is None:
        print("Error: No se encontró el objeto 'contour_obj' en los datos de la integral.")
        return None

    if contour:
        # 1. Obtener puntos y dibujar
        z_points = contour.get_plot_points()
        if len(z_points) > 0:
            x_c = [z.real for z in z_points]
            y_c = [z.imag for z in z_points]
            ax.plot(x_c, y_c, 'b-', linewidth=2, label="Contorno C")

        # 2. Añadir una flecha para indicar orientación (opcional)
        mid = len(x_c) // 4
        ax.annotate('', xy=(x_c[mid + 1], y_c[mid + 1]), xytext=(x_c[mid], y_c[mid]),
                    arrowprops=dict(arrowstyle='->', color='blue', lw=2))

    # 3. Forzar límites basados en el objeto contour
    x_min, x_max, y_min, y_max = contour.bounds()

    # Calculamos un margen dinámico
    dx = x_max - x_min if x_max != x_min else 1.0
    dy = y_max - y_min if y_max != y_min else 1.0

    margin = 0.2 * max(dx, dy, 0.5)  # Evita margen cero si es un punto

    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(y_min - margin, y_max + margin)

    # 4. Dibujar Singularidades (Polos)
    # Polos dentro (Círculos verdes con X)
    inside = [complex(sp.N(p)) for p in res_data.get("inside", [])]
    if inside:
        ax.scatter([p.real for p in inside], [p.imag for p in inside],
                   color='green', marker='x', s=100, label="Polos Internos")
        for p in inside:
            ax.text(p.real, p.imag, f"  {p.real:.2f}+{p.imag:.2f}j", color='green', fontsize=9)

    # Polos fuera (Círculos rojos con X)
    outside = [complex(sp.N(p)) for p in res_data.get("outside", [])]
    if outside:
        ax.scatter([p.real for p in outside], [p.imag for p in outside],
                   color='red', marker='x', s=100, alpha=0.5, label="Polos Externos")

    # 4. Ajustes finales de ejes
    ax.axhline(0, color='black', linewidth=1)  # Eje Real
    ax.axvline(0, color='black', linewidth=1)  # Eje Imaginario
    ax.set_aspect('equal', adjustable='box')  # Para que los círculos no parezcan elipses y el tamaño
                                                # del lienzo pueda variar
    ax.legend()

    path = get_output_path("grafico_integral.png")
    plt.savefig(path)

    if show:
        plt.show()

    return fig