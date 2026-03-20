import sympy as sp
from integrals.param_integrator import (
    integrate_parametric, param_arc, param_segment
)
from Integrales_linea import (
    parse_expr_math, parse_number_math,
    CircleContour, PolygonContour,
    integrate_by_residues, format_report
)
def ask(prompt: str) -> str:
    return input(prompt).strip()


def main():
    print("=== Integrales de Línea por Residuos (CLI) ===")
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
    opt = ask("Opción (1/2/3/4):")

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

#Lógica paramétrica (Opciones 3 y 4)
    elif opt == "3":
        z1 = parse_number_math(ask("Punto inicial z1: "))
        z2 = parse_number_math(ask("Punto final z2: "))
        z_t, t_start, t_end = param_segment(z1, z2, t)

        result = integrate_parametric(f, z, z_t, t, t_start, t_end)
        print(f"\nResultado Integral de Línea (Segmento): {sp.nsimplify(sp.simplify(result))}")
        print("\nCálculo finalizado con éxito.")
        print("Recuerda: Si el resultado es 0 en una curva cerrada, puede que no haya polos dentro.")
    elif opt == "4":

        c = parse_number_math(ask("Centro del arco: "))
        _R = parse_number_math(ask("Radio: "))
        theta1 = parse_number_math(ask("Ángulo inicial (rad, ej 0): "))
        theta2 = parse_number_math(ask("Ángulo final (rad, ej 3.14): "))

        z_t, t_start, t_end = param_arc(c, _R, theta1, theta2, t)

        print(f"\nIntegrando f(z) desde ángulo {theta1} hasta {theta2}...")
        result = integrate_parametric(f, z, z_t, t, t_start, t_end)

        print("-" * 30)
        print(f"Resultado Integral de Arco: {sp.simplify(result)}")
        print(f"Valor aproximado: {sp.simplify(result.evalf())}")
        print("-" * 30)

    else:
        print("Opción inválida.")

if __name__ == "__main__":
    main()