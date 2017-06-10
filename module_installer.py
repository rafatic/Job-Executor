#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess

nbModulesManquant = 0

try:
	import pika
except ImportError:
	print "Installation de pika"
	try:
		subprocess.check_output(["pip", "install", "pika"])
		print("installation reussie")
		nbModulesManquant +=1
	except subprocess.CalledProccessError, e:
		print "Erreur lors de l'installation du module pika"
		print e.message
		sys.exit()

try:
	import paramiko
except ImportError:
	print "Installation de paramiko"
	try:
		subprocess.check_output(["pip", "install", "paramiko"])
		print("installation reussie")

		nbModulesManquant += 1
	except subprocess.CalledProccessError, e:
		print "Erreur lors de l'installation du module paramiko"
		print e.message
		sys.exit()

if nbModulesManquant > 0:
	print "--------------------------------"
	print "Installation de " + str(nbModulesManquant) + " module(s) reussie"
else:
	print "Les modules necessaires sont deja presents"
sys.exit()