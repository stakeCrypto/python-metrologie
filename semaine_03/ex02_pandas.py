"""
SEMAINE 3 - Exercice 2 : Introduction a Pandas
Objectif : Analyser des donnees de metrologie avec Pandas
"""

import pandas as pd
import numpy as np

# =============================================================================
# PREPARATION : Creer un fichier CSV de test
# =============================================================================

# Simuler des mesures de 3 machines sur 5 jours
np.random.seed(42)
data = {
    'date': ['2024-01-01']*10 + ['2024-01-02']*10 + ['2024-01-03']*10,
    'machine': ['M1', 'M1', 'M2', 'M2', 'M3', 'M3', 'M1', 'M2', 'M3', 'M1'] * 3,
    'mesure': np.round(np.random.normal(50.0, 0.02, 30), 4),
    'operateur': ['Alice', 'Bob'] * 15
}
df_test = pd.DataFrame(data)
df_test.to_csv('mesures_machines.csv', index=False)
print("Fichier 'mesures_machines.csv' cree avec 30 mesures.\n")

# =============================================================================
# PARTIE 1 : Lire un CSV avec Pandas
# =============================================================================

# TODO 1 : Lire le fichier CSV avec pd.read_csv()
df = pd.read_csv('mesures_machines.csv')

print("TODO 1 - Lecture CSV :")
print(df)
print(f"\nNombre de lignes : {len(df)}")

# =============================================================================
# PARTIE 2 : Explorer le DataFrame
# =============================================================================

# TODO 2 : Explorer le DataFrame
# - df.head() : premiers enregistrements
# - df.info() : types de colonnes
# - df.describe() : statistiques descriptives

print("\n" + "="*50)
print("TODO 2 - Exploration du DataFrame :")
print("\n--- head() : 5 premieres lignes ---")
print(df.head())

print("\n--- info() : structure du DataFrame ---")
print(df.info())

print("\n--- describe() : statistiques ---")
print(df.describe())

# =============================================================================
# PARTIE 3 : Selectionner des colonnes et lignes
# =============================================================================

# TODO 3 : Selections
# - df['mesure'] : selectionner une colonne (retourne une Series)
# - df[['date', 'mesure']] : selectionner plusieurs colonnes
# - df[df['machine'] == 'M1'] : filtrer les lignes

print("\n" + "="*50)
print("TODO 3 - Selections :")
print("\n--- Colonne 'mesure' (Series) ---")
print(df['mesure'].head())

print("\n--- Mesures de M1 uniquement ---")
df_m1 = df[df['machine'] == 'M1']
print(df_m1)
print(f"\nNombre de mesures M1 : {len(df_m1)}")

# =============================================================================
# PARTIE 4 : Statistiques par groupe (groupby)
# =============================================================================

# TODO 4 : Calculer les statistiques par machine
# - df.groupby('machine')['mesure'].mean() : moyenne par machine
# - df.groupby('machine')['mesure'].agg(['mean', 'std', 'min', 'max'])

print("\n" + "="*50)
print("TODO 4 - Statistiques par machine :")
stats_par_machine = df.groupby('machine')['mesure'].agg(['mean', 'std', 'min', 'max', 'count'])
print(stats_par_machine)

print("\n--- Quelle machine a le plus grand ecart-type ? ---")
pire_machine = stats_par_machine['std'].idxmax()
print(f"Machine avec plus de dispersion : {pire_machine}")

# =============================================================================
# PARTIE 5 : Ajouter des colonnes calculees
# =============================================================================

nominal = 50.0
tolerance = 0.05

# TODO 5 : Ajouter des colonnes
# - df['ecart'] = df['mesure'] - nominal
# - df['conforme'] = (df['mesure'] >= LSI) & (df['mesure'] <= LSS)

lsi = nominal - tolerance  # 49.95
lss = nominal + tolerance  # 50.05

df['ecart'] = df['mesure'] - nominal
df['conforme'] = (df['mesure'] >= lsi) & (df['mesure'] <= lss)

print("\n" + "="*50)
print("TODO 5 - Colonnes calculees :")
print(f"Limites : LSI={lsi}, LSS={lss}")
print(df[['machine', 'mesure', 'ecart', 'conforme']].head(10))

# =============================================================================
# PARTIE 6 : Taux de conformite par machine
# =============================================================================

# TODO 6 : Calculer le taux de conformite par machine
# - Grouper par machine
# - Calculer la moyenne de 'conforme' (True=1, False=0)
# - Multiplier par 100 pour avoir un pourcentage

print("\n" + "="*50)
print("TODO 6 - Taux de conformite par machine :")
taux_conf = df.groupby('machine')['conforme'].mean() * 100
print(taux_conf)

# Taux global
taux_global = df['conforme'].mean() * 100
print(f"\nTaux de conformite global : {taux_global:.1f}%")

# =============================================================================
# PARTIE 7 : Exporter les resultats
# =============================================================================

# TODO 7 : Exporter le DataFrame enrichi en CSV
df.to_csv('mesures_analysees.csv', index=False)

print("\n" + "="*50)
print("TODO 7 - Export CSV :")
print("Fichier 'mesures_analysees.csv' cree.")
print(f"Colonnes exportees : {list(df.columns)}")

print("\n" + "="*50)
print("EXERCICE TERMINE !")
print("="*50)
