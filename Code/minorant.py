#! usr/bin/python
# -*- coding: utf-8 -*-

import math
import sys
import time

import lecteur


duree = lecteur.donnees.duree
precedence = lecteur.donnees.precedence
ressources = lecteur.donnees.ressources
ressource_max = lecteur.donnees.ressource_max
activites = lecteur.donnees.activites
nb_activites = lecteur.donnees.nb_activites


###Calcul du minorant geometrique

print()
aire_totale = 0

#On calcule l'aire totale en additionnant les aires de toutes les activites (duree x ressource)
for i in range (0,len(duree)):
    aire_totale = aire_totale + duree[i]*ressources[i]

#Puis, si quand on divise l'aire totale par ressource max, le resultat est entier, alors c'est le minorant
#Sinon, on prend la valeur entiere et on rajoute 1 (car une duree est forcément entiere dans ce probleme)
if (aire_totale // ressource_max) != (aire_totale / ressource_max):
    minorant_geom = aire_totale // ressource_max + 1
else:
    minorant_geom = aire_totale // ressource_max
    
print("Minorant geometrique =", minorant_geom)


###Calcul du minorant par chemin de precedences

activites_modifiees = []                           #On cree une liste dans laquelle on met les activites dont on a change les durees
durees_modifiees = duree[:]
while len(activites_modifiees) != (len(duree)):
    for i in range (0, len(duree)):
        state = "activite non modifiee"

        #Si la duree de l'activite i+1 est nulle, alors on ne change pas sa valeur
        if duree[i] == 0:
            durees_modifiees[i] = 0
            activites_modifiees += [i+1]
            continue
            
        for k in activites_modifiees :              #On verifie si l'activite i+1 a deja ete rajoutee a la liste
            if k == (i+1):                          #Si c'est le cas, on passe a l'activite suivante
                state = "activite modifiee"
        if state == "activite modifiee":
            continue
        
        maxi = 0
        a = []                                  #On cree une autre liste qui permet de verifier si tous les predecesseurs de i sont bien dans la liste
        for p in precedence[i]:
            for k in activites_modifiees:
                if p == k:

                    a += [p]          
        if  a == precedence[i]:                 #Si tous les predecesseurs de i sont dans la liste, alors la duree de i change de valeur
            for j in precedence[i]:             #et prend la valeur duree[i] + la plus grande duree de ses predecesseurs
                if durees_modifiees[j-1] > maxi:
                    maxi = durees_modifiees[j-1]    
            durees_modifiees[i] += maxi
            activites_modifiees += [i+1]       #On a change (si besoin ) la valeur de duree[i] donc on peut rajouter l'activite i+1 a la liste

#Enfin, pour trouver le minorant, on prend la plus grande duree
minorant_chemin = 0
for i in range (0,len(duree)):   
    if durees_modifiees[i] > minorant_chemin:
        minorant_chemin = durees_modifiees[i]
print("Minorant par chemin =", minorant_chemin)


###Calcul du minorant par empilements

#On va d'abord trier les activites dans l'ordre decroissant des ressources
ressources_triees = []
durees_triees = []
nb_activites_non_nulles = 0

#On enleve les activites qui ont une duree nulle
for i in range (nb_activites):
    if duree[i] != 0:
        durees_triees += [duree[i]]
        ressources_triees += [ressources[i]]
        nb_activites_non_nulles += 1

#On fait un premier tri a bulle pour avoir l'ordre croissant des durees
for j in range (nb_activites_non_nulles-1,0,-1):
    for k in range (j):
        if (durees_triees[k]>durees_triees[k+1]):
            temp_1 = ressources_triees[k]
            temp_2 = durees_triees[k]
            ressources_triees[k] = ressources_triees[k+1]
            durees_triees[k] = durees_triees[k+1]
            ressources_triees[k+1] = temp_1
            durees_triees[k+1] = temp_2
            
#On fait un tri a bulle pour avoir l'ordre croissant des ressources

for l in range (nb_activites_non_nulles-1,0,-1):
    for m in range (l):
        if (ressources_triees[m]>ressources_triees[m+1]):
            temp_1 = ressources_triees[m]
            temp_2 = durees_triees[m]
            ressources_triees[m] = ressources_triees[m+1]
            durees_triees[m] = durees_triees[m+1]
            ressources_triees[m+1] = temp_1
            durees_triees[m+1] = temp_2

#Puis on inverse les listes pour avoir l'ordre decroissant des ressources
ressources_triees.reverse()
durees_triees.reverse()

state = "continuer"
minorant_empilement = 0

#Ce minorant ne se calcule que s'il y a au moins une activite qui a une ressource superieure a la moitie de la ressource max
if ressources_triees[0] > ressource_max/2:      
    minorant_empilement = durees_triees[0]
    
    while state != "fini":
        for o in range(1,nb_activites_non_nulles):
            
            #S'il n'y a pas assez de place pour mettre l'activite d'indice o au dessus de l'activite d'avant
            if ressources_triees[o] > (ressource_max - ressources_triees[o-1]):
                #Alors on la place apres l'activite d'avant
                minorant_empilement += durees_triees[o]

            #Si l'activite o a la meme ressource que l'activite d'avant et qu'on ne peut pas empiler plus de deux fois l'activite o sur elle-meme,
            elif ressources_triees[o] == ressources_triees[o-1] and (ressource_max - 2*ressources_triees[o]) < ressources_triees[o]:
                #On declare une nouvelle variable qui contiendra l'indice de l'activite qu'on est en train de tester
                p = o
                #On declare une nouvelle variable somme qui contiendra la somme de toutes les durees des activites qui ont le meme besoin en ressource que l'activite o (dont o-1)
                somme = durees_triees[o-1]
                
                #On fait tourner le programme tant que l'activite p a le meme besoin en ressource que celle de depart o
                while ressources_triees[p] == ressources_triees[o]:
                    somme += durees_triees[p]
                    p += 1
                    
                #On divise la somme par 2 (puisqu'on peut placer 2 activites l'une sur l'autre en chaque temps) tout en s'assurant que le résultat est entier
                somme = int((somme-0.5)/2)+1

                #Enfin, si la nouvelle duree minimale trouvee est plus grande que l'activite o-1
                if durees_triees[o-1]<somme:
                    #On enleve au minorant la duree de l'activite o-1 et on rajoute la duree minimale des activites avec les memes ressources 
                    minorant_empilement += (somme - durees_triees[o-1]) 
                
                #On arrete le programme                                                         
                state = "fini"
                break
            
            #Sinon, on arrete le programme
            else:
                state = "fini"
                break
            
print("Minorant par empilements =", minorant_empilement)
    


#Maintenant qu'on a trouvé trois minorants, on garde le meilleur
minorants = [minorant_geom,minorant_chemin,minorant_empilement]
minorant = 0
for i in minorants:
    if i > minorant:
        minorant = i

print("Meilleur minorant =", minorant)



