import sympy as sp
import os
from datetime import datetime

def get_output_path(filename):
    """Crea la carpeta outputs si no existe y devuelve la ruta completa."""
    folder = "outputs"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return os.path.join(folder, filename)

def export_to_latex(res_data: dict, calc_type: str = "integral", method: str = "residues"):
    """Genera un archivo .tex basado en el tipo de cálculo."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = get_output_path(f"reporte_{calc_type}_{timestamp}.tex")

    with open(filename, "w", encoding="utf-8") as f:
        # Encabezado estándar de LaTeX
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\usepackage[utf8]{inputenc}" + "\n")
        f.write(r"\usepackage{amsmath}" + "\n")
        f.write(r"\begin{document}" + "\n")

        if calc_type == "integral":
                if method == "residues":
                    f.write(r"\section*{Reporte de Integración por Residuos}" + "\n")
                    f.write(f"Función: $f(z) = {sp.latex(res_data['function'])}$\n\n")
                    f.write(r"\subsection*{Singularidades y Residuos}" + "\n")
                    f.write(r"\begin{itemize}" + "\n")
                    for p, res in res_data.get("residues", []):
                        f.write(rf"    \item Polo en $z = {sp.latex(p)}$ con residuo ${sp.latex(res)}$\n")
                    f.write(r"\end{itemize}" + "\n")
                    f.write(rf"\nResultado Final: \[ {sp.latex(res_data['integral'])} \]\n")
                elif method == "parametric":
                    f.write(r"\section*{Reporte de Integración Paramétrica}" + "\n")
                    f.write(rf"Función: $f(z) = {sp.latex(res_data['function'])}$\n\n")
                    f.write(r"\subsection*{Parametrización de la curva}" + "\n")
                    f.write(r"Se define la trayectoria mediante la curva:" + "\n")
                    f.write(rf"\[z(t) = {sp.latex(res_data['parameters'])}\]" + "\n")
                    t_min, t_max = res_data['limits']
                    f.write(rf"para el intervalo $t \in [{sp.latex(t_min)}, {sp.latex(t_max)}]$." + "\n\n")
                    f.write(r"Al realizar la sustitución $z \to z(t)$ y aplicar el diferencial $dz = z'(t)dt$, " + "\n")
                    f.write(r"la integral de línea se transforma en una integral definida respecto a $t$:" + "\n")
                    # Usamos {{{ }}} para que LaTeX no se confunda con las f-strings de Python
                    f.write(rf"\[ \int_C f(z) \, dz = \int_{{{sp.latex(t_min)}}}^{{{sp.latex(t_max)}}} \left( {sp.latex(res_data['integrand_t'])} \right) \, dt \]" + "\n")

                    f.write(r"\vspace{1em}" + "\n")
                    f.write(rf"\textbf{{Resultado Final:}} ${sp.latex(res_data['integral'])}$" + "\n")

        elif calc_type == "fourier":
            f.write(r"\section*{Reporte de Serie de Fourier}" + "\n")
            f.write(rf"Señal original: $f(x) = {sp.latex(res_data['expression'])}$\n\n")
            f.write(rf"Periodo: $L = {sp.latex(res_data['L'])}$, Armónicos: $N = {res_data['N']}$\n\n")
            f.write(r"\subsection*{Coeficientes}" + "\n")
            f.write(rf"\[ a_0 = {sp.latex(res_data['a0'])} \]\n")
            # Aquí podrías iterar sobre an y bn si los tienes en una lista
            f.write(r"\subsection*{Serie Resultante}" + "\n")
            f.write(rf"\[ S_n(x) = {sp.latex(res_data['fourier_series'])} \]\n")

        f.write(r"\end{document}" + "\n")

    print(f"\n[Sistema] Reporte LaTeX generado en: {filename}")