"""
SEMAINE 4 - Exercice 3 : Generation de rapports automatises
Objectif : Creer des rapports de metrologie en differents formats
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# =============================================================================
# PREPARATION : Donnees de test
# =============================================================================

np.random.seed(42)

# Informations du rapport
info_rapport = {
    'titre': 'Rapport de Controle Qualite',
    'reference': 'RCQ-2024-001',
    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
    'operateur': 'Jean Dupont',
    'piece': 'Axe de transmission',
    'numero_lot': 'LOT-2024-0042'
}

# Specification
nominal = 50.0
tolerance = 0.05
lsi, lss = nominal - tolerance, nominal + tolerance

# Mesures
mesures = np.random.normal(50.0, 0.015, 20)
mesures = np.round(mesures, 4)

# Statistiques
stats = {
    'n': len(mesures),
    'moyenne': np.mean(mesures),
    'ecart_type': np.std(mesures, ddof=1),
    'min': np.min(mesures),
    'max': np.max(mesures)
}

# Cpk
sigma = stats['ecart_type']
cpu = (lss - stats['moyenne']) / (3 * sigma)
cpl = (stats['moyenne'] - lsi) / (3 * sigma)
cpk = min(cpu, cpl)

# Conformite
conformes = np.sum((mesures >= lsi) & (mesures <= lss))
taux_conformite = (conformes / len(mesures)) * 100

print("Donnees preparees pour la generation du rapport")
print(f"Piece : {info_rapport['piece']}")
print(f"Mesures : {stats['n']}, Cpk : {cpk:.2f}")

# =============================================================================
# TODO 1 : Generer un rapport TEXTE
# =============================================================================

print("\n" + "="*60)
print("TODO 1 - Rapport format TEXTE")
print("="*60)

# Creer un fichier .txt avec toutes les informations
rapport_txt = f"""
{'='*60}
{info_rapport['titre'].upper():^60}
{'='*60}

Reference : {info_rapport['reference']}
Date      : {info_rapport['date']}
Operateur : {info_rapport['operateur']}

{'-'*60}
IDENTIFICATION PIECE
{'-'*60}
Designation : {info_rapport['piece']}
Numero lot  : {info_rapport['numero_lot']}

{'-'*60}
SPECIFICATION
{'-'*60}
Nominal     : {nominal} mm
Tolerance   : +/- {tolerance} mm
Limites     : [{lsi}, {lss}] mm

{'-'*60}
RESULTATS DE MESURE
{'-'*60}
Nombre de mesures : {stats['n']}
Moyenne           : {stats['moyenne']:.4f} mm
Ecart-type        : {stats['ecart_type']:.4f} mm
Min               : {stats['min']:.4f} mm
Max               : {stats['max']:.4f} mm

{'-'*60}
CAPABILITE
{'-'*60}
Cpk : {cpk:.2f}
{'CAPABLE' if cpk >= 1.33 else 'ACCEPTABLE' if cpk >= 1.0 else 'NON CAPABLE'}

{'-'*60}
CONFORMITE
{'-'*60}
Pieces conformes : {conformes}/{stats['n']}
Taux             : {taux_conformite:.1f}%

{'='*60}
VERDICT : {'CONFORME' if taux_conformite == 100 and cpk >= 1.0 else 'NON CONFORME'}
{'='*60}
"""

# Sauvegarder le fichier
with open('rapport_qualite.txt', 'w') as f:
    f.write(rapport_txt)

print("Rapport TXT genere : rapport_qualite.txt")
print(rapport_txt)

# =============================================================================
# TODO 2 : Generer le graphique pour le rapport
# =============================================================================

print("\n" + "="*60)
print("TODO 2 - Graphique pour le rapport")
print("="*60)

# Creer un graphique combiné (evolution + histogramme)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Graphique 1 : Evolution des mesures
ax1.plot(range(1, len(mesures)+1), mesures, 'bo-', markersize=6)
ax1.axhline(y=nominal, color='green', linestyle='-', label=f'Nominal ({nominal})')
ax1.axhline(y=lss, color='red', linestyle='--', label=f'LSS ({lss})')
ax1.axhline(y=lsi, color='red', linestyle='--', label=f'LSI ({lsi})')
ax1.fill_between(range(0, len(mesures)+2), lsi, lss, alpha=0.1, color='green')
ax1.set_xlabel('Numero de mesure')
ax1.set_ylabel('Valeur (mm)')
ax1.set_title('Evolution des mesures')
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, len(mesures)+1)

# Graphique 2 : Histogramme
ax2.hist(mesures, bins=10, edgecolor='black', alpha=0.7, orientation='horizontal')
ax2.axhline(y=nominal, color='green', linestyle='-', linewidth=2)
ax2.axhline(y=lss, color='red', linestyle='--', linewidth=2)
ax2.axhline(y=lsi, color='red', linestyle='--', linewidth=2)
ax2.set_xlabel('Frequence')
ax2.set_ylabel('Valeur (mm)')
ax2.set_title('Distribution')

# Titre global
fig.suptitle(f"{info_rapport['piece']} - {info_rapport['numero_lot']}", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('rapport_graphique.png', dpi=150, bbox_inches='tight')
plt.close()

print("Graphique genere : rapport_graphique.png")

# =============================================================================
# TODO 3 : Generer un rapport HTML
# =============================================================================

print("\n" + "="*60)
print("TODO 3 - Rapport format HTML")
print("="*60)

# Creer un fichier HTML avec style CSS integre
verdict = 'CONFORME' if taux_conformite == 100 and cpk >= 1.0 else 'NON CONFORME'
verdict_color = '#28a745' if verdict == 'CONFORME' else '#dc3545'
cpk_status = 'CAPABLE' if cpk >= 1.33 else 'ACCEPTABLE' if cpk >= 1.0 else 'NON CAPABLE'

rapport_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{info_rapport['titre']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .info {{ background: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #007bff; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .verdict {{ font-size: 24px; font-weight: bold; color: {verdict_color};
                   text-align: center; padding: 20px; border: 3px solid {verdict_color};
                   border-radius: 10px; margin: 20px 0; }}
        .graphique {{ text-align: center; margin: 30px 0; }}
        .graphique img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 5px; }}
        .footer {{ text-align: center; color: #888; margin-top: 30px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{info_rapport['titre']}</h1>

        <div class="info">
            <strong>Reference:</strong> {info_rapport['reference']} |
            <strong>Date:</strong> {info_rapport['date']} |
            <strong>Operateur:</strong> {info_rapport['operateur']}
        </div>

        <h2>Identification</h2>
        <table>
            <tr><th>Designation</th><td>{info_rapport['piece']}</td></tr>
            <tr><th>Numero de lot</th><td>{info_rapport['numero_lot']}</td></tr>
        </table>

        <h2>Specification</h2>
        <table>
            <tr><th>Nominal</th><td>{nominal} mm</td></tr>
            <tr><th>Tolerance</th><td>+/- {tolerance} mm</td></tr>
            <tr><th>Limites</th><td>[{lsi}, {lss}] mm</td></tr>
        </table>

        <h2>Resultats</h2>
        <table>
            <tr><th>Parametre</th><th>Valeur</th></tr>
            <tr><td>Nombre de mesures</td><td>{stats['n']}</td></tr>
            <tr><td>Moyenne</td><td>{stats['moyenne']:.4f} mm</td></tr>
            <tr><td>Ecart-type</td><td>{stats['ecart_type']:.4f} mm</td></tr>
            <tr><td>Min</td><td>{stats['min']:.4f} mm</td></tr>
            <tr><td>Max</td><td>{stats['max']:.4f} mm</td></tr>
            <tr><td><strong>Cpk</strong></td><td><strong>{cpk:.2f}</strong> ({cpk_status})</td></tr>
            <tr><td><strong>Taux de conformite</strong></td><td><strong>{taux_conformite:.1f}%</strong></td></tr>
        </table>

        <div class="graphique">
            <h2>Graphiques</h2>
            <img src="rapport_graphique.png" alt="Graphique de mesures">
        </div>

        <div class="verdict">
            VERDICT : {verdict}
        </div>

        <div class="footer">
            Rapport genere automatiquement - {info_rapport['date']}
        </div>
    </div>
</body>
</html>
"""

with open('rapport_qualite.html', 'w') as f:
    f.write(rapport_html)

print("Rapport HTML genere : rapport_qualite.html")

# =============================================================================
# TODO 4 : Fonction de generation de rapport reutilisable
# =============================================================================

print("\n" + "="*60)
print("TODO 4 - Fonction reutilisable")
print("="*60)

# Fonction complete de generation de rapport
def generer_rapport(mesures, info, nominal, tolerance, dossier='rapports'):
    """
    Genere un rapport complet (TXT + PNG + HTML) pour un lot de mesures.

    Args:
        mesures: array de mesures
        info: dict avec titre, reference, date, operateur, piece, numero_lot
        nominal: valeur nominale
        tolerance: tolerance (+/-)
        dossier: dossier de sortie
    """
    import os

    # Creer le dossier si necessaire
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    # Calculs
    lsi, lss = nominal - tolerance, nominal + tolerance
    stats = {
        'n': len(mesures),
        'moyenne': np.mean(mesures),
        'ecart_type': np.std(mesures, ddof=1),
        'min': np.min(mesures),
        'max': np.max(mesures)
    }

    sigma = stats['ecart_type']
    cpu = (lss - stats['moyenne']) / (3 * sigma) if sigma > 0 else 0
    cpl = (stats['moyenne'] - lsi) / (3 * sigma) if sigma > 0 else 0
    cpk = min(cpu, cpl)

    conformes = np.sum((mesures >= lsi) & (mesures <= lss))
    taux_conformite = (conformes / len(mesures)) * 100

    verdict = 'CONFORME' if taux_conformite == 100 and cpk >= 1.0 else 'NON CONFORME'

    # Prefixe pour les fichiers
    prefixe = f"{dossier}/{info['numero_lot']}"

    # 1. Generer le graphique
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(range(1, len(mesures)+1), mesures, 'bo-', markersize=6)
    ax1.axhline(y=nominal, color='green', linestyle='-', label=f'Nominal')
    ax1.axhline(y=lss, color='red', linestyle='--', label=f'LSS/LSI')
    ax1.axhline(y=lsi, color='red', linestyle='--')
    ax1.fill_between(range(0, len(mesures)+2), lsi, lss, alpha=0.1, color='green')
    ax1.set_xlabel('Mesure')
    ax1.set_ylabel('Valeur (mm)')
    ax1.set_title('Evolution')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    ax2.hist(mesures, bins=10, edgecolor='black', alpha=0.7, orientation='horizontal')
    ax2.axhline(y=nominal, color='green', linestyle='-')
    ax2.axhline(y=lss, color='red', linestyle='--')
    ax2.axhline(y=lsi, color='red', linestyle='--')
    ax2.set_xlabel('Frequence')
    ax2.set_title('Distribution')

    fig.suptitle(f"{info['piece']} - {info['numero_lot']}", fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{prefixe}_graphique.png", dpi=150, bbox_inches='tight')
    plt.close()

    # 2. Generer le TXT
    rapport_txt = f"""{'='*50}
{info['titre'].upper():^50}
{'='*50}
Reference : {info['reference']}
Date      : {info['date']}
Piece     : {info['piece']}
Lot       : {info['numero_lot']}
{'-'*50}
RESULTATS
  Moyenne  : {stats['moyenne']:.4f} mm
  Ecart-type: {stats['ecart_type']:.4f} mm
  Cpk      : {cpk:.2f}
  Conformite: {taux_conformite:.1f}%
{'-'*50}
VERDICT : {verdict}
{'='*50}
"""
    with open(f"{prefixe}_rapport.txt", 'w') as f:
        f.write(rapport_txt)

    # 3. Generer le HTML (simplifie)
    verdict_color = '#28a745' if verdict == 'CONFORME' else '#dc3545'
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{info['titre']}</title>
<style>body{{font-family:Arial;margin:40px}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #ddd;padding:8px}}th{{background:#007bff;color:white}}
.verdict{{font-size:20px;font-weight:bold;color:{verdict_color};text-align:center;padding:15px;border:2px solid {verdict_color}}}</style>
</head><body>
<h1>{info['titre']}</h1>
<p><b>Reference:</b> {info['reference']} | <b>Date:</b> {info['date']} | <b>Lot:</b> {info['numero_lot']}</p>
<h2>Resultats</h2>
<table><tr><th>Parametre</th><th>Valeur</th></tr>
<tr><td>Moyenne</td><td>{stats['moyenne']:.4f} mm</td></tr>
<tr><td>Ecart-type</td><td>{stats['ecart_type']:.4f} mm</td></tr>
<tr><td>Cpk</td><td>{cpk:.2f}</td></tr>
<tr><td>Conformite</td><td>{taux_conformite:.1f}%</td></tr></table>
<img src="{info['numero_lot']}_graphique.png" style="max-width:100%">
<div class="verdict">VERDICT : {verdict}</div>
</body></html>"""

    with open(f"{prefixe}_rapport.html", 'w') as f:
        f.write(html)

    print(f"Rapport genere pour {info['numero_lot']} dans '{dossier}/'")
    print(f"  - {info['numero_lot']}_rapport.txt")
    print(f"  - {info['numero_lot']}_graphique.png")
    print(f"  - {info['numero_lot']}_rapport.html")

    return {'cpk': cpk, 'conformite': taux_conformite, 'verdict': verdict}

print("Fonction generer_rapport() creee.")

# =============================================================================
# TODO 5 : Generer un rapport pour un nouveau lot
# =============================================================================

print("\n" + "="*60)
print("TODO 5 - Test avec nouveau lot")
print("="*60)

# Generer des rapports pour plusieurs lots

# Lot 1 : Bon (conforme)
info_lot1 = {
    'titre': 'Rapport de Controle Qualite',
    'reference': 'RCQ-2024-002',
    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
    'operateur': 'Marie Martin',
    'piece': 'Roulement a billes',
    'numero_lot': 'LOT-2024-0101'
}
mesures_lot1 = np.random.normal(25.0, 0.008, 15)  # Bon centrage, faible dispersion
result1 = generer_rapport(mesures_lot1, info_lot1, nominal=25.0, tolerance=0.03)

# Lot 2 : Mauvais (non conforme)
info_lot2 = {
    'titre': 'Rapport de Controle Qualite',
    'reference': 'RCQ-2024-003',
    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
    'operateur': 'Pierre Durand',
    'piece': 'Roulement a billes',
    'numero_lot': 'LOT-2024-0102'
}
mesures_lot2 = np.random.normal(25.02, 0.025, 15)  # Decentre, grande dispersion
result2 = generer_rapport(mesures_lot2, info_lot2, nominal=25.0, tolerance=0.03)

# Resume
print("\n" + "-"*50)
print("RESUME DES LOTS")
print("-"*50)
print(f"LOT-2024-0101 : Cpk={result1['cpk']:.2f}, {result1['verdict']}")
print(f"LOT-2024-0102 : Cpk={result2['cpk']:.2f}, {result2['verdict']}")

print("\n" + "="*60)
print("EXERCICE TERMINE !")
print("="*60)
