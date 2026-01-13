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

# Calculer les limites de controle (3 sigma)
moyenne = df['mesure'].mean()
sigma = df['mesure'].std()
ucl = moyenne + 3 * sigma
lcl = moyenne - 3 * sigma

plt.figure(figsize=(10, 5))

# Identifier les points hors controle
hors_controle = (df['mesure'] > ucl) | (df['mesure'] < lcl)
dans_controle = ~hors_controle

# Tracer les points (vert = OK, rouge = hors controle)
plt.plot(df.loc[dans_controle, 'date'], df.loc[dans_controle, 'mesure'],
         'go', markersize=5, label='Sous controle')
plt.plot(df.loc[hors_controle, 'date'], df.loc[hors_controle, 'mesure'],
         'ro', markersize=8, label='Hors controle')
plt.plot(df['date'], df['mesure'], 'b-', alpha=0.3)  # Ligne de connexion

# Limites de controle
plt.axhline(y=moyenne, color='green', linestyle='-', label=f'Moyenne ({moyenne:.4f})')
plt.axhline(y=ucl, color='orange', linestyle='--', label=f'UCL ({ucl:.4f})')
plt.axhline(y=lcl, color='orange', linestyle='--', label=f'LCL ({lcl:.4f})')

plt.xlabel('Date')
plt.ylabel('Mesure (mm)')
plt.title('Carte de controle (Control Chart)')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.savefig('04_carte_controle.png', dpi=100, bbox_inches='tight')
plt.close()

print(f"Moyenne : {moyenne:.4f}, Sigma : {sigma:.4f}")
print(f"UCL : {ucl:.4f}, LCL : {lcl:.4f}")
print(f"Points hors controle : {hors_controle.sum()}")
print("Graphique sauvegarde : 04_carte_controle.png")

# =============================================================================
# PARTIE 5 : Graphiques multiples (subplots)
# =============================================================================

# TODO 5 : Creer une figure avec 2 graphiques cote a cote
# - fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
# - ax1.plot(), ax1.set_title(), etc.

print("\n" + "="*50)
print("TODO 5 - Subplots :")

# Creer une figure avec 2 graphiques cote a cote
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Graphique 1 : Evolution temporelle avec limites
ax1.plot(df['date'], df['mesure'], 'b-o', markersize=3)
ax1.axhline(y=nominal, color='green', linestyle='-', label='Nominal')
ax1.axhline(y=lss, color='red', linestyle='--', label='LSS/LSI')
ax1.axhline(y=lsi, color='red', linestyle='--')
ax1.set_xlabel('Date')
ax1.set_ylabel('Mesure (mm)')
ax1.set_title('Evolution temporelle')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Graphique 2 : Histogramme
ax2.hist(df['mesure'], bins=15, edgecolor='black', alpha=0.7, orientation='horizontal')
ax2.axhline(y=nominal, color='green', linestyle='-', linewidth=2)
ax2.axhline(y=lss, color='red', linestyle='--', linewidth=2)
ax2.axhline(y=lsi, color='red', linestyle='--', linewidth=2)
ax2.set_xlabel('Frequence')
ax2.set_ylabel('Mesure (mm)')
ax2.set_title('Distribution')

# Titre global
fig.suptitle('Rapport de metrologie - Vue combinee', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('05_rapport_combine.png', dpi=100, bbox_inches='tight')
plt.close()
print("Graphique sauvegarde : 05_rapport_combine.png")

print("\n" + "="*50)
print("EXERCICE TERMINE !")
print("="*50)
