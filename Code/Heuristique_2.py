#! usr/bin/python
# -*- coding: utf-8 -*-

import math
import sys
import time

import lecteur
import contraintes
import minorant



def placer_activites(i, nb_activites, activites_finies, state, activites, precedence, debut_activite, fin_activite, ressources, duree_max, duree, ressource_max, liste_ressource_disponible):

    # on appelle la fonction "ressources_disponibles" du programme "contraintes" pour creer une liste ou est stockee la quantite de ressources disponibles a chaque instant
    liste_ressource_disponible = contraintes.ressources_disponibles(lecteur.donnees.duree_max, lecteur.donnees.ressource_max)

    # on appelle la fonction "condition_precedence_1" du programme "contraintes" pour verifier si l'activite i possede une liste de precedence ou pas
    condition_1 = contraintes.condition_precedence_1(i, lecteur.donnees.precedence)


    # L'état "pre-first" nous permet de séparer l'ensemble des activités en 2 listes.
    # La liste "activites_sans_precedence" va contenir les activités dont la liste de
    # précédence est vide ou dont la durée est nulle.
    if state == "pre first" :

        print ("----- PREMIERE ETAPE : ON SEPARE LA LISTE EN DEUX --------")

        #on crée la nouvelle liste
        activites_sans_precedence = []

        for i in activites :

            # On teste si les activités ont une durée nulle ou une liste de précédence vide
            # Si c'est le cas, on les ajoute à la nouvelle liste et on remplace leur numéro
            # dans l'ancienne liste par un "0"
            if len(precedence[i-1]) == 0 or duree[i-1] == 0 :
                activites_sans_precedence = activites_sans_precedence + [i]
                activites[i-1] = 0

            # Sinon, on ajoute un "0" à la nouvelle liste à la place de l'activité i
            else :
                activites_sans_precedence = activites_sans_precedence + [0]
                
        print ("LISTE 1 - ACTIVITES SANS PRECEDENCE OU DE DUREE NULLE =", activites_sans_precedence)

        print ("LISTE 2 - ACTIVITES AVEC PRECEDENCE=", activites)

        state = "placer_activites_sans_precedence"

        
    # On va placer en priorité les activités de la nouvelle liste
    if state == "placer_activites_sans_precedence":

        print ("----- DEUXIEME ETAPE : ON PLACE LES ACTIVITES DE LA PREMIERE LISTE --------")

        # On parcourt la liste des activites qui n'ont pas de condition de précédence et dont la durée est nulle
        for i in activites_sans_precedence:

            # on peut placer l'activite si la condition de precedence est verifiee et si elle n'a pas déjà été placée
            if (i != 0 and contraintes.condition_precedence_2(i, lecteur.donnees.precedence, activites_finies) == 1) :

                # t1 correspond au temps a partir duquel on peut placer l'activite i en fonction des conditions de precedence
                t1 = contraintes.temps_debut_activite(i, lecteur.donnees.precedence, fin_activite, condition_1)

                # t2 correspond au temps a partir duquel on peut placer l'activite i en fonction des conditions de ressources
                t2 = contraintes.condition_ressource(t1, i, lecteur.donnees.ressources, lecteur.donnees.duree_max, lecteur.donnees.duree, liste_ressource_disponible)                    

                print (" Duree de l'activite",i, "=", duree[i-1])
                print ("Consommation de ressources pour l'activite",i, "=", ressources [i-1])

                # On modifie les listes ou sont stockees les debuts et les fins de chaque activite lorsqu'elles sont placees
                debut_activite[i-1] = t2
                if duree[i-1] == 0:
                    f = t2
                else :
                    f = t2 + duree[i-1]
                fin_activite[i-1] = f
                
                print("Debut activite", i, "=", t2)
                print("Fin activite", i, "=", f)
                
                # On modifie la liste des ressources disponibles en enlevant la quantité de ressources
                # utilisées par l’activité i à la quantité initiale. 
                for j in range (t2, t2 + duree[i-1]):
                    liste_ressource_disponible[j] = liste_ressource_disponible[j] - ressources[i-1]

                # on remplace le numero de l'activite par un 0 pour montrer qu'elle a ete placee
                # on ajoute a la liste "activites_finies" l'activite qu'on vient de placer
                activites_sans_precedence[i-1] = 0
                activites_finies = activites_finies + [i]
                
                print ("Activites finies", activites_finies)

            else :

                # Si on ne peut pas placer l'activité de la nouvelle liste, on l'ajoute à la deuxième liste
                # et on va essayer de la placer dans un second temps
                activites[i-1] = i

        state = "placer_activites_avec_precedence"

    
    # On va placer le reste des activités
    if state == "placer_activites_avec_precedence" :

        print ("----- TROISIEME ETAPE : ON PLACE LES ACTIVITES RESTANTES --------")

        # On parcourt la liste "activites" 
        for i in activites:
            
            # on peut placer l'activite si la condition de precedence est verifiee et si elle n'a pas déjà été placée
            if (i != 0 and contraintes.condition_precedence_2(i, lecteur.donnees.precedence, activites_finies) == 1) :

                # t1 correspond au temps a partir duquel on peut placer l'activite i en fonction des conditions de precedence
                t1 = contraintes.temps_debut_activite(i, lecteur.donnees.precedence, fin_activite, condition_1)

                # t2 correspond au temps a partir duquel on peut placer l'activite i en fonction des conditions de ressources
                t2 = contraintes.condition_ressource(t1, i, lecteur.donnees.ressources, lecteur.donnees.duree_max, lecteur.donnees.duree, liste_ressource_disponible)                    

                print ("Consommation de ressources pour l'activite",i, "=", ressources [i-1])
                print ("Duree de l'activite",i, "=", duree[i-1])

                # On modifie les listes ou sont stockees les debuts et les fins de chaque activite lorsqu'elles sont placees
                debut_activite[i-1] = t2
                if duree[i-1] == 0:
                    f = t2
                else :
                    f = t2 + duree[i-1]
                fin_activite[i-1] = f
                print("Debut activite", i, "=", t2)
                print("Fin activite", i, "=", f)

                # On modifie la liste des ressources disponibles en enlevant la quantité de ressources
                # utilisées par l’activité i à la quantité initiale.
                for j in range (t2, t2 + duree[i-1]):
                    liste_ressource_disponible[j] = liste_ressource_disponible[j] - ressources[i-1]
                print("Liste ressources disponibles", liste_ressource_disponible)
                
                # on remplace le numero de l'activite par un 0 pour montrer qu'elle a ete placee
                # on ajoute a la liste "activites_finies" l'activite qu'on vient de placer
                activites[i-1] = 0
                activites_finies = activites_finies + [i]

                print (activites_finies)

                state = "second"
                
            # si la condition de precedence n'est pas verifiee pour l'activite i, ou si elle a deja ete placee,
            # on passe a l'activite suivante  
            else :
                state = "second"
                
     # "L'etat 2" est un etat intermediaire qui nous permet de verifier a chaque fois si
     # l'ensemble des activites a ete placé
    if state == "second" :

        # si l'ensemble des activites n'a pas ete placé, on refait un tour de boucle pour placer de nouvelles activités
        if len(activites_finies) != nb_activites :
            state = "placer_activites_avec_precedence"
            
        # si toutes les activites ont ete placees, on peut passer a "l'etat end" et afficher les resultats
        else :
            state = "end"

    # on affiche les resultats
    if state == "end" :
        
        #on remet la liste des activites finies dans l'ordre
        activites_finies_ordre = []
        for i in range (nb_activites-1):
            if duree[i] == 0:
                activites_finies_ordre += [i+1]
        cpt = 0
        while (len(activites_finies_ordre)+1)!=nb_activites:
            for i in range (nb_activites-1):
                if (i+1)not in activites_finies_ordre and debut_activite[i]==cpt:
                    activites_finies_ordre += [i+1]
            cpt += 1
        activites_finies_ordre += [nb_activites]

        activites_finies = activites_finies_ordre
        
        print ("--RESULTATS--")
        print ("LISTE ACTIVITES FINIES DANS L'ORDRE =", activites_finies)
        print ("LISTE DEBUT DE CHAQUE ACTIVITE =", debut_activite)
        print ("LISTE FIN DE CHAQUE ACTIVITE =", fin_activite)

        fin = 0
        for k in range (nb_activites + 1) :
            if fin_activite[k-1] > fin :
                fin = fin_activite[k-1]

        print ("FIN DU PROJET =", fin)
            
        print ("LISTE RESSOURCES DISPONIBLES =", liste_ressource_disponible)

        
        state = "recherche_locale"

    if state == "recherche_locale" :
        print()
        print()
        print("--------RECHERCHE LOCALE--------")
        print()

        #Initialisation
        meilleure_solution_temporaire = activites_finies[:]
        meilleure_duree_tot_temporaire = fin
        meilleur_fin_activite_temporaire = fin_activite[:]
        meilleur_debut_activite_temporaire = debut_activite[:]

        nb_cycles_permutations = 0
        nb_total_de_solutions_testees = 0
        solutions_testees = [activites_finies]
        state = "continue"

        print("La solution de depart est ", activites_finies)
        print("Sa duree totale =",fin)

        while (state != "end"):
            print()
            print("----CYCLE",nb_cycles_permutations + 1,"----")
            nb_solutions_valables_cycle = 0
            meilleure_duree_cycle = meilleure_duree_tot_temporaire
            meilleur_debuts_cycle = meilleur_debut_activite_temporaire[:]
            meilleur_fins_cycle = meilleur_fin_activite_temporaire[:]
            meilleure_solution_cycle = meilleure_solution_temporaire[:]
            activite_permutee_1 = 0
            activite_permutee_2 = 0

            print()
            print("Solution sur laquelle on fait les permutations =",meilleure_solution_temporaire)
            #i et j representent les deux valeurs que l'on va echanger
            #La premiere et la derniere activites de la solution sont fixes
            #Donc i et j sont compris entre 1 et le nombre d'activites - 2
            for i in range (1,len(meilleure_solution_temporaire)-1):
                for j in range (1,len(meilleure_solution_temporaire)-1):
                    state = "continuer"
                    
                    ###Etape 1: On prend la solution temporaire et on effectue une permutation

                    #Si i=j, on passe au prochain j car inutile d'echanger les memes valeurs (on obtiendrait la meme solution)
                    if i == j:      
                        continue

                    #Si l'activite en position i ou en position j a une duree nulle, inutile de faire la permutation
                    if duree[meilleure_solution_temporaire[i]-1] == 0 or duree[meilleure_solution_temporaire[j]-1] == 0:
                        continue
                    
                    #Echange de 2 valeurs
                    solution_a_tester = meilleure_solution_temporaire[:]
                    tmp = solution_a_tester[i]
                    solution_a_tester[i] = solution_a_tester[j]
                    solution_a_tester[j] = tmp
                    
                    #On regarde si la solution a tester a deja ete testee auparavant
                    if solution_a_tester in solutions_testees:
                        state = "break"
                    
                    #On passe au prochain j
                    if state == "break":
                        continue
                        
                    #Si la solution n'a pas encore été testée, on la rajoute dans la liste des solutions testées
                    solutions_testees += [solution_a_tester]
                    nb_total_de_solutions_testees += 1

                        
                    ###Etape 2: On vérifie si les précédences sont toujours respectées

                    #Le compteur_a nous permet de savoir à quelle indice se trouve l'activité que l'on est en train de traiter
                    compteur_a = 0

                    for a in solution_a_tester:
                        
                        #Si le state = break, cela veut dire qu'une précédence n'a pas été respectée et qu'il faut donc sortir de la boucle et passer à une autre solution
                        if state == "break":
                            break

                        #Si la duree de l'activite a est nulle, ca ne sert a rien de verifier si les precedences sont respectees
                        if duree[a-1]==0:
                            compteur_a += 1
                            continue

                        compteur_a += 1

                        #b prend les valeurs des predecesseurs de a
                        for b in precedence[a-1]:
                            
                            #Si un des predecesseurs n'est pas place avant l'activite a, solution pas valable donc on passe a une autre solution
                            if b not in solution_a_tester[0:compteur_a]:
                                state = "break"
                                break
                            
                    if state == "break":
                        continue

                        
                    ###Etape 3: On place toutes les activites pour que la duree totale soit minimale

                    #On crée une liste debut_activites dans laquelle on met les dates de debut des activites dans l'ordre dans lequel les activites se deroulent

                    #Initialisation : on y met les valeurs de la premiere activite (qui debute et finit toujours a 0)
                    debut_activites = [0]
                    fin_activites = [0]

                    #Le compteur permet de savoir a quel indice se trouve l'activite a 

                    
                    #On place chaque activité
                    for a in solution_a_tester:

                        #On a deja place la premiere activite donc si a est la premiere activite, on passe a la suivante sans continuer le programme
                        if a == solution_a_tester[0]:        
                            continue

                        #Si la duree de l'activite a est egale a 0, on la place directement au temps 0
                        if duree[a-1] == 0:
                            debut_activites += [0]
                            fin_activites += [0]
                            continue

                        #Maintenant qu'on s'est occupe des cas particuliers, on peut faire le cas general:
                        
                        #l'activité a commence au plus tôt après le début de la derniere activite placee
                        maxi = 0
                        for g in range (len(debut_activites)):
                            if debut_activites[g]>maxi:
                                maxi = debut_activites[g]
                        debut_activite_a = maxi

                        
                        #On regarde si "a" a des précédences. Si oui, alors l'activité a commence au plus tôt après la fin de tous ses prédécesseurs
                        for c in range (len(debut_activites)):
                            for p in precedence[a-1]:
                                if p == solution_a_tester[c]:
                                    if fin_activites[c] > debut_activite_a:
                                        debut_activite_a = fin_activites[c]

                        #Enfin, on regarde si on peut placer l'activité a ce moment là (debut_activite_a) grâce aux ressources
                        #Si non, on rajoute 1 à debut_activite_a jusqu'à ce que ça soit possible
                        t = debut_activite_a
                        while t != None:
                            ressource_dispo = ressource_max
                            for d in range (len(debut_activites)):
                                if fin_activites[d] > t:
                                    ressource_dispo -= ressources[solution_a_tester[d] - 1]
                            if  ressource_dispo >= ressources [a-1]:
                                debut_activites += [t]
                                fin_activites += [t + duree[a-1]]

                                t = None
                            else:
                                t +=1
     
                    #On remet les dates de debut et de fin dans l'ordre des activites numerotees
                    #pour qu'elles soient en cohesion avec les resultats que nous affichent les autres algorithmes de resolution
                    debut_activites_temp = debut_activites[:]
                    fin_activites_temp = fin_activites[:]
                    cpt = 0
                    for r in solution_a_tester:
                        debut_activites[r-1] = debut_activites_temp[cpt]
                        fin_activites[r-1] = fin_activites_temp[cpt]
                        cpt += 1

                    nb_solutions_valables_cycle += 1
                    
                    ###Etape 4: On calcule la duree totale

                    duree_tot_a_tester = 0
                    
                    #On parcourt la liste de la fin des activites
                    #La plus grande valeur de cette liste nous donnera la duree totale de cette solution
                    for e in range (len(fin_activites)):
                        if fin_activites[e] > duree_tot_a_tester:
                            duree_tot_a_tester = fin_activites[e]

                    # (enlever les guillemets si on veut avoir les détails affichés)
                    """
                    print()
                    print("La solution ", solution_a_tester, "est valable")
                    print("Permutation effectuée: Activités",meilleure_solution_temporaire[i], "et", meilleure_solution_temporaire[j])
                    print("debut activites",debut_activites)
                    print("fin activites",fin_activites)
                    print("Sa duree totale =", duree_tot_a_tester)
                    """
                    
                    ###Etape 5: Comparaison de cette solution avec la meilleure du cycle
                    
                    #On regarde si la solution qui vient d'être trouvée donne une meilleure durée que le résultat trouvé jusqu'à présent dans ce cycle
                    #Si oui, alors c'est cette solution qui devient la "meilleure" et on change toutes les données de la meilleure solution du cycle
                    if duree_tot_a_tester < meilleure_duree_cycle:
                        meilleure_duree_cycle = duree_tot_a_tester
                        meilleur_debuts_cycle = debut_activites
                        meilleur_fins_cycle = fin_activites
                        meilleure_solution_cycle = solution_a_tester
                        activite_permutee_1 = meilleure_solution_temporaire[i]
                        activite_permutee_2 = meilleure_solution_temporaire[j]

                    
            ###Etape 6: On affiche les resultats de ce cycle

            nb_cycles_permutations += 1
            print()
            print()

            if nb_solutions_valables_cycle == 0:
                print("Il n'y avait pas de nouvelles solutions valables dans le cycle", nb_cycles_permutations)
                state = "end"
            elif meilleure_duree_cycle == meilleure_duree_tot_temporaire:
                print()
                print("La duree n'a pas ete diminuee lors de ce cycle donc on arrete le programme")
                state = "end"
            else:
                #Si la solution a été améliorée, on affiche ce qui suit:
                print("Nombre de solutions valables nouvelles dans le cycle",nb_cycles_permutations," =",nb_solutions_valables_cycle)
                print()
                print("MEILLEURE SOLUTION DU CYCLE",nb_cycles_permutations)
                print()
                print("Permutation effectuee: Activites", activite_permutee_1, "et", activite_permutee_2)
                print("Liste des activites dans l'ordre =", meilleure_solution_cycle)
                print("Liste debut de chaque activite =", meilleur_debuts_cycle)
                print("Liste fin de chaque activite =", meilleur_fins_cycle)
                print("Sa duree totale =", meilleure_duree_cycle)
                meilleure_solution_temporaire = meilleure_solution_cycle
                meilleur_debut_activite_temporaire = meilleur_debuts_cycle
                meilleur_fin_activite_temporaire = meilleur_fins_cycle
                meilleure_duree_tot_temporaire = meilleure_duree_cycle


        #On change les listes de debut et fin des activites avec la meilleure solution pour pouvoir tester cette solution avec le verificateur
        debut_activite = meilleur_debut_activite_temporaire
        fin_activite = meilleur_fin_activite_temporaire
        
        print()
        print()
        print("---------------------------------------")
        print()
        print("Nombre de cycles effectués:", nb_cycles_permutations)
        print("Nombre total de solutions testees:", nb_total_de_solutions_testees)
        print()
        print("-------- LA MEILLEURE SOLUTION --------")
        print()
        print("LISTE ACTIVITES FINIES DANS L'ORDRE =", meilleure_solution_temporaire)
        print("LISTE DEBUT DE CHAQUE ACTIVITE =", meilleur_debut_activite_temporaire)
        print("LISTE FIN DE CHAQUE ACTIVITE =", meilleur_fin_activite_temporaire)
        print("FIN DU PROJET =", meilleure_duree_tot_temporaire)
                            

        print()
        print()
        
  
       
def verifsolution(debut_activite,fin_activite,precedence,ressources,activites,ressource_max, duree):

    
    #vérification du respect des précédences
    for i in activites :

        if duree[i-1] != 0 :
            for j in precedence[i-1]:
                if fin_activite[j-1]>debut_activite[i-1]:
                    print("Les precedences de l'activite", i ,"ne sont pas respectees")
                    print("car l'activite", j, "termine a t =",fin_activite[j-1],"alors que l'activite ", i, "debute a t =", debut_activite[i-1])
                    return None
        
    print("Les precedences sont respectees")

                
    #vérification du non dépassement de ressource max
                
    for t in debut_activite:
        conso=0
        for a in range (0,len(activites)):
            if debut_activite[a]<=t and fin_activite[a]>t and debut_activite[a]!=fin_activite[a]:
                conso = conso + ressources[a]
        if conso>ressource_max:
            print("On a depasse la quantite de ressource consommable en l'instant t =", t, "(conso =", conso , ")")
            return None
    print("On ne depasse jamais la ressource max")

def main() :
    
    # On stocke toutes les valeurs de sortie de l’algorithme “lecteur.py” dans des variables

    nb_activites = lecteur.donnees.nb_activites
    duree_max = lecteur.donnees.duree_max
    ressource_max = lecteur.donnees.ressource_max

    activites = lecteur.donnees.activites
    precedence = lecteur.donnees.precedence
    duree = lecteur.donnees.duree
    ressources = lecteur.donnees.ressources

    liste_ressource_disponible = contraintes.ressources_disponibles(lecteur.donnees.duree_max, lecteur.donnees.ressource_max)

    # On cree de nouvelles variables afin d'y stocker de nouvelles informations

    activites_finies = []
    
    debut_activite = []
    for i in range (nb_activites):
        debut_activite = debut_activite + [0]
    
    fin_activite = []
    for i in range (nb_activites):
        fin_activite = fin_activite + [0]

    state = "pre first"
    placer_activites(i, nb_activites, activites_finies, state, activites, precedence, debut_activite, fin_activite, ressources, duree_max, duree, ressource_max, liste_ressource_disponible)

    print ("---CHECKER DE SOLUTIONS---")
    verifsolution(debut_activite,fin_activite,precedence,ressources,activites,ressource_max, duree)

    print("----------MINORANT----------")
    print("Minorant =", minorant.minorant)
    
main()

