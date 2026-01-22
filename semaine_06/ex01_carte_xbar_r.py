"""
SEMAINE 6 - Exercice 1 : Carte de controle X-barre/R
Objectif : Implementer une carte SPC complete pour echantillons groupes
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# CONSTANTES SPC (tables statistiques)
# =============================================================================

# Constantes pour cartes X-barre et R selon taille echantillon n
SPC_CONSTANTS = {
    2: {'A2': 1.880, 'D3': 0, 'D4': 3.267},
    3: {'A2': 1.023, 'D3': 0, 'D4': 2.574},
    4: {'A2': 0.729, 'D3': 0, 'D4': 2.282},
    5: {'A2': 0.577, 'D3': 0, 'D4': 2.114},
    6: {'A2': 0.483, 'D3': 0, 'D4': 2.004},
    7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924},
    8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864},
    9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816},
    10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777},
}

# =============================================================================
# PARTIE 1 : Generer des donnees de production simulees
# =============================================================================

def generer_donnees_production(n_echantillons=25, taille_echantillon=5,
                                nominal=50.0, sigma_procede=0.02):
    """
    Simule des donnees de production avec echantillons groupes.

    Parametres:
    - n_echantillons : nombre de prelevements (ex: 25 heures)
    - taille_echantillon : pieces par prelevement (ex: 5 pieces)
    - nominal : valeur cible
    - sigma_procede : ecart-type du procede

    Retourne : DataFrame avec colonnes [echantillon, piece_1, piece_2, ...]
    """
    np.random.seed(42)  # Reproductibilite

    # Simuler une legere derive (realiste en production)
    derive = np.linspace(0, 0.01, n_echantillons)

    # TODO 1 : Completer la generation des donnees
    # Generer n_echantillons lignes, chacune avec taille_echantillon mesures
    # Ajouter la derive progressive pour simuler l'usure outil

    data = []
    for i in range(n_echantillons):
        # Chaque echantillon : nominal + derive + bruit aleatoire
        echantillon = nominal + derive[i] + np.random.normal(0, sigma_procede, taille_echantillon)
        data.append(echantillon)

    # Creer le DataFrame
    colonnes = [f'piece_{j+1}' for j in range(taille_echantillon)]
    df = pd.DataFrame(data, columns=colonnes)
    df.insert(0, 'echantillon', range(1, n_echantillons + 1))

    return df


# =============================================================================
# PARTIE 2 : Calculer X-barre et R pour chaque echantillon
# =============================================================================

def calculer_xbar_r(df):
    """
    Calcule la moyenne (X-barre) et l'etendue (R) de chaque echantillon.

    Retourne : DataFrame avec colonnes [echantillon, xbar, R]
    """
    # TODO 2 : Calculer X-barre (moyenne) et R (max - min) pour chaque ligne
    # Exclure la colonne 'echantillon' du calcul

    colonnes_mesures = [col for col in df.columns if col.startswith('piece_')]

    resultats = pd.DataFrame()
    resultats['echantillon'] = df['echantillon']
    resultats['xbar'] = df[colonnes_mesures].mean(axis=1)
    resultats['R'] = df[colonnes_mesures].max(axis=1) - df[colonnes_mesures].min(axis=1)

    return resultats


# =============================================================================
# PARTIE 3 : Calculer les limites de controle
# =============================================================================

def calculer_limites(df_xbar_r, taille_echantillon):
    """
    Calcule les limites de controle UCL/LCL pour X-barre et R.

    Formules:
    - X-barre-barre = moyenne des X-barre
    - R-barre = moyenne des R
    - UCL_X = X-barre-barre + A2 * R-barre
    - LCL_X = X-barre-barre - A2 * R-barre
    - UCL_R = D4 * R-barre
    - LCL_R = D3 * R-barre
    """
    # TODO 3 : Recuperer les constantes SPC et calculer les limites

    constants = SPC_CONSTANTS[taille_echantillon]
    A2, D3, D4 = constants['A2'], constants['D3'], constants['D4']

    xbar_bar = df_xbar_r['xbar'].mean()
    r_bar = df_xbar_r['R'].mean()

    limites = {
        'xbar_bar': xbar_bar,
        'r_bar': r_bar,
        'UCL_X': xbar_bar + A2 * r_bar,
        'LCL_X': xbar_bar - A2 * r_bar,
        'UCL_R': D4 * r_bar,
        'LCL_R': D3 * r_bar,
    }

    return limites


# =============================================================================
# PARTIE 4 : Tracer les cartes X-barre et R
# =============================================================================

def tracer_cartes_xbar_r(df_xbar_r, limites, titre="Cartes X-barre / R"):
    """
    Trace les deux cartes de controle sur une figure.
    """
    # TODO 4 : Creer une figure avec 2 subplots (X-barre en haut, R en bas)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # --- Carte X-barre ---
    ax1.plot(df_xbar_r['echantillon'], df_xbar_r['xbar'], 'bo-', markersize=6)
    ax1.axhline(y=limites['xbar_bar'], color='green', linestyle='-',
                label=f"X-barre-barre = {limites['xbar_bar']:.4f}")
    ax1.axhline(y=limites['UCL_X'], color='red', linestyle='--',
                label=f"UCL = {limites['UCL_X']:.4f}")
    ax1.axhline(y=limites['LCL_X'], color='red', linestyle='--',
                label=f"LCL = {limites['LCL_X']:.4f}")

    # Identifier points hors controle
    hors_controle_x = (df_xbar_r['xbar'] > limites['UCL_X']) | (df_xbar_r['xbar'] < limites['LCL_X'])
    if hors_controle_x.any():
        ax1.plot(df_xbar_r.loc[hors_controle_x, 'echantillon'],
                 df_xbar_r.loc[hors_controle_x, 'xbar'],
                 'ro', markersize=10, label='Hors controle')

    ax1.set_ylabel('X-barre (moyenne)')
    ax1.set_title('Carte X-barre')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # --- Carte R ---
    ax2.plot(df_xbar_r['echantillon'], df_xbar_r['R'], 'go-', markersize=6)
    ax2.axhline(y=limites['r_bar'], color='green', linestyle='-',
                label=f"R-barre = {limites['r_bar']:.4f}")
    ax2.axhline(y=limites['UCL_R'], color='red', linestyle='--',
                label=f"UCL = {limites['UCL_R']:.4f}")
    ax2.axhline(y=limites['LCL_R'], color='red', linestyle='--',
                label=f"LCL = {limites['LCL_R']:.4f}")

    # Identifier points hors controle
    hors_controle_r = (df_xbar_r['R'] > limites['UCL_R']) | (df_xbar_r['R'] < limites['LCL_R'])
    if hors_controle_r.any():
        ax2.plot(df_xbar_r.loc[hors_controle_r, 'echantillon'],
                 df_xbar_r.loc[hors_controle_r, 'R'],
                 'ro', markersize=10, label='Hors controle')

    ax2.set_xlabel('Echantillon')
    ax2.set_ylabel('R (etendue)')
    ax2.set_title('Carte R')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    fig.suptitle(titre, fontsize=14, fontweight='bold')
    plt.tight_layout()

    return fig, hors_controle_x.sum(), hors_controle_r.sum()


# =============================================================================
# PROGRAMME PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print("CARTE DE CONTROLE X-BARRE / R")
    print("="*60)

    # Configuration
    TAILLE_ECHANTILLON = 5  # pieces par prelevement
    N_ECHANTILLONS = 25     # nombre de prelevements
    NOMINAL = 50.0          # valeur cible (mm)

    # 1. Generer les donnees
    print("\n1. Generation des donnees de production...")
    df_production = generer_donnees_production(
        n_echantillons=N_ECHANTILLONS,
        taille_echantillon=TAILLE_ECHANTILLON,
        nominal=NOMINAL
    )
    print(f"   {N_ECHANTILLONS} echantillons de {TAILLE_ECHANTILLON} pieces")
    print(df_production.head())

    # 2. Calculer X-barre et R
    print("\n2. Calcul de X-barre et R...")
    df_xbar_r = calculer_xbar_r(df_production)
    print(df_xbar_r.head())

    # 3. Calculer les limites de controle
    print("\n3. Calcul des limites de controle...")
    limites = calculer_limites(df_xbar_r, TAILLE_ECHANTILLON)
    print(f"   X-barre-barre : {limites['xbar_bar']:.4f}")
    print(f"   R-barre       : {limites['r_bar']:.4f}")
    print(f"   UCL_X / LCL_X : {limites['UCL_X']:.4f} / {limites['LCL_X']:.4f}")
    print(f"   UCL_R / LCL_R : {limites['UCL_R']:.4f} / {limites['LCL_R']:.4f}")

    # 4. Tracer les cartes
    print("\n4. Tracage des cartes de controle...")
    fig, hors_x, hors_r = tracer_cartes_xbar_r(df_xbar_r, limites)

    # Sauvegarder
    fig.savefig('carte_xbar_r.png', dpi=150, bbox_inches='tight')
    print(f"   Graphique sauvegarde : carte_xbar_r.png")
    print(f"   Points hors controle X-barre : {hors_x}")
    print(f"   Points hors controle R       : {hors_r}")

    plt.close()

    # 5. Exporter les donnees
    df_production.to_csv('donnees_echantillons.csv', index=False)
    df_xbar_r.to_csv('xbar_r_resultats.csv', index=False)
    print("\n5. Donnees exportees : donnees_echantillons.csv, xbar_r_resultats.csv")

    print("\n" + "="*60)
    print("EXERCICE TERMINE !")
    print("="*60)
