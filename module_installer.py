#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess

missingModulesCount = 0

print "This installer will download the required modules in order to run the job executor"
print "The following modules are needed : "
print "		- pika"
print "		- paramiko"

try:
	import pika
except ImportError:
	print "Installing pika"

	try:
		subprocess.check_output(["pip", "install", "pika"])
		print "Success"
		missingModulesCount +=1
	except subprocess.CalledProccessError, e:
		print "Failed to install pika"
		print e.message
		sys.exit()

try:
	import paramiko
except ImportError:
	print "Installing paramiko"
	try:
		subprocess.check_output(["pip", "install", "paramiko"])
		print "Success"
		missingModulesCount += 1
	except subprocess.CalledProccessError, e:
		print "Failed to install paramiko"
		print e.message
		sys.exit()

if missingModulesCount > 0:
	print "--------------------------------"
	print "Installed successfully " + str(missingModulesCount) + " module(s)"
else:
	print "All the modules were already installed"
sys.exit()