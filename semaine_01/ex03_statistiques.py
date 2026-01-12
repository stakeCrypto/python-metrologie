import csv
import statistics

temperatures = []

with open('mesures.csv', 'r') as f:
    lecteur = csv.DictReader(f)
    for ligne in lecteur:
        temp = float(ligne['temperature'])
        temperatures.append(temp)

moyenne = statistics.mean(temperatures)
ecart_type = statistics.stdev(temperatures)
temp_min = min(temperatures)
temp_max = max(temperatures)

print("=== STATISTIQUES TEMPÉRATURES ===")
print(f"Nombre de mesures : {len(temperatures)}")
print(f"Moyenne : {moyenne:.2f}°C")
print(f"Écart-type : {ecart_type:.2f}°C")
print(f"Min : {temp_min:.2f}°C")
print(f"Max : {temp_max:.2f}°C")
