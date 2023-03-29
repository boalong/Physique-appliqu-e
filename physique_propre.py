# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 10:50:21 2023

@author: Letellier
"""


import random
from matplotlib import pyplot as plt
import numpy as np


# Il faut utiliser random.seed() pour générer des nombres pseudo-aléatoires
# et obtenir la même suite de nombre aléatoires à chaque fois
# pour que les résultats restent identiques
random.seed(0)


'''
Partie I : On fait simplement des simulations comme dans le papier de Kirman (Figure II)
'''


def nlle_iteration(N, k, epsilon, delta):
    '''
    Cette fonction calcule le nombre de fourmis sur la source noire après une itération.
    INPUT:
        N: int, nombre de fourmis
        k: int, nombre de fourmis sur la source noire
        epsilon: float, probabilité qu'une fourmi s'autoconvertisse
        delta: float, probabilité qu'une fourmi ne soit pas convertie
    OUTPUT:
        k: int, nombre de fourmis sur la source noire après l'itération
    '''

    # On tire un réel entre 0 et 1 (pour simuler un tirage aléatoire)
    tirage = random.random()
    
    # Calculer p1, p2, p3
    p1 = (1 - k/N)*(epsilon + (1 - delta)*(k/(N-1)))
    
    p2 = (k/N)*(epsilon + (1 - delta)*((N-k)/(N-1)))
    
    # p3 = 1 - p1 - p2 # Ce calcul est inutile
    
    # Créer des intervalles et voir dans lequel atterrit le tirage
    # intervalle pour p1 : [0,p1)
    # intervalle pour p2 : [p1, p1 + p2)
    # intervalle pour p3 : [p1 + p2, 1)
    # Si le tirage est dans l'intervalle [0,p1), alors on ajoute une fourmi
    # Si le tirage est dans l'intervalle [p1, p1 + p2), alors on enlève une fourmi
    # Si le tirage est dans l'intervalle [p1 + p2, 1), alors on garde le même nombre de fourmis
    if 0 <= tirage < p1:
        k += 1
    elif p1 <= tirage < p1 + p2:
        k -= 1      

    # On renvoie le nombre de fourmis
    return k


def afficher_graphe(delta, epsilon, N=100, nb_iterations=100000):
    '''
    Cette fonction affiche le graphe du nombre de fourmis sur la source noire en fonction du nombre de rencontres.
    INPUT:
    INPUT:
        delta: float, probabilité qu'une fourmi ne soit pas convertie
        epsilon: float, probabilité qu'une fourmi s'autoconvertisse
        N: int, nombre de fourmis
        nb_iterations: int, nombre de rencontres
    OUTPUT:
        None
    '''

    # On veut stocker le nombre de fourmis sur la source noire à chaque itération.

    # On initialise. Au début, disons qu'il y a autant de fourmis sur chaque source.

    k = N//2 # la moitié des fourmis sont sur la source noire au début


    # On vérifie que le choix de epsilon et delta est correct

    p1 = (1 - k/N)*(epsilon + (1 - delta)*(k/(N-1)))
        
    p2 = (k/N)*(epsilon + (1 - delta)*((N-k)/(N-1)))

    # print(p1 + p2)

    if p1 + p2 > 1:
        print("Le choix de epsilon et delta n'est pas correct")
        return None


    # Créer une liste dans laquelle on stocke les valeurs de k, le nombre de fourmis sur la source noire

    liste_etats = []

    liste_etats.append(k) # on ajoute l'état initial à la liste des états

    for _ in range(nb_iterations):
        k = nlle_iteration(N, k, epsilon, delta)
        liste_etats.append(k)
        
    # print(liste_etats)

    # On a la liste des états

    # On ne veut n'afficher qu'1 valeur sur 50

    print(nb_iterations//50 + 1) # on veut 2001
    x = [i for i in range(nb_iterations//50 + 1)] # on va faire 100000 itérations
    y = [liste_etats[i] for i in range(len(liste_etats) + 1) if i%50 == 0]

    # Il ne reste qu'à plotter
    plt.plot(x,y)
    plt.xlim(0, nb_iterations//50)
    plt.ylim(0, N)
    plt.show()
    

# afficher_graphe(delta=1, epsilon=0.5) # Premier cas particulier évoqué par Kirman : equilibrium distribution binomiale de paramètres N (le nombre de fourmis), 1/2
# afficher_graphe(delta=0, epsilon=0) # Second cas particulier évoqué par Kirman : martingale avec absorption finale k = 0 ou k = N

# afficher_graphe(delta=0.3, epsilon=0.15) # Figure IIa
# afficher_graphe(delta=0.01, epsilon=0.002) # Figure IIb





'''
Partie II : On vérifie les estimations théoriques données par Kirman (Figure I)
'''


def obtenir_liste_etats(delta, epsilon, N=100, nb_iterations=100000):
    '''
    Cette fonction renvoie la liste des états du nombre de fourmis sur la source noire.
    INPUT:
        delta: float, probabilité qu'une fourmi ne soit pas convertie
        epsilon: float, probabilité qu'une fourmi s'autoconvertisse
        N: int, nombre de fourmis
        nb_iterations: int, nombre de rencontres
    OUTPUT:
        liste_etats: list, liste des états du nombre de fourmis sur la source noire  
    '''

    # On veut stocker le nombre de fourmis sur la source noire à chaque itération.

    # On initialise. Au début, disons qu'il y a autant de fourmis sur chaque source.

    k = N//2 # la moitié des fourmis sont sur la source noire au début


    # On vérifie que le choix de epsilon et delta est correct

    p1 = (1 - k/N)*(epsilon + (1 - delta)*(k/(N-1)))
        
    p2 = (k/N)*(epsilon + (1 - delta)*((N-k)/(N-1)))

    if p1 + p2 > 1:
        print("Le choix de epsilon et delta n'est pas correct")
        return None

    # Créer une liste dans laquelle on stocke les valeurs de k, le nombre de fourmis sur la source noire

    liste_etats = []

    liste_etats.append(k) # on ajoute l'état initial à la liste des états

    for _ in range(nb_iterations):
        k = nlle_iteration(N, k, epsilon, delta)
        liste_etats.append(k)
    
    return liste_etats




def afficher_temps(delta, epsilon, N=100, nb_iterations=100000):
    '''
    Cette fonction affiche le graphe du temps passé à chaque état.
    INPUT:
        delta: float, probabilité qu'une fourmi ne soit pas convertie
        epsilon: float, probabilité qu'une fourmi s'autoconvertisse
        N: int, nombre de fourmis
        nb_iterations: int, nombre de rencontres
    OUTPUT:
        None
    '''

    # On veut une liste de 100 éléments, qui contient le temps passé à chaque état (en considérant le temps comme le nombre
    # d'itérations où on a été à cet état)

    # On veut stocker le nombre de fourmis sur la source noire à chaque itération.
    liste_etats = obtenir_liste_etats(delta, epsilon, N, nb_iterations)

    liste_temps = []
    for i in range(N + 1):
        ct = 0
        for j in liste_etats:
            if j == i:
                ct += 1
        liste_temps.append(ct)

    # On a la liste des temps
    # Maintenant on va la plotter

    x = [i for i in range(101)]
    y = liste_temps

    # Il ne reste qu'à plotter
    plt.plot(x,y)
    plt.xlabel("Nombre de fourmis sur la source noire")
    plt.xlim(0, N)
    plt.ylabel("Temps passé à cet état (en nombre d'itérations)")
    plt.ylim(0, 20000)
    plt.show()

# afficher_temps(delta=0.01, epsilon=0.005) # Figure Ia
# plt.close()
# afficher_temps(delta=0.3, epsilon=0.15) # Figure Ic
# plt.close()
# afficher_temps(delta=0.02, epsilon=0.01) # Figure Ib
# plt.close()


'''
On n'a pas ce qu'on veut, on va devoir estimer vers quoi ça converge pour un grand nombre de processus
'''



def obtenir_temps(delta, epsilon, N=100, nb_iterations=100000):
    '''
    Cette fonction renvoie la liste du temps passé sur chaque état.
    INPUT:
        delta: float, probabilité qu'une fourmi ne soit pas convertie
        epsilon: float, probabilité qu'une fourmi s'autoconvertisse
        N: int, nombre de fourmis
        nb_iterations: int, nombre de rencontres
    OUTPUT:
        liste_temps: list, liste des temps passés à chaque état
    '''

    # On veut une liste de 100 éléments, qui contient le temps passé à chaque état (en considérant le temps comme le nombre
    # d'itérations où on a été à cet état)

    # On veut stocker le nombre de fourmis sur la source noire à chaque itération.
    liste_etats = obtenir_liste_etats(delta, epsilon, N, nb_iterations)

    liste_temps = []
    for i in range(N + 1):
        ct = 0
        for j in liste_etats:
            if j == i:
                ct += 1
        liste_temps.append(ct)

    return liste_temps



def afficher_convergence_temps(delta, epsilon, N=100, nb_iterations=100000, nb_processus=100):
    # On veut avoir 100 listes de temps et calculer le temps moyen sur ces 100 listes

    liste_de_listes = []

    for i in range(nb_processus):
        print(i+1)
        liste_de_listes.append(obtenir_temps(delta, epsilon, N, nb_iterations))
    
    # On a 100 listes de 100 éléments
    # On veut une seule liste avec les moyennes à chaque fois

    liste_moyennes = []

    for i in range(N + 1):
        liste_moyennes.append(np.mean([liste_de_listes[j][i] for j in range(nb_processus)]))

    # On a la liste des moyennes

    # Maintenant on va la plotter

    x = [i for i in range(101)]

    plt.plot(x,liste_moyennes)
    plt.xlabel("Nombre de fourmis sur la source noire")
    plt.xlim(0, N)
    plt.ylabel("Temps moyen passé à cet état (en nombre d'itérations)")
    plt.ylim(0, 10000)
    plt.show()
    

# afficher_convergence_temps(delta=1, epsilon=0.5, nb_processus=100)
# plt.close()

# Pour avoir des figures bien lisses, il faut faire 100 processus, mais c'est long (le compteur des processus s'affiche dans le terminal)
# afficher_convergence_temps(delta=0.01, epsilon=0.005, nb_processus=100) # Figure Ia
# plt.close()
# afficher_convergence_temps(delta=0.02, epsilon=0.01, nb_processus=100) # Figure Ib
# plt.close()
# afficher_convergence_temps(delta=0.3, epsilon=0.15, nb_processus=100) # Figure Ic
# plt.close()



def afficher_convergence_temps_densite(delta, epsilon, N=100, nb_iterations=100000, nb_processus=100):
    # On veut avoir 100 listes de temps et calculer le temps moyen sur ces 100 listes

    liste_de_listes = []

    for i in range(nb_processus):
        print(i+1)
        liste_de_listes.append(obtenir_temps(delta, epsilon, N, nb_iterations))
    
    # On a 100 listes de 100 éléments
    # On veut une seule liste avec les moyennes à chaque fois

    liste_moyennes = []

    for i in range(N + 1):
        liste_moyennes.append(np.mean([liste_de_listes[j][i] for j in range(nb_processus)])/100000)

    # On a la liste des moyennes

    # Maintenant on va la plotter

    x = [i for i in range(101)]

    plt.plot(x,liste_moyennes)
    plt.xlabel("Number of ants on the black source")
    plt.xlim(0, N)
    plt.ylabel("Density of time spent at this state")
    plt.ylim(0, 0.075)
    plt.show()


# afficher_convergence_temps_densite(delta=1, epsilon=0.5, nb_processus=100)


def comparer_convergence_temps_densite_cas_1(delta=1, epsilon=0.5, N=100, nb_iterations=100000, nb_processus=100):
    # On veut avoir 100 listes de temps et calculer le temps moyen sur ces 100 listes

    liste_de_listes = []

    for i in range(nb_processus):
        print(i+1)
        liste_de_listes.append(obtenir_temps(delta, epsilon, N, nb_iterations))
    
    # On a 100 listes de 100 éléments
    # On veut une seule liste avec les moyennes à chaque fois

    liste_moyennes = []

    for i in range(N + 1):
        liste_moyennes.append(np.mean([liste_de_listes[j][i] for j in range(nb_processus)])/100000)

    # On a la liste des moyennes

    # Maintenant on va la plotter

    x = [i for i in range(101)]

    plt.plot(x,liste_moyennes)
    plt.xlabel("Number of ants on the black source")
    plt.xlim(0, N)
    plt.ylabel("Density of time spent in this state")
    plt.ylim(0, 0.1)

    from scipy.stats import binom

    # setting the values
    # of n and p
    n = 100
    p = 1/2
    # defining list of r values
    r_values = list(range(n + 1))
    # list of pmf values
    dist = [binom.pmf(r, n, p) for r in r_values ]
    # plotting the graph 
    # plt.bar(r_values, dist)
    plt.plot(r_values, dist, 'r+')

    plt.show()


# comparer_convergence_temps_densite_cas_1()




# III. Ant model applied to Becker's restaurants example

def nlle_iteration_becker(N, k, epsilon, delta):
    '''
    Cette fonction calcule le nombre de fourmis sur la source noire après une itération.
    INPUT:
        N: int, nombre de fourmis
        k: int, nombre de fourmis sur la source noire
        epsilon: float, probabilité qu'une fourmi s'autoconvertisse
        delta: float, probabilité qu'une fourmi ne soit pas convertie
    OUTPUT:
        k: int, nombre de fourmis sur la source noire après l'itération
    '''

    # On tire un réel entre 0 et 1 (pour simuler un tirage aléatoire)
    tirage = random.random()

    # On regarde si la majorité est blanche ou noire
    if k == N-k:
        majority = None
    elif k/N > 0.5:
        majority = 'black'
    elif k/N < 0.5:
        majority = 'white'

    if majority == None:
        p1 = (1 - k/N)*(epsilon + (1 - delta)*(k/(N-1))) # Probabilité qu'une fourmi passe de la source blanche à la source noire
        p2 = (k/N)*(epsilon + (1 - delta)*((N-k)/(N-1))) # Probabilité qu'une fourmi passe de la source noire à la source blanche

    elif majority == 'white':
        # Calculer p1, p2, p3
        p1 = (1 - k/N)*(epsilon + (1 - delta)*(k/(N-1))*(1 - k/N)) # Probabilité qu'une fourmi passe de la source blanche à la source noire
        p2 = (k/N)*(epsilon + (1 - delta)*((N-k)/(N-1))*(1 + k/N)) # Probabilité qu'une fourmi passe de la source noire à la source blanche

    elif majority == 'black':
        # Calculer p1, p2, p3
        p1 = (1 - k/N)*(epsilon + (1 - delta)*(k/(N-1))*(1 + k/N)) # Probabilité qu'une fourmi passe de la source blanche à la source noire
        p2 = (k/N)*(epsilon + (1 - delta)*((N-k)/(N-1))*(1 - k/N)) # Probabilité qu'une fourmi passe de la source noire à la source blanche
    
    # p3 = 1 - p1 - p2 # Ce calcul est inutile, probabilité qu'une fourmi reste sur la même source
    
    # Créer des intervalles et voir dans lequel atterrit le tirage
    # intervalle pour p1 : [0,p1)
    # intervalle pour p2 : [p1, p1 + p2)
    # intervalle pour p3 : [p1 + p2, 1)
    # Si le tirage est dans l'intervalle [0,p1), alors on ajoute une fourmi
    # Si le tirage est dans l'intervalle [p1, p1 + p2), alors on enlève une fourmi
    # Si le tirage est dans l'intervalle [p1 + p2, 1), alors on garde le même nombre de fourmis
    if 0 <= tirage < p1:
        k += 1
    elif p1 <= tirage < p1 + p2:
        k -= 1      

    # On renvoie le nombre de fourmis
    return k


def afficher_graphe_becker(delta, epsilon, N=100, nb_iterations=100000):
    '''
    Cette fonction affiche le graphe du nombre de fourmis sur la source noire en fonction du nombre de rencontres.
    INPUT:
    INPUT:
        delta: float, probabilité qu'une fourmi ne soit pas convertie
        epsilon: float, probabilité qu'une fourmi s'autoconvertisse
        N: int, nombre de fourmis
        nb_iterations: int, nombre de rencontres
    OUTPUT:
        None
    '''

    # On veut stocker le nombre de fourmis sur la source noire à chaque itération.

    # On initialise. Au début, disons qu'il y a autant de fourmis sur chaque source.

    k = N//2 # la moitié des fourmis sont sur la source noire au début


    # On vérifie que le choix de epsilon et delta est correct

    p1 = (1 - k/N)*(epsilon + (1 - delta)*(k/(N-1)))
        
    p2 = (k/N)*(epsilon + (1 - delta)*((N-k)/(N-1)))

    # print(p1 + p2)

    if p1 + p2 > 1:
        print("Le choix de epsilon et delta n'est pas correct")
        return None


    # Créer une liste dans laquelle on stocke les valeurs de k, le nombre de fourmis sur la source noire

    liste_etats = []

    liste_etats.append(k) # on ajoute l'état initial à la liste des états

    for _ in range(nb_iterations):
        k = nlle_iteration_becker(N, k, epsilon, delta)
        liste_etats.append(k)
        
    # print(liste_etats)

    # On a la liste des états

    # On ne veut n'afficher qu'1 valeur sur 50

    print(nb_iterations//50 + 1) # on veut 2001
    x = [i for i in range(nb_iterations//50 + 1)] # on va faire 100000 itérations
    y = [liste_etats[i] for i in range(len(liste_etats) + 1) if i%50 == 0]

    # Il ne reste qu'à plotter
    plt.plot(x,y)
    plt.xlim(0, nb_iterations//50)
    plt.ylim(0, N)
    plt.show()
    

# afficher_graphe_becker(delta=1, epsilon=0.5) # Premier cas particulier évoqué par Kirman : equilibrium distribution binomiale de paramètres N (le nombre de fourmis), 1/2
# afficher_graphe_becker(delta=0, epsilon=0) # Second cas particulier évoqué par Kirman : martingale avec absorption finale k = 0 ou k = N
# afficher_graphe_becker(delta=0, epsilon=0)

# afficher_graphe_becker(delta=0.3, epsilon=0.15) # Figure IIa
# afficher_graphe_becker(delta=0.01, epsilon=0.002) # Figure IIb











