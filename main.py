from db_init import (
    collection_heroes,
    collection_monstres,
    collection_scores,
    initialiser_db,
)
from utils import (
    intro,
    menu_principal_affichage,
    charger_heroes_db,
    charger_monstres_db,
    save_score,
    lire_top_scores,
    afficher_top_scores,
)
import copy
import random
import time


def ask_pseudo():
    username = input("Veuillez chosir votre pseudo pour cette partie...")
    if username.isalpha() == False or len(username) > 12:
        print("Pseudo incorrecte : lettre uniquement, 12 caractères max.")
        return ask_pseudo()
    return username






# PARTIE EQUIPE



def afficher_perso(heroes):
    for heroe in heroes:
        print(f"{heroe}\n")


def afficher_team(team, heroes):
    print("Votre équipe est composée de :")
    for nom in team:
        for hero in heroes:
            if nom in hero:
                print(f"- {hero}")
                break


def converti_equipe_objet(choix, heroes):
    # Convertir les noms en objets héros
    team = []
    for nom in choix:
        for hero in heroes:
            if nom in hero:
                team.append(hero)
                break
    return team


def changement(choix, heroes):
    modif = input("Ecris VALIDER pour valider l'équipe, ou CHANGER pour la changer...")

    if modif == "VALIDER":
        return choix
    elif modif == "CHANGER":
        return create_team(heroes)
    else:
        return changement(choix, heroes)


def create_team(heroes):
    afficher_perso(heroes)
    choix = input("Choisissez 3 personages parmis cela...").split()
    team = converti_equipe_objet(choix, heroes)
    afficher_team(choix, heroes)
    return changement(team, heroes)





# PARTIE COMBAT





def attaque(team):
    stats_attaquant = []
    for i in range(len(team)):
        stats_attaquant.append(team[i][list(team[i].keys())[0]]["ATK"])
    return stats_attaquant


def defense(perso_defendant, stats_attaquant):
    points_attaque = 0
    pv_defendeur = perso_defendant[list(perso_defendant.keys())[0]]["PV"]
    for Attaque in stats_attaquant:
        points_attaque += Attaque

    pv_defendeur -= points_attaque * (1 - (perso_defendant[list(perso_defendant.keys())[0]]["DEF"]) / 100)
    if pv_defendeur < 0:
        pv_defendeur = 0
    perso_defendant[list(perso_defendant.keys())[0]]["PV"] = pv_defendeur
    return pv_defendeur

def choix_monstre(monstres):
    monstre = random.choice(monstres)
    return monstre


def deroulement_partie(team, monstre, monstre_nom):
    tour = True  # True = tour du joueur, False = tour du monstre
    while True:
        if tour == True:
            # Tour du joueur
            print("\n--- Tour de l'équipe ---")
            stats_attaquant = attaque(team)
            pv_monstre = defense(monstre, stats_attaquant)
            
            
            if pv_monstre <= 0:
                print(f"\n{monstre_nom} est vaincu. vous avez gagné")
                return True
            print(f"Le monstre a {pv_monstre} PV restants")
            time.sleep(0.5)

            tour = False  # Changement de tour

        else:
            # Tour du monstre
            print("\n--- Tour du monstre ---")
            atk_monstre = monstre[monstre_nom]["ATK"]
            print(f"{monstre_nom} attaque avec {atk_monstre} ATK")
            
            for hero in team:
                hero_nom = list(hero.keys())[0]
                if hero[hero_nom]["PV"] > 0:
                    pv_hero = defense(hero, [atk_monstre])
                    if pv_hero <= 0:
                        print(f"{hero_nom} est mort")
                    else:
                        print(f"{hero_nom} a {int(pv_hero)} PV restants")

            # Vérifie si est morte
            equipe_ko = True
            for hero in team:
                hero_nom = list(hero.keys())[0]
                if hero[hero_nom]["PV"] > 0:
                    equipe_ko = False
                    break
            
            if equipe_ko:
                print("\nL'équipe est morte, vous avez perdu")
                return False
            time.sleep(0.5)
            tour = True  # Changement de tour


def combat(team, monstres):
    print("------------Le combat commence------------")

    compteur_win = 0
    while True:
        monstre = copy.deepcopy(choix_monstre(monstres))
        monstre_nom = list(monstre.keys())[0]
        print(f"\nUn monstre apparait: {monstre_nom} (PV: {monstre[monstre_nom]['PV']})")

        victoire = deroulement_partie(team, monstre, monstre_nom)
        if victoire:
            compteur_win += 1
            print(f"Vagues survécues: {compteur_win}")
        else:
            break

    return compteur_win


def lancer_jeu():
    heroes = charger_heroes_db(collection_heroes)
    monstres = charger_monstres_db(collection_monstres)

    pseudo = ask_pseudo()
    print(f"\nBonne chance, {pseudo}!\n")

    team = create_team(heroes)
    score = combat(team, monstres)

    print(f"\nPartie terminée. Score de {pseudo}: {score} vagues")
    save_score(collection_scores, pseudo, score)
    afficher_top_scores(lire_top_scores(collection_scores))


def afficher_classement():
    afficher_top_scores(lire_top_scores(collection_scores))


def menu_principal():
    initialiser_db()
    intro()

    while True:
        menu_principal_affichage()
        choix = input("Choix: ")

        if choix == "1":
            lancer_jeu()
        elif choix == "2":
            afficher_classement()
        elif choix == "3":
            print("A bientôt !")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    menu_principal()