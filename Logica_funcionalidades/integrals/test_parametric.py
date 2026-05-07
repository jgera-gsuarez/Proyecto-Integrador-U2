import sympy as sp
from param_integrator import integrate_parametric, param_segment


def test_line_integral():
    z = sp.Symbol('z')
    t = sp.Symbol('t', real=True)

    # 1. Definimos la función f(z) = z^2
    f_z = z ** 2

    # 2. Definimos el segmento: de 0 a 1 + i
    z1 = 0
    z2 = 1 + sp.I
    z_t, t_start, t_end = param_segment(z1, z2, t)

    # 3. Calculamos la integral
    resultado = integrate_parametric(f_z, z, z_t, t, t_start, t_end)

    # Verificación manual:
    # La primitiva es z^3 / 3.
    # Evaluado: (1+i)^3 / 3 - 0 = (-2 + 2i) / 3
    print(f"Función: f(z) = {f_z}")
    print(f"Trayectoria: de {z1} a {z2}")
    print(f"Resultado SymPy: {resultado}")
    print(f"Resultado Simplificado: {sp.expand(resultado)}")


if __name__ == "__main__":
    test_line_integral()