from functions import *

import random

random.seed(0)

# Partie I

# afficher_graphe(delta=1, epsilon=0.5) # Premier cas particulier évoqué par Kirman : equilibrium distribution binomiale de paramètres N (le nombre de fourmis), 1/2
# afficher_graphe(delta=0, epsilon=0) # Second cas particulier évoqué par Kirman : martingale avec absorption finale k = 0 ou k = N
# afficher_graphe(delta=0, epsilon=0)

# afficher_graphe(delta=0.3, epsilon=0.15) # Figure IIa
# afficher_graphe(delta=0.01, epsilon=0.002) # Figure IIb



# Partie II

# Premier cas particulier évoqué par Kirman : equilibrium distribution binomiale de paramètres N (le nombre de fourmis), 1/2

# comparer_convergence_temps_densite_cas_1()


# afficher_convergence_temps_densite(delta=0.01, epsilon=0.005, nb_processus=100) # Figure Ia
# plt.close()
# afficher_convergence_temps_densite(delta=0.02, epsilon=0.01, nb_processus=100) # Figure Ib
# plt.close()
# afficher_convergence_temps_densite(delta=0.3, epsilon=0.15, nb_processus=100) # Figure Ic
# plt.close()



# Partie III

random.seed(0) # On réinitialise le générateur de nombres aléatoires pour que les tirages soient les mêmes que dans la partie I

afficher_graphe_becker(delta=1, epsilon=0.5) # Premier cas particulier évoqué par Kirman : equilibrium distribution binomiale de paramètres N (le nombre de fourmis), 1/2
afficher_graphe_becker(delta=0, epsilon=0) # Second cas particulier évoqué par Kirman : martingale avec absorption finale k = 0 ou k = N
afficher_graphe_becker(delta=0, epsilon=0)

# afficher_graphe_becker(delta=0.3, epsilon=0.15) # Figure IIa
# afficher_graphe_becker(delta=0.01, epsilon=0.002) # Figure IIb