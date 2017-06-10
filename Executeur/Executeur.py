#!/usr/bin/python
# -*- coding: utf-8 -*-

import pika
import sys
import signal
import time
import paramiko
import os
import subprocess
from jobRequest import jobRequest
from jobResult import jobResult
from jobErrorResult import jobErrorResult


def sigint_handler(signal, frame):
    connection.close()
    sys.exit(0)

# Procedure de connexion au serveur distant et de télechargement du fichier à exécuter
def serveurConnection(request):

    dir = os.path.dirname(__file__)
    targetDir = os.path.join(dir, "scripts")
    # Si le fichier à exécuter n'est pas présent en local
    if os.path.isfile(targetDir + "/"+ request.command) != True :
        try:
            # Création et établissement de la connexion au serveur
            transport = paramiko.Transport(request.url, 22)
            transport.connect(username = request.login, password = request.password)
        # Si la connexion a échouée, une erreur est levée et est envoyée dans la file de résultat de job
        except paramiko.SSHException, sshError:
            print "Erreur lors de la connexion avec le serveur distant : " + sshError.message
            error = jobErrorResult("SSH Error", str(sshError.args), sshError.message)

            transport.close()
            return error.toXML()
        

        sftp = paramiko.SFTPClient.from_transport(transport)
        
        try:
            # Télechargement du fichier à exécuter
            # Le fichier est placé dans le dossier "scripts" de l'application
            sftp.get( request.path + "/" + request.command, targetDir + "/" + request.command)
        except IOError, fileError:
            # Si le fichier spécifié est introuvable, une erreur est levée et est envoyée dans la file de résultat de job
            print "Erreur lors de la récupération du fichier : " + fileError.message
            error = jobErrorResult("File Error", str(fileError.args), fileError.message)
            sftp.close()
            transport.close()
            return error.toXML()
        sftp.close()
        transport.close()

    
    # Une fois le fichier téléchargé, il est executé
    try:
        # La chaine d'argument est divisé selon les espaces, permettant de traiter chaque arguement indépendament
        argsTab = request.args.split()
        
        # Le fichier est exécuté
        programReturnValue = subprocess.check_output(["python", "scripts/" + request.command, argsTab[0], argsTab[1], argsTab[2]])
    
    except subprocess.CalledProcessError, e:
        # Si l'exécution échoue, une erreur est levée et est envoyée dans la file de résultat de job
        print "Erreur d'execution : " + e.output
        error = jobErrorResult("Execution Error", e.returncode, e.message)
        return error.toXML()
        
    # Une fois l'exécution terminée, le résultat est recupéré dans un objet "JobResult"
    outputTab = programReturnValue.split(":")
    result = jobResult(request.command + " " + request.args, outputTab[0], outputTab[1])

    print "Result : " + programReturnValue
    # Le resultat est retouné sous forme de chaine XML
    return result.toXML()


# Ce callback est appelé lorsqu'une requête de job est récupérée
def callbackJobRequest(ch, method, properties, body):
    print(body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    request = jobRequest()
    request.XmlToObject(body)
    
    print(request.toString())
    # Appel de la procédure permettant le téléchargement du fichier à exécuter
    response = serveurConnection(request)
    channelJobResult.basic_publish(exchange='result_queue',
                          routing_key=request.sender,
                          body=response)
    
    
    print("result sent")





def main():

    if len(sys.argv) < 4:
        print("Utilisation de la commande :")
        print("     Serveur.py <ip locale du serveur rabbitMq> <utilisateur> <mot de passe> <port> (optionnel : 5672 par defaut)")
        
        sys.exit()

    # On installe un signal d'interruption de l'application
    signal.signal(signal.SIGINT, sigint_handler)

    global connection, channelJobResult
    credentials = pika.PlainCredentials(sys.argv[2], sys.argv[3])
    port = 5672
    # Si un port RabbitMq à été défini en argument de ligne de commande
    if len(sys.argv) == 5:
        port = int(sys.argv[4])
    # Création et établissement de la connexion à la file de requete de job
    try:
        parameters = pika.ConnectionParameters(sys.argv[1], port, '/', credentials)
        connection = pika.BlockingConnection(parameters)

    # Si la connexion a échouée, une erreur est levée et l'application est arrêtée
    except pika.exceptions.ConnectionClosed, ConnectionError:
        print("Erreur lors de la connexion au serveur RabbitMq")
        print(ConnectionError.message)
        sys.exit()
    # Si l'authentification à la file à échoue, une erreur est levée et l'application est arrêtée
    except pika.exceptions.ProbableAuthenticationError, AuthError:
        print("Erreur lors de l'authentification au serveur RabbitMq")
        print(AuthError.message)
        sys.exit()

    # Creation et declaration du channel de requete de job
    channelJobRequest = connection.channel()

    channelJobRequest.queue_declare(queue='job_queue', durable=True)

    # Creation et declaration du channel de reponse
    channelJobResult = connection.channel()

    channelJobResult.exchange_declare(exchange='result_queue',
                                      type='direct')
    # L'application indique qu'elle ne peut recevoir qu'un message à la fois
    channelJobRequest.basic_qos(prefetch_count=1)

    channelJobRequest.basic_consume(callbackJobRequest,
                          queue='job_queue'
                          )

    print(' [*] En attente de message. Pour quitter, appuyez sur CTRL+C')
    # Commence à consommer les messages dans la file de requête de job
    channelJobRequest.start_consuming()
    
    



if __name__ == '__main__' :
    main()
