#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Déc 2012 - Avril 2015- Tous droits réservés
# GPLv3 - www.mon-club-elec.fr

# modules a importer 
from PyQt4.QtGui import *
from PyQt4.QtCore import *  # inclut QTimer..

import os,sys
import serial # communication serie
import time

from SimpleGCodeGUI import * # fichier obtenu à partir QtDesigner et pyuic4

a=None #objet global pour application - pour gestion processEvents

class myApp(QWidget, Ui_Form): # la classe reçoit le Qwidget principal ET la classe définie dans test.py obtenu avec pyuic4
	def __init__(self, parent=None):
		QWidget.__init__(self) # initialise le Qwidget principal 
		self.setupUi(parent) # Obligatoire 

		#Ici, personnalisez vos widgets si nécessaire

		#Réalisez les connexions supplémentaires entre signaux et slots
		self.connect(self.pushButtonOuvrir, SIGNAL("clicked()"), self.pushButtonOuvrirClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButtonEnregistrer, SIGNAL("clicked()"), self.pushButtonEnregistrerClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButtonNouveau, SIGNAL("clicked()"), self.pushButtonNouveauClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 

		self.connect(self.pushButtonStopGCode, SIGNAL("clicked()"), self.pushButtonStopGCodeClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButtonPassGCode, SIGNAL("clicked()"), self.pushButtonPassGCodeClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 

		self.connect(self.pushButtonEnvoiGCode, SIGNAL("clicked()"), self.pushButtonEnvoiGCodeClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 

		#self.connect(self.pushButtonOuvrirRep, SIGNAL("clicked()"), self.pushButtonOuvrirRepClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 

		# boutons de contrôle des axes X,Y,Z de la machine 
		# -- X
		self.connect(self.pushButton_X_PLUS_UN, SIGNAL("clicked()"), self.pushButton_X_PLUS_UN_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_X_PLUS_DIX, SIGNAL("clicked()"), self.pushButton_X_PLUS_DIX_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_X_MOINS_UN, SIGNAL("clicked()"), self.pushButton_X_MOINS_UN_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_X_MOINS_DIX, SIGNAL("clicked()"), self.pushButton_X_MOINS_DIX_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_HOME_X, SIGNAL("clicked()"), self.pushButton_HOME_X_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_RAZ_X, SIGNAL("clicked()"), self.pushButton_RAZ_X_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_X_GOTO_ZERO, SIGNAL("clicked()"), self.pushButton_X_GOTO_ZERO_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 

		# -- Y
		self.connect(self.pushButton_Y_PLUS_UN, SIGNAL("clicked()"), self.pushButton_Y_PLUS_UN_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Y_PLUS_DIX, SIGNAL("clicked()"), self.pushButton_Y_PLUS_DIX_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Y_MOINS_UN, SIGNAL("clicked()"), self.pushButton_Y_MOINS_UN_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Y_MOINS_DIX, SIGNAL("clicked()"), self.pushButton_Y_MOINS_DIX_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_HOME_Y, SIGNAL("clicked()"), self.pushButton_HOME_Y_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_RAZ_Y, SIGNAL("clicked()"), self.pushButton_RAZ_Y_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Y_GOTO_ZERO, SIGNAL("clicked()"), self.pushButton_Y_GOTO_ZERO_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 

		# -- Z
		self.connect(self.pushButton_Z_PLUS_ZERO_UN, SIGNAL("clicked()"), self.pushButton_Z_PLUS_ZERO_UN_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Z_PLUS_UN, SIGNAL("clicked()"), self.pushButton_Z_PLUS_UN_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Z_PLUS_DIX, SIGNAL("clicked()"), self.pushButton_Z_PLUS_DIX_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Z_MOINS_ZERO_UN, SIGNAL("clicked()"), self.pushButton_Z_MOINS_ZERO_UN_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Z_MOINS_UN, SIGNAL("clicked()"), self.pushButton_Z_MOINS_UN_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Z_MOINS_DIX, SIGNAL("clicked()"), self.pushButton_Z_MOINS_DIX_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_HOME_Z, SIGNAL("clicked()"), self.pushButton_HOME_Z_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_RAZ_Z, SIGNAL("clicked()"), self.pushButton_RAZ_Z_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButton_Z_GOTO_ZERO, SIGNAL("clicked()"), self.pushButton_Z_GOTO_ZERO_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 

		# -- Speed - slider et pushbutton
		self.connect(self.horizontalSlider_SET_SPEED, SIGNAL("valueChanged(int)"), self.horizontalSlider_SET_SPEED_ValueChanged) 
		self.connect(self.horizontalSlider_SET_SPEED, SIGNAL("sliderReleased()"), self.horizontalSlider_SET_SPEED_Released) 

		self.connect(self.pushButton_SET_SPEED, SIGNAL("clicked()"), self.pushButton_SET_SPEED_Clicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
 
		# port série 
		self.connect(self.pushButtonInitSerial, SIGNAL("clicked()"), self.pushButtonInitSerialClicked) 
		self.connect(self.pushButtonEnvoi, SIGNAL("clicked()"), self.pushButtonEnvoiClicked) 
		self.connect(self.pushButtonStop, SIGNAL("clicked()"), self.pushButtonStopClicked) 

		# - pour envoi sur appui return dans lineEdit
		self.connect(self.lineEditChaineEnvoi, SIGNAL("returnPressed()"), self.pushButtonEnvoiClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 

		#initialisation Timer
		self.timerSerial=QTimer() # déclare un timer Qt
		self.connect(self.timerSerial, SIGNAL("timeout()"), self.timerSerialEvent) # connecte le signal timeOut de l'objet timer à l'appel de la fonction voulue 

		#--- déclaration utiles --- 
		self.serialPort=None # déclaration initiale
		
		self.stopGCode=False # variable classe pour stopper GCode
		self.flagOK=False # variable classe pour témoin bonne réception OK
		
	# les fonctions appelées, utilisées par les signaux 

	#---- les boutons de contrôle des axes X,Y,Z de l'interface
	# -- X 
	def pushButton_X_PLUS_UN_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton X+1 cliqué")
		
		gcode=(
"""G91
G01 X1
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_X_PLUS_DIX_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton X+10 cliqué")
		
		gcode=(
"""G91
G01 X10
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_X_MOINS_UN_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton X-1 cliqué")
		
		gcode=(
"""G91
G01 X-1
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_X_MOINS_DIX_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton X-10 cliqué")
		
		gcode=(
"""G91
G01 X-10
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_HOME_X_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton HOME X cliqué")
		
		gcode=(
"""G28 X0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	# -- Y 
	def pushButton_Y_PLUS_UN_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Y+1 cliqué")
		
		gcode=(
"""G91
G01 Y1
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_Y_PLUS_DIX_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Y+10 cliqué")
		
		gcode=(
"""G91
G01 Y10
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_Y_MOINS_UN_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Y-1 cliqué")
		
		gcode=(
"""G91
G01 Y-1
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_Y_MOINS_DIX_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Y-10 cliqué")
		
		gcode=(
"""G91
G01 Y-10
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_HOME_Y_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton HOME Y cliqué")
		
		gcode=(
"""G28 Y0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	# -- Z 
	def pushButton_Z_PLUS_ZERO_UN_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Z+0.1 cliqué")
		
		gcode=(
"""G91
G01 Z0.1
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_Z_PLUS_UN_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Z+1 cliqué")
		
		gcode=(
"""G91
G01 Z1
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_Z_PLUS_DIX_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Z+10 cliqué")
		
		gcode=(
"""G91
G01 Z10
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_Z_MOINS_ZERO_UN_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Z-0.1 cliqué")
		
		gcode=(
"""G91
G01 Z-0.1
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_Z_MOINS_UN_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Z-1 cliqué")
		
		gcode=(
"""G91
G01 Z-1
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	def pushButton_Z_MOINS_DIX_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton Z-10 cliqué")
		
		gcode=(
"""G91
G01 Z-10
G90
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- home Z
	def pushButton_HOME_Z_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton HOME Z cliqué")
		
		gcode=(
"""G28 Z0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- RAZ X
	def pushButton_RAZ_X_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton RAZ X cliqué")
		
		gcode=(
"""G92 X0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- RAZ X
	def pushButton_RAZ_Y_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton RAZ Y cliqué")
		
		gcode=(
"""G92 Y0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- RAZ Z
	def pushButton_RAZ_Z_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton RAZ Z cliqué")
		
		gcode=(
"""G92 Z0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- GOTO ZERO X
	def pushButton_X_GOTO_ZERO_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton GOTO XO cliqué")
		
		gcode=(
"""G01 X0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- GOTO ZERO Y
	def pushButton_Y_GOTO_ZERO_Clicked(self): # lors appui bouton initialisation série 
		print("Bouton GOTO Y0 cliqué")
		
		gcode=(
"""G01 Y0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- GOTO ZERO Z
	def pushButton_Z_GOTO_ZERO_Clicked(self): # lors appui bouton 
		print("Bouton GOTO Z0 cliqué")
		
		gcode=(
"""G01 Z0
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- Slider SET SPEED
	def horizontalSlider_SET_SPEED_ValueChanged(self, valeur): # fonction appelée si changement valeur slider - reçoit la valeur courante
		print("Slider modifié : valeur = " + str(valeur))

	def horizontalSlider_SET_SPEED_Released(self): # fonction appelée si changement souris relâchée
		print("Slider : clic souris relaché")
		print("Valeur = " + str(self.horizontalSlider_SET_SPEED.value()))

		speed=self.horizontalSlider_SET_SPEED.value() # récupère valeur courante slider
		
		gcode=(
"""G01 F"""+str(speed)+"""
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

	#-- pushbutton SET SPEED
	def pushButton_SET_SPEED_Clicked(self): # lors appui bouton 
		print("Bouton SET SPEED cliqué")

		speed=self.horizontalSlider_SET_SPEED.value() # récupère valeur courante slider
		
		gcode=(
"""G01 F"""+str(speed)+"""
""")
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>

		#----- les fonctions des signaux des boutons du Terminal série ---- 				
	def pushButtonInitSerialClicked(self): # lors appui bouton initialisation série 
		print("Bouton Init cliqué")
		if self.serialPort: # si le port existe déjà 
			self.serialPort.close() # ferme le port si existe

		# -- initialise paramètres initialisation
		if self.comboBoxPort.currentText()=="" : # si le champ d'initialisation Port est vide = initialisation par défaut 
			strPortInit="/dev/ttyACM0" # port par défaut
		else :
			strPortInit=str(self.comboBoxPort.currentText()) #sinon utilise paramètre champ texte pour le port
		
		strDebitInit=str(self.comboBoxDebit.currentText()) # paramètre champ texte pour debit 
		
		#--- initialisation série avec gestion erreur --- 			
		try: # essaie d'exécuter les instructions 
			# initialise port serie avec délai attente en réception en ms
			self.serialPort=serial.Serial(strPortInit, strDebitInit, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0.1) 			
			#self.serialPort=serial.Serial(strPortInit, strDebitInit) # initialise port serie forme réduite 
			self.serialPort.flushInput() # vide la file d'attente série
			print("Initialisation Port Série : " + strPortInit +" @ " + strDebitInit +" = OK ") # affiche debug
			
			#-- change aspect bouton init
			self.pushButtonInitSerial.setStyleSheet(QString.fromUtf8("background-color: rgb(0, 255, 0);")) # bouton en vert
			self.pushButtonInitSerial.setText("OK")  # change titre bouton 
			
		except: # si erreur initialisation 
			print("Erreur initialisation Série")		
				
			#-- change aspect bouton init
			self.pushButtonInitSerial.setStyleSheet(QString.fromUtf8("background-color: rgb(255, 127, 0);")) # bouton en orange
			self.pushButtonInitSerial.setText(QString.fromUtf8("PB"))  # change titre bouton 

		#self.timerSerial.start(20) # lance le timer avec délai en ms - 10 pour réception rapide 
		self.timerSerial.start(self.spinBoxDelaiReception.value()) # lance le timer avec délai en ms avec valeur spinbox
		
	def pushButtonEnvoiClicked(self): # lors appui bouton envoi série du champ du Terminal Série
		print("Bouton ENVOI appuyé")
		self.envoiChaineSerie(str(self.lineEditChaineEnvoi.text())) # envoi le contenu du champ texte sur le port série 
	
	#----- fonction de classe commune d'envoi d'une chaîne sur le port série ---- 
	def envoiChaineSerie(self, chaineIn): # la fonction reçoit un objet chaîne Str
		
		if self.serialPort: # seulement si le port série existe - n'existe pas (=None) tant que pas initialisé 

			self.timerSerial.stop() # stoppe le timer le temps d'envoyer message sur le port série		
			
			# combobox avec index 0 = rien, 1=saut de ligne (LF), 2=retour chariot (CR), 3= les 2 LF+CR
			if self.comboBoxFinLigne.currentIndex()==0: # si rien sélectionné
				# self.serialPort.write(str(self.lineEditChaineEnvoi.text())+'\n'  ) # envoie la chaine sur le port serie		
				self.serialPort.write(chaineIn)  # envoie la chaine sur le port serie	- variante ascii	
				print("Envoi Série : " + chaineIn )
				self.textEditTraceEnvoiSerie.append(chaineIn) # ajoute texteEdit de visualisation 

			if self.comboBoxFinLigne.currentIndex()==1: # si saut de ligne sélectionné
				self.serialPort.write(chaineIn +chr(10) ) # envoie la chaine sur le port serie	- variante ascii	
				print("Envoi Série : " + chaineIn + '\n')
				self.textEditTraceEnvoiSerie.append(chaineIn) # ajoute texteEdit de visualisation 
				
			if self.comboBoxFinLigne.currentIndex()==2: # si retour chariot sélectionné
				self.serialPort.write(chaineIn+chr(13)  ) # envoie la chaine sur le port serie	- variante ascii	
				print("Envoi Série : " + chaineIn + '\r')
				self.textEditTraceEnvoiSerie.append(chaineIn) # ajoute texteEdit de visualisation 
				
			if self.comboBoxFinLigne.currentIndex()==3: # si saut de ligne + retour chariot sélectionné
				self.serialPort.write(chaineIn+chr(10)+chr(13)  ) # envoie la chaine sur le port serie	- variante ascii
				print("Envoi Série : " + chaineIn + '\n'+'\r')
				self.textEditTraceEnvoiSerie.append(chaineIn) # ajoute texteEdit de visualisation 
			
			self.timerSerial.start(self.spinBoxDelaiReception.value()) # lance le timer avec délai en ms avec valeur spinbox	
			#self.timerSerial.start() # redémarre le timer - laisse délai pour réception en réinitialisation Timer à 0
			# car sinon l'appui survient n'importe quand et si survient peu de temps avant fin délai
			# la réception est hachée
			
	
	#--- fin envoiChaineSerie

	#--- fonction envoi du GCode sur le port série
	# envoie le GCode vers machine avec attente des réponses <ok>
	def envoiGCode(self, gcodeIn):
		
		gcodeLines=gcodeIn.splitlines()
		print gcodeLines
		
		# desactive timer serial
		if self.serialPort: # seulement si le port série existe 
			self.timerSerial.stop() # stoppe le timer le temps de lire les caractères et éviter "réentrée"

		# défile les lignes du gcode
		for line in gcodeLines: # défile les lignes
			if line.startswith(';'):
				continue
			else : 
			
				#self.envoiChaineSerie(line+"\n") # envoi ligne --> cette fonction réactive timer... donc pb.. 
				
				self.serialPort.write(line+"\n")  # envoie la chaine sur le port serie
				
				print "envoi ligne : " + line 
				
				# lecture des données reçues		

				self.flagOK=False
				self.chaineIn=""
				self.char=""
				
				while self.flagOK==False : # on attend réception <ok>
					
					# reception d'une ligne
					while (self.serialPort.inWaiting()): # tant que au moins un caractère en réception
						self.char=self.serialPort.read() # on lit le caractère
						#self.chaineIn=self.chaineIn+self.char		# forme minimale...
						
						if self.char=='\n': # si saut de ligne, on sort du while
							#print("saut ligne reçu") # debug
							self.char=''
							break # sort du while inWaiting
						else: #tant que c'est pas le saut de ligne, on l'ajoute à la chaine 
							self.chaineIn=self.chaineIn+self.char					
						
						if self.serialPort.inWaiting()==0 : # si aucun nouveau char en réception, on attend un peu...  
							time.sleep(0.01) # pause en secondes
						
					a.processEvents() # traite events app dans while inWaiting - évite freeze - à évaluer de façon régulière mais pas trop...
					
					if self.stopGCode==True :
						self.stopGCode=False # RAZ variable
						self.timerSerial.start() # redémarre le timer 
						return # sortie de la fonction 
					
					# si pass, OK aura été mis à True
					
					# fin serialPort inWaiting
					
					#print "sortie while inwaiting"
					#print self.chaineIn
					
					# analyse chaine recue 
					if self.chaineIn!="" :
						
						print self.chaineIn
						
						#ici analyser attente <ok>
						if "<ok>" in self.chaineIn : 
							#print "OK valide."
							flagOK=True
							break
						else: 
							self.chaineIn="" #RAZ chaineIn
							
							
				#print "sortie while flagOK"
				
			time.sleep(0.001) # pause en secondes entre 2 envoi
			
		# fin for
		
		self.timerSerial.start() # redémarre le timer


	#-- fonction gestion clicked pushButton Stop 
	def pushButtonStopClicked(self):
		print("Bouton Stop cliqué")

		#-- stoppe la réception série -- 
		if self.serialPort: # si le port existe déjà 
			self.serialPort.close() # ferme le port si existe
			self.timerSerial.stop() # stoppe le timer
		
		#-- change aspect bouton init
		self.pushButtonInitSerial.setStyleSheet(QString.fromUtf8("background-color: rgb(255, 127, 0);")) # bouton en orange
		self.pushButtonInitSerial.setText(QString.fromUtf8("Off"))  # change titre bouton 
	
	#-- fin fonction gestion clicked pushButton Stop 

	#----- fonction de gestion du signal timeout du QTimer = réception série
	def timerSerialEvent(self): # fonction appelée lors de la survenue d'un évènement Timer - nom fonction indiférrent 
		#-- variables de réception -- 
		self.chaineIn="";
		self.char="";
		
		# lecture des données reçues		
		if self.serialPort: # seulement si le port série existe 
			self.timerSerial.stop() # stoppe le timer le temps de lire les caractères et éviter "réentrée"
			
			while (self.serialPort.inWaiting()): # tant que au moins un caractère en réception
				self.char=self.serialPort.read() # on lit le caractère
				#self.chaineIn=self.chaineIn+self.char		# forme minimale...
				
				if self.char=='\n': # si saut de ligne, on sort du while
					print("saut ligne reçu") # debug
					break # sort du while
				else: #tant que c'est pas le saut de ligne, on l'ajoute à la chaine 
					self.chaineIn=self.chaineIn+self.char					
			
			flagDetect=False
			
			if len(self.chaineIn)>0: # ... pour ne pas avoir d'affichage si ""	
				print(self.chaineIn) # affiche la chaîne 
				self.textEditReception.append(self.chaineIn[:-1]) # ajoute le texte au textEdit en enlevant le dernier caractère (saut de ligne)
				
				#if self.chaineIn[:1].isalnum(): # si la chaine est un chiffre
					#print("Tout des chiffres")
					#self.draw(int(self.chaineIn)) # // ajoute la valeur au graphique
					
				#self.analyseChaine(self.chaineIn[:-1], str(self.lineEditRacineChaine.text())) # appelle la fonction d'analyse de chaine
				# l'utilisation de :-1 couplé à l'utilisation de )$ ci-dessous impose une fin de chaîne par ) une fois le saut de ligne enlevé
				
				"""
				#--- ls(/chemin)
				result=self.testInstructionString("ls(",self.chaineIn[:-1], True) # appelle fonction test instruction format fonction(chaine)
				if(result):
					self.textEditTraceAnalyseChaine.append(QString.fromUtf8(result)) # ajoute la chaine au champ
					self.getContentDir(self.lineEditCheminRep.text()+result) # affiche contenu répertoire en se basant sur racine courante

				#--- read(nomfichier) --- 
				result=self.testInstructionString("read(",self.chaineIn[:-1], True) # appelle fonction test instruction format fonction(chaine)				
				if(result):
					self.textEditTraceAnalyseChaine.append(QString.fromUtf8(result)) # ajoute la chaine au champ
					self.readFile(self.lineEditCheminRep.text()+"/ "+result) # affiche contenu répertoire en se basant sur racine courante
				"""
				
			self.timerSerial.start(self.spinBoxDelaiReception.value()) # lance le timer avec délai en ms avec valeur spinbox
			#self.timerSerial.start() # redémarre le timer
			# ne pas stopper le timerSerial permet plus grande vitesse réception... Il faut que Arduino envoie à même fréquence également
			
	#---- fin timerEvent 
	
	#========== analyse de chaine ========================= 
	
	#---- test instruction string ------ 
	def testInstructionString (self, chaineTestIn, chaineRefIn, debugIn):
		# Les paramètres reçus par la fonction sont :
		# chaineTestIn : chaîne à trouver
		# chaineRefIn : chaine entière à tester
		# debugIn : flag pour message de débug
		
		# cast paramètres reçus 
		str(chaineTestIn)
		str(chaineRefIn)
		bool(debugIn)
		
		if (debugIn): print(chaineTestIn)
		if (debugIn): print(chaineRefIn)
		if (debugIn): print(debugIn)
		
		posRef=len(chaineTestIn)# position de référence pour analyse (xxx) 
		if (debugIn): print("posRef= "+str(posRef))
		
		paramString=None # le String reste "none" tant que pas initialisé par =""

		if (debugIn): print(chaineRefIn[0:posRef]) 

		if chaineRefIn[0:posRef]==chaineTestIn : # si reçoit l'instruction chaineTest(
     
			if (debugIn): print("Racine reconnue : "+str(chaineTestIn)) 
 
			paramString=chaineRefIn[posRef:len(chaineRefIn)-1] # extrait la chaine de caractere recue en parametre 
			if (debugIn): print(paramString) # affiche la chaine de caractere
     
			if chaineRefIn[len(chaineRefIn)-1:len(chaineRefIn)]==")" : # si fermeture parenthèse = instruction valide
			
				if (debugIn) : print(")") # affiche
				if (debugIn) : print("Instruction valide !") # affiche
				return(paramString) # renvoie true si instruction valide 
		
			#fin si fermeture parenthèse
		
			else: # si parenthese absente 
			
				if (debugIn) : print("Instruction invalide !") # affiche
				return(0) # renvoie null 
					
			# fin else
		
		# fin si recoit chaineTest(
		
		else : # si pas bonne chaine Test présente
			
			if (debugIn) : print(".") # affiche
			return(0) # renvoie null si instruction invalide
          
		# fin else 

	#-- fin testInstructionString
	
	
	#---- fonction analyse de chaine --- 
	def analyseChaine(self, chaineIn, chaineRacineIn): # fonction reçoit chaine à analyser et la racine à utiliser - reconnaît fonction racine(**,**, ..,**)
		
		args=None # valeur par défaut de args 
		flagRacine=False # drapeau racine OK 
		
		self.textEditTraceAnalyseChaine.setText(QString.fromUtf8("Chaine à analyser : " + chaineIn)) # trace analyse chaine

		#result=re.findall(r'^.*\((.*)\).*$',chaineIn) # extrait ** de la chaine au format --(**) si la chaîne est au format valide  
		result=re.findall(r'^.*\((.*)\)$',chaineIn) # extrait ** de la chaine au format --(**) si la chaîne est au format valide  
		self.textEditTraceAnalyseChaine.append(str(len(result)) + QString.fromUtf8(" chaine valide")) # trace analyse chaine 

		#racine=re.findall(r'^(.*)\(.*\).*$',chaineIn) # extrait ** de la chaine au format **(--) si la chaîne est au format valide  
		racine=re.findall(r'^(.*)\(.*\)',chaineIn) # extrait ** de la chaine au format **(--) si la chaîne est au format valide  
		self.textEditTraceAnalyseChaine.append(str(len(racine)) + QString.fromUtf8(" racine valide")) # trace analyse chaine 
		
		
		#-- analyse racine --		
		if len(racine)==1:
			self.textEditTraceAnalyseChaine.append(QString.fromUtf8("Racine reçue : ")+ racine[0]) # trace analyse chaine 
						
			if racine[0] == str(chaineRacineIn): 
				self.textEditTraceAnalyseChaine.append(QString.fromUtf8("Racine reçue conforme"))# trace analyse chaine 
				flagRacine=True # flag racine OK
			else:
				self.textEditTraceAnalyseChaine.append(QString.fromUtf8("Racine reçue non conforme"))# trace analyse chaine 
			# fin else

		# fin if
						
		if len(result)==1 and flagRacine: # si une seule chaine valide détectée et que la racine OK 
			#self.textEditTraceAnalyseChaine.append(QString.fromUtf8(result[0])) # trace analyse chaine : affiche la chaine des arguments
			self.textEditTraceAnalyseChaine.append(QString.fromUtf8("Paramètres reçus :")) # trace analyse chaine : affiche la chaine des arguments
			args=result[0].split(',') # récupère la liste des arguments séparés par une parenthèse
			self.textEditTraceAnalyseChaine.append(QString.fromUtf8(str(args))) # trace analyse chaine : affiche la liste des arguments
			
			# boucle sans l'indice
			#for valeur in args: # défile les arguments de la liste
				#self.textEditTraceAnalyseChaine.append(QString.fromUtf8(str(valeur))) # trace analyse chaine : affiche la liste des arguments
			
			# boucle avec indice
			for i in range(0,len(args)): # défile indice args - attention range c'est valeur de départ, nombre de valeur donc range(0,3) défile de 0 à 2 !
				valeur=int(args[i])
				self.textEditTraceAnalyseChaine.append(QString.fromUtf8(str(valeur))) # trace analyse chaine : affiche la liste des valeurs int des arguments 
			
		
		return args # renvoie la liste des arguments - None si pas d'arguments
		
		# pour tester en Terminal Python 
		# analyse de la chaine 
			#chaine="CAN(123,122,121)"
			# result=re.findall(r'^.*\((.*)\)',chaine) # extrait --(**)
			# result=re.findall(r'^.*\((.*,.*,.*)\)',chaine) # extrait --(*,*,*) = 3 paramètres 
			# sub=result[0].split(',') 
			# print sub
			# => 123, 122, 121
			# print len(sub)
			# => 3
			# print int(sub[0])
			# => 123
	
	#========== fonctions des signaux pour la gestion du fichier ====================
	def pushButtonOuvrirClicked(self):
		print("Bouton <OUVRIR> appuyé")
		
		# ouvre fichier en tenant compte du chemin déjà saisi dans le champ 
		if self.lineEditChemin.text()=="":
			self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', os.getenv('HOME')) # ouvre l'interface fichier - home par défaut
			#self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', QDir.currentPath()) # ouvre l'interface fichier - chemin courant par défaut
		else:
			info=QFileInfo(self.lineEditChemin.text()) # définit un objet pour manipuler info sur fichier à partir chaine champ
			print info.absoluteFilePath() # debug	
			self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', info.absoluteFilePath()) # ouvre l'interface fichier - à partir chemin 
	
		#self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', os.getenv('HOME')) # ouvre l'interface fichier - home par défaut
		#self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', QDir.currentPath()) # ouvre l'interface fichier - chemin courant par défaut
		# getOpenFileName ouvre le fichier sans l'effacer
		
		print(self.filename) # affiche le chemin obtenu dans la console
		self.lineEditChemin.setText(self.filename) # affiche le chemin obtenu dans le champ texte
				
		
		#-- ouverture du fichier Ui et récupération du contenu 
		myFile=open(self.filename,"r") # ouvre le fichier en lecture
		myFileContent=myFile.read() # lit le contenu du fichier
		myFile.close() # ferme le fichier - tant que le fichier reste ouvert, il est inacessible à d'autres ressources
		
		self.textEdit.setText(myFileContent) # copie le contenu dans la zone texte 
		
		
		"""
		#-- ouverture du fichier et récupération du contenu - version avec fonctions PyQt 
		myFile=QFile(self.filename) # définit objet fichier
		myFile.open(QFile.ReadOnly) # ouvre le fichier en lecture
		myFileContent=myFile.readAll() # lit le contenu du fichier - attentino renvoie un QByteArray... 
		myFile.close() # ferme le fichier - tant que le fichier reste ouvert, il est inacessible à d'autres ressources

		self.textEdit.setText(str(myFileContent)) # copie le contenu dans la zone texte 
		"""
	# -- fin def pushButtonOuvrirClicked

	def pushButtonNouveauClicked(self):
		print("Bouton NOUVEAU appuyé")
		
		# ouvre fichier en tenant compte du chemin déjà saisi dans le champ 
		if self.lineEditChemin.text()=="":
			self.filename=QFileDialog.getSaveFileName(self, 'Ouvrir fichier', os.getenv('HOME')) # ouvre l'interface fichier - home par défaut
			#self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', QDir.currentPath()) # ouvre l'interface fichier - chemin courant par défaut
		else:
			info=QFileInfo(self.lineEditChemin.text()) # définit un objet pour manipuler info sur fichier à partir chaine champ
			print info.absoluteFilePath() # debug	
			self.filename=QFileDialog.getSaveFileName(self, 'Ouvrir fichier', info.absoluteFilePath()) # ouvre l'interface fichier - à partir chemin 

		#self.filename=QFileDialog.getSaveFileName(self, 'Nouveau fichier', os.getenv('HOME')) # ouvre l'interface fichier
		# self.filename=QFileDialog.getSaveFileName(self, 'Save File', QDir.currentPath()) # ouvre l'interface fichier - alternative chemin

		# self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', os.getenv('HOME')) # ouvre l'interface fichier
		# getOpenFileName ouvre le fichier sans l'effacer et getSaveFileName l'efface si il existe 
		
		print(self.filename)
		self.lineEditChemin.setText(self.filename)

		#--- efface le contenu du fichier --- 
		if self.lineEditChemin.text()!="":
			#self.myFile = open(self.filename, 'a') # ouverture du fichier en mode écriture append
			self.myFile = open(self.filename, 'w') # ouverture du fichier en mode écriture write - efface contenu existant
			# open est une fonction du langage python : http://docs.python.org/2/library/functions.html#open
			# mode peut-être r, w, a (append)		
			self.myFile.write("") # écrit les données dans le fichier		
			self.myFile.close() # ferme le fichier 
		

	def pushButtonEnregistrerClicked(self):		
		print("Bouton <ENREGISTRE> appuyé")			
	
		if self.lineEditChemin.text()!="":
			#self.myFile = open(self.filename, 'a') # ouverture du fichier en mode écriture append
			self.myFile = open(self.filename, 'w') # ouverture du fichier en mode écriture write - efface contenu existant
			# open est une fonction du langage python : http://docs.python.org/2/library/functions.html#open
			# mode peut-être r, w, a (append)		
			self.myFile.write(str(self.textEdit.toPlainText())) # écrit les données dans le fichier		
			self.myFile.close() # ferme le fichier 

	def pushButtonEnvoiGCodeClicked(self):
		print("Bouton <Envoi GCode> appuyé")
		
		gcode=str(self.textEdit.toPlainText())
		
		self.envoiGCode(gcode) # envoie le GCode vers machine avec attente des réponses <ok>
		
		"""
		gcodeLines=gcode.splitlines()
		print gcodeLines
		
		# desactive timer serial
		if self.serialPort: # seulement si le port série existe 
			self.timerSerial.stop() # stoppe le timer le temps de lire les caractères et éviter "réentrée"

		# défile les lignes du gcode
		for line in gcodeLines: # défile les lignes
			if line.startswith(';'):
				continue
			else : 
			
				#self.envoiChaineSerie(line+"\n") # envoi ligne --> cette fonction réactive timer... donc pb.. 
				
				self.serialPort.write(line+"\n")  # envoie la chaine sur le port serie
				
				print "envoi ligne : " + line 
				
				# lecture des données reçues		

				self.flagOK=False
				self.chaineIn=""
				self.char=""
				
				while self.flagOK==False : # on attend réception <ok>
					
					# reception d'une ligne
					while (self.serialPort.inWaiting()): # tant que au moins un caractère en réception
						self.char=self.serialPort.read() # on lit le caractère
						#self.chaineIn=self.chaineIn+self.char		# forme minimale...
						
						if self.char=='\n': # si saut de ligne, on sort du while
							#print("saut ligne reçu") # debug
							self.char=''
							break # sort du while inWaiting
						else: #tant que c'est pas le saut de ligne, on l'ajoute à la chaine 
							self.chaineIn=self.chaineIn+self.char					
						
						if self.serialPort.inWaiting()==0 : # si aucun nouveau char en réception, on attend un peu...  
							time.sleep(0.01) # pause en secondes
						
					a.processEvents() # traite events app dans while inWaiting - évite freeze - à évaluer de façon régulière mais pas trop...
					
					if self.stopGCode==True :
						self.stopGCode=False # RAZ variable
						self.timerSerial.start() # redémarre le timer 
						return # sortie de la fonction 
					
					# si pass, OK aura été mis à True
					
					# fin serialPort inWaiting
					
					#print "sortie while inwaiting"
					#print self.chaineIn
					
					# analyse chaine recue 
					if self.chaineIn!="" :
						
						print self.chaineIn
						
						#ici analyser attente <ok>
						if "<ok>" in self.chaineIn : 
							#print "OK valide."
							flagOK=True
							break
						else: 
							self.chaineIn="" #RAZ chaineIn
							
							
				#print "sortie while flagOK"
				
			time.sleep(0.001) # pause en secondes entre 2 envoi
			
		# fin for
		
		self.timerSerial.start() # redémarre le timer
		"""
		
		"""
		#-- ajoute une ligne de donnée au fichier
		if self.lineEditChemin.text()!="":
			self.myFile = open(self.filename, 'a') # ouverture du fichier en mode écriture append
			#self.myFile = open(self.filename, 'w') # ouverture du fichier en mode écriture write - efface contenu existant
			# open est une fonction du langage python : http://docs.python.org/2/library/functions.html#open
			# mode peut-être r, w, a (append)		
			self.myFile.write(str(self.lineEditData.text()+"\n")) # écrit les données dans le fichier		
			self.myFile.close() # ferme le fichier 		
			
			#-- ajoute une ligne de donnée au champt texte
			self.textEdit.append(self.lineEditData.text()) # copie le champ texte dans la zone de texte + saut de ligne
		"""

	#--- fonctions stop envoi GCode ----
	def pushButtonStopGCodeClicked(self):
		self.stopGCode=True # active sortie GCode
		print "stop GCode"
		

	#--- fonctions gestion envoi GCode ----
	def pushButtonPassGCodeClicked(self):
		self.flagOK=True # active flag reception OK
		
		print "pass GCode"



	#====== gestion signaux repertoire ==========
	def pushButtonOuvrirRepClicked(self):
		print("Bouton <Sélectionner Répertoire> appuyé")
		
		#self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', os.getenv('HOME')) # ouvre l'interface fichier - home par défaut
		#self.filename=QFileDialog.getOpenFileName(self, 'Ouvrir fichier', QDir.currentPath()) # ouvre l'interface fichier - chemin courant par défaut
		# getOpenFileName ouvre le fichier sans l'effacer
		
		self.dirname = QFileDialog.getExistingDirectory(self,"Choisir repertoire",os.getenv('HOME'),QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks)
		
		print(self.dirname) # affiche le chemin obtenu dans la console
		self.lineEditCheminRep.setText(QString.fromUtf8(self.dirname)) # affiche le chemin obtenu dans le champ texte
		
		
		#-- ouverture du fichier et récupération du contenu 
		#myFile=open(self.filename,"r") # ouvre le fichier en lecture
		#myFileContent=myFile.read() # lit le contenu du fichier
		#myFile.close() # ferme le fichier - tant que le fichier reste ouvert, il est inacessible à d'autres ressources
		
		#self.textEdit.setText(myFileContent) # copie le contenu dans la zone texte 

		"""
		#-- ouverture du fichier et récupération du contenu - version avec fonctions PyQt 
		myFile=QFile(self.filename) # définit objet fichier
		myFile.open(QFile.ReadOnly) # ouvre le fichier en lecture
		myFileContent=myFile.readAll() # lit le contenu du fichier - attentino renvoie un QByteArray... 
		myFile.close() # ferme le fichier - tant que le fichier reste ouvert, il est inacessible à d'autres ressources

		self.textEdit.setText(str(myFileContent)) # copie le contenu dans la zone texte 
		"""

		"""
		#-- ouverture du répertoire et récupération du contenu - fonctions Python 
		path=str(self.lineEditChemin.text())  # le chemin du répertoire
		dirList=os.listdir(path) # la liste du contenu du fichier
		
		for filename in dirList: # affiche les noms
			print filename		
		"""

		#-- ouverture du répertoire et récupération du contenu - fonctions PyQt
		myDir=QDir(self.lineEditChemin.text()) # définit objet répertoire
		#filesList=myDir.entryList() # liste des entrées... = liste du contenu 
		#filesList=myDir.entryList(["*.*"], QDir.Files, QDir.Name) # liste des entrées... avec filtres 
		filesList=myDir.entryList(["*.txt"], QDir.Files, QDir.Name) # liste des entrées... avec filtres 
		# ici que les fichier triés par nom - filtre *.txt
		
		# QStringList QDir.entryList (self, Filters filters = QDir.NoFilter, SortFlags sort = QDir.NoSort)
		# QStringList QDir.entryList (self, QStringList nameFilters, Filters filters = QDir.NoFilter, SortFlags sort = QDir.NoSort)
		
		# les filtres possibles http://pyqt.sourceforge.net/Docs/PyQt4/qdir.html#Filter-enum
		# classement possibles : http://pyqt.sourceforge.net/Docs/PyQt4/qdir.html#SortFlag-enum
		self.textEdit.setText("") # efface le champ texte 
		
		for fileName in filesList: # défile les noms des fichiers..
			print fileName # affiche le fichier
			self.textEdit.append(fileName) # ajoute le fichier à la zone texte


	#---- fonctions commune utiles ------- 
		
	def getContentDir(self,pathIn):
		
		QString.fromUtf8(pathIn) # chemin reçu 
			
		#-- ouverture du répertoire et récupération du contenu - fonctions PyQt
		myDir=QDir(pathIn) # définit objet répertoire
		filesList=myDir.entryList() # liste des entrées... = liste du contenu 
		#filesList=myDir.entryList(["*.*"], QDir.Files, QDir.Name) # liste des entrées... avec filtres 
		#filesList=myDir.entryList(["*.txt"], QDir.Files, QDir.Name) # liste des entrées... avec filtres 
		# ici que les fichier triés par nom - filtre *.txt
		
		# QStringList QDir.entryList (self, Filters filters = QDir.NoFilter, SortFlags sort = QDir.NoSort)
		# QStringList QDir.entryList (self, QStringList nameFilters, Filters filters = QDir.NoFilter, SortFlags sort = QDir.NoSort)
		
		# les filtres possibles http://pyqt.sourceforge.net/Docs/PyQt4/qdir.html#Filter-enum
		# classement possibles : http://pyqt.sourceforge.net/Docs/PyQt4/qdir.html#SortFlag-enum
		self.textEdit.setText("") # efface le champ texte 
		
		for fileName in filesList: # défile les noms des fichiers..
			print fileName # affiche le fichier
			self.textEdit.append(fileName) # ajoute le fichier à la zone texte

	def readFile(self,absoluteFilenameIn):
		
		str(absoluteFilenameIn) # chemin reçu 

		#-- ouverture du fichier Ui et récupération du contenu 
		myFile=open(absoluteFilenameIn,"r") # ouvre le fichier en lecture
		myFileContent=myFile.read() # lit le contenu du fichier
		myFile.close() # ferme le fichier - tant que le fichier reste ouvert, il est inacessible à d'autres ressources
		
		self.textEdit.setText(myFileContent) # copie le contenu dans la zone texte 
			

			
#-- fonction principale de lancement de l'application 
def main(args):
	
	global a # objet app global
	a=QApplication(args) # crée l'objet application 
	f=QWidget() # crée le QWidget racine
	c=myApp(f) # appelle la classe contenant le code de l'application 
	f.show() # affiche la fenêtre QWidget
	r=a.exec_() # lance l'exécution de l'application 
	return r

#-- pour rendre le code exécutable
if __name__=="__main__": # pour rendre le code exécutable 
	main(sys.argv) # appelle la fonction main



