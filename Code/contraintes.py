#! usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys
import time

import lecteur



# Cet algorithme va permettre de vérifier si les contraintes de précédence et de ressources sont vérifiées pour chaque activite.

# Si l’activité i ne possède pas de précédence, c’est-à-dire si la liste de précédence de l’activité est de longueur nulle,
# on peut la placer et le programme nous retournera 1.
def condition_precedence_1(i,precedence):
    
    if len(precedence[i-1]) == 0 :
        return 1

    else :
        return precedence [i-1]

    

# Cette fonction nous permet de vérifier si les activités figurant dans la liste de précédence de l’activité i ont déjà été placées.
# Elle retourne 1 si la condition de precedence est verifiee et si on peut placer l'activite
# Elle retourne None si la condition n'est pas verifiee
def condition_precedence_2(i, precedence, activites_finies):
    
    # condition_1 correspond a la liste de precedence de l'activite i si elle existe
    condition_1 = condition_precedence_1(i, precedence)
    res = 0

    # si condition_1 est egal a 1, alors il y n'y a aucune condition de precedence a verifier
    if condition_1 != 1 :

        # si la liste contenant l’ensemble des activités terminées ne contient aucun élément,
        # la contrainte de précédence n’est pas respectée.
        if len(activites_finies) == 0 :
            print("----- ACTIVITE", i, "----- : condition de precedence non verifiee")
            return None

        # sinon, on verifie si chacune des activités de la liste de précédence de l’activité i a déjà été placée
        # on regarde si toutes les activites de la liste de precedence figurent dans la liste des activités terminées.
        else :
            for k in precedence[i-1] :
                for j in activites_finies :
                    if k == j :
                        res = res + 1
            
            if res == len(precedence[i-1]):
                print ("----- ACTIVITE", i, "----- :Condition de precedence verifiee, on peut placer l'activite")
                return 1

            else :
                print ("----- ACTIVITE", i, "----- : condition de precedence non verifiee")
                return None
    else :
        print ("----- ACTIVITE", i, "----- : Pas de precedence, on peut placer l'activite")
        return 1



    

# On cree une liste « ressource_disponible » qui va nous permettre de vérifier si la condition de ressource est vérifiée.
def ressources_disponibles(duree_max, ressource_max):

    ressource_disponible = []

    # On initialise l’ensemble des éléments de la liste avec la valeur de la borne maximale Bk, qui correspond à la
    # quantité maximale de ressources à utiliser à chaque instant. 
    for i in range (0, duree_max):
        ressource_disponible = ressource_disponible + [ressource_max]

    return ressource_disponible



# Cette fonction nous permet de déterminer à partir de quel moment on peut placer l’activité i. 
def temps_debut_activite(i, precedence, fin_activite,condition_1):

    # Si la liste de precedence de l'activite i est vide, on peut essayer de la placer à partir du temps t = 0. 
    if condition_1 == 1:
        t = 0
        return t

    # Sinon, on peut placer l'activite i lorsque toutes les activites de la liste de precedence ont ete terminees,
    # c'est a dire a partir de la date de fin la plus elevee des activites de cette liste. 
    else :
        t = 0
        for j in precedence[i-1] :
            if fin_activite[j-1] > t :
                t = fin_activite[j-1]

        print("Precedence", precedence[i-1])
        print ("Fin de la derniere activite de precedence =", t)
      
        print ("Je peux placer l'activite",i,"a partir du temps",t)
        return t



# on vérifie si l'on dispose d’assez de ressources durant toute la durée de l'activite i, et ce à partir du temps t défini dans la fonction precedente 
def condition_ressource (t, i, ressources, duree_max, duree, ressource_disponible):

    # si la duree de l'activite est nulle, on considere qu'elle debute et se termine au temps t = 0
    if duree[i-1] == 0 :
        t = 0
        return t

    # Si il n'y a pas assez de place dans la liste ressource_disponible pour placer l'activite i
    # durant toute sa duree, on se place au temps t + 1
    else :
        for k in range(t, duree_max+1):
            for j in range (t, t + duree[i-1]):
                if ressource_disponible[j] - ressources[i-1] < 0 :
                    t = t + 1
        return t
            
