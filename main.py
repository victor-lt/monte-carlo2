from colorama import Fore
import sys
sys.setrecursionlimit(10000)  # set new recursion limit

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
	d = etat[4].copy()
	m = etat[5]
	if action == 'Doubler':
		d[m-1] = True
	else:
		d[m-1] = False
	if (action == 'Rester' and norme1(j2) >= 1 and m == 1) or ((action == 'Tirer' or action == 'Doubler') and m == 2):
		S = []
		for carte in range(10):
			pioche = etat[0].copy()
			j2 = j2.copy()
			if pioche[carte] >= 1:
				pioche[carte] -= 1
				j2[carte] += 1
				S.append([pioche, j1, j2, c, d, 2])
		return S
	elif action == 'Rester':
		S = []
		for carte in range(10):
			pioche = etat[0].copy()
			c = c.copy()
			if pioche[carte] >= 1:
				pioche[carte] -= 1
				c[carte] += 1
				S.append([pioche, j1, j2, c, d, m])
		return S
	elif action == 'Doubler' or action == 'Tirer':
		S = []
		for carte in range(10):
			pioche = etat[0].copy()
			j1 = j1.copy()
			if pioche[carte] >= 1:
				pioche[carte] -= 1
				j1[carte] += 1
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

def est_une_paire(main):
	if norme1(main) == 2 and 2 in main:
		return True
	else:
		return False

def theta_max(etat):
	DEBUG(etat)
	j1 = etat[1]
	j2 = etat[2]
	c = etat[3]
	d = etat[4]
	m = etat[5]
	A = ['Rester']

	if valeur(c) >= 17: #Cas de base
		return ['Rester' ,retour(etat)]
	else: #Cas récursif
	
		if norme1(c) == 1 and ((valeur(j1) <= 20 and m == 1) or (valeur(j2) <= 20 and m == 2) ) :
			A.append('Tirer')
			if (d[1] == False and m == 1) or (d[2] == False and m == 2):
				A.append('Doubler')
			if norme1(j2) == 0 and est_une_paire(j1) :
				A.append('Split')
		
		A_resultats = {}
		
		for action in A:

			somme = 0
			for etat2 in S(etat, action):
				somme += fonction_de_transition(etat, etat2)*theta_max(etat2)[1]
			A_resultats[action] = somme

		return max(A_resultats.items(), key=lambda x: x[1])



#------------# TOUR DE CONTROLE #-----------------#

def DEBUG(variable):
	print(Fore.RED + 'DEBUG PRINT:' + Fore.WHITE , variable)

def TEST():
	pioche1 = [4,4,4,4,4,4,4,4,4,16]
	j11 = [0,0,0,0,1,0,0,0,0,1]
	j21 = [0]*10
	c1 = [0,0,0,0,0,0,0,0,0,1]
	d1 = [False, False]
	m1 = 1

	etat1 = [pioche1, j11, j21, c1, d1, m1]

	#DEBUG(S(etat1, 'Rester'))

	pioche2 = [4,4,4,4,4,4,4,4,3,16]
	j12 = [0,1,1,0,0,0,0,0,1,0]
	j22 = [0]*10
	c2 = [0,0,0,0,0,0,1,0,0,0]
	d2 = [False, False]
	m2 = 1

	etat2 = [pioche2, j12, j22, c2, d2, m2]

	print(theta_max(etat1))


TEST()
