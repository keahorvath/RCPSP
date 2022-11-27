#! usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys
import time

# Cet algorithme prend en entrée le fichier texte à lire et retournera l’ensemble des données permettant de représenter de manière claire le problème. 

# On cree une classe qui regroupera l'ensemble des informations lues dans le fichier texte
class donnees_RCPSP:
    "Donnees du probleme"

# On fait en sorte que l'on puisse directement choisir quel fichier lire dans le terminal (on y ecrirera le nom du programme suivi du nom du fichier)    
nomFichier = sys.argv[1]
file = open (nomFichier, "r")
print("Donnees lues dans " + nomFichier)

# On cree une place pour stocker les donnees dans la classe "donneees_RCPSP"
donnees = donnees_RCPSP()

# On lit la ligne 1 (ou 2, ou 3) puis on separe chaque donnee que l'on stocke dans un tableau
line_1 = file.readline().split()
# On affecte a nos variables les informations presentes dans le fichier dont nous avons besoin
donnees.nb_activites = int(line_1[1])
print("Nombre d'activites =", donnees.nb_activites)

line_2 = file.readline().split()
donnees.duree_max = int(line_2[1])
print("Duree maximum = ", donnees.duree_max)

line_3 = file.readline()

# on cree deux listes vides qui vont nous permettre de stocker les informations relatives aux numeros des activites et a la liste de precedence de chaque activite
donnees.activites = []
donnees.precedence = []

# on fait de meme que pour les lignes precedentes, mais on associe le premier element de la ligne a la liste "activites"
# si il n'y a plus aucune information sur la ligne, on cree une liste de precedence vide pour l'activite i
# sinon, on ajoute tous les autres elements de la ligne a la liste de precedence de l activite i 
for i in range (1, donnees.nb_activites + 1):
    precedence_act = []
    
    line = file.readline().split()
    numero_activite = int(line[0])
    
    donnees.activites = donnees.activites + [numero_activite]

    taille = len(line)
    
    if taille == 1 :
        precedence_act = []
        
    else :
        for j in range (1, taille):
            precedence_act = precedence_act + [int(line[j])]

    donnees.precedence = donnees.precedence + [precedence_act]

print ("Activites=", donnees.activites)
print ("Precedence=" , donnees.precedence)

# on refait la meme operation que pour les lignes 1, 2 et 3
line_4 = file.readline().split()
donnees.ressource_max = int(line_4[1])
print ("Ressource_max =", donnees.ressource_max)

line_5 = file.readline()

# on cree deux listes vides pour la duree et les ressources consommees par chaque activite
donnees.duree=[]
donnees.ressources=[]

# on affecte le deuxieme element de la ligne a la liste ressources et le 3e a la liste duree
# ainsi, la duree de l'activite i se situera au rang d'indice i de la liste "duree"
for i in range (1, donnees.nb_activites + 1):
    line = file.readline().split()
    donnees.ressources = donnees.ressources + [int(line[1])]
    donnees.duree = donnees.duree + [int(line[2])]

print ("Duree=", donnees.duree)
print ("Ressources=", donnees.ressources)

file.close()

