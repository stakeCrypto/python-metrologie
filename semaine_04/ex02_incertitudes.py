"""
SEMAINE 4 - Exercice 2 : Calcul d'incertitudes (GUM)
Objectif : Appliquer la norme GUM pour calculer l'incertitude de mesure

GUM = Guide to the expression of Uncertainty in Measurement (ISO/IEC Guide 98-3)
"""

import numpy as np
import pandas as pd

# =============================================================================
# INTRODUCTION AU GUM
# =============================================================================
"""
Le GUM definit deux types d'incertitudes :

TYPE A : Evaluation statistique
  - Basee sur des mesures repetees
  - u_A = ecart-type / sqrt(n)  (ecart-type de la moyenne)

TYPE B : Evaluation non-statistique
  - Basee sur d'autres informations : certificats, specifications, experience
  - Distribution rectangulaire : u_B = a / sqrt(3)  (a = demi-largeur)
  - Distribution normale : u_B = valeur / k  (k = facteur de confiance)

INCERTITUDE COMBINEE :
  u_c = sqrt(u_A^2 + u_B1^2 + u_B2^2 + ...)

INCERTITUDE ELARGIE :
  U = k * u_c  (k=2 pour niveau de confiance ~95%)
"""

print("="*60)
print("CALCUL D'INCERTITUDES SELON LE GUM")
print("="*60)

# =============================================================================
# SCENARIO : Mesure de longueur avec un pied a coulisse
# =============================================================================

print("\nSCENARIO : Mesure d'une piece avec un pied a coulisse")
print("-"*60)

# Donnees du probleme
mesures = np.array([50.02, 50.01, 49.99, 50.03, 50.00,
                    50.02, 49.98, 50.01, 50.00, 50.01])  # 10 mesures en mm

# Sources d'incertitude de type B :
resolution_pied = 0.01  # mm (resolution du pied a coulisse)
erreur_etalonnage = 0.02  # mm (donnee du certificat d'etalonnage, k=2)
coef_dilatation = 0.005  # mm (incertitude due a la temperature)

print(f"Nombre de mesures : {len(mesures)}")
print(f"Resolution instrument : {resolution_pied} mm")
print(f"Erreur etalonnage (U95) : {erreur_etalonnage} mm")
print(f"Effet temperature : {coef_dilatation} mm")

# =============================================================================
# TODO 1 : Calculer l'incertitude de Type A
# =============================================================================

print("\n" + "="*60)
print("TODO 1 - Incertitude de Type A (statistique)")
print("="*60)

# Formule : u_A = ecart_type / sqrt(n)
# C'est l'ecart-type de la moyenne, pas des mesures

moyenne = np.mean(mesures)
ecart_type = np.std(mesures, ddof=1)  # ddof=1 pour ecart-type echantillon
n = len(mesures)

u_A = ecart_type / np.sqrt(n)

print(f"Moyenne des mesures : {moyenne:.4f} mm")
print(f"Ecart-type (s)      : {ecart_type:.4f} mm")
print(f"Nombre de mesures   : {n}")
print(f"u_A = s/sqrt(n)     : {u_A:.4f} mm")

# =============================================================================
# TODO 2 : Calculer les incertitudes de Type B
# =============================================================================

print("\n" + "="*60)
print("TODO 2 - Incertitudes de Type B (non-statistiques)")
print("="*60)

# u_B1 : Resolution (distribution rectangulaire)
#        La resolution cree une incertitude de +/- resolution/2
u_B1 = (resolution_pied / 2) / np.sqrt(3)
print(f"u_B1 (resolution)   : {u_B1:.4f} mm  [rectangulaire, a={resolution_pied/2}]")

# u_B2 : Etalonnage (deja donnee avec k=2, distribution normale)
#        On divise par k=2 pour retrouver l'incertitude-type
u_B2 = erreur_etalonnage / 2
print(f"u_B2 (etalonnage)   : {u_B2:.4f} mm  [normale, U/k avec k=2]")

# u_B3 : Temperature (distribution rectangulaire)
#        Effet estime de la variation de temperature
u_B3 = coef_dilatation / np.sqrt(3)
print(f"u_B3 (temperature)  : {u_B3:.4f} mm  [rectangulaire, a={coef_dilatation}]")

# =============================================================================
# TODO 3 : Calculer l'incertitude combinee
# =============================================================================

print("\n" + "="*60)
print("TODO 3 - Incertitude combinee")
print("="*60)

# Formule : u_c = sqrt(u_A^2 + u_B1^2 + u_B2^2 + u_B3^2)
# (somme quadratique - les sources sont independantes)

u_c = np.sqrt(u_A**2 + u_B1**2 + u_B2**2 + u_B3**2)

print(f"u_c = sqrt({u_A:.4f}^2 + {u_B1:.4f}^2 + {u_B2:.4f}^2 + {u_B3:.4f}^2)")
print(f"u_c = sqrt({u_A**2:.6f} + {u_B1**2:.6f} + {u_B2**2:.6f} + {u_B3**2:.6f})")
print(f"u_c = {u_c:.4f} mm")

# =============================================================================
# TODO 4 : Calculer l'incertitude elargie
# =============================================================================

print("\n" + "="*60)
print("TODO 4 - Incertitude elargie (U95)")
print("="*60)

# Formule : U = k * u_c
# k = 2 pour un niveau de confiance d'environ 95%

k = 2
U = k * u_c

print(f"Facteur d'elargissement : k = {k}")
print(f"U = k * u_c = {k} * {u_c:.4f}")
print(f"U = {U:.4f} mm (niveau de confiance ~95%)")

# =============================================================================
# TODO 5 : Exprimer le resultat final
# =============================================================================

print("\n" + "="*60)
print("TODO 5 - Resultat final")
print("="*60)

# Format standard : X = (valeur +/- U) unite [k=2, 95%]
# Arrondir l'incertitude a 2 chiffres significatifs
# Arrondir la valeur au meme niveau de decimales

# Arrondir U a 2 chiffres significatifs (ici 0.024)
U_arrondi = round(U, 3)  # 0.024 mm

# Arrondir la moyenne au meme niveau
moyenne_arrondie = round(moyenne, 3)  # 50.007 mm

print("RESULTAT DE MESURE (format GUM) :")
print("-" * 40)
print(f"L = ({moyenne_arrondie} +/- {U_arrondi}) mm")
print(f"    [k={k}, niveau de confiance ~95%]")
print("-" * 40)
print(f"\nInterpretation : La vraie valeur se trouve")
print(f"entre {moyenne_arrondie - U_arrondi:.3f} mm et {moyenne_arrondie + U_arrondi:.3f} mm")
print(f"avec une probabilite de 95%.")

# =============================================================================
# TODO 6 : Creer un bilan d'incertitude (tableau)
# =============================================================================

print("\n" + "="*60)
print("TODO 6 - Bilan d'incertitude")
print("="*60)

# Creer un DataFrame avec toutes les informations

# Calculer les contributions (en %)
variance_totale = u_c**2
contrib_A = (u_A**2 / variance_totale) * 100
contrib_B1 = (u_B1**2 / variance_totale) * 100
contrib_B2 = (u_B2**2 / variance_totale) * 100
contrib_B3 = (u_B3**2 / variance_totale) * 100

bilan = pd.DataFrame({
    'Source': ['Repetabilite', 'Resolution', 'Etalonnage', 'Temperature'],
    'Valeur': [f's={ecart_type:.4f}', f'r={resolution_pied}', f'U={erreur_etalonnage}', f'a={coef_dilatation}'],
    'Type': ['A', 'B', 'B', 'B'],
    'Distribution': ['Normale', 'Rectangulaire', 'Normale', 'Rectangulaire'],
    'Diviseur': [f'sqrt({n})', 'sqrt(3)', '2', 'sqrt(3)'],
    'u (mm)': [u_A, u_B1, u_B2, u_B3],
    'Contrib (%)': [contrib_A, contrib_B1, contrib_B2, contrib_B3]
})

print("BILAN D'INCERTITUDE :")
print(bilan.to_string(index=False))

print(f"\nSource dominante : Etalonnage ({contrib_B2:.1f}%)")
print("Recommandation : Utiliser un instrument mieux etalonne pour reduire l'incertitude.")

print("\n" + "="*60)
print("EXERCICE TERMINE !")
print("="*60)
