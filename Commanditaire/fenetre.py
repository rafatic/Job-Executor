#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from jobRequest import jobRequest
from jobResult import jobResult
from jobErrorResult import jobErrorResult
import os
import pika
import xml.etree.ElementTree as ET
import socket



class Fenetre(Frame):

    # Initialisation de la fenêtre et des éléments.
    # Ajout du listener lors de clic sur "Envoyer"
    def __init__(self, parent):


        if len(sys.argv) < 4:
            print("Utilisation de la commande :")
            print("     Client.py <ip locale du serveur rabbitMq> <utilisateur> <mot de passe> <port> (optionnel : 5672 par defaut)")
            sys.exit()
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.centerWindow()
        self.initUI()

        # Le pid de l'application est récupéré afin de nommer la queue dans laquelle le commanditaire attendra les résultats du job
        pid = os.getpid()

      
        
        credentials = pika.PlainCredentials(sys.argv[2], sys.argv[3])
        port = 5672
        # Si un port RabbitMq à été défini en argument de ligne de commande
        if len(sys.argv) == 5:
            port = int(sys.argv[4])
        # Création et établissement de la connexion à la file de requete de job
        try:
            parameters = pika.ConnectionParameters(sys.argv[1], port, '/', credentials)
            self.connection = pika.BlockingConnection(parameters)
            # Création et déclaration du canal de requete de job
            self.channelJobRequest = self.connection.channel()
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


        # Déclaration de la file de requête de jpb
        self.channelJobRequest.queue_declare(queue='job_queue', durable=True)

        
        # Création et déclaration du canal de reception du resutlat
        self.channelJobResult = self.connection.channel()
        self.channelJobResult.exchange_declare(exchange='result_queue',
                                                    type='direct')

        self.result = self.channelJobResult.queue_declare(exclusive=True)
        self.queue_name = self.result.method.queue

        # Le canal de reception des resultats est lié à la file correspondante
        # la file de reception est nommée d'après le pid de l'application et l'adresse ip locale de la machine
        self.channelJobResult.queue_bind(exchange='result_queue',
                               queue=self.queue_name,
                               routing_key=str(pid) + socket.gethostbyname(socket.gethostname()))

        

    # Fonction permettant de centrer la fenêtre créée sur l'écran
    def centerWindow(self):
      
        w = 800
        h = 600

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


    def initUI(self):

        # Déclaration des variables associées aux éléments de saisie de la fenêtre
        global txtNomCommande, txtArguments, txtDatasource, txtPath, txtResultat, txtLogin, txtPassword, txtNbExec

        self.parent.title("Commanditaire")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)


        # Association du bouton à l'évènement permettant la fermeture de la fenêtre
        quitButton = Button(self, text="Quitter",
            command=self.quit)
        quitButton.place(x=700, y=550)

        Label(self, text="Saisissez les informations du programme que vous souhaitez faire éxecuter : ").grid(row=0, column=0, sticky=W)
        
        # Creation Frame formulaire saisie de job
        formFrame = Frame(self)
        formFrame.pack()
        formFrame.place(x=10, y=30)

        

        # label et input saisie nom commande
        Label(formFrame, text="Commande : ").grid(row=1, column=0, sticky=W)
        txtNomCommande = StringVar()
        txtNomCommande = Entry(formFrame, textvariable=txtNomCommande)
        txtNomCommande.grid(row=1, column=1, sticky=W)

        # label et input saisie arguments
        Label(formFrame, text="Arguments : ").grid(row=2, column=0, sticky=W)
        txtArguments = StringVar()
        txtArguments = Entry(formFrame, textvariable=txtArguments)
        txtArguments.grid(row=2, column=1, sticky=W)

        # label et input saisie datasource
        Label(formFrame, text="Datasource : ").grid(row=3, column=0, sticky=W)
        txtDatasource = StringVar()
        txtDatasource = Entry(formFrame, textvariable=txtDatasource)
        txtDatasource.grid(row=3, column=1, sticky=W)


        # label et input saisie path
        Label(formFrame, text="Chemin : ").grid(row=4, column=0, sticky=W)
        txtPath = StringVar()
        txtPath = Entry(formFrame, textvariable=txtPath)
        txtPath.grid(row=4, column=1, sticky=W)

        # label et input saisie login
        Label(formFrame, text="Login : ").grid(row=5, column=0, sticky=W)
        txtLogin = StringVar()
        txtLogin = Entry(formFrame, textvariable=txtLogin)
        txtLogin.grid(row=5, column=1, sticky=W)

        # label et input saisie mot de passe
        Label(formFrame, text="Mot de passe : ").grid(row=6, column=0, sticky=W)
        txtPassword = StringVar()
        txtPassword = Entry(formFrame, textvariable=txtPassword, show="*")
        txtPassword.grid(row=6, column=1, sticky=W)

        # label et input saisie nbExec
        Label(formFrame, text="Nombre d'executions ").grid(row=7, column=0, sticky=W)
        txtNbExec = StringVar()
        txtNbExec = Entry(formFrame, textvariable=txtNbExec)
        txtNbExec.grid(row=7, column=1, sticky=W)

        
        # Création et assoication du bouton d'envoi de requête à la fonction d'envoi de requête
        submitJob = Button(formFrame, text="Envoyer", command=self.sendJob).grid(row=8, column=0, sticky=W)


        # Creation Frame resultat
        resultFrame = Frame(self)
        resultFrame.pack()
        resultFrame.place(x=300, y=30)

        # MessageBox resultat (affichage du xml)
        txtResultat = Text (resultFrame)
        txtResultat.grid(row=0, column=0, sticky=W)

    # Procédure de fermeture de la fenêtre
    def quit(self):
        # Si une connection a étée ouverte, elle est fermée avant la fermeture de l'application
        if self.connection.is_open:
            self.connection.close()
        exit(0)

    # Procédure d'envoi de requête de job
    # Cette procédure est appelée lorsqu'on clique sur le bouton "Envoyer"
    def sendJob(self):
        txtResultat.delete(1.0, END)
        self.printResult("Calcul en cours, veuillez patienter")
 
        # Création de l'objet de requête à partir des informations saisies
        request = jobRequest(txtNomCommande.get(), txtArguments.get(), txtDatasource.get(), txtPath.get(), txtLogin.get(), txtPassword.get(), str(os.getpid()) + socket.gethostbyname(socket.gethostname()) )
        

        argTaille = request.args


        # On définit le nombre de colonne que chaque executeur devra calculer en fonction du nombre total de colonnes et du nombre d'éxecutions demandées
        nbCol = int(argTaille) / int(txtNbExec.get())  
        # On définit si le nombre total de colonnes et le nombre d'exécutions sont entièrement divisibles
        remain = int(argTaille) % int(txtNbExec.get())  
        firstCol = 0
        lastCol = 0


        # Envoie de N requêtes où N = nombre d'éxecutions demandées    
        for i in range(0, int(txtNbExec.get())):
            publishStatus = False
            firstCol = lastCol
            lastCol += nbCol

            # Si le nombre total de colonnes et le nombre d'executions ne sont pas entièrement divisibles, on répartis le nombre restant de colonnes entre chaque execution
            # Exemple : nDames 7 sur 2 executions
            # 7 % 2 = 1
            # 7 / 2 = 3
            # Chaque exécution portera sur un intervalle de 3 colonnes.
            # Il restera une colonne à calculer.
            # Cette colonne est attribuée arbitrairement à une exécution
            if  remain != 0:
                lastCol += 1
                remain -= 1

           
            # Construction de la chaine d'argument
            # La chaine d'arguments est de la forme : 7 0 2 tel que :
            #   7 : taille du tableau
            #   0 : première colonne à calculer
            #   2 : dernière colonne à calculer
            request.args = argTaille + " " + str(firstCol) + " " + str(lastCol)

            # BlockingConnection.basic_publish retourne False si l'envoi ne s'est pas realisé
            publishStatus = self.channelJobRequest.basic_publish(exchange='',
                                            routing_key='job_queue',
                                            body=request.toXML(),
                                            properties=pika.BasicProperties(
                                            delivery_mode = 2,
                                            ))

            # Dans le cas ou l'envoi est un echec, on tente de renvoyer le message (BlockingConnection.basic_publish = false)
            # 3 essais sont reaslisé, si aucun ne fonctionne, la requete est abandonnée
            nbRetry = 0
            while publishStatus != True | nbRetry != 3:
                publishStatus = self.channelJobRequest.basic_publish(exchange='',
                                            routing_key='job_queue',
                                            body=request.toXML(),
                                            properties=pika.BasicProperties(
                                            delivery_mode = 2,
                                            ))
                nbRetry += 1

            if publishStatus == False & nbRetry == 3:
                self.printResult("Abandon de la requete : impossible de contacter le serveur RabbitMq")
                return
            

        print(" [x] Requetes envoyees")


        resultReceived = 0
        # Création des objets JobResult déstinés à recevoir les résultats d'exécution
        lstResults = [ jobResult() for i in range(0, int(txtNbExec.get()))]
        jobHasFailed = False
        
        # Tant que tous les résultats n'ont pas étés recus
        while resultReceived < int(txtNbExec.get()):
            method_frame, header_frame, body = self.channelJobResult.basic_get(queue = self.queue_name)
            # Si le message recu contient bien des données
            if body != None:
                # Lorsque le premier résultat est recu, on efface la zone de texte de résultat
                if resultReceived == 0:
                    txtResultat.delete(1.0, END)

                # Si le message contient le résultat d'une exécution
                if ET.fromstring(body).tag == '{http://www.w3.org/2001/XMLSchema-instance}jobResult':
                    # le résultat est enregistré et est ensuite affiché
                    lstResults[resultReceived].XmlToObject(body)
                    print lstResults[resultReceived].toString()
                    self.printResult(lstResults[resultReceived].toString())
                # Si le message correspond à une erreur
                elif ET.fromstring(body).tag == '{http://www.w3.org/2001/XMLSchema-instance}error':
                    # L'erreur est enregistrée puis affichée
                    jobError = jobErrorResult()
                    jobError.XmlToObject(body)
                    self.printResult(jobError.toString())
                    jobHasFailed = True
                    
                resultReceived += 1

        self.printResult("---------------------\n")

        if jobHasFailed == False:
            # L'objet finalResult fait la synthèse de l'ensemble des résultats obtenus
            finalResult = jobResult()
            finalResult.execTime = 0
            finalResult.result = 0
            finalResult.command = lstResults[0].command[:-4]
            for i in range(0, len(lstResults)):
                finalResult.execTime += lstResults[i].execTime
                finalResult.result += lstResults[i].result
            # Le résultat final est affiché
            print finalResult.toString()
            
            self.printResult("Résultat total : \n")
            self.printResult(finalResult.toString())
        else:
            self.printResult("L'exécution d'un ou plusieurs site a echouée")
 

    def printResult(self, string):
        txtResultat.insert(INSERT, string)


   