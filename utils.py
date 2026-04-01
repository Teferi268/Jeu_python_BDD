def intro():
	print("=" * 50)
	print("       BIENVENUE DANS L'ARÈNE DES HÉROS")
	print("=" * 50)
	print()
	print("Vous êtes sur le point de former votre équipe")
	print("et d'affronter des monstres terrifiants!")
	print()
	print("Règles du jeu:")
	print("- Choisissez 3 héros pour votre équipe")
	print("- Combattez des monstres tour par tour")
	print("- Survivez le plus longtemps possible!")
	print()
	print("-" * 50)


def menu_principal_affichage():
	print("\n=== MENU PRINCIPAL ===")
	print("1. Démarrer le jeu")
	print("2. Afficher le classement")
	print("3. Quitter")


def charger_heroes_db(collection_heroes):
	heroes = []
	for doc in collection_heroes.find({}, {"_id": 0}):
		if "nom" in doc:
			heroes.append({doc["nom"]: {"ATK": doc["ATK"], "DEF": doc["DEF"], "PV": doc["PV"]}})
		else:
			for key, value in doc.items():
				if isinstance(value, dict) and "ATK" in value and "DEF" in value and "PV" in value:
					#Verifie que c'est bien un dictionaire avant d'ajouter l'heros
					heroes.append({key: value})
					break
	return heroes


def charger_monstres_db(collection_monstres):
	monstres = []
	for doc in collection_monstres.find({}, {"_id": 0}):
		if "nom" in doc:
			monstres.append(
				{doc["nom"]: {"ATK": doc["ATK"], "DEF": doc["DEF"], "PV": doc["PV"]}}
			)
		else:
			for key, value in doc.items():
				if isinstance(value, dict) and "ATK" in value and "DEF" in value and "PV" in value:
					#Verifie que c'est bien un dictionaire avant d'ajouter le monstre
					monstres.append({key: value})
					break
	return monstres


def save_score(collection_scores, pseudo, score):
	collection_scores.insert_one({"pseudo": pseudo, "score": score})


def lire_top_scores(collection_scores, limite=3):
	return list(collection_scores.find({}, {"_id": 0}).sort("score", -1).limit(limite))


def afficher_top_scores(scores):
	print("\n=== TOP 3 SCORES ===")
	if len(scores) == 0:
		print("Aucun score enregistré.")
		return

	rang = 1
	for score in scores:
		print(f"{rang}. {score['pseudo']} - {score['score']} vagues")
		rang += 1
