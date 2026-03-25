import os
import sympy as sp
from Integrales_linea import(
    format_report,
    parse_expr_math, parse_number_math,
    export_to_latex,
    CircleContour, PolygonContour,
    integrate_by_residues,
    integrate_parametric, param_arc, param_segment,
    plot_complex_contour
)
from Integrales_linea.core.exporter import compile_latex


def ask(prompt: str) -> str:
    return input(prompt).strip()

def main():
    print("=== Elije que quieres hacer? ===")
    print("  1) Integrales")
    print("  2) Series de Fourier")
    option = ask("Opción (1/2):")
    if option == "1":
        integrals_menu()

    else:
        fourier_menu()

def integrals_menu():
    print("============= Integrales de Línea =============")
    print("======= Por Residuos o Parametrización =======")
    print("Entrada de complejos: a+bi, a-bi, i, -2i, etc.")
    print("Funciones: sin(z), cos(z), exp(z), etc. Potencias con ^ o **.\n")

    z = sp.Symbol('z')
    t = sp.Symbol('t', real=True)
    f_str = ask("Ingresa f(z): ")
    f = parse_expr_math(f_str)

    print("\nElige tipo de integral:")
    print("  1) Círculo completo (Residuos)")
    print("  2) Polígono cerrado (Residuos)")
    print("  3) Segmento de recta (Paramétrico)")
    print("  4) Arco de círculo (Paramétrico)")
    opt = ask("Opción:")

    path_al_tex = None

    if opt in["1", "2"]:
        orient_in = ask("Orientación (A=antihorario, H=horario) [A]: ").upper() or "A"
        orientation = 1 if orient_in == "A" else -1

        if opt == "1":
            c = parse_number_math(ask("Centro c (ej. i, 1-2i): "))
            _R_str = float (ask("Radio R (real): "))
            _R = float(_R_str)
            contour = CircleContour(center_sym=c, radius=_R, orientation=orientation)

        else:
            n_str = ask("Número de vértices (3 para triángulo, 4 para rectángulo): ")
            n = int(n_str)
            verts = [parse_number_math(ask(f"Vértice {k+1}: "))for k in range(n)]
            contour = PolygonContour(vertices_sym=verts, orientation=orientation)

        result = integrate_by_residues(f, contour, z_symbol=z)
        print("\n" + format_report(result.report))
        print("\nResultado final(simbólico):", sp.simplify(result.integral))

        #Preguntar si desea graficar
        ver_grafica = ask("\n¿Deseas ver la gráfica? (s/n): ").lower()
        if ver_grafica == 's':
            plot_complex_contour(result.report)

        # Preguntar si desea exportar el reporte en LaTeX
        ver_reporte_latex = ask("\n¿Deseas exportar el reporte en LaTeX? (s/n): ").lower()
        if ver_reporte_latex == 's':
            path_al_tex = export_to_latex(result.report, calc_type="integral")

        #Preguntar si desea exportar el reporte en PDF
        ver_reporte_pdf = ask("\n¿Deseas exportar el reporte en PDF?")
        if ver_reporte_pdf == 's':
            compile_latex(path_al_tex)

    #Lógica paramétrica (Opciones 3 y 4)
    elif opt == "3":
        z1 = parse_number_math(ask("Punto inicial z1: "))
        z2 = parse_number_math(ask("Punto final z2: "))
        z_t, t_start, t_end = param_segment(z1, z2, t)

        result = integrate_parametric(f, z, z_t, t, t_start, t_end)
        print(f"\nResultado Integral de Línea (Segmento): {sp.nsimplify(sp.simplify(result.integral))}")
        print("\nCálculo finalizado con éxito.")
        print("Recuerda: Si el resultado es 0 en una curva cerrada, puede que no haya polos dentro.")

        # Preguntar si desea graficar
        ver_grafica = ask("\n¿Deseas ver la gráfica? (s/n): ").lower()
        if ver_grafica == 's':
            plot_complex_contour(result.report)

        # Preguntar si desea exportar el reporte en LaTeX
        ver_reporte_latex = ask("\n¿Deseas exportar el reporte en LaTeX? (s/n): ").lower()
        if ver_reporte_latex == 's':
            path_al_tex = export_to_latex(result.report, calc_type="integral")

        # Preguntar si desea exportar el reporte en PDF
        ver_reporte_pdf = ask("\n¿Deseas exportar el reporte en PDF?")
        if ver_reporte_pdf == 's':
            compile_latex(path_al_tex)

    elif opt == "4":

        c = parse_number_math(ask("Centro del arco: "))
        _R = parse_number_math(ask("Radio: "))
        theta1 = parse_number_math(ask("Ángulo inicial (rad, ej 0): "))
        theta2 = parse_number_math(ask("Ángulo final (rad, ej 3.14): "))

        z_t, t_start, t_end = param_arc(c, _R, theta1, theta2, t)

        print(f"\nIntegrando f(z) desde ángulo {theta1} hasta {theta2}...")
        result = integrate_parametric(f, z, z_t, t, t_start, t_end)

        print("-" * 30)
        print(f"Resultado Integral de Arco: {sp.simplify(result.integral)}")
        print(f"Valor aproximado: {sp.simplify(result.integral.evalf())}")
        print("-" * 30)

        # Preguntar si desea graficar
        ver_grafica = ask("\n¿Deseas ver la gráfica? (s/n): ").lower()
        if ver_grafica == 's':
            plot_complex_contour(result.report)

        # Preguntar si desea exportar el reporte en PDF
        ver_reporte_latex = ask("\n¿Deseas exportar el reporte en LaTex? (s/n): ").lower()
        if ver_reporte_latex == 's':
            path_al_tex = export_to_latex(result.report, calc_type="integral")

        #Preguntar si desea exportar el reporte en PDF
        ver_reporte_pdf = ask("\n¿Deseas exportar el reporte en PDF?")
        if ver_reporte_pdf == 's':
            compile_latex(path_al_tex)

    else:
        print("Opción inválida.")

from Integrales_linea import(
    compute_fourier,
    plot_fourier_result, # Importar el nuevo plotter
    SignalSpec
)

def fourier_menu():
    print("\n=== Análisis de Series de Fourier ===")
    x = sp.Symbol('x', real=True)

    path_al_tex = None

    try:
        f_str = ask("Ingresa f(x): ")
        f_expr = parse_expr_math(f_str, local_dict={'x': x})

        _L_str = ask("Ingresa L (solo el valor, ej. pi): ")
        _L = parse_number_math(_L_str)

        _N = int(ask("Número de armónicos (N): "))

        # Creamos la señal
        signal = SignalSpec(expression=f_expr, symbol=x, lower_limit=-_L, upper_limit=_L)

        print(f"DEBUG: Llamando a compute_fourier con L={_L} y N={_N}...")

        # Llamada al motor
        result = compute_fourier(signal, _N)

        if result.status == "ok":
            # Usamos la función de reporte que escribimos en engine.py
            from Integrales_linea import format_fourier_report
            print(format_fourier_report(result))

            # 2. Preguntar si desea graficar
            ver_grafica = ask("\n¿Deseas ver la gráfica? (s/n): ").lower()
            if ver_grafica == 's':
                plot_fourier_result(result)

            # 3. Preguntar si desea exportar el reporte en LaTeX
            ver_reporte_latex = ask("\n¿Deseas exportar el reporte en LaTeX? (s/n): ").lower()
            if ver_reporte_latex == 's':
                path_al_tex = export_to_latex(result.report, calc_type="fourier")

            # Preguntar si desea exportar el reporte en PDF
            ver_reporte_pdf = ask("\n¿Deseas exportar el reporte en PDF?")
            if ver_reporte_pdf == 's':
                compile_latex(path_al_tex)

        else:
            print(f"DEBUG: El motor devolvió error: {result.message}")

    except Exception as e:
        print(f"DEBUG: Error en menu_fourier: {e}")




if __name__ == "__main__":
    main()