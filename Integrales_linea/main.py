import sympy as sp
from Integrales_linea import (
    parse_sympy_expr, parse_complex_math,
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

    f_str = ask("Ingresa f(z): ")
    f = parse_sympy_expr(f_str)

    print("\nElige contorno:")
    print("  1) Círculo |z - c| = R")
    print("  2) Polígono (triángulo/rectángulo) por vértices")
    opt = ask("Opción (1/2): ")

    orient_in = ask("Orientación (A=antihorario, H=horario) [A]: ").upper() or "A"
    orientation = 1 if orient_in == "A" else -1

    if opt == "1":
        c_str = ask("Centro c (ej. i, 1-2i): ")
        _R_str = ask("Radio R (real): ")
        c = parse_complex_math(c_str)
        _R = float(_R_str)
        contour = CircleContour(center_sym=c, radius=_R, orientation=orientation)

    elif opt == "2":
        n_str = ask("Número de vértices (3 para triángulo, 4 para rectángulo): ")
        n = int(n_str)
        verts = []
        for k in range(n):
            v_str = ask(f"Vértice {k+1} (ej. 1+i): ")
            verts.append(parse_complex_math(v_str))
        contour = PolygonContour(vertices_sym=verts, orientation=orientation)
    else:
        print("Opción inválida.")
        return

    result = integrate_by_residues(f, contour, z_symbol=z)
    print("\n" + format_report(result.report))
    print("\nResultado final (simbólico):", result.integral)

if __name__ == "__main__":
    main()