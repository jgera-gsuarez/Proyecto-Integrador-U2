import sympy as sp

def format_report(rep: dict) -> str:
    if rep.get("status") != "ok":
        lines = ["[ERROR] " + rep.get("reason", "Error desconocido.")]
        if rep.get("on_boundary"):
            lines.append("Singularidades en el contorno:")
            for p in rep["on_boundary"]:
                lines.append(f"  - {sp.simplify(p)}")
        return "\n".join(lines)

    lines = []
    lines.append("=== REPORTE (Teorema de Residuos) ===")
    lines.append(f"f(z) = {sp.simplify(rep['function'])}")
    lines.append("")
    lines.append("Singularidades candidatas (polos):")
    if rep["candidates"]:
        for p in rep["candidates"]:
            lines.append(f"  - {sp.simplify(p)}")
    else:
        lines.append("  (no se detectaron por el método actual)")

    lines.append("")
    lines.append("Clasificación respecto al contorno:")
    lines.append("  Dentro:")
    for p in rep["inside"]:
        lines.append(f"    * {sp.simplify(p)}")
    if not rep["inside"]:
        lines.append("    * (ninguna)")

    lines.append("  Fuera:")
    for p in rep["outside"]:
        lines.append(f"    * {sp.simplify(p)}")
    if not rep["outside"]:
        lines.append("    * (ninguna)")

    lines.append("")
    lines.append("Residuos en singularidades dentro:")
    if rep["residues"]:
        for a, r in rep["residues"]:
            lines.append(f"  Res(f, z={sp.simplify(a)}) = {sp.simplify(r)}")
    else:
        lines.append("  (no hay)")

    lines.append("")
    lines.append(f"Suma de residuos = {sp.simplify(rep['sum_residues'])}")
    orient = "antihorario (+1)" if rep["orientation"] == 1 else "horario (-1)"
    lines.append(f"Orientación = {orient}")
    lines.append("")
    lines.append(f"Integral = 2*pi*i * (suma) * orientación = {sp.simplify(rep['integral'])}")
    lines.append("====================================")
    return "\n".join(lines)
