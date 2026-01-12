"""
Calculateur de Cp et Cpk pour métrologie
"""

import statistics

def calculer_cp_cpk(mesures, nominal, tolerance):
    """
    Calcule Cp et Cpk
    
    Args:
        mesures: liste de valeurs mesurées
        nominal: valeur nominale
        tolerance: tolérance (±)
    
    Returns:
        dict avec cp, cpk, moyenne, sigma
    """
    moyenne = statistics.mean(mesures)
    sigma = statistics.stdev(mesures)
    
    # Limites
    lss = nominal + tolerance  # Limite Supérieure Spécification
    lsi = nominal - tolerance  # Limite Inférieure Spécification
    
    # Cp = tolérance totale / 6 sigma
    cp = (2 * tolerance) / (6 * sigma)
    
    # Cpk = min des deux côtés
    cpk_sup = (lss - moyenne) / (3 * sigma)
    cpk_inf = (moyenne - lsi) / (3 * sigma)
    cpk = min(cpk_sup, cpk_inf)
    
    return {
        'cp': cp,
        'cpk': cpk,
        'moyenne': moyenne,
        'sigma': sigma,
        'lss': lss,
        'lsi': lsi
    }

def interpreter_cpk(cpk):
    """Interprète la valeur de Cpk"""
    if cpk < 1.0:
        return "❌ Non capable"
    elif cpk < 1.33:
        return "⚠️ Acceptable"
    elif cpk < 1.67:
        return "✅ Capable"
    else:
        return "🌟 Excellent"

# EXEMPLE D'UTILISATION
if __name__ == "__main__":
    # Mesures d'un diamètre (en mm)
    mesures = [50.02, 49.98, 50.01, 49.99, 50.03, 
               50.00, 49.97, 50.02, 50.01, 49.98]
    
    nominal = 50.0
    tolerance = 0.05  # ±0.05 mm
    
    resultat = calculer_cp_cpk(mesures, nominal, tolerance)
    
    print("=" * 50)
    print("ANALYSE DE CAPABILITÉ PROCESSUS")
    print("=" * 50)
    print(f"Nominal : {nominal} mm")
    print(f"Tolérance : ±{tolerance} mm")
    print(f"Nombre de mesures : {len(mesures)}")
    print()
    print(f"Moyenne : {resultat['moyenne']:.4f} mm")
    print(f"Écart-type (σ) : {resultat['sigma']:.4f} mm")
    print()
    print(f"Cp  = {resultat['cp']:.2f}")
    print(f"Cpk = {resultat['cpk']:.2f}")
    print()
    print(f"Verdict : {interpreter_cpk(resultat['cpk'])}")
    print("=" * 50)
