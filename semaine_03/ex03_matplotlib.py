"""
SEMAINE 3 - Exercice 3 : Introduction a Matplotlib
Objectif : Visualiser des donnees de metrologie
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# =============================================================================
# PREPARATION : Charger les donnees
# =============================================================================

# Generer des donnees de test
np.random.seed(42)
n = 50
dates = pd.date_range('2024-01-01', periods=n, freq='D')
mesures = 50.0 + np.cumsum(np.random.normal(0, 0.005, n))  # Derive progressive

df = pd.DataFrame({
    'date': dates,
    'mesure': mesures
})

nominal = 50.0
tolerance = 0.05
lsi, lss = nominal - tolerance, nominal + tolerance

print(f"Donnees : {len(df)} mesures sur {n} jours")
print(f"Nominal : {nominal}, Tolerance : +/-{tolerance}")

# =============================================================================
# PARTIE 1 : Graphique de base - Evolution temporelle
# =============================================================================

# TODO 1 : Creer un graphique lineaire simple
# - plt.figure(figsize=(10, 5))  : taille du graphique
# - plt.plot(x, y)               : tracer la courbe
# - plt.xlabel(), plt.ylabel()   : etiquettes des axes
# - plt.title()                  : titre
# - plt.savefig('nom.png')       : sauvegarder
# - plt.show() ou plt.close()    : afficher ou fermer

print("\n" + "="*50)
print("TODO 1 - Graphique lineaire :")

plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['mesure'], marker='o', markersize=3)
plt.xlabel('Date')
plt.ylabel('Mesure (mm)')
plt.title('Evolution des mesures dans le temps')
plt.grid(True, alpha=0.3)
plt.savefig('01_evolution.png', dpi=100, bbox_inches='tight')
plt.close()
print("Graphique sauvegarde : 01_evolution.png")

# =============================================================================
# PARTIE 2 : Ajouter les limites de specification
# =============================================================================

# TODO 2 : Ajouter des lignes horizontales pour les limites
# - plt.axhline(y, color, linestyle, label) : ligne horizontale
# - plt.legend() : afficher la legende

print("\n" + "="*50)
print("TODO 2 - Avec limites de specification :")

plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['mesure'], marker='o', markersize=3, label='Mesures')

# Lignes horizontales pour les limites
plt.axhline(y=nominal, color='green', linestyle='-', label=f'Nominal ({nominal})')
plt.axhline(y=lss, color='red', linestyle='--', label=f'LSS ({lss})')
plt.axhline(y=lsi, color='red', linestyle='--', label=f'LSI ({lsi})')

plt.xlabel('Date')
plt.ylabel('Mesure (mm)')
plt.title('Mesures avec limites de specification')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('02_avec_limites.png', dpi=100, bbox_inches='tight')
plt.close()
print("Graphique sauvegarde : 02_avec_limites.png")

# =============================================================================
# PARTIE 3 : Histogramme de distribution
# =============================================================================

# TODO 3 : Creer un histogramme
# - plt.hist(data, bins=20, edgecolor='black')
# - plt.axvline(x, color, linestyle) : ligne verticale pour les limites

print("\n" + "="*50)
print("TODO 3 - Histogramme :")

plt.figure(figsize=(10, 5))
plt.hist(df['mesure'], bins=15, edgecolor='black', alpha=0.7, label='Distribution')

# Lignes verticales pour les limites
plt.axvline(x=nominal, color='green', linestyle='-', linewidth=2, label=f'Nominal')
plt.axvline(x=lss, color='red', linestyle='--', linewidth=2, label=f'LSS')
plt.axvline(x=lsi, color='red', linestyle='--', linewidth=2, label=f'LSI')

plt.xlabel('Mesure (mm)')
plt.ylabel('Frequence')
plt.title('Distribution des mesures')
plt.legend()
plt.savefig('03_histogramme.png', dpi=100, bbox_inches='tight')
plt.close()
print("Graphique sauvegarde : 03_histogramme.png")

# =============================================================================
# PARTIE 4 : Carte de controle (Control Chart)
# =============================================================================

# TODO 4 : Creer une carte de controle avec limites UCL/LCL
# Limites de controle (3 sigma) :
# - UCL = moyenne + 3*sigma
# - LCL = moyenne - 3*sigma
# Colorer les points hors limites en rouge

print("\n" + "="*50)
print("TODO 4 - Carte de controle :")
# Ton code ici

# =============================================================================
# PARTIE 5 : Graphiques multiples (subplots)
# =============================================================================

# TODO 5 : Creer une figure avec 2 graphiques cote a cote
# - fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
# - ax1.plot(), ax1.set_title(), etc.

print("\n" + "="*50)
print("TODO 5 - Subplots :")
# Ton code ici

print("\n" + "="*50)
print("EXERCICE TERMINE !")
print("="*50)
