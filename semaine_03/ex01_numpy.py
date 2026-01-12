"""
SEMAINE 3 - Exercice 1 : Introduction a NumPy
Objectif : Utiliser NumPy pour les calculs de metrologie
"""

import numpy as np

# =============================================================================
# PARTIE 1 : Creation d'arrays
# =============================================================================

# Mesures de diametres (en mm)
mesures_liste = [50.02, 49.98, 50.01, 49.99, 50.03, 49.97, 50.00, 50.02, 49.98, 50.01]

# TODO 1 : Convertir la liste en array NumPy
mesures = np.array(mesures_liste)
print("TODO 1 - Array NumPy :")
print(mesures)
print(f"Type : {type(mesures)}")

# =============================================================================
# PARTIE 2 : Statistiques avec NumPy
# =============================================================================

# TODO 2 : Calculer les statistiques avec NumPy
# - moyenne avec np.mean()
# - ecart-type avec np.std(ddof=1) pour l'ecart-type echantillon
# - min et max avec np.min() et np.max()

moyenne = np.mean(mesures)
sigma = np.std(mesures, ddof=1)  # ddof=1 pour ecart-type echantillon
val_min = np.min(mesures)
val_max = np.max(mesures)

print("\nTODO 2 - Statistiques NumPy :")
print(f"Moyenne : {moyenne:.4f}")
print(f"Sigma   : {sigma:.4f}")
print(f"Min     : {val_min:.4f}")
print(f"Max     : {val_max:.4f}")

# =============================================================================
# PARTIE 3 : Operations vectorielles
# =============================================================================

nominal = 50.00

# TODO 3 : Calculer les ecarts par rapport au nominal (vectoriel)
# Soustraction sur tout l'array d'un coup - pas de boucle for !
ecarts = mesures - nominal

print("\nTODO 3 - Ecarts par rapport au nominal :")
print(f"Ecarts : {ecarts}")
print(f"Ecart moyen : {np.mean(ecarts):.4f}")
print(f"Ecart max absolu : {np.max(np.abs(ecarts)):.4f}")

# =============================================================================
# PARTIE 4 : Filtrage avec conditions
# =============================================================================

tolerance = 0.03  # +/- 0.03 mm

# TODO 4 : Trouver les mesures hors tolerance
# - Creer un masque booleen : hors_tol = (mesures < LSI) | (mesures > LSS)
# - Compter combien sont hors tolerance
# - Extraire les valeurs hors tolerance

lsi = nominal - tolerance  # 49.97
lss = nominal + tolerance  # 50.03

# Masque booleen : True si hors tolerance
hors_tol = (mesures < lsi) | (mesures > lss)

print("\nTODO 4 - Mesures hors tolerance :")
print(f"LSI = {lsi}, LSS = {lss}")
print(f"Masque : {hors_tol}")
print(f"Nombre hors tol : {np.sum(hors_tol)}")  # sum() compte les True
print(f"Valeurs hors tol : {mesures[hors_tol]}")  # Filtrage avec masque

# =============================================================================
# PARTIE 5 : Calcul du Cpk avec NumPy
# =============================================================================

# TODO 5 : Calculer le Cpk en utilisant NumPy
# CPU = (LSS - moyenne) / (3 * sigma)
# CPL = (moyenne - LSI) / (3 * sigma)
# Cpk = min(CPU, CPL)

cpu = (lss - moyenne) / (3 * sigma)
cpl = (moyenne - lsi) / (3 * sigma)
cpk = min(cpu, cpl)  # ou np.minimum(cpu, cpl) pour des arrays

print("\nTODO 5 - Calcul Cpk :")
print(f"CPU : {cpu:.2f}")
print(f"CPL : {cpl:.2f}")
print(f"Cpk : {cpk:.2f}")

# =============================================================================
# BONUS : Comparaison performance Python vs NumPy
# =============================================================================

# TODO BONUS : Generer 1 million de mesures aleatoires et comparer les temps
# Utiliser np.random.normal(mean, std, size) pour generer des donnees
# Utiliser time.time() pour mesurer le temps

print("\n" + "="*50)
print("BONUS - A toi de jouer !")
print("="*50)
