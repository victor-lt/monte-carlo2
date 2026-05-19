from colorama import Fore

def pioche_vide():
    return [0]*10

def produit_scalaire(liste1, liste2):
    resultat = pioche_vide()
    for i in range(10):
        resultat[i] = liste1[i]*liste2[i]
    return resultat

def difference(liste1, liste2):
    resultat = pioche_vide()
    for i in range(10):
        resultat[i] = liste1[i] - liste2[i]
    return resultat

def norme1(liste):
    somme = 0
    for i in range(10):
        somme += liste[i]
    return somme

def fonction_de_transition(etat1, etat2):
    pioche1 = etat1[0]
    pioche2 = etat2[0]
    return norme1(produit_scalaire(pioche1, difference(pioche1, pioche2)))/norme1(pioche1)

def valeur(main):
    valeur = 0
    for i in range(10):
        valeur += main[i]*(i+1)
    if valeur <= 11 and main[0] > 0: #ajoute 10 si un as est présent et cet ajout ne fait pas depasser 21.
        valeur += 10
    return valeur

def retour(etat): #Renvoie la valeur R(s) lorsque s est un état final
    retour = 0
    j1 = etat[1]
    j2 = etat[2]
    c = etat[3]
    d = etat[4]

    #Verifie si il y a blackjack
    if j2 == pioche_vide() and j1 == [1,0,0,0,0,0,0,0,0,1]:
        return 2.5
    else:
        for i in range(2):
            main = etat[i+1]
            coeff = 1 if d[i] == False else 2
            valeur_main = valeur(main)
            valeur_croupier = valeur(etat[3])

            if valeur_main >= 22:
                retour -= coeff
            elif valeur_croupier >= 22:
                retour += coeff
            elif valeur_main == valeur_croupier:
                pass;
            elif valeur_main > valeur_croupier:
                retour += coeff
            else:
                retour -= coeff
        return retour
        
def S(etat, action):
    pioche = etat[0]
    j1 = etat[1]
    j2 = etat[2]
    c = etat[3]
    if action == 'Doubler':
        d = True
    else:
        d = False
    m = etat[5]
    if (action == 'Rester' and norm1(j1) >= 1 and m == 1) or ((action == 'Tirer' or action == 'Doubler') and m == 2):
        S = []
        for carte in range(10):
            pioche = etat[1].copy()
            j2 = j2.copy()
            if pioche[i] >= 1:
                pioche[i] -= 1
                j2[i] += 1
                S.append([pioche, j1, j2, c, d, m])
        return S
    elif action == 'Rester':
        S = []
        for carte in range(10):
            pioche = etat[1].copy()
            c = c.copy()
            if pioche[i] >= 1:
                pioche[i] -= 1
                c[i] += 1
                S.append([pioche, j1, j2, c, d, m])
        return S
    elif action == 'Doubler' or action == 'Tirer':
        S = []
        for carte in range(10):
            pioche = etat[1].copy()
            j1 = j1.copy()
            if pioche[i] >= 1:
                pioche[i] -= 1
                j1[i] += 1
                S.append([pioche, j1, j2, c, d, m])
        return S
    else: #Event of a split
        flag = True
        i = 0
        j1 = j1.copy()
        j2 = j2.copy()
        while flag:
            if j1[i] >= 1:
                j1[i] = 1
                j2[i] = 1
                flag = False
            else:
                i += 1
        return [[pioche, j1, j2, c, d, m]]




#------------# TOUR DE CONTROLE #-----------------#

def DEBUG(variable):
    print(Fore.RED + 'DEBUG PRINT:' + Fore.WHITE , variable)

def TEST():
    pioche1 = [4,4,4,4,4,4,4,4,4,16]
    j11 = [0,1,1,0,0,0,0,0,0,0]
    j21 = [0]*10
    c1 = [0,0,0,0,0,0,1,0,0,0]
    d1 = False
    m1 = 1

    etat1 = [pioche1, j11, j21, c1, d1, m1]
    
    pioche2 = [4,4,4,4,4,4,4,4,3,16]
    j12 = [0,1,1,0,0,0,0,0,1,0]
    j22 = [0]*10
    c2 = [0,0,0,0,0,0,1,0,0,0]
    d2 = False
    m2 = 1

    etat2 = [pioche2, j12, j22, c2, d2, m2]

    print(fonction_de_transition(etat1, etat2))

