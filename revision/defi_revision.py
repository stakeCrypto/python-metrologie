"""
DÉFI RÉVISION : Programme complet de métrologie
Objectif : Lire un CSV, calculer stats + Cpk, afficher rapport
"""

import csv
import statistics

# TODO 1 : Créer une fonction lire_csv(fichier)
# qui retourne une liste de mesures (float)

def lire_csv(fichier):
    """
    Lit un fichier CSV et retourne une liste de mesures (float).
    Ignore la ligne d'en-tête.
    """
    mesures = []
    with open(fichier, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Saute l'en-tête
        for ligne in reader:
            if ligne:  # Vérifie que la ligne n'est pas vide
                mesures.append(float(ligne[0]))
    return mesures

# TODO 2 : Créer une fonction calculer_statistiques(mesures)
# qui retourne un dict avec : moyenne, sigma, min, max

def calculer_statistiques(mesures):
    """
    Calcule les statistiques descriptives d'une liste de mesures.
    Retourne un dictionnaire avec moyenne, sigma (écart-type), min et max.
    """
    return {
        'moyenne': statistics.mean(mesures),
        'sigma': statistics.stdev(mesures),  # Écart-type échantillon
        'min': min(mesures),
        'max': max(mesures)
    }

# TODO 3 : Créer une fonction calculer_cpk(mesures, nominal, tolerance)
# qui retourne le Cpk

def calculer_cpk(mesures, nominal, tolerance):
    """
    Calcule le Cpk (indice de capabilité centré).

    Formule : Cpk = min(CPU, CPL)
    - CPU = (LSS - moyenne) / (3 * sigma)
    - CPL = (moyenne - LSI) / (3 * sigma)

    où LSS = nominal + tolerance et LSI = nominal - tolerance
    """
    moyenne = statistics.mean(mesures)
    sigma = statistics.stdev(mesures)

    lss = nominal + tolerance  # Limite Supérieure de Spécification
    lsi = nominal - tolerance  # Limite Inférieure de Spécification

    cpu = (lss - moyenne) / (3 * sigma)
    cpl = (moyenne - lsi) / (3 * sigma)

    return min(cpu, cpl)

# TODO 4 : Créer une fonction afficher_rapport(stats, cpk)
# qui affiche tout de manière formatée

def afficher_rapport(stats, cpk):
    """
    Affiche un rapport formaté des statistiques et du Cpk.
    """
    print("=" * 40)
    print("      RAPPORT DE MÉTROLOGIE")
    print("=" * 40)
    print(f"Moyenne : {stats['moyenne']:.4f}")
    print(f"Sigma   : {stats['sigma']:.4f}")
    print(f"Min     : {stats['min']:.4f}")
    print(f"Max     : {stats['max']:.4f}")
    print("-" * 40)
    print(f"Cpk     : {cpk:.2f}")

    # Interprétation du Cpk
    if cpk >= 1.33:
        verdict = "Excellent - Processus capable"
    elif cpk >= 1.0:
        verdict = "Acceptable - Processus limite"
    else:
        verdict = "Non conforme - Amélioration requise"

    print(f"Verdict : {verdict}")
    print("=" * 40)

# TODO 5 : Dans le main, combiner tout

if __name__ == "__main__":
    # Créer un CSV de test
    with open('mesures_revision.csv', 'w') as f:
        f.write('mesure\n')
        f.write('50.01\n50.02\n49.98\n50.00\n50.03\n')
        f.write('49.97\n50.01\n49.99\n50.02\n50.00\n')
    
    # TODO 5 : Combiner tout dans le main
    # Paramètres de spécification : nominal = 50.00, tolérance = ±0.05
    nominal = 50.00
    tolerance = 0.05

    # Étape 1 : Lire les mesures
    mesures = lire_csv('mesures_revision.csv')
    print(f"Nombre de mesures lues : {len(mesures)}")

    # Étape 2 : Calculer les statistiques
    stats = calculer_statistiques(mesures)

    # Étape 3 : Calculer le Cpk
    cpk = calculer_cpk(mesures, nominal, tolerance)

    # Étape 4 : Afficher le rapport
    afficher_rapport(stats, cpk)
