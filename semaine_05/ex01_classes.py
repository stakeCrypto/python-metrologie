"""
SEMAINE 5 - Exercice 1 : Programmation Orientee Objet (POO)
Objectif : Creer des classes pour la metrologie
"""

import numpy as np
from datetime import datetime

# =============================================================================
# INTRODUCTION A LA POO
# =============================================================================
"""
La POO permet de structurer le code en "objets" qui ont :
- Des ATTRIBUTS (donnees)
- Des METHODES (fonctions)

Avantages :
- Code reutilisable
- Plus facile a maintenir
- Modelise le monde reel
"""

print("="*60)
print("PROGRAMMATION ORIENTEE OBJET - METROLOGIE")
print("="*60)

# =============================================================================
# TODO 1 : Creer une classe Instrument
# =============================================================================

print("\n" + "="*60)
print("TODO 1 - Classe Instrument")
print("="*60)

# Creer une classe Instrument avec :
# - Attributs : nom, resolution, incertitude_etalonnage
# - Methode : __init__(self, nom, resolution, incertitude)
# - Methode : __str__(self) pour affichage
# - Methode : incertitude_type_b(self) qui retourne l'incertitude

class Instrument:
    """Represente un instrument de mesure."""

    def __init__(self, nom, resolution, incertitude_etalonnage):
        """Constructeur - initialise les attributs."""
        self.nom = nom
        self.resolution = resolution
        self.incertitude_etalonnage = incertitude_etalonnage

    def __str__(self):
        """Affichage lisible de l'instrument."""
        return f"Instrument({self.nom}, res={self.resolution}mm, U={self.incertitude_etalonnage}mm)"

    def incertitude_type_b(self):
        """Calcule l'incertitude type B combinee (resolution + etalonnage)."""
        u_resolution = (self.resolution / 2) / np.sqrt(3)
        u_etalonnage = self.incertitude_etalonnage / 2  # k=2
        return np.sqrt(u_resolution**2 + u_etalonnage**2)


# Test de la classe
pied_coulisse = Instrument("Pied a coulisse", 0.01, 0.02)
print(pied_coulisse)
print(f"Incertitude type B : {pied_coulisse.incertitude_type_b():.4f} mm")

# =============================================================================
# TODO 2 : Creer une classe Mesure
# =============================================================================

print("\n" + "="*60)
print("TODO 2 - Classe Mesure")
print("="*60)

# Creer une classe Mesure avec :
# - Attributs : valeur, date, instrument, operateur
# - Methode : __init__
# - Methode : __str__
# - Propriete : @property est_valide(self) -> bool

class Mesure:
    """Represente une mesure individuelle."""

    def __init__(self, valeur, instrument, operateur, date=None):
        """Constructeur."""
        self.valeur = valeur
        self.instrument = instrument  # Objet Instrument
        self.operateur = operateur
        self.date = date or datetime.now()

    def __str__(self):
        """Affichage de la mesure."""
        return f"Mesure({self.valeur:.4f}mm par {self.operateur})"

    def __repr__(self):
        """Representation technique (pour debug)."""
        return f"Mesure({self.valeur}, '{self.operateur}')"

    @property
    def incertitude(self):
        """Incertitude de la mesure (type B de l'instrument)."""
        return self.instrument.incertitude_type_b()


# Test de la classe
m1 = Mesure(50.02, pied_coulisse, "Alice")
m2 = Mesure(49.98, pied_coulisse, "Bob")

print(m1)
print(f"Incertitude : {m1.incertitude:.4f} mm")
print(f"Liste : {[m1, m2]}")  # Utilise __repr__

# =============================================================================
# TODO 3 : Creer une classe Lot
# =============================================================================

print("\n" + "="*60)
print("TODO 3 - Classe Lot")
print("="*60)

# Creer une classe Lot avec :
# - Attributs : numero, piece, nominal, tolerance, mesures (liste)
# - Methode : ajouter_mesure(mesure)
# - Proprietes : moyenne, ecart_type, cpk, taux_conformite
# - Methode : rapport() qui affiche un resume

class Lot:
    """Represente un lot de pieces mesurees."""

    def __init__(self, numero, piece, nominal, tolerance):
        """Constructeur."""
        self.numero = numero
        self.piece = piece
        self.nominal = nominal
        self.tolerance = tolerance
        self.mesures = []  # Liste vide au depart

    def ajouter_mesure(self, mesure):
        """Ajoute une mesure au lot."""
        self.mesures.append(mesure)

    @property
    def valeurs(self):
        """Retourne un array des valeurs de mesure."""
        return np.array([m.valeur for m in self.mesures])

    @property
    def n(self):
        """Nombre de mesures."""
        return len(self.mesures)

    @property
    def moyenne(self):
        """Moyenne des mesures."""
        return np.mean(self.valeurs) if self.n > 0 else 0

    @property
    def ecart_type(self):
        """Ecart-type des mesures."""
        return np.std(self.valeurs, ddof=1) if self.n > 1 else 0

    @property
    def lsi(self):
        """Limite de specification inferieure."""
        return self.nominal - self.tolerance

    @property
    def lss(self):
        """Limite de specification superieure."""
        return self.nominal + self.tolerance

    @property
    def cpk(self):
        """Indice de capabilite Cpk."""
        if self.ecart_type == 0:
            return 0
        cpu = (self.lss - self.moyenne) / (3 * self.ecart_type)
        cpl = (self.moyenne - self.lsi) / (3 * self.ecart_type)
        return min(cpu, cpl)

    @property
    def taux_conformite(self):
        """Pourcentage de pieces conformes."""
        if self.n == 0:
            return 0
        conformes = np.sum((self.valeurs >= self.lsi) & (self.valeurs <= self.lss))
        return (conformes / self.n) * 100

    def rapport(self):
        """Affiche un rapport du lot."""
        print(f"\n{'='*40}")
        print(f"LOT : {self.numero}")
        print(f"Piece : {self.piece}")
        print(f"{'='*40}")
        print(f"Specification : {self.nominal} +/- {self.tolerance} mm")
        print(f"Mesures : {self.n}")
        print(f"Moyenne : {self.moyenne:.4f} mm")
        print(f"Ecart-type : {self.ecart_type:.4f} mm")
        print(f"Cpk : {self.cpk:.2f}")
        print(f"Conformite : {self.taux_conformite:.1f}%")
        print(f"{'='*40}")


# Test de la classe
lot1 = Lot("LOT-001", "Axe", 50.0, 0.05)
lot1.ajouter_mesure(m1)
lot1.ajouter_mesure(m2)
lot1.ajouter_mesure(Mesure(50.01, pied_coulisse, "Alice"))
lot1.ajouter_mesure(Mesure(49.99, pied_coulisse, "Bob"))

lot1.rapport()

# =============================================================================
# TODO 4 : Heritage - Classe InstrumentEtalonne
# =============================================================================

print("\n" + "="*60)
print("TODO 4 - Heritage : InstrumentEtalonne")
print("="*60)

# Creer une classe InstrumentEtalonne qui herite de Instrument
# - Attribut supplementaire : date_etalonnage, validite_mois
# - Methode : est_valide() qui verifie si l'etalonnage est encore valide
# - Override : incertitude_type_b() avec calcul different

class InstrumentEtalonne(Instrument):
    """Instrument avec certificat d'etalonnage."""

    def __init__(self, nom, resolution, incertitude_etalonnage,
                 date_etalonnage, validite_mois=12):
        # Appeler le constructeur de la classe parente
        super().__init__(nom, resolution, incertitude_etalonnage)
        # Ajouter les nouveaux attributs
        self.date_etalonnage = date_etalonnage
        self.validite_mois = validite_mois

    def __str__(self):
        """Override de __str__ pour ajouter la date."""
        status = "VALIDE" if self.est_valide() else "PERIME"
        return f"InstrumentEtalonne({self.nom}, {status})"

    def est_valide(self):
        """Verifie si l'etalonnage est encore valide."""
        from dateutil.relativedelta import relativedelta
        date_limite = self.date_etalonnage + relativedelta(months=self.validite_mois)
        return datetime.now() <= date_limite

    def jours_restants(self):
        """Nombre de jours avant expiration."""
        from dateutil.relativedelta import relativedelta
        date_limite = self.date_etalonnage + relativedelta(months=self.validite_mois)
        delta = date_limite - datetime.now()
        return max(0, delta.days)


# Test de la classe
from datetime import datetime
micrometre = InstrumentEtalonne(
    "Micrometre 0-25",
    resolution=0.001,
    incertitude_etalonnage=0.003,
    date_etalonnage=datetime(2024, 6, 15),
    validite_mois=12
)

print(micrometre)
print(f"Etalonnage valide : {micrometre.est_valide()}")
print(f"Jours restants : {micrometre.jours_restants()}")
print(f"Incertitude type B : {micrometre.incertitude_type_b():.4f} mm")

# =============================================================================
# TODO 5 : Utiliser les classes ensemble
# =============================================================================

print("\n" + "="*60)
print("TODO 5 - Utilisation complete")
print("="*60)

# Scenario complet : Controle d'un lot de roulements

# 1. Creer un instrument etalonne (valide)
comparateur = InstrumentEtalonne(
    nom="Comparateur numerique",
    resolution=0.001,
    incertitude_etalonnage=0.002,
    date_etalonnage=datetime(2025, 9, 1),  # Recemment etalonne
    validite_mois=12
)

print(f"Instrument : {comparateur}")
print(f"Valide pour les mesures : {comparateur.est_valide()}")

# 2. Creer un lot
lot_roulements = Lot(
    numero="LOT-2024-R042",
    piece="Roulement 6205",
    nominal=25.0,
    tolerance=0.02
)

# 3. Simuler des mesures
np.random.seed(42)
valeurs_mesurees = np.random.normal(25.0, 0.006, 10)
operateurs = ["Marie", "Jean", "Marie", "Jean", "Marie",
              "Jean", "Marie", "Jean", "Marie", "Jean"]

for val, op in zip(valeurs_mesurees, operateurs):
    mesure = Mesure(val, comparateur, op)
    lot_roulements.ajouter_mesure(mesure)

# 4. Afficher le rapport
lot_roulements.rapport()

# 5. Acces aux proprietes
print(f"\nAcces direct aux proprietes :")
print(f"  lot.n = {lot_roulements.n}")
print(f"  lot.moyenne = {lot_roulements.moyenne:.4f}")
print(f"  lot.cpk = {lot_roulements.cpk:.2f}")

# 6. Lister les mesures
print(f"\nListe des mesures :")
for i, m in enumerate(lot_roulements.mesures[:3], 1):
    print(f"  {i}. {m}")

print("\n" + "="*60)
print("EXERCICE TERMINE !")
print("="*60)
