import unittest
from calculateur_cpk import calculer_cp_cpk, interpreter_cpk

class TestCalculateurCpk(unittest.TestCase):
    
    def test_processus_excellent(self):
        mesures = [50.00, 50.01, 49.99, 50.00, 50.01,
                   49.99, 50.00, 50.01, 49.99, 50.00]
        resultat = calculer_cp_cpk(mesures, 50.0, 0.1)
        self.assertGreater(resultat['cpk'], 1.67)
    
    def test_processus_non_capable(self):
        mesures = [50.05, 49.95, 50.08, 49.92, 50.10,
                   49.90, 50.07, 49.93, 50.06, 49.94]
        resultat = calculer_cp_cpk(mesures, 50.0, 0.05)
        self.assertLess(resultat['cpk'], 1.0)
    
    def test_moyenne_correcte(self):
        mesures = [10, 20, 30, 40, 50]
        resultat = calculer_cp_cpk(mesures, 30, 20)
        self.assertEqual(resultat['moyenne'], 30.0)

if __name__ == '__main__':
    unittest.main()
