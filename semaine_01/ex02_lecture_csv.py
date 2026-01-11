"""
Exercice 2 : Lecture de fichiers CSV
====================================
Objectif : Apprendre a lire des donnees depuis un fichier CSV

Pour executer ce fichier :
    python3 semaine_01/ex02_lecture_csv.py
"""

import csv  # Module integre a Python pour lire les CSV

# =============================================================================
# 1. OUVRIR ET LIRE UN FICHIER
# =============================================================================
# Le mot-cle 'with' ouvre le fichier et le ferme automatiquement

print("=== LECTURE SIMPLE ===")

with open("data/mesures_temperature.csv", "r") as fichier:
    contenu = fichier.read()
    print(contenu)


# =============================================================================
# 2. LIRE LIGNE PAR LIGNE AVEC CSV.READER
# =============================================================================
# csv.reader() transforme chaque ligne en liste

print("=== LECTURE AVEC CSV.READER ===")

with open("data/mesures_temperature.csv", "r") as fichier:
    lecteur = csv.reader(fichier)

    for ligne in lecteur:
        print(ligne)  # Chaque ligne est une liste


# =============================================================================
# 3. LIRE AVEC EN-TETES (CSV.DICTREADER)
# =============================================================================
# DictReader utilise la 1ere ligne comme cles du dictionnaire

print("\n=== LECTURE AVEC DICTREADER (recommande) ===")

with open("data/mesures_temperature.csv", "r") as fichier:
    lecteur = csv.DictReader(fichier)

    for ligne in lecteur:
        # Chaque ligne est un dictionnaire
        print(f"Date: {ligne['date']}, Temp: {ligne['temperature']}C")


# =============================================================================
# 4. STOCKER LES DONNEES DANS UNE LISTE
# =============================================================================

print("\n=== STOCKAGE EN LISTE ===")

mesures = []  # Liste vide

with open("data/mesures_temperature.csv", "r") as fichier:
    lecteur = csv.DictReader(fichier)

    for ligne in lecteur:
        mesures.append(ligne)  # Ajouter chaque ligne a la liste

# Maintenant on peut utiliser les donnees
print(f"Nombre de mesures : {len(mesures)}")
print(f"Premiere mesure : {mesures[0]}")
print(f"Derniere mesure : {mesures[-1]}")  # -1 = dernier element


# =============================================================================
# 5. EXTRAIRE UNE COLONNE
# =============================================================================

print("\n=== EXTRAIRE LES TEMPERATURES ===")

temperatures = []

with open("data/mesures_temperature.csv", "r") as fichier:
    lecteur = csv.DictReader(fichier)

    for ligne in lecteur:
        temp = float(ligne['temperature'])  # Convertir str -> float
        temperatures.append(temp)

print(f"Temperatures : {temperatures}")
print(f"Min : {min(temperatures)}C")
print(f"Max : {max(temperatures)}C")


# =============================================================================
# 6. EXERCICES PRATIQUES
# =============================================================================

print("\n=== A TOI DE JOUER ! ===")

# TODO: Decommenter et completer les exercices ci-dessous

# Exercice A : Calculer la moyenne des temperatures
# Indice : sum(liste) donne la somme, len(liste) donne le nombre d'elements
moyenne_temp = sum(temperatures) / len(temperatures)
print(f"Temperature moyenne : {moyenne_temp:.2f}C")

# Exercice B : Extraire toutes les valeurs d'humidite dans une liste
humidites = []
with open("data/mesures_temperature.csv", "r") as fichier:
    lecteur = csv.DictReader(fichier)
    for ligne in lecteur:
        humidites.append(float(ligne['humidite']))
print(f"Humidites : {humidites}")

# Exercice C : Compter combien de mesures ont ete faites par "Alice"
compteur_alice = 0
with open("data/mesures_temperature.csv", "r") as fichier:
    lecteur = csv.DictReader(fichier)
    for ligne in lecteur:
        if ligne['operateur'] == "Alice":
            compteur_alice += 1
print(f"Mesures par Alice : {compteur_alice}")

print("\nBravo ! Tu as termine l'exercice 2.")
