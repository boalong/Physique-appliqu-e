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


def nlle_iteration(N, k, epsilon, delta):
    '''
    Cette fonction calcule le nombre de fourmis sur la source noire après une itération.
    INPUT:
        N: int, nombre de fourmis
        k: int, nombre de fourmis sur la source noire
        epsilon: float, probabilité qu'une fourmi soit convertie
        delta: float, probabilité qu'une fourmi s'autoconvertisse
    OUTPUT:
        k: int, nombre de fourmis sur la source noire après une itération
    '''

    # On tire un réel entre 0 et 1 (pour simuler un tirage aléatoire)
    tirage = random.random()
    
    # Calculer p1, p2, p3
    p1 = (1 - k/N)*(epsilon + (1 - delta)*(k/(N-1)))
    
    p2 = (k/N)*(epsilon + (1 - delta)*((N-k)/(N-1)))
    
    p3 = 1 - p1 - p2 
    
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

'''
Partie I : On fait simplement des simulations comme dans le papier de Kirman (Figure II)
'''

def afficher_graphe(delta, epsilon, N=100, nb_iterations=100000):
    '''
    Cette fonction affiche le graphe du nombre de fourmis sur la source noire en fonction du nombre de rencontres.
    INPUT:
        nb_iterations: int, nombre d'itérations
        delta: float, probabilité qu'une fourmi s'autoconvertisse
        epsilon: float, probabilité qu'une fourmi soit convertie
        N: int, nombre de fourmis
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


def obtenir_liste_etats(delta, epsilon, N=100, nb_iterations=100000):

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

def afficher_convergence(delta, epsilon, N=100, nb_iterations=100000, nb_processus=100):
    # On veut avoir 100 listes d'états et calculer l'état moyen sur ces 100 listes

    liste_de_listes = []

    for i in range(nb_processus):
        print(i)
        liste_de_listes.append(obtenir_liste_etats(delta, epsilon, N, nb_iterations))
    
    # On a 100 listes de 100000 éléments
    # On veut une seule liste avec les moyennes à chaque fois

    liste_moyennes = []
    for i in range(nb_iterations + 1):
        liste_moyennes.append(np.mean([liste_de_listes[j][i] for j in range(nb_processus)]))

    # On a la liste des moyennes
    # Maintenant on va la plotter

    print(nb_iterations//50 + 1) # on veut 2001
    x = [i for i in range(nb_iterations//50 + 1)] # on va faire 100000 itérations
    y = [liste_moyennes[i] for i in range(len(liste_moyennes) + 1) if i%50 == 0]

    # Il ne reste qu'à plotter
    plt.plot(x,y)
    plt.xlim(0, nb_iterations//50)
    plt.ylim(0, N)
    plt.show()

# afficher_convergence(delta=0, epsilon=0, nb_processus=100)
# afficher_convergence(delta=0.001, epsilon=0.005)

'''
Partie II : On vérifie les estimations théoriques données par Kirman (Figure I)
'''

def afficher_temps_moyen(delta, epsilon, N=100, nb_iterations=100000):

    # On veut une liste de 100 éléments, qui contient le temps moyen passé à chaque état (en considérant le temps comme le nombre
    # d'itérations où on a été à cet état)

    # On veut stocker le nombre de fourmis sur la source noire à chaque itération.
    liste_etats = obtenir_liste_etats(delta, epsilon, N, nb_iterations)

    liste_temps_moyens = []
    for i in range(N + 1):
        print(i)
        ct = 0
        for j in liste_etats:
            if j == i:
                ct += 1
        liste_temps_moyens.append(ct)

    # On a la liste des temps moyens
    # Maintenant on va la plotter

    x = [i for i in range(101)]
    y = liste_temps_moyens


    total = 0
    for i in y:
        total += i
    print(total)

    # Il ne reste qu'à plotter
    plt.plot(x,y)
    plt.xlim(0, N)
    plt.ylim(0, 20000)
    plt.show()

# afficher_temps_moyen(delta=0.01, epsilon=0.005)
# plt.close()
# afficher_temps_moyen(delta=0.3, epsilon=0.15)
# plt.close()
# afficher_temps_moyen(delta=0, epsilon=0)


def obtenir_temps_moyen(delta, epsilon, N=100, nb_iterations=100000):

    # On veut une liste de 100 éléments, qui contient le temps moyen passé à chaque état (en considérant le temps comme le nombre
    # d'itérations où on a été à cet état)

    # On veut stocker le nombre de fourmis sur la source noire à chaque itération.
    liste_etats = obtenir_liste_etats(delta, epsilon, N, nb_iterations)

    liste_temps_moyens = []
    for i in range(N + 1):
        ct = 0
        for j in liste_etats:
            if j == i:
                ct += 1
        liste_temps_moyens.append(ct)

    return liste_temps_moyens


def afficher_convergence_temps_moyen(delta, epsilon, N=100, nb_iterations=100000, nb_processus=100):
    # On veut avoir 100 listes de temps moyen et calculer le temps moyen sur ces 100 listes

    liste_de_listes = []

    for i in range(nb_processus):
        print(i)
        liste_de_listes.append(obtenir_temps_moyen(delta, epsilon, N, nb_iterations))
    
    # On a 100 listes de 100 éléments
    # On veut une seule liste avec les moyennes à chaque fois

    liste_moyennes = []

    for i in range(N + 1):
        liste_moyennes.append(np.mean([liste_de_listes[j][i] for j in range(nb_processus)]))

    # On a la liste des moyennes

    # Maintenant on va la plotter

    x = [i for i in range(101)]

    plt.plot(x,liste_moyennes)
    plt.xlim(0, N)
    plt.ylim(0, 10000)
    plt.show()   

afficher_convergence_temps_moyen(delta=0.01, epsilon=0.005, nb_processus=100)













