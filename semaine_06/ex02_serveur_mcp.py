"""
SEMAINE 6 - Exercice 2 : Premier serveur MCP pour metrologie
Objectif : Creer un serveur MCP qui expose des outils de calcul metrologique

Ce serveur expose 3 outils :
1. calculer_statistiques - Calcule moyenne, sigma, min, max
2. calculer_cpk - Calcule le Cpk d'un procede
3. analyser_echantillon - Analyse complete d'un echantillon

Installation requise :
    pip install mcp

Lancement :
    python ex02_serveur_mcp.py

Configuration Claude Code (claude_desktop_config.json) :
    {
      "mcpServers": {
        "metrologie": {
          "command": "python",
          "args": ["/chemin/vers/ex02_serveur_mcp.py"]
        }
      }
    }
"""

import asyncio
import json
import statistics
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# =============================================================================
# CONFIGURATION DU SERVEUR MCP
# =============================================================================

# Creer une instance du serveur MCP
server = Server("metrologie-server")


# =============================================================================
# OUTIL 1 : Calculer les statistiques de base
# =============================================================================

@server.list_tools()
async def list_tools():
    """Declare les outils disponibles pour Claude."""
    return [
        Tool(
            name="calculer_statistiques",
            description="Calcule les statistiques de base (moyenne, ecart-type, min, max) pour une serie de mesures",
            inputSchema={
                "type": "object",
                "properties": {
                    "mesures": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Liste des mesures (valeurs numeriques)"
                    }
                },
                "required": ["mesures"]
            }
        ),
        Tool(
            name="calculer_cpk",
            description="Calcule le Cpk (indice de capabilite) d'un procede",
            inputSchema={
                "type": "object",
                "properties": {
                    "mesures": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Liste des mesures"
                    },
                    "nominal": {
                        "type": "number",
                        "description": "Valeur nominale (cible)"
                    },
                    "tolerance": {
                        "type": "number",
                        "description": "Tolerance (ex: 0.05 pour +/-0.05)"
                    }
                },
                "required": ["mesures", "nominal", "tolerance"]
            }
        ),
        Tool(
            name="analyser_echantillon",
            description="Analyse complete d'un echantillon avec verdict qualite",
            inputSchema={
                "type": "object",
                "properties": {
                    "mesures": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Liste des mesures"
                    },
                    "nominal": {
                        "type": "number",
                        "description": "Valeur nominale"
                    },
                    "tolerance": {
                        "type": "number",
                        "description": "Tolerance"
                    }
                },
                "required": ["mesures", "nominal", "tolerance"]
            }
        ),
    ]


# =============================================================================
# IMPLEMENTATION DES OUTILS
# =============================================================================

def _calculer_statistiques(mesures: list) -> dict:
    """Calcule les statistiques de base."""
    if len(mesures) < 2:
        return {"erreur": "Il faut au moins 2 mesures"}

    return {
        "n": len(mesures),
        "moyenne": round(statistics.mean(mesures), 6),
        "ecart_type": round(statistics.stdev(mesures), 6),
        "minimum": round(min(mesures), 6),
        "maximum": round(max(mesures), 6),
        "etendue": round(max(mesures) - min(mesures), 6)
    }


def _calculer_cpk(mesures: list, nominal: float, tolerance: float) -> dict:
    """Calcule le Cpk."""
    if len(mesures) < 2:
        return {"erreur": "Il faut au moins 2 mesures"}

    moyenne = statistics.mean(mesures)
    sigma = statistics.stdev(mesures)

    lss = nominal + tolerance  # Limite Superieure de Specification
    lsi = nominal - tolerance  # Limite Inferieure de Specification

    # Protection division par zero
    if sigma == 0:
        return {"erreur": "Ecart-type nul, impossible de calculer Cpk"}

    cpk_sup = (lss - moyenne) / (3 * sigma)
    cpk_inf = (moyenne - lsi) / (3 * sigma)
    cpk = min(cpk_sup, cpk_inf)

    # Cp (capabilite potentielle)
    cp = (lss - lsi) / (6 * sigma)

    return {
        "cpk": round(cpk, 4),
        "cp": round(cp, 4),
        "moyenne": round(moyenne, 6),
        "sigma": round(sigma, 6),
        "lsi": lsi,
        "lss": lss
    }


def _analyser_echantillon(mesures: list, nominal: float, tolerance: float) -> dict:
    """Analyse complete avec verdict."""
    stats = _calculer_statistiques(mesures)
    if "erreur" in stats:
        return stats

    cpk_result = _calculer_cpk(mesures, nominal, tolerance)
    if "erreur" in cpk_result:
        return cpk_result

    cpk = cpk_result["cpk"]

    # Verdict selon le Cpk
    if cpk >= 1.67:
        verdict = "EXCELLENT - Procede tres capable"
        niveau = "A"
    elif cpk >= 1.33:
        verdict = "BON - Procede capable"
        niveau = "B"
    elif cpk >= 1.0:
        verdict = "ACCEPTABLE - Surveillance requise"
        niveau = "C"
    else:
        verdict = "NON CAPABLE - Action corrective necessaire"
        niveau = "D"

    # Verifier si des pieces sont hors tolerance
    lsi = nominal - tolerance
    lss = nominal + tolerance
    hors_tolerance = [m for m in mesures if m < lsi or m > lss]

    return {
        "statistiques": stats,
        "capabilite": cpk_result,
        "verdict": verdict,
        "niveau": niveau,
        "pieces_hors_tolerance": len(hors_tolerance),
        "ppm_estime": round((1 - _calculer_rendement(cpk)) * 1_000_000, 0)
    }


def _calculer_rendement(cpk: float) -> float:
    """Estime le rendement (%) basé sur le Cpk (approximation)."""
    # Approximation basee sur distribution normale
    import math
    if cpk <= 0:
        return 0.0
    z = 3 * cpk
    # Fonction de repartition normale approximee
    rendement = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    return min(0.9999999, rendement)


# =============================================================================
# HANDLER DES APPELS D'OUTILS
# =============================================================================

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute l'outil demande par Claude."""

    if name == "calculer_statistiques":
        result = _calculer_statistiques(arguments["mesures"])

    elif name == "calculer_cpk":
        result = _calculer_cpk(
            arguments["mesures"],
            arguments["nominal"],
            arguments["tolerance"]
        )

    elif name == "analyser_echantillon":
        result = _analyser_echantillon(
            arguments["mesures"],
            arguments["nominal"],
            arguments["tolerance"]
        )

    else:
        result = {"erreur": f"Outil inconnu: {name}"}

    # Retourner le resultat en JSON
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


# =============================================================================
# POINT D'ENTREE
# =============================================================================

async def main():
    """Lance le serveur MCP."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    print("Demarrage du serveur MCP Metrologie...")
    print("Ce serveur expose 3 outils :")
    print("  - calculer_statistiques")
    print("  - calculer_cpk")
    print("  - analyser_echantillon")
    print("\nPour l'utiliser avec Claude Code, configurez-le dans :")
    print("  ~/.config/claude/claude_desktop_config.json")
    print("\n" + "="*50)
    asyncio.run(main())
