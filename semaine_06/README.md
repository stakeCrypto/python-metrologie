# Semaine 6 : SPC Avance et Serveur MCP

## Objectifs
- Maitriser les cartes de controle X-barre/R pour echantillons groupes
- Comprendre le Model Context Protocol (MCP)
- Creer un serveur MCP pour exposer des outils de metrologie

## Theorie : Cartes X-barre/R

### Difference avec la carte X individuel (Semaine 3)
- **Carte X individuel** : 1 mesure par point (UCL/LCL a 3 sigma)
- **Carte X-barre/R** : Echantillons de n pieces, analyse moyenne + etendue

### Pourquoi X-barre/R ?
En production, on preleve souvent des echantillons de n pieces (ex: 5 pieces toutes les heures).
La carte X-barre surveille la **moyenne** de chaque echantillon.
La carte R surveille l'**etendue** (variabilite intra-echantillon).

### Formules SPC
```
X-barre (moyenne) = somme(xi) / n
R (etendue) = max(echantillon) - min(echantillon)

Limites X-barre:
  UCL_X = X-barre-barre + A2 * R-barre
  LCL_X = X-barre-barre - A2 * R-barre

Limites R:
  UCL_R = D4 * R-barre
  LCL_R = D3 * R-barre
```

### Constantes SPC (selon taille echantillon n)
| n | A2    | D3   | D4    |
|---|-------|------|-------|
| 2 | 1.880 | 0    | 3.267 |
| 3 | 1.023 | 0    | 2.574 |
| 4 | 0.729 | 0    | 2.282 |
| 5 | 0.577 | 0    | 2.114 |
| 6 | 0.483 | 0    | 2.004 |

## Exercices
1. `ex01_carte_xbar_r.py` - Carte de controle X-barre/R complete
2. `ex02_serveur_mcp.py` - Premier serveur MCP pour metrologie

## Ressources
- [NIST/SEMATECH Handbook - Control Charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc3.htm)
- [MCP Documentation](https://modelcontextprotocol.io)
