"""
Exercice 1 : Variables et Types de donnees
==========================================
Objectif : Comprendre les types de base en Python

Pour executer ce fichier :
    python semaine_01/ex01_variables.py
"""

# =============================================================================
# 1. LES VARIABLES
# =============================================================================
# Une variable stocke une valeur. Pas besoin de declarer le type !

nom = "Thierry"           # str  (chaine de caracteres)
age = 30                  # int  (nombre entier)
taille = 1.75             # float (nombre decimal)
est_metrologue = True     # bool (vrai ou faux)

print("=== MES PREMIERES VARIABLES ===")
print(nom)
print(age)
print(taille)
print(est_metrologue)


# =============================================================================
# 2. LES TYPES DE DONNEES
# =============================================================================
# Python a 4 types de base : str, int, float, bool

# --- Entiers (int) ---
temperature = 25
nombre_mesures = 100

# --- Decimaux (float) ---
pression = 101.325        # en kPa
incertitude = 0.05

# --- Chaines (str) ---
unite = "kPa"
instrument = "Manometre digital"

# --- Booleens (bool) ---
calibre = True
hors_tolerance = False

# La fonction type() permet de verifier le type
print("\n=== VERIFICATION DES TYPES ===")
print(f"temperature: {type(temperature)}")    # <class 'int'>
print(f"pression: {type(pression)}")          # <class 'float'>
print(f"unite: {type(unite)}")                # <class 'str'>
print(f"calibre: {type(calibre)}")            # <class 'bool'>


# =============================================================================
# 3. OPERATIONS DE BASE
# =============================================================================

print("\n=== OPERATIONS MATHEMATIQUES ===")

a = 10
b = 3

print(f"a + b = {a + b}")      # Addition: 13
print(f"a - b = {a - b}")      # Soustraction: 7
print(f"a * b = {a * b}")      # Multiplication: 30
print(f"a / b = {a / b}")      # Division: 3.333...
print(f"a // b = {a // b}")    # Division entiere: 3
print(f"a % b = {a % b}")      # Modulo (reste): 1
print(f"a ** b = {a ** b}")    # Puissance: 1000


# =============================================================================
# 4. CONCATENATION DE CHAINES
# =============================================================================

print("\n=== CHAINES DE CARACTERES ===")

prenom = "Thierry"
nom_famille = "Fischer"

# Methode 1 : Concatenation avec +
nom_complet = prenom + " " + nom_famille
print(nom_complet)

# Methode 2 : f-string (recommande!)
message = f"Bonjour, je suis {prenom} {nom_famille}"
print(message)

# Methode 3 : Formatage avec valeurs numeriques
mesure = 23.456
print(f"Valeur mesuree : {mesure} {unite}")
print(f"Valeur arrondie : {mesure:.2f} {unite}")  # 2 decimales


# =============================================================================
# 5. EXERCICES PRATIQUES
# =============================================================================

print("\n=== A TOI DE JOUER ! ===")

# TODO: Decommenter et completer les exercices ci-dessous

# Exercice A : Creer une variable pour stocker une mesure de 15.7 degres
ma_mesure = 15.7
print(f"Ma mesure : {ma_mesure} degres")

# Exercice B : Calculer la moyenne de 3 mesures
m1 = 10.2
m2 = 10.5
m3 = 10.3
moyenne = (m1 + m2 + m3) / 3
print(f"Moyenne : {moyenne}")

# Exercice C : Verifier si une mesure est dans la tolerance
valeur = 100.5
tolerance = 1.0
valeur_cible = 100.0
dans_tolerance = abs(valeur - valeur_cible) <= tolerance
print(f"Dans tolerance : {dans_tolerance}")

print("\nBravo ! Tu as termine l'exercice 1.")
