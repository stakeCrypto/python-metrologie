"""
SEMAINE 4 - Exercice 1 : Analyse complete de mesures
Objectif : Combiner NumPy, Pandas, Matplotlib pour une analyse reelle
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# PREPARATION : Generer un jeu de donnees realiste
# =============================================================================

np.random.seed(123)

# Simuler 3 lots de production avec caracteristiques differentes
lot1 = np.random.normal(50.00, 0.015, 30)  # Lot stable
lot2 = np.random.normal(50.02, 0.025, 30)  # Lot decentre avec plus de dispersion
lot3 = np.random.normal(49.98, 0.018, 30)  # Lot legerement sous nominal

# Ajouter quelques valeurs aberrantes
lot2[5] = 50.12   # Valeur aberrante haute
lot3[20] = 49.85  # Valeur aberrante basse

# Creer le DataFrame
dates = pd.date_range('2024-01-01', periods=90, freq='D')
df = pd.DataFrame({
    'date': dates,
    'lot': ['LOT_A']*30 + ['LOT_B']*30 + ['LOT_C']*30,
    'mesure': np.concatenate([lot1, lot2, lot3]),
    'operateur': np.tile(['Alice', 'Bob', 'Charlie'], 30)
})

# Sauvegarder en CSV
df.to_csv('donnees_production.csv', index=False)
print("Fichier 'donnees_production.csv' cree avec 90 mesures (3 lots)")

# Specifications
nominal = 50.00
tolerance = 0.05
lsi, lss = nominal - tolerance, nominal + tolerance

print(f"Specification : {nominal} +/- {tolerance} mm")
print(f"Limites : LSI={lsi}, LSS={lss}")

# =============================================================================
# TODO 1 : Charger et explorer les donnees
# =============================================================================

print("\n" + "="*60)
print("TODO 1 - Exploration des donnees")
print("="*60)

# Charger le CSV
df = pd.read_csv('donnees_production.csv')
df['date'] = pd.to_datetime(df['date'])  # Convertir en datetime

print(f"Shape : {df.shape}")
print(f"\nApercu :")
print(df.head())

# Statistiques par lot
print(f"\nStatistiques par lot :")
stats_lot = df.groupby('lot')['mesure'].agg(['count', 'mean', 'std', 'min', 'max'])
print(stats_lot)

# =============================================================================
# TODO 2 : Detecter les valeurs aberrantes (methode IQR)
# =============================================================================

print("\n" + "="*60)
print("TODO 2 - Detection des valeurs aberrantes")
print("="*60)

# Methode IQR (Interquartile Range) :
# Q1 = 25e percentile, Q3 = 75e percentile
# IQR = Q3 - Q1
# Aberrant si : valeur < Q1 - 1.5*IQR  ou  valeur > Q3 + 1.5*IQR

Q1 = df['mesure'].quantile(0.25)
Q3 = df['mesure'].quantile(0.75)
IQR = Q3 - Q1

borne_basse = Q1 - 1.5 * IQR
borne_haute = Q3 + 1.5 * IQR

# Masque pour les valeurs aberrantes
aberrantes = (df['mesure'] < borne_basse) | (df['mesure'] > borne_haute)

print(f"Q1 = {Q1:.4f}, Q3 = {Q3:.4f}, IQR = {IQR:.4f}")
print(f"Bornes : [{borne_basse:.4f}, {borne_haute:.4f}]")
print(f"\nValeurs aberrantes detectees : {aberrantes.sum()}")

if aberrantes.sum() > 0:
    print(df[aberrantes][['date', 'lot', 'mesure']])

# =============================================================================
# TODO 3 : Calculer le Cpk par lot
# =============================================================================

print("\n" + "="*60)
print("TODO 3 - Calcul du Cpk par lot")
print("="*60)

# Fonction pour calculer le Cpk
def calculer_cpk(mesures):
    moyenne = mesures.mean()
    sigma = mesures.std()

    if sigma == 0:
        return np.nan

    cpu = (lss - moyenne) / (3 * sigma)
    cpl = (moyenne - lsi) / (3 * sigma)
    return min(cpu, cpl)

# Appliquer a chaque lot
cpk_par_lot = df.groupby('lot')['mesure'].apply(calculer_cpk)

print("Cpk par lot :")
for lot, cpk in cpk_par_lot.items():
    if cpk >= 1.33:
        status = "Excellent"
    elif cpk >= 1.0:
        status = "Acceptable"
    else:
        status = "Non capable"
    print(f"  {lot} : Cpk = {cpk:.2f} ({status})")

# =============================================================================
# TODO 4 : Creer une visualisation complete
# =============================================================================

print("\n" + "="*60)
print("TODO 4 - Visualisation")
print("="*60)

# Creer une figure avec 4 subplots (2x2)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
ax1, ax2, ax3, ax4 = axes.flatten()

colors = {'LOT_A': 'blue', 'LOT_B': 'orange', 'LOT_C': 'green'}

# 1. Evolution temporelle par lot
for lot in df['lot'].unique():
    data_lot = df[df['lot'] == lot]
    ax1.plot(data_lot['date'], data_lot['mesure'], 'o-', label=lot, color=colors[lot], markersize=4)
ax1.axhline(y=lss, color='red', linestyle='--', label='LSS/LSI')
ax1.axhline(y=lsi, color='red', linestyle='--')
ax1.axhline(y=nominal, color='green', linestyle='-', alpha=0.5)
ax1.set_xlabel('Date')
ax1.set_ylabel('Mesure (mm)')
ax1.set_title('Evolution temporelle par lot')
ax1.legend()
ax1.tick_params(axis='x', rotation=45)

# 2. Boxplot par lot
df.boxplot(column='mesure', by='lot', ax=ax2)
ax2.axhline(y=lss, color='red', linestyle='--')
ax2.axhline(y=lsi, color='red', linestyle='--')
ax2.set_xlabel('Lot')
ax2.set_ylabel('Mesure (mm)')
ax2.set_title('Distribution par lot (Boxplot)')
plt.suptitle('')  # Supprimer le titre auto du boxplot

# 3. Histogramme global
ax3.hist(df['mesure'], bins=20, edgecolor='black', alpha=0.7)
ax3.axvline(x=lss, color='red', linestyle='--', linewidth=2, label='LSS/LSI')
ax3.axvline(x=lsi, color='red', linestyle='--', linewidth=2)
ax3.axvline(x=nominal, color='green', linestyle='-', linewidth=2, label='Nominal')
ax3.set_xlabel('Mesure (mm)')
ax3.set_ylabel('Frequence')
ax3.set_title('Distribution globale')
ax3.legend()

# 4. Cpk par lot (bar chart)
cpk_values = cpk_par_lot.values
lot_names = cpk_par_lot.index
bar_colors = ['green' if c >= 1.33 else 'orange' if c >= 1.0 else 'red' for c in cpk_values]
ax4.bar(lot_names, cpk_values, color=bar_colors, edgecolor='black')
ax4.axhline(y=1.33, color='green', linestyle='--', label='Excellent (1.33)')
ax4.axhline(y=1.0, color='orange', linestyle='--', label='Acceptable (1.0)')
ax4.set_xlabel('Lot')
ax4.set_ylabel('Cpk')
ax4.set_title('Cpk par lot')
ax4.legend()

plt.tight_layout()
plt.savefig('analyse_complete.png', dpi=100, bbox_inches='tight')
plt.close()
print("Graphique sauvegarde : analyse_complete.png")

# =============================================================================
# TODO 5 : Generer un rapport de synthese
# =============================================================================

print("\n" + "="*60)
print("TODO 5 - Rapport de synthese")
print("="*60)

# Calculer la conformite (dans les limites LSI/LSS)
df['conforme'] = (df['mesure'] >= lsi) & (df['mesure'] <= lss)
taux_conf = df.groupby('lot')['conforme'].mean() * 100

# Rapport complet
print("=" * 60)
print("           RAPPORT D'ANALYSE DE PRODUCTION")
print("=" * 60)
print(f"\nSpecification : {nominal} +/- {tolerance} mm")
print(f"Limites : LSI = {lsi}, LSS = {lss}")
print(f"Total mesures : {len(df)}")

print("\n" + "-" * 60)
print("ANALYSE PAR LOT")
print("-" * 60)

for lot in df['lot'].unique():
    data_lot = df[df['lot'] == lot]
    cpk = cpk_par_lot[lot]
    taux = taux_conf[lot]
    nb_aberr = aberrantes[df['lot'] == lot].sum()

    print(f"\n{lot}:")
    print(f"  Mesures     : {len(data_lot)}")
    print(f"  Moyenne     : {data_lot['mesure'].mean():.4f}")
    print(f"  Ecart-type  : {data_lot['mesure'].std():.4f}")
    print(f"  Conformite  : {taux:.1f}%")
    print(f"  Cpk         : {cpk:.2f}", end="")
    if cpk >= 1.33:
        print(" (Excellent)")
    elif cpk >= 1.0:
        print(" (Acceptable)")
    else:
        print(" (Non capable - ACTION REQUISE)")
    print(f"  Aberrantes  : {nb_aberr}")

print("\n" + "-" * 60)
print("CONCLUSION")
print("-" * 60)
lots_non_capables = [lot for lot, cpk in cpk_par_lot.items() if cpk < 1.0]
if lots_non_capables:
    print(f"ATTENTION : {len(lots_non_capables)} lot(s) non capable(s) : {', '.join(lots_non_capables)}")
    print("Actions recommandees :")
    print("  - Investiguer les causes des valeurs aberrantes")
    print("  - Verifier les reglages machines")
    print("  - Reduire la variabilite du processus")
else:
    print("Tous les lots sont capables. Production conforme.")

print("\n" + "="*60)
print("EXERCICE TERMINE !")
print("="*60)
