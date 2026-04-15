# Attention ! le sujet comporte plusieurs erreurs et incohérences.

class Transmission:

	def __init__(self, trame):
		self._id = None
		self._temperature = None
		self._humidite = None
		self._trame = trame
		
		self.decoder()
		
	def __repr__(self):
		""" Méthode magique pour affichage """
		return f"ID : {self._id} / Temp. : {self._temperature}°C / Hum. : {self._humidite}%"
		
	def decoder(self):
		self.decoder_id()
		self.decoder_temperature()
		self.decoder_humidite()
		
	def decoder_id(self):
		self._id = int(self._trame[0:8], 2) # int(s, 2) : conversion binaire -> décimal
		
	def decoder_temperature(self):
		# méthode complétée pour la question 1
		temp_bin = self._trame[16:28]
		self._temperature = (int(temp_bin, 2) - 900) / 10

		
	def decoder_humidite(self):
		# méthode complétée pour la question 1
		# Extraire les 8 bits d'humidité (positions 28 à 36)
		hum_bin = self._trame[28:36]
		
		# Cas spécial : si la valeur est "10100000", l'humidité est 100%
		if hum_bin == "10100000":
			self._humidite = 100
		else:
			# Convertir les 4 premiers bits en décimal pour le premier chiffre
			chiffre1 = str(int(hum_bin[0:4], 2))
			# Convertir les 4 derniers bits en décimal pour le deuxième chiffre
			chiffre2 = str(int(hum_bin[4:8], 2))
			# Concaténer les deux chiffres et convertir en entier
			humidite = chiffre1 + chiffre2
			self._humidite = int(humidite)

		
	def get_id(self):
		return self._id
		
	def get_temperature(self):
		return self._temperature
		
	def get_humidite(self):
		return self._humidite
		
	def est_valide(self):
		# méthode complétée pour la question 2
		# Vérifier que les 40 bits sont présents : ajout de la question 4
		if len(self._trame) != 40:
			return False
		# Découpage de la trame en segments
		id_bin = self._trame[0:8]
		cle_bin = self._trame[8:16]
		temp_bin = self._trame[16:28]
		hum_bin = self._trame[28:36]
		check_bin = self._trame[36:40]
		# Intialisation de la valeur de retour
		valide = True
		# Vérification des bits de parité
		if id_bin.count("1") % 2 != int(check_bin[0]): # Parité de l'ID
			valide = False
			# print("Erreur de parité sur l'ID")
		if cle_bin.count("1") % 2 != int(check_bin[1]): # Parité de la clé
			valide = False
			# print("Erreur de parité sur la clé")
		if temp_bin.count("1") % 2 != int(check_bin[2]): # Parité de la température
			valide = False
			#print("Erreur de parité sur la température")
		if hum_bin.count("1") % 2 != int(check_bin[3]): # Parité de l'humidité
			valide = False
			# print("Erreur de parité sur l'humidité")
		return valide


# Question 1 : test des méthodes decoder_temperature et decoder_humidite
print("Test de la question 1 :")
# On reprend l'exemple de l'énoncé
t1 = Transmission("0010101011001000010010001100011000101101")
print(t1) # ID : 42 / Temp. : 25.0°C / Hum. : 50%

# Question 2 : test de la méthode est_valide
print("\nTest de la question 2 :")
# Trame valide
t2 = Transmission("0010101011001000010010001100011000101101")
print(t2.est_valide()) # True
# Trame invalide (erreur dans la température)
t3 = Transmission("1010101011001000010010001100011000101101")
print(t3.est_valide()) # False

# Question 3 : le programme produit une erreur du type Index out of range.
# On peut observer que certaines trames dans `data.txt` n'ont pas exactement 40 bits. On observe 3 trames malformées :

# - Trame 21 : 41 caractères (1 bit en trop)
# - Trame 24 : 38 caractères (2 bits manquants)
# - Trame 27 : 41 caractères (1 bit en trop)

# Lorsqu'on tente de décoder ces trames, les indices de découpage (`trame[16:28]`, `trame[28:36]`, etc.) ne correspondent plus aux bons blocs de données. Cela peut provoquer des valeurs aberrantes.

# La classe `Transmission` ne vérifie pas la longueur de la trame avant de la décoder, ce qui la rend vulnérable aux données corrompues.

# Question 4
# On ajoute une vérification de la longueur de la trame au début de la méthode `est_valide`. Si la trame n'a pas exactement 40 bits, on retourne `False` immédiatement. Cela permet d'éviter les erreurs de décodage et de signaler que la trame est invalide.
