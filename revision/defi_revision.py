"""
DÉFI RÉVISION : Programme complet de métrologie
Objectif : Lire un CSV, calculer stats + Cpk, afficher rapport
"""

import csv
import statistics

def lire_csv(fichier):
    """Lit un fichier CSV et retourne une liste de mesures"""
    mesures = []
    with open(fichier, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            mesures.append(float(row[0]))
    return mesures

def calculer_statistiques(mesures):
    """Calcule moyenne, sigma, min, max"""
    moyenne = statistics.mean(mesures)
    sigma = statistics.stdev(mesures)
    minimum = min(mesures)
    maximum = max(mesures)
    
    return {
        'moyenne': moyenne,
        'sigma': sigma,
        'min': minimum,
        'max': maximum
    }

def calculer_cpk(mesures, nominal, tolerance):
    """Calcule le Cpk"""
    stats = calculer_statistiques(mesures)
    moyenne = stats['moyenne']
    sigma = stats['sigma']
    
    lss = nominal + tolerance
    lsi = nominal - tolerance
    
    cpk_sup = (lss - moyenne) / (3 * sigma)
    cpk_inf = (moyenne - lsi) / (3 * sigma)
    cpk = min(cpk_sup, cpk_inf)
    
    return cpk

def afficher_rapport(stats, cpk, nb_mesures):
    """Affiche le rapport formaté"""
    print("=== RAPPORT MÉTROLOGIE ===")
    print(f"Mesures : {nb_mesures}")
    print(f"Moyenne : {stats['moyenne']:.2f} mm")
    print(f"Sigma   : {stats['sigma']:.2f} mm")
    print(f"Min/Max : {stats['min']:.2f} / {stats['max']:.2f} mm")
    
    if cpk < 1.0:
        verdict = "❌ Non capable"
    elif cpk < 1.33:
        verdict = "⚠️ Acceptable"
    else:
        verdict = "✅ Capable"
    
    print(f"Cpk     : {cpk:.2f} {verdict}")

if __name__ == "__main__":
    # Créer un CSV de test
    with open('mesures_revision.csv', 'w') as f:
        f.write('mesure\n')
        f.write('50.01\n50.02\n49.98\n50.00\n50.03\n')
        f.write('49.97\n50.01\n49.99\n50.02\n50.00\n')
    
    # Lire les mesures
    mesures = lire_csv('mesures_revision.csv')
    
    # Calculer les statistiques
    stats = calculer_statistiques(mesures)
    
    # Calculer le Cpk (nominal 50mm, tolérance ±0.05mm)
    cpk = calculer_cpk(mesures, 50.0, 0.05)
    
    # Afficher le rapport
    afficher_rapport(stats, cpk, len(mesures))
