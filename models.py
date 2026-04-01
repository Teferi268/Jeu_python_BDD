class Personnage:
	def __init__(self, nom, atk, defense, pv):
		self.nom = nom
		self.atk = atk
		self.defense = defense
		self.pv = pv

	def to_dict(self):
		return {self.nom: {"ATK": self.atk, "DEF": self.defense, "PV": self.pv}}


class Monstre(Personnage):
	pass


class ScorePartie:
	def __init__(self, pseudo, score):
		self.pseudo = pseudo
		self.score = score

	def to_dict(self):
		return {"pseudo": self.pseudo, "score": self.score}
