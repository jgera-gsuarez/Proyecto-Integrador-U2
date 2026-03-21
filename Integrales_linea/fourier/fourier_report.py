import sympy as sp
from ..core.types import FourierResult

def format_fourier_report(fr: FourierResult) -> str:
    if fr.status != "ok":
        return f"[ERROR] {fr.message}"

    # Simplificamos los valores para que se vean bien (ej.: 2*pi en vez de 6.28...)
    a_nice = sp.simplify(fr.a)
    b_nice = sp.simplify(fr.b)
    t_nice = sp.simplify(fr.T)
    a0_nice = sp.simplify(fr.a0)

    lines = [
        "=== REPORTE SERIE DE FOURIER ===",
         f"Intervalo: [a,b] = [{a_nice}, {b_nice}],  T = {t_nice}",
         f"Armónicos calculados: {fr.n_harmonics}, Método utilizado: {fr.method_used}", "",
         "\nCoeficientes:",
         f"a0 = {a0_nice}"
    ]

    # Mostramos los primeros 5 por brevedad
    '''Para mostrar solo 5 coeficientes
    for i in range(min(len(fr.an),5)):
        n_val = i + 1
        an_val = sp.simplify(fr.an[i])
        bn_val = sp.simplify(fr.bn[i])
        lines.append(f"  n={n_val}: an={an_val}, bn={bn_val}")

    if len(fr.an) > 5:
        lines.append(f"  ... (+ {len(fr.an) - 5} coeficientes)"'''

    #Para mostrar todos los coeficientes
    for i in range(len(fr.an)):
        n_val = i + 1
        an_val = sp.simplify(fr.an[i])
        bn_val = sp.simplify(fr.bn[i])
        lines.append(f"  n={n_val}: an={an_val}, bn={bn_val}")

    lines.append("=========================")
    return "\n".join(lines)